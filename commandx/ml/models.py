from typing import TypedDict, Optional, Dict, Any
from dataclasses import dataclass, asdict

# ==============================================================================
# STRONGLY-TYPED DATA MODELS (Engineering Standard)
# ==============================================================================

class TelemetryPacket(TypedDict):
    """
    Formalized Telemetry Schema for CommandX Mission Assets.
    Used for high-frequency (50Hz+) streaming and ML inference.
    """
    timestamp: float           # Unix Epoch of event
    generated_at: float        # Clock time at sensor generation
    cpu_load: float            # CPU utilization percentage (0.0 - 100.0)
    memory_usage: float        # RAM utilization percentage (0.0 - 100.0)
    bus_temp: float            # Bus temperature in Celsius
    network_tx: float          # Network transmission rate in kbps
    ground_truth_attack: bool  # Simulation flag for labeled anomaly testing
    
    # --- ML-Enriched Metadata ---
    ml_is_anomaly: Optional[bool]
    ml_anomaly_score: Optional[float]
    ml_predicted_cpu_t5: Optional[float]

@dataclass
class OrbitalState:
    """
    Physical state of an asset within the Guidance, Navigation, and Control loop.
    """
    x: float
    y: float
    z: float
    vx: float
    vy: float
    vz: float
    epoch: float
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
