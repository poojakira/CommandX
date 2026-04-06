import time
import random
import threading
import logging
import queue
from collections import deque
from typing import Dict, List, Any, Optional, Sequence

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import Ridge

from commandx.ml.models import TelemetryPacket

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
    """
    def __init__(self, batch_size: int = 32, max_latency_ms: float = 50.0):
        self.batch_size = batch_size
        self.max_latency_sec = max_latency_ms / 1000.0

        # Threat Detection (Isolation Forest)
        self.anomaly_detector = IsolationForest(
            n_estimators=100,
            contamination=0.05,
            random_state=42,
            n_jobs=-1
        )
        self._is_detector_trained: bool = False
        self._training_buffer: List[List[float]] = []
        self._training_required: int = 200

        # Trajectory Predictor (Ridge Regression)
        self.predictor = Ridge(alpha=1.0)
        self._predictor_buffer_x: deque = deque(maxlen=200)
        self._predictor_buffer_y: deque = deque(maxlen=200)
        self._is_predictor_trained: bool = False

        logger.info(f"Initialized BatchInferenceEngine (Max Batch: {self.batch_size}, Latency SLA: {max_latency_ms}ms)")

    def _extract_features(self, payload: TelemetryPacket) -> List[float]:
        return [
            payload.get('cpu_load', 0.0),
            payload.get('memory_usage', 0.0),
            payload.get('bus_temp', 0.0),
            payload.get('network_tx', 0.0)
        ]

    def process_batch(self, batch: List[TelemetryPacket]) -> List[TelemetryPacket]:
        if not batch:
            return []

        feature_matrix = [self._extract_features(item) for item in batch]

        if not self._is_detector_trained:
            self._training_buffer.extend(feature_matrix)
            if len(self._training_buffer) >= self._training_required:
                logger.info("Training Isolation Forest on baseline telemetry...")
                start_time = time.time()
                self.anomaly_detector.fit(self._training_buffer)
                self._is_detector_trained = True
                logger.info(f"Isolation Forest trained in {(time.time() - start_time)*1000:.1f}ms")
            anomalies = [1] * len(batch)
            scores = [0.0] * len(batch)
        else:
            anomalies = self.anomaly_detector.predict(feature_matrix)
            scores = self.anomaly_detector.decision_function(feature_matrix)

        for item in batch:
            self._predictor_buffer_x.append(item['timestamp'])
            self._predictor_buffer_y.append(item['cpu_load'])

        predicted_cpus = [item['cpu_load'] for item in batch]
        if len(self._predictor_buffer_x) >= 50:
            try:
                X_train = np.array(self._predictor_buffer_x).reshape(-1, 1)
                y_train = np.array(self._predictor_buffer_y)
                self.predictor.fit(X_train, y_train)
                self._is_predictor_trained = True
                future_times = np.array([[item['timestamp'] + 5.0] for item in batch])
                predicted_cpus = self.predictor.predict(future_times)
                predicted_cpus = np.clip(predicted_cpus, 0.0, 100.0)
            except Exception as e:
                logger.warning(f"Predictor convergence failed: {e}")

        for i, item in enumerate(batch):
            item['ml_is_anomaly'] = bool(anomalies[i] == -1)
            item['ml_anomaly_score'] = float(scores[i])
            item['ml_predicted_cpu_t5'] = float(predicted_cpus[i])
        return batch

# ==============================================================================
# PIPELINE ORCHESTRATOR
# ==============================================================================
class PipelineOrchestrator:
    """
    Manages the thread-safe lifecycle of the telemetry stream and batched inference.
    """
    def __init__(self, frequency_hz: int = 50, buffer_duration_sec: int = 15):
        self.frequency = frequency_hz
        self.interval = 1.0 / frequency_hz
        self.buffer_size = frequency_hz * buffer_duration_sec

        self.ingestion_queue: queue.Queue[TelemetryPacket] = queue.Queue(maxsize=1000)
        self.output_buffer: deque[TelemetryPacket] = deque(maxlen=self.buffer_size)
        self.engine = BatchInferenceEngine(batch_size=16, max_latency_ms=20.0)

        self._running: bool = False
        self._ingestion_thread: Optional[threading.Thread] = None
        self._inference_thread: Optional[threading.Thread] = None

        self.start_time: float = 0.0
        self.messages_ingested: int = 0
        self.messages_inferred: int = 0
        self.last_batch_latency_ms: float = 0.0

        # FIX: lock to protect messages_inferred counter from concurrent writes
        self._counter_lock = threading.Lock()

    def start(self) -> None:
        if not self._running:
            self._running = True
            self.start_time = time.time()
            self._ingestion_thread = threading.Thread(target=self._ingestion_loop, daemon=True, name="IngestionThread")
            self._inference_thread = threading.Thread(target=self._inference_loop, daemon=True, name="InferenceThread")
            self._ingestion_thread.start()
            self._inference_thread.start()
            logger.info(f"Pipeline Orchestrator started at {self.frequency}Hz.")

    def stop(self) -> None:
        self._running = False
        if self._ingestion_thread:
            self._ingestion_thread.join(timeout=2.0)
        if self._inference_thread:
            self._inference_thread.join(timeout=2.0)
        logger.info("Pipeline Orchestrator shutting down.")

    def _generate_synthetic_payload(self) -> TelemetryPacket:
        is_attack = random.random() < 0.02
        return {
            'timestamp': time.time(),
            'generated_at': time.time(),
            # FIX: clamp cpu_load to [0, 100] — np.random.normal can produce negatives
            'cpu_load': random.uniform(90, 100) if is_attack else max(0.0, min(100.0, np.random.normal(45, 10))),
            'memory_usage': max(0.0, min(100.0, np.random.normal(60, 5))),
            'bus_temp': np.random.normal(25, 2),
            'network_tx': random.uniform(8000, 15000) if is_attack else max(0.0, np.random.normal(500, 100)),
            'ground_truth_attack': is_attack,
            'ml_is_anomaly': None,
            'ml_anomaly_score': None,
            'ml_predicted_cpu_t5': None
        }

    def _ingestion_loop(self) -> None:
        while self._running:
            loop_start = time.time()
            payload = self._generate_synthetic_payload()
            try:
                self.ingestion_queue.put_nowait(payload)
                self.messages_ingested += 1
            except queue.Full:
                logger.warning("Ingestion Queue FULL. Dropping telemetry packet.")
            sleep_time = max(0.0, self.interval - (time.time() - loop_start))
            time.sleep(sleep_time)

    def _inference_loop(self) -> None:
        while self._running:
            batch: List[TelemetryPacket] = []
            batch_start = time.time()

            while len(batch) < self.engine.batch_size:
                try:
                    item = self.ingestion_queue.get(timeout=0.005)
                    batch.append(item)
                except queue.Empty:
                    break
                if (time.time() - batch_start) >= self.engine.max_latency_sec:
                    break

            if batch:
                # FIX: removed dead process_start variable
                enriched_batch = self.engine.process_batch(batch)
                self.last_batch_latency_ms = (time.time() - batch_start) * 1000.0
                for item in enriched_batch:
                    self.output_buffer.append(item)
                    # FIX: thread-safe counter increment
                    with self._counter_lock:
                        self.messages_inferred += 1
            else:
                time.sleep(0.01)

    def get_latest_data(self) -> List[TelemetryPacket]:
        return list(self.output_buffer)

    def get_metrics(self) -> Dict[str, float]:
        elapsed = time.time() - self.start_time if self.start_time else 1.0
        with self._counter_lock:
            inferred = self.messages_inferred
        throughput = inferred / elapsed
        return {
            'latency_ms': self.last_batch_latency_ms,
            'throughput_hz': throughput,
            'queue_size': self.ingestion_queue.qsize(),
            'total_inferred': inferred,
            'buffer_usage': (len(self.output_buffer) / self.buffer_size) * 100.0 if self.buffer_size > 0 else 0.0
        }
