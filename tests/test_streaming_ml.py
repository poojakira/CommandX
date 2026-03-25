import pytest
import time
from streaming_ml_engine import PipelineOrchestrator, BatchInferenceEngine

def test_inference_engine_initialization():
    engine = BatchInferenceEngine(batch_size=16)
    assert engine.batch_size == 16
    assert engine._is_detector_trained is False
    assert engine._is_predictor_trained is False

def test_inference_engine_cold_start():
    engine = BatchInferenceEngine(batch_size=2)
    
    # Create mock anomalous and normal data
    batch = [
        {'timestamp': time.time(), 'cpu_load': 45.0, 'memory_usage': 60.0, 'bus_temp': 25.0, 'network_tx': 500.0},
        {'timestamp': time.time(), 'cpu_load': 99.0, 'memory_usage': 90.0, 'bus_temp': 80.0, 'network_tx': 15000.0}
    ]
    
    # Process batch during cold start (before training threshold is met)
    enriched = engine.process_batch(batch)
    
    assert len(enriched) == 2
    # Should default to benign (False) during cold start phase
    assert enriched[0]['ml_is_anomaly'] is False
    assert enriched[1]['ml_is_anomaly'] is False
    assert 'ml_predicted_cpu_t5' in enriched[0]

def test_pipeline_orchestrator_lifecycle():
    orchestrator = PipelineOrchestrator(frequency_hz=100, buffer_duration_sec=2)
    
    assert orchestrator._running is False
    orchestrator.start()
    assert orchestrator._running is True
    
    # Let it run briefly to ingest and infer
    time.sleep(0.5)
    
    metrics = orchestrator.get_metrics()
    
    assert metrics['total_inferred'] > 0
    assert metrics['queue_size'] >= 0
    
    orchestrator.stop()
    assert orchestrator._running is False
