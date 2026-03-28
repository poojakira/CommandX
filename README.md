# CommandX — Orbital Dynamics & Mission Planning

**Orbital mechanics simulation for satellite constellation management — academic/personal project**

[![Version](https://img.shields.io/badge/version-v7.0-blue.svg?style=flat-square)](https://github.com/poojakira/CommandX)
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg?style=flat-square)](LICENSE)

**Genetic Algorithm Optimizer** · **Extended Kalman Filter** · **Monte Carlo IV&V** · **TLE Data Pipeline** · **Streamlit Dashboard**

---

## 1. Overview

CommandX is an orbital mechanics simulation platform built to explore satellite constellation management, proximity operations, and mission trajectory optimization. It integrates Space-Track TLE data with GNC (Guidance, Navigation, and Control) algorithms as a hands-on learning project in orbital mechanics, ML systems, and DevOps.

### Key Features

- **Genetic Algorithm Optimizer** — Multi-objective fuel-optimal trajectory optimization over N-dimensional search space
- **Extended Kalman Filter (EKF)** — 6-DOF orbit estimation with noise cancellation for state awareness
- **Monte Carlo IV&V** — 1,000 stochastic docking simulations with 3-sigma confidence intervals
- **TLE Data Pipeline** — Parses live 3LE Space-Track catalogs for 17,000+ active satellite records
- **Streaming ML Engine** — Async telemetry buffering with real-time ML inference backend

---

## 2. Module Structure

### GNC & Orbital Mechanics

| # | Module | Description |
|---|---|---|
| 1 | `mission_engine.py` | Orbital physics (J2 perturbations, Hohmann transfers, Keplerian dynamics) |
| 2 | `gnc_kalman.py` | Guidance, Navigation, and Control via Extended Kalman Filters (EKF) |
| 3 | `rl_pilot.py` | Actuator control and PID logic for precision docking simulation |
| 4 | `graphics_engine.py` | 3D trajectory visualizations using Plotly |
| 5 | `model_3d.py` | Spacecraft geometry and mass property models |
| 6 | `subsystem_manager.py` | Satellite bus telemetry abstraction |
| 7 | `emergency_ops.py` | Fail-safe and decommissioning protocols |

### ML & Data

| # | Module | Description |
|---|---|---|
| 1 | `ga_optimizer.py` | Multi-objective trajectory optimization via Genetic Algorithms |
| 2 | `streaming_ml_engine.py` | Async telemetry buffering and real-time ML inference backend |
| 3 | `system_analytics.py` | Monte Carlo IV&V suite for statistical verification |
| 4 | `data_processor.py` | TLE parsing, catalog management, and data cleaning |
| 5 | `run_anomaly_test.py` | Isolation Forest-based anomaly detection on telemetry streams |
| 6 | `entropy_engine.py` | Statistical analysis of state-space uncertainty |

### Shared Infrastructure

| # | Module | Description |
|---|---|---|
| 1 | `app_dashboard.py` | Main Streamlit mission control dashboard |
| 2 | `Dockerfile` | Containerization for Docker/K8s deployment |
| 3 | `k8s/` | Kubernetes manifests for orchestration |

---

## 3. Quick Start

```bash
git clone https://github.com/poojakira/CommandX.git
cd CommandX
pip install -r requirements.txt
streamlit run app_dashboard.py
```

---

## 4. Deployment

### Docker

```bash
docker build -t commandx:latest .
docker run -d -p 8501:8501 --name commandx commandx:latest
```

### Kubernetes (Minikube)

```bash
minikube start --driver=docker
docker build -t commandx:latest .
minikube image load commandx:latest
kubectl apply -f k8s/
```

### Amazon EC2

- Launch EC2 instance (Amazon Linux or Ubuntu)
- Paste contents of `ec2-user-data.sh` into User Data field
- Allow inbound HTTP on Port 80

---

## 5. Testing & Verification

```bash
python system_analytics.py
```

Executes 1,000 stochastic docking simulations and reports 3-sigma accuracy confidence intervals.

| Suite | Count |
|---|---|
| Monte Carlo simulations | 1,000 scenarios |

---

## 6. References

- **Orbital Mechanics**: Bate, Mueller & White, Fundamentals of Astrodynamics
- **Kalman Filter**: Welch & Bishop, Introduction to the Kalman Filter
- **Space-Track TLE Data**: https://www.space-track.org/

---

## 7. Team Contributions

> This is an academic/personal project built to learn orbital mechanics simulation, ML systems, and DevOps. Neither contributor has professional industry experience — all work was done as self-directed learning.

### Pooja Kiran

| # | What I Worked On | What I Built / Learned | Outcome |
|---|---|---|---|
| 1 | Genetic Algorithm Trajectory Optimizer | Implemented `ga_optimizer.py`: multi-objective fuel-optimal trajectory optimization via Genetic Algorithms over N-dimensional search space, evading radiation belts and high-drag zones | Produces fuel-optimal Hohmann transfer solutions; tested across multiple constraint configurations |
| 2 | Real-Time Streaming ML Engine | Built `streaming_ml_engine.py`: async telemetry buffering and real-time ML inference backend with dynamic batching | Async inference pipeline for high-frequency distributed telemetry |
| 3 | Monte Carlo IV&V Suite | Implemented `system_analytics.py`: Monte Carlo verification suite executing 1,000 stochastic docking simulations and reporting 3-sigma accuracy confidence intervals | 1,000 randomized scenarios; 3-sigma statistical verification of docking accuracy |
| 4 | TLE Data Pipeline | Built `data_processor.py`: parsing of live 3LE Space-Track catalogs, space-object catalog management, and data cleaning | Processes 17,000+ active satellite TLE records for conjunction risk analysis |
| 5 | Cyber Anomaly Detection | Implemented `run_anomaly_test.py`: Isolation Forest-based anomaly detection on satellite telemetry streams | Anomaly detection integrated with streaming ML backend |
| 6 | Entropy Engine | Built `entropy_engine.py`: statistical analysis of state-space uncertainty and information gain for orbit estimation quality | Quantifies estimation uncertainty in 6-DOF orbital state vectors |

### Rhutvik Pachghare

| # | What I Worked On | What I Built / Learned | Outcome |
|---|---|---|---|
| 1 | Repository documentation restructure | Restructured the README and authored CODEOWNERS.md for engineering domain separation between GNC and ML modules | Clear separation of GNC vs ML engineering domains; CODEOWNERS.md establishes code ownership |
| 2 | Kubernetes deployment infrastructure | Added complete K8s manifests in `k8s/` directory; verified locally on Minikube | Kubernetes manifests verified on Minikube; supports Docker + K8s + EC2 deployment targets |
| 3 | Docker & EC2 provisioning | Added `Dockerfile`, Docker build pipeline, and `ec2-user-data.sh` for auto-provisioning EC2 instances | 3-target deployment: Docker (localhost:8501) + Kubernetes + Amazon EC2 (Port 80) |
| 4 | CI workflow & test infrastructure | Added `.github/workflows/ci.yml` and Pytest configurations; integrated `pytest.ini` and `__init__.py` | CI runs on every push to main; Pytest configured for strict type checking |
| 5 | Streamlit dashboard improvements | Improved `app_dashboard.py` visualization and telemetry display for real-time mission monitoring | Enhanced dashboard layout and telemetry visualization |

---

**Version**: v7.0 | **License**: MIT
