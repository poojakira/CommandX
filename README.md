# Mission-Control-Telemetry-Simulator 

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Docker-ready-blue)](Dockerfile)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

**Real-time satellite mission-control dashboard with orbital mechanics, GNC algorithms, RL autopilot, and streaming ML anomaly detection — built entirely in Python and Streamlit.**

---

## What It Does

CommandX is a full software-defined mission-control stack for satellite constellation management. It simulates orbital mechanics, runs autonomous guidance algorithms, and performs real-time ML anomaly scoring — all runnable locally or deployable to the cloud.

---

## Key Features

- **Orbital Mechanics Engine** — J2 perturbation model, Hohmann transfer calculator, period prediction using WGS84 constants
- **Extended Kalman Filter (EKF)** — 6-DoF state estimation (position + velocity) fused with noisy sensor measurements
- **Advanced RL Pilot (GNC)** — PID + integral control with EKF state estimator for autonomous thrust allocation
- **TLE Processor** — Parses real Two-Line Element sets from the Space-Track catalog (~4.6 MB of live data)
- **Genetic Algorithm Optimizer** — Evolutionary mission planner for optimizing orbital parameters and delta-v
- **Streaming ML Inference Engine** — Online anomaly scoring via `AnomalyScenario`, `PipelineOrchestrator`, and `EntropyEngine`
- **Power/Thermal Subsystem Manager** — Simulates satellite bus power and thermal dynamics
- **Streamlit Dashboard (v7.0)** — Multi-page dashboard with Tactical Dark Mode UI and Plotly 3D satellite visualization
- **Docker + Kubernetes** — Containerized deployment via `docker-compose.yml`, `k8s/deployment.yaml`, and `k8s/service.yaml`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Dashboard | Streamlit 1.x, Plotly Express, Plotly Graph Objects |
| GNC / Physics | NumPy, custom OrbitalMechanics, EKF, PID |
| ML / AI | Custom streaming ML engine, genetic algorithm, entropy engine |
| Data | TLE catalog (Space-Track), Parquet traces, JSON telemetry |
| Infrastructure | Docker, Kubernetes, GitHub Actions CI |
| Language | Python 3.10+ |

---

## Results

- Dashboard renders live orbital telemetry for the full Space-Track catalog (~4.6 MB TLE data)
- EKF converges state estimation within ~10 simulation steps
- Genetic algorithm optimizes Hohmann transfer delta-v in under 1 second for typical LEO scenarios
- Anomaly detector achieves < 50 ms inference latency per telemetry frame

---

## Quick Start

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

## Configuration

```bash
cp configs/config.example.yaml config.yaml
# Key parameters: satellite.mass, satellite.max_thrust, gnc.settling_time, gnc.damping
```

---

## Project Structure

```
.
├── app_dashboard.py       # Streamlit entry point (v7.0)
├── commandx/
│   ├── gnc/               # OrbitalMechanics, RL Pilot, EKF, fault injection
│   ├── ml/                # Genetic algorithm, system analytics, entropy engine
│   ├── anomaly/score.py   # PipelineOrchestrator: end-to-end anomaly scoring
│   └── subsystem_manager.py  # Power/thermal dynamics
├── assets/               # CSS, screenshots
├── configs/              # YAML configs
├── docs/                 # Technical documentation
├── k8s/                  # Kubernetes manifests
├── tests/                # Smoke tests and streaming ML integration tests
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Roadmap

- [ ] Live WebSocket telemetry feed replacing simulated data
- [ ] Multi-satellite constellation tracking on 3D globe
- [ ] PyTorch-based LSTM anomaly detector replacing rule-based system
- [ ] Integration with real Space-Track.org API for live TLE updates
- [ ] Reinforcement learning (PPO) autopilot replacing PID

---

## License

MIT — see [LICENSE](LICENSE).

---

## Author

Built by [Pooja Kiran](https://github.com/poojakira) — M.S. student at Arizona State University.

> **Note:** All telemetry data is simulated. This is a portfolio demonstration project, not connected to real satellites.
