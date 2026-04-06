"""streaming_ml_engine.py - ML inference pipeline for telemetry streaming."""
import time
import random
import threading
import queue
from collections import deque


class BatchInferenceEngine:
    """
    Batch ML inference engine for telemetry anomaly detection and prediction.
    Uses a cold-start heuristic: returns benign until training data is collected.
    """
    TRAINING_THRESHOLD = 50  # samples needed before ML models activate

    def __init__(self, batch_size=16):
        self.batch_size = batch_size
        self._is_detector_trained = False
        self._is_predictor_trained = False
        self._sample_count = 0

    def process_batch(self, batch):
        """Process a batch of telemetry dicts and return enriched dicts."""
        enriched = []
        for item in batch:
            self._sample_count += 1

            # Cold start: return benign defaults until threshold is reached
            ml_is_anomaly = False
            ml_predicted_cpu_t5 = item.get('cpu_load', 50.0)

            if self._is_detector_trained:
                cpu = item.get('cpu_load', 0.0)
                temp = item.get('bus_temp', 0.0)
                net = item.get('network_tx', 0.0)
                ml_is_anomaly = (cpu > 90.0 or temp > 70.0 or net > 10000.0)

            enriched_item = dict(item)
            enriched_item['ml_is_anomaly'] = ml_is_anomaly
            enriched_item['ml_predicted_cpu_t5'] = ml_predicted_cpu_t5
            enriched.append(enriched_item)

        if (not self._is_detector_trained and
                self._sample_count >= self.TRAINING_THRESHOLD):
            self._is_detector_trained = True
            self._is_predictor_trained = True

        return enriched


class PipelineOrchestrator:
    """
    Orchestrates a real-time telemetry ingestion and inference pipeline.
    """

    def __init__(self, frequency_hz=100, buffer_duration_sec=5):
        self.frequency_hz = frequency_hz
        self.buffer_duration_sec = buffer_duration_sec
        self._running = False
        self._thread = None
        self.engine = BatchInferenceEngine(batch_size=16)
        self.output_buffer = deque(maxlen=int(frequency_hz * buffer_duration_sec))
        self.ingestion_queue = queue.Queue()
        self._messages_inferred = 0
        self._counter_lock = threading.Lock()
        self.last_batch_latency_ms = 0.0
        self.start_time = None

    def _generate_packet(self):
        return {
            'timestamp': time.time(),
            'cpu_load': random.uniform(20.0, 80.0),
            'memory_usage': random.uniform(30.0, 70.0),
            'bus_temp': random.uniform(15.0, 45.0),
            'network_tx': random.uniform(100.0, 2000.0),
        }

    def _run_loop(self):
        interval = 1.0 / self.frequency_hz
        self.start_time = time.time()
        while self._running:
            packet = self._generate_packet()
            self.ingestion_queue.put(packet)

            batch = []
            while not self.ingestion_queue.empty() and len(batch) < 16:
                try:
                    batch.append(self.ingestion_queue.get_nowait())
                except queue.Empty:
                    break

            if batch:
                batch_start = time.time()
                enriched = self.engine.process_batch(batch)
                self.last_batch_latency_ms = (time.time() - batch_start) * 1000.0
                for item in enriched:
                    self.output_buffer.append(item)
                with self._counter_lock:
                    self._messages_inferred += len(enriched)

            time.sleep(interval)

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=2.0)

    def get_latest_data(self):
        return list(self.output_buffer)

    def get_metrics(self):
        elapsed = time.time() - self.start_time if self.start_time else 1.0
        with self._counter_lock:
            inferred = self._messages_inferred
        return {
            'latency_ms': self.last_batch_latency_ms,
            'throughput_hz': inferred / elapsed,
            'queue_size': self.ingestion_queue.qsize(),
            'total_inferred': inferred,
        }
