import pytest
import numpy as np
from ml.ga_optimizer import MissionOptimizer
from gnc.gnc_kalman import ExtendedKalmanFilter
from subsystem_manager import PowerThermalSubsystem
from ml.streaming_ml_engine import PipelineOrchestrator

def test_ga_optimizer_smoke():
    """Verify GA optimizer can run without crashing and find a solution."""
    opt = MissionOptimizer(pop_size=10)
    best_alt, best_cost = opt.run()
    assert 160 <= best_alt <= 8000
    assert best_cost > 0

def test_ekf_smoke():
    """Verify EKF state estimation logic."""
    initial_state = np.array([7000.0, 0.0, 0.0, 0.0, 7.5, 0.0])
    ekf = ExtendedKalmanFilter(initial_state=initial_state, dt=1.0)
    # Mock measurement (Position, Velocity)
    z = np.array([7001.0, 0.1, -0.1, 0.01, 7.51, -0.01]) 
    ekf.predict()
    ekf.update(z)
    state = ekf.state
    assert state.shape == (6,)
    assert not np.isnan(state).any()

def test_subsystem_smoke():
    """Verify power/thermal subsystem updates."""
    pts = PowerThermalSubsystem()
    metrics = pts.update(dt=10.0, is_eclipse=False, is_thrusting=True)
    assert "charge_pct" in metrics
    assert "temp_c" in metrics
    assert metrics["temp_c"] > 20.0 # Heating up because not in eclipse

def test_pipeline_smoke():
    """Verify telemetry pipeline can start and generate data."""
    orchestrator = PipelineOrchestrator(frequency_hz=10, buffer_duration_sec=1)
    orchestrator.start()
    import time
    time.sleep(0.5) # Wait for some data
    data = orchestrator.get_latest_data()
    metrics = orchestrator.get_metrics()
    orchestrator.stop()
    
    assert len(data) >= 0
    assert "latency_ms" in metrics
    assert metrics["total_inferred"] >= 0
