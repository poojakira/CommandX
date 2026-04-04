import time
import random
import threading
import logging
import queue
from collections import deque
from typing import Dict, List, Any, Optional

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import Ridge

# ==============================================================================
# LOGGING CONFIGURATION (Enterprise Standard)
# ==============================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("TelemetryPipeline")

# ==============================================================================
# BATCH INFERENCE ENGINE (NVIDIA-Grade Design)
# ==============================================================================
class BatchInferenceEngine:
    """
    Handles high-throughput, batched machine learning inference.
    
    In a real production system, this module would wrap Triton Inference Server 
    or TensorRT. Here, we simulate batched ML on the CPU.
    """
    def __init__(self, batch_size: int = 32, max_latency_ms: float = 50.0):
        self.batch_size = batch_size
        self.max_latency_sec = max_latency_ms / 1000.0
        
        # Threat Detection (Isolation Forest)
        self.anomaly_detector = IsolationForest(
            n_estimators=100,
            contamination=0.05,
            random_state=42,
            n_jobs=-1  # Utilize all CPU cores
        )
        self._is_detector_trained: bool = False
        self._training_buffer: List[List[float]] = []
        self._training_required: int = 200  # Requires 200 samples before online training
        
        # Trajectory Predictor (Ridge Regression)
        self.predictor = Ridge(alpha=1.0)
        self._predictor_buffer_x: deque = deque(maxlen=200)
        self._predictor_buffer_y: deque = deque(maxlen=200)
        self._is_predictor_trained: bool = False

        logger.info(f"Initialized BatchInferenceEngine (Max Batch: {self.batch_size}, Latency SLA: {max_latency_ms}ms)")

    def _extract_features(self, payload: Dict[str, Any]) -> List[float]:
        """Extracts numerical features required for inference."""
        return [
            payload.get('cpu_load', 0.0),
            payload.get('memory_usage', 0.0),
            payload.get('bus_temp', 0.0),
            payload.get('network_tx', 0.0)
        ]

    def process_batch(self, batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Executes vectorized inference on a batch of telemetry payloads.
        
        Args:
            batch: A list of raw telemetry dictionaries.
            
        Returns:
            The list of dictionaries enriched with ML predictions.
        """
        if not batch:
            return []

        # 1. Feature Extraction (Vectorized where possible)
        feature_matrix = [self._extract_features(item) for item in batch]
        
        # 2. Threat Detection Inference
        if not self._is_detector_trained:
            self._training_buffer.extend(feature_matrix)
            if len(self._training_buffer) >= self._training_required:
                logger.info("Training Isolation Forest on baseline telemetry...")
                start_time = time.time()
                self.anomaly_detector.fit(self._training_buffer)
                self._is_detector_trained = True
                logger.info(f"Isolation Forest trained in {(time.time() - start_time)*1000:.1f}ms")
            
            # Default to benign during cold-start
            anomalies = [1] * len(batch)
            scores = [0.0] * len(batch)
        else:
            # Predict returns 1 for inlier, -1 for outlier
            anomalies = self.anomaly_detector.predict(feature_matrix)
            scores = self.anomaly_detector.decision_function(feature_matrix)

        # 3. Trajectory Prediction (Predicting CPU load t+5 seconds)
        # Update trailing buffer with the new batch
        for item in batch:
            self._predictor_buffer_x.append(item['timestamp'])
            self._predictor_buffer_y.append(item['cpu_load'])
            
        predicted_cpus = [item['cpu_load'] for item in batch] # Default fallback
        
        if len(self._predictor_buffer_x) >= 50:
            try:
                X_train = np.array(self._predictor_buffer_x).reshape(-1, 1)
                y_train = np.array(self._predictor_buffer_y)
                self.predictor.fit(X_train, y_train)
                self._is_predictor_trained = True
                
                # Predict for t+5s for every item in the batch
                future_times = np.array([[item['timestamp'] + 5.0] for item in batch])
                predicted_cpus = self.predictor.predict(future_times)
                predicted_cpus = np.clip(predicted_cpus, 0.0, 100.0)
            except Exception as e:
                logger.warning(f"Predictor convergence failed: {e}")

        # 4. Enrich & Return
        for i, item in enumerate(batch):
            item['ml_is_anomaly'] = (anomalies[i] == -1)
            item['ml_anomaly_score'] = float(scores[i])
            item['ml_predicted_cpu_t5'] = float(predicted_cpus[i])
            
        return batch


# ==============================================================================
# PIPELINE ORCHESTRATOR
# ==============================================================================
class PipelineOrchestrator:
    """
    Manages the thread-safe lifecycle of the telemetry stream and batched inference.
    Demonstrates true Systems Thinking by decoupling ingestion from compute.
    """
    def __init__(self, frequency_hz: int = 50, buffer_duration_sec: int = 15):
        self.frequency = frequency_hz
        self.interval = 1.0 / frequency_hz
        self.buffer_size = frequency_hz * buffer_duration_sec
        
        # Thread-safe queues and buffers
        self.ingestion_queue: queue.Queue = queue.Queue(maxsize=1000)
        self.output_buffer: deque = deque(maxlen=self.buffer_size)
        
        self.engine = BatchInferenceEngine(batch_size=16, max_latency_ms=20.0)
        
        # Concurrency management
        self._running: bool = False
        self._ingestion_thread: Optional[threading.Thread] = None
        self._inference_thread: Optional[threading.Thread] = None
        
        # Telemetry Metrics
        self.start_time: float = 0.0
        self.messages_ingested: int = 0
        self.messages_inferred: int = 0
        self.last_batch_latency_ms: float = 0.0

    def start(self) -> None:
        """Starts the background pipeline threads."""
        if not self._running:
            self._running = True
            self.start_time = time.time()
            
            self._ingestion_thread = threading.Thread(target=self._ingestion_loop, daemon=True, name="IngestionThread")
            self._inference_thread = threading.Thread(target=self._inference_loop, daemon=True, name="InferenceThread")
            
            self._ingestion_thread.start()
            self._inference_thread.start()
            logger.info(f"Pipeline Orchestrator started at {self.frequency}Hz.")

    def stop(self) -> None:
        """Gracefully halts the pipeline."""
        self._running = False
        if self._ingestion_thread:
            self._ingestion_thread.join(timeout=2.0)
        if self._inference_thread:
            self._inference_thread.join(timeout=2.0)
        logger.info("Pipeline Orchestrator shutting down.")

    def _generate_synthetic_payload(self) -> Dict[str, Any]:
        """Generates realistic aerospace telemetry noise."""
        is_attack = random.random() < 0.02
        return {
            'timestamp': time.time(),
            'generated_at': time.time(), # High-precision creation mark
            'cpu_load': random.uniform(90, 100) if is_attack else np.random.normal(45, 10),
            'memory_usage': max(0.0, min(100.0, np.random.normal(60, 5))),
            'bus_temp': np.random.normal(25, 2),
            'network_tx': random.uniform(8000, 15000) if is_attack else max(0.0, np.random.normal(500, 100)),
            'ground_truth_attack': is_attack
        }

    def _ingestion_loop(self) -> None:
        """High-frequency data generation bound by the target Hz."""
        while self._running:
            loop_start = time.time()
            
            payload = self._generate_synthetic_payload()
            try:
                # Non-blocking put to avoid clogging ingestion if inference is slow
                self.ingestion_queue.put_nowait(payload)
                self.messages_ingested += 1
            except queue.Full:
                logger.warning("Ingestion Queue FULL. Dropping telemetry framework.")
            
            sleep_time = max(0.0, self.interval - (time.time() - loop_start))
            time.sleep(sleep_time)

    def _inference_loop(self) -> None:
        """Dynamic batching consumer loop."""
        while self._running:
            batch = []
            batch_start = time.time()
            
            # Drain queue until batch size is met or max latency is hit
            while len(batch) < self.engine.batch_size:
                try:
                    # Wait slightly for data
                    item = self.ingestion_queue.get(timeout=0.005)
                    batch.append(item)
                except queue.Empty:
                    # If queue is empty, dispatch whatever we have
                    break
                    
                # If we are waiting too long, dispatch the batch to maintain SLA
                if (time.time() - batch_start) >= self.engine.max_latency_sec:
                    break
            
            if batch:
                process_start = time.time()
                enriched_batch = self.engine.process_batch(batch)
                
                # Track Latency (Time waiting + Time processing)
                self.last_batch_latency_ms = (time.time() - batch_start) * 1000.0
                
                for item in enriched_batch:
                    self.output_buffer.append(item)
                    self.messages_inferred += 1
            else:
                # Prevent CPU spinning if idle
                time.sleep(0.01)

    def get_latest_data(self) -> List[Dict[str, Any]]:
        """Returns a stable snapshot of the circular buffer."""
        return list(self.output_buffer)

    def get_metrics(self) -> Dict[str, float]:
        """Calculates realtime SLA metrics for the dashboard."""
        elapsed = time.time() - self.start_time if self.start_time else 1.0
        throughput = self.messages_inferred / elapsed
        
        return {
            'latency_ms': self.last_batch_latency_ms,
            'throughput_hz': throughput,
            'queue_size': self.ingestion_queue.qsize(),
            'total_inferred': self.messages_inferred,
            'buffer_usage': (len(self.output_buffer) / self.buffer_size) * 100.0 if self.buffer_size > 0 else 0.0
        }
