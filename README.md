# 🛰️ CommandX
### Orbital Mission Control Platform — v7.0

> A flight-ready satellite mission control system built on real orbital physics, autonomous GNC, and AI-driven trajectory optimization. CommandX brings together the tools mission operators need — from live fleet monitoring to hardware stress simulation — inside a single command interface.



## Table of Contents

- [Overview](#overview)
- [Core Capabilities](#core-capabilities)
- [System Architecture](#system-architecture)
-  [Mission Phases](#mission-phases)
- [Getting Started](#getting-started)
- [Enterprise Value](#enterprise-value)

---

## Overview

Orbital Mission Control Platform — v7.0

A flight-ready satellite mission control system built on real orbital physics, autonomous GNC, and AI-driven trajectory optimization. CommandX brings together the tools mission operators need — from live fleet monitoring to hardware stress simulation — inside a single, containerized command interface.

Unlike generic space visualizers, CommandX is built for operators. Every module reflects actual flight software architecture — from IMU drift modeling in the Entropy Engine to 3-sigma certification testing in the Monte Carlo validator. The system is deployable via Docker and runs entirely in a browser through Streamlit.

🚀 Proven Performance Metrics

60.0% Fuel & Risk Optimization: Engineered a Genetic Algorithm that autonomously routes trajectories to bypass high-density orbital shells (e.g., Starlink constellations). By natively avoiding collision-prone corridors, the system reduces total mission cost ($\Delta V$ + risk penalties) by 60% compared to unoptimized baseline transfers.

<img width="580" height="251" alt="image" src="https://github.com/user-attachments/assets/187817bb-d348-4400-bd00-1fef367aaf77" />


99.9% Verification Time Compression: Architected a high-throughput Monte Carlo IV&V suite that executes 1,000+ stochastic simulations in under 7 minutes. This replaces traditional 2-week Hardware-in-the-Loop (HITL) testing cycles, accelerating flight-readiness certification by over three orders of magnitude.


3-Sigma Reliability (99.28%): Mathematically validated GNC robustness by simulating extreme hardware degradation (IMU drift, radiation-induced bit-flips). The system maintains a 99.27% worst-case accuracy ($\mu - 3\sigma$), exceeding strict aerospace industry requirements with a 1.27% safety margin.

<img width="722" height="336" alt="image" src="https://github.com/user-attachments/assets/3d2b2e07-1fc6-4b6a-9b94-887cc995f7d1" />


Massive-Scale Data Ingestion: Developed a real-time pipeline that ingests, maps, and propagates the live Space-Track catalog, maintaining high-fidelity state awareness for 15,348+ active space assets.

### ⚙️ Core Capabilities

🌍 Live Fleet Tracking
Parses the full Space-Track satellite catalog (spacetrack_full_catalog.3le.txt). Satellites are rendered on an interactive global map showing real-time position, coverage zones, and AOS/LOS (Acquisition of Signal / Loss of Signal) windows for active passes.

🧭 Autonomous Guidance, Navigation & Control (GNC)
Simulates proximity operations for rendezvous, inspection, and docking. At its core is an Extended Kalman Filter (EKF) operating at 10Hz, fusing noisy sensor measurements into clean state estimates across six degrees of freedom. An RL Pilot reads these estimates to compute real-time thrust commands, steering a 500kg spacecraft bus with a 50N thruster toward its target.

🧬 AI Trajectory Optimization
The Genetic Algorithm (ga_optimizer.py) evaluates candidate transfer trajectories against live physics and traffic constraints:

Delta-V Fuel Cost (Hohmann base calculations)

Environmental Penalties (Atmospheric drag, Van Allen radiation belt exposure)

Collision Risk (Dynamic penalty scoring based on a live 10km-binned density map of 15,000+ real satellites)

⚡ Entropy Engine — Hardware Degradation
Real hardware is never perfect. The entropy_engine.py module transforms CommandX into an honest test environment by injecting physics-accurate noise:

Thermal white noise (±5cm positional jitter, ±1cm/s velocity jitter)

IMU gyroscope bias drift modeled as a random walk

Stochastic Single Event Upsets (SEUs) caused by radiation bit-flips

📊 Monte Carlo Certification (IV&V)
Missions must pass Independent Verification & Validation. system_analytics.py executes thousands of full GNC docking simulations through the Entropy Engine's noise field. Results are scored by docking accuracy and aggregated to prove 3-sigma worst-case margins stay above strict 98% aerospace requirement thresholds.

🖥️ Tactical 3D Visualization
Renders interactive Plotly-based 3D spacecraft models, orbital trajectories, proximity approach corridors, and tactical overlays natively in the browser.

 ### 🗺️ Mission Phases (Dashboard UI)
CommandX organizes operations into four sequential mission phases, mapped directly to the Streamlit UI:

Phase 1 — Command Center: Live global fleet status. Monitor satellite health, link budget margins, and AOS/LOS scheduling.

Phase 2 — Flight Dynamics (GNC): Simulation workspace. Run proximity operations, observe docking approaches, and review thruster fuel consumption in real time.

Phase 3 — Certification (IV&V): Monte Carlo testing suite. Execute thousands of trials and generate a pass/fail statistical margin report.

Phase 4 — Mission Planning: AI trajectory optimization. Input target orbits and let the Genetic Algorithm return the safest, most efficient transfer path.

## System Architecture

## Note: Extract the zip folder and place it as follows

----

<img width="567" height="620" alt="image" src="https://github.com/user-attachments/assets/e50edad6-5db2-4df0-96c2-83bd88e4f83f" />


---

## Getting Started

### Requirements

- Python 3.9 or higher
- Docker (optional, recommended for clean deployment)

### Run with Docker

```bash
# Build the image
docker build -t commandx .

# Run the dashboard
docker run -p 8501:8501 commandx
```

Open your browser at `http://localhost:8501`.

### Manual Setup

```bash
# Step 1 — Install all dependencies
pip install -r requirements.txt

# Step 2 — Launch the dashboard
streamlit run app_dashboard.py
```

### Dependencies

<img width="652" height="256" alt="image" src="https://github.com/user-attachments/assets/dc90af8f-f4de-4a32-967d-1cc287937c30" />


---


## Enterprise Value

Operationalizing AI: Automates complex orbital planning, allowing leaner teams to identify optimal, collision-free transfer orbits without relying purely on manual dynamicist heuristics.

Risk Intelligence: Quantifies the exact statistical impact of hardware degradation on mission success probability, outputting hard data for insurance underwriting and regulatory compliance.

Scalability: Built on a unified catalog architecture that scales effortlessly from tracking 5 owned assets to monitoring a 500-satellite constellation without underlying code rewrites.

---

![commandx](https://github.com/user-attachments/assets/3e3c3e07-0fa4-4d66-8df5-e840ecd55b03)
