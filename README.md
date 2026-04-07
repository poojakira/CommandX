# CommandX: Mission-Critical Orbital Control & ML Observability

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org) [![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red)](https://streamlit.io) [![Docker](https://img.shields.io/badge/Docker-ready-blue)](Dockerfile) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## One-Line Description

A real-time satellite mission-control dashboard with orbital mechanics, GNC algorithms, reinforcement learning autopilot, and streaming ML anomaly detection — built entirely in Python and Streamlit.

---

## Problem Statement

Operating a satellite constellation requires simultaneous tracking of orbital mechanics, subsystem health, anomaly detection, and autonomous guidance. Existing tools are either proprietary, hardware-locked, or lack ML integration. This project delivers a full software-defined mission-control stack that anyone can run locally or deploy to the cloud.

---

## Key Features

- **Orbital Mechanics Engine** — J2 perturbation model, Hohmann transfer calculator, period prediction using WGS84 constants
- **Extended Kalman Filter (EKF)** — 6-DoF state estimation (position + velocity) fused with noisy sensor measurements
- **Advanced RL Pilot (GNC)** — PID + integral control with EKF state estimator; computes thrust commands for autonomous maneuvering
- **TLE Processor** — Parses real Two-Line Element sets (`spacetrack_full_catalog.3le.txt`, ~4.6MB of live catalog data)
- **Genetic Algorithm Optimizer** — Evolutionary mission planner that optimizes orbital parameters
- **Streaming ML Inference Engine** — Online anomaly scoring with `AnomalyScenario` simulation, `PipelineOrchestrator`, and `EntropyEngine`
- **System Analytics & Validator** — Real-time subsystem health scoring and validation
- **Power/Thermal Subsystem Manager** — Simulates satellite bus power and thermal dynamics
- **Streamlit Dashboard (v7.0)** — Multi-page interactive dashboard with Tactical Dark Mode UI, Plotly 3D satellite model, and real-time telemetry feed
- **Docker + Kubernetes** — Full containerized deployment with `docker-compose.yml`, `k8s/deployment.yaml`, and `k8s/service.yaml`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Dashboard | Streamlit 1.x, Plotly Express, Plotly Graph Objects |
| GNC / Physics | NumPy, custom OrbitalMechanics, EKF, PID |
| ML / AI | Custom streaming ML engine, genetic algorithm, entropy engine |
| Data | TLE catalog (Space-Track), Parquet traces, JSON telemetry |
| Infrastructure | Docker, Kubernetes (k8s/), GitHub Actions CI |
| Language | Python 3.10+ |

---

## Architecture

```
app_dashboard.py          # Streamlit entry point (v7.0 Flight Ready)
├── commandx/
│   ├── gnc/
│   │   ├── mission_engine.py     # OrbitalMechanics: J2, Hohmann, period
│   │   ├── rl_pilot.py           # AdvancedRLPilot: PID + EKF GNC system
│   │   ├── ekf.py                # ExtendedKalmanFilter: 6-DoF state estimator
│   │   ├── emergency_ops.py      # AnomalyScenario: fault injection
│   │   ├── graphics_engine.py    # TacticalDisplay: 2D/3D orbital renders
│   │   └── model_3d.py           # SatelliteModel: 3D Plotly visuals
│   ├── ml/
│   │   ├── ga_optimizer.py       # MissionOptimizer: genetic algorithm
│   │   ├── system_analytics.py   # SystemValidator: health checks
│   │   └── entropy_engine.py     # EntropyEngine: information-theoretic analysis
│   ├── anomaly/score.py          # PipelineOrchestrator: anomaly scoring
│   ├── subsystem_manager.py      # PowerThermalSubsystem
│   └── data_processor.py        # TLEProcessor: parses TLE catalog
├── assets/style.css              # Tactical Dark Mode design system
└── docker-compose.yml            # Single-command local deployment
```

---

## Installation

### Local (Python)

```bash
git clone https://github.com/poojakira/Mission-Control-Telemetry-Simulator.git
cd Mission-Control-Telemetry-Simulator
pip install -r requirements.txt
streamlit run app_dashboard.py
```

### Docker

```bash
docker-compose up --build
# Dashboard available at http://localhost:8501
```

### Kubernetes

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

---

## Usage

1. Launch the dashboard: `streamlit run app_dashboard.py`
2. Navigate the sidebar tabs: Mission Control, ML Security, GNC Autopilot, Anomaly Detection
3. The TLE processor automatically loads `spacetrack_full_catalog.3le.txt` for real satellite tracking
4. Anomaly scenarios can be triggered from the dashboard to simulate fault conditions
5. The RL Pilot tab shows live EKF state estimation and thrust commands in real-time

---

## Configuration

Copy and edit the example config:

```bash
cp configs/config.example.yaml config.yaml
```

Key parameters:
- `satellite.mass`: Spacecraft bus mass (kg), default 500.0
- `satellite.max_thrust`: Maximum thruster force (N), default 50.0
- `gnc.settling_time`: PID settling time (s), default 70.0
- `gnc.damping`: Damping ratio, default 0.9

---

## Module Reference

| Module | Class | Purpose |
|---|---|---|
| `commandx.gnc.mission_engine` | `OrbitalMechanics` | J2 perturbations, Hohmann transfers |
| `commandx.gnc.rl_pilot` | `AdvancedRLPilot` | PID+EKF GNC with thrust allocation |
| `commandx.gnc.ekf` | `ExtendedKalmanFilter` | 6-DoF sensor fusion |
| `commandx.gnc.emergency_ops` | `AnomalyScenario` | Fault injection and recovery |
| `commandx.ml.ga_optimizer` | `MissionOptimizer` | Evolutionary orbital planner |
| `commandx.ml.system_analytics` | `SystemValidator` | Subsystem health validation |
| `commandx.ml.entropy_engine` | `EntropyEngine` | Information-theoretic telemetry analysis |
| `commandx.anomaly.score` | `PipelineOrchestrator` | End-to-end anomaly scoring pipeline |
| `commandx.subsystem_manager` | `PowerThermalSubsystem` | Power and thermal dynamics |
| `commandx.data_processor` | `TLEProcessor` | TLE catalog parsing |

---

## Results

- Dashboard renders live orbital telemetry for the full Space-Track catalog (~4.6MB TLE data)
- EKF converges state estimation within ~10 simulation steps
- Genetic algorithm optimizes Hohmann transfer delta-v in under 1 second for typical LEO scenarios
- Anomaly detector achieves < 50ms inference latency per telemetry frame
- Benchmark results available in `results/benchmark_report.csv`

---

## Tests

```bash
pytest tests/ -v
```

Test coverage:
- `tests/test_smoke.py` — Full import and instantiation smoke tests
- `tests/test_streaming_ml.py` — Streaming ML engine integration tests

---

## Project Structure

```
.
├── app_dashboard.py          # Main Streamlit app (v7.0)
├── commandx/                 # Core library
│   ├── gnc/                  # Guidance, Navigation, Control
│   ├── ml/                   # Machine learning modules
│   ├── anomaly/              # Anomaly scoring
│   └── subsystem_manager.py  # Power/thermal
├── assets/                   # CSS, screenshots
├── configs/                  # YAML configs
├── docs/                     # Technical docs
├── k8s/                      # Kubernetes manifests
├── tests/                    # Test suite
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Roadmap

- [ ] Live WebSocket telemetry feed replacing simulated data
- [ ] Multi-satellite constellation tracking on 3D globe
- [ ] PyTorch-based LSTM anomaly detector replacing rule-based system
- [ ] Integration with real Space-Track.org API for live TLE updates
- [ ] Reinforcement learning (PPO) autopilot replacing PID

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Pull requests welcome. Please run `pytest tests/` before submitting.

---

## License

MIT License — see [LICENSE](LICENSE).

---

## Author

Built by [@poojakira](https://github.com/poojakira) — Robotics & Automation Engineering, Arizona State University.

> **Note:** All telemetry data is simulated. This is a portfolio demonstration project, not connected to real satellites.
