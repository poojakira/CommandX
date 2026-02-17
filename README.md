# 🛰️ CommandX
### Orbital Mission Control Platform — v7.0

> A flight-ready satellite mission control system built on real orbital physics, autonomous GNC, and AI-driven trajectory optimization. CommandX brings together the tools mission operators need — from live fleet monitoring to hardware stress simulation — inside a single command interface.

![CommandX Dashboard](https://github.com/user-attachments/assets/177b5513-88e9-4822-8015-dc77089f9009)

---

## Table of Contents

- [Overview](#overview)
- [Core Capabilities](#core-capabilities)
- [System Architecture](#system-architecture)
- [Getting Started](#getting-started)
- [Mission Phases](#mission-phases)
- [Enterprise Value](#enterprise-value)

---

## Overview

CommandX is a Python-based orbital mission control dashboard designed to simulate and manage satellite operations with real-world fidelity. It ingests live TLE (Two-Line Element) data from the Space-Track full catalog, propagates orbital states using verified physical constants, and runs an autonomous GNC (Guidance, Navigation & Control) loop powered by an Extended Kalman Filter.

Unlike generic space visualizers, CommandX is built for operators. Every module reflects actual flight software architecture — from IMU drift modelling in the Entropy Engine to 3-sigma certification testing in the Monte Carlo validator. The system is deployable via Docker and runs entirely in a browser through Streamlit.

---

## Core Capabilities

### 🌍 Live Fleet Tracking
CommandX parses the full Space-Track satellite catalog (`spacetrack_full_catalog.3le.txt`) containing thousands of active and historical objects. Satellites are rendered on an interactive global map showing real-time position, coverage zones, and AOS/LOS (Acquisition of Signal / Loss of Signal) windows for active passes.

### 🧭 Guidance, Navigation & Control (GNC)
The GNC system simulates proximity operations — the precise close-range maneuvering required for rendezvous, inspection, and docking. At its core is an Extended Kalman Filter (`gnc_kalman.py`) operating at 10Hz, fusing noisy sensor measurements into clean state estimates of position and velocity across all six degrees of freedom. The `rl_pilot.py` autonomous pilot reads these estimates and computes real-time thrust commands, steering a 500kg spacecraft bus with a 50N thruster toward a target.

### 🧬 Trajectory Optimization
The Genetic Algorithm optimizer (`ga_optimizer.py`) searches the mission solution space to find the optimal orbital altitude and transfer trajectory. Each candidate solution is evaluated against three real constraints — Delta-V fuel cost, Van Allen radiation belt exposure, and atmospheric drag — and cross-referenced against the live satellite catalog to flag Starlink-shell collision corridors. The optimizer returns the trajectory that minimizes total mission cost while satisfying all safety margins.

### ⚡ Entropy Engine — Hardware Degradation Simulation
Real hardware is never perfect. The `entropy_engine.py` module injects physics-accurate noise into every simulation step: thermal white noise (±5cm positional jitter, ±1cm/s velocity jitter), IMU gyroscope bias drift modelled as a random walk, and stochastic Single Event Upsets (SEUs) caused by radiation bit-flips. This transforms CommandX from an idealized simulator into an honest test environment.

### 🔋 Power & Thermal Subsystem Monitoring
The `subsystem_manager.py` models a 6U CubeSat power bus in real time. It tracks solar panel generation (28% efficient triple-junction cells, 0.12m² area), battery state-of-charge across eclipse and sunlit periods, thruster power draw (45W), avionics baseline load (5W), and heater activation during eclipse (12W). Thermal state evolves continuously, cooling during shadow passes and heating in direct sunlight.

### 📊 Monte Carlo Certification
Before any mission can be marked flight-ready, it must pass Independent Verification & Validation (IV&V). `system_analytics.py` runs configurable Monte Carlo trials, each executing a full GNC docking simulation through the Entropy Engine's noise field. Results are scored by final docking accuracy, aggregated into mean, standard deviation, and 3-sigma worst-case margins, and compared against the 98% accuracy requirement threshold. A negative margin means the mission fails certification.

### 🖥️ 3D Visualization & Tactical Display
`graphics_engine.py` and `model_3d.py` render interactive Plotly-based 3D spacecraft models, orbital trajectories, proximity operation approach corridors, and tactical overlays — all navigable in the browser without any external 3D software.

---

## System Architecture

```
commandx/
│
├── app_dashboard.py            # Streamlit UI — main entry point & command center
│
├── Core Physics
│   ├── mission_engine.py       # Orbital mechanics, Kepler equations, env constants
│   └── data_processor.py       # TLE ingestion & satellite catalog parsing
│
├── GNC Stack
│   ├── gnc_kalman.py           # Extended Kalman Filter — state estimation
│   └── rl_pilot.py             # Autonomous pilot — thrust command generation
│
├── Mission Planning
│   └── ga_optimizer.py         # Genetic Algorithm — trajectory & altitude optimizer
│
├── Simulation Layer
│   ├── entropy_engine.py       # IMU drift, thermal noise, radiation events
│   └── subsystem_manager.py    # Power budget, battery, thermal monitoring
│
├── Validation
│   └── system_analytics.py     # Monte Carlo IV&V, 3-sigma certification
│
├── Visualization
│   ├── graphics_engine.py      # 2D tactical display & orbital overlays
│   └── model_3d.py             # Interactive 3D spacecraft renderer
│
├── Data
│   └── spacetrack_full_catalog.3le.txt   # Full satellite TLE catalog
│
├── requirements.txt
└── Dockerfile
```

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

| Package | Role |
|---|---|
| `streamlit` | Web dashboard UI |
| `plotly` | Interactive 3D and 2D visualizations |
| `numpy` | Linear algebra, state vectors, physics |
| `scipy` | Scientific computing utilities |
| `pandas` | Tabular satellite data handling |
| `skyfield` | TLE propagation and orbital computation |
| `deap` | Genetic algorithm framework |
| `watchdog` | File system event monitoring |

---

## Mission Phases

CommandX organizes operations into four sequential mission phases, each mapping to a dedicated section of the dashboard.

**Phase 1 — Command Center**
Live global fleet status. Operators monitor satellite health indicators, link budget margins, and AOS/LOS scheduling across the entire tracked constellation.

**Phase 2 — Flight Dynamics**
GNC simulation workspace. Run proximity operations, tune Kalman Filter parameters, observe docking approach trajectories, and review thruster fuel consumption in real time.

**Phase 3 — Certification**
Monte Carlo testing suite. Define the number of trial iterations, execute the full IV&V run, and receive a pass/fail certification report with 3-sigma statistical margins against the 98% accuracy requirement.

**Phase 4 — Mission Planning**
AI-assisted trajectory optimization. Input mission constraints (target orbit, fuel budget, radiation tolerance) and let the Genetic Algorithm return the safest, most efficient transfer trajectory with full collision risk scoring.

---

## Enterprise Value

CommandX was designed with production-grade mission operations in mind. For organizations operating satellite programs — whether commercial, research, or defence — the platform delivers measurable value at multiple levels.

### Reducing the Cost of Mission Validation
Traditional spacecraft validation relies on expensive hardware-in-the-loop (HITL) test benches and contracted IV&V services. CommandX brings that capability into software. The Monte Carlo certification engine can run thousands of simulated docking scenarios in minutes, identifying failure modes before hardware is ever involved. For a commercial operator, this compresses pre-launch verification timelines and reduces dependency on third-party testing contracts — translating directly into lower program costs and faster time-to-orbit.

### Operationalizing AI-Driven Mission Planning
Orbital mission planning is still largely manual at many organizations — a flight dynamicist reviews trajectory options and selects based on heuristics and experience. CommandX automates this through a Genetic Algorithm that simultaneously optimizes for fuel cost, radiation risk, atmospheric drag, and collision avoidance against the full live catalog. This makes optimal planning accessible without requiring deep orbital mechanics expertise on every shift, enabling leaner ground operations teams while improving decision quality.

### Fleet Scalability Without Architectural Rework
The platform is built around the full Space-Track satellite catalog rather than a fixed list of owned assets. As an operator's constellation grows — from five satellites to five hundred — CommandX scales without architectural changes. The same TLE ingestion pipeline, the same visualization stack, and the same GNC tools apply regardless of fleet size. For constellation operators, this is a significant operational advantage over bespoke per-satellite tooling that becomes a maintenance liability at scale.

### Quantifiable Risk Intelligence for Mission Assurance
The Entropy Engine's IMU drift, thermal noise, and radiation bit-flip simulation gives risk and reliability teams a tool to quantify the impact of hardware degradation on mission success probability. Running certification trials through intentionally degraded hardware states produces statistical evidence of system robustness — 3-sigma worst-case margins — that can support insurance underwriting, regulatory submissions, and formal mission assurance reviews. These outputs have direct financial and compliance implications at the enterprise level that generic simulators cannot provide.

### Subsystem Health for Asset Lifecycle Management
The power and thermal subsystem monitor provides continuous visibility into battery state-of-charge, solar generation efficiency, and thermal margin across eclipse cycles. For operators managing satellite lifetime and planning end-of-life deorbit, this data directly informs battery degradation modelling and remaining useful life estimates. Those decisions affect asset valuation on balance sheets, spectrum license compliance with regulators, and orbital slot management — all critical concerns for any operator running a commercial satellite program.

### Rapid Integration into Existing Ground Infrastructure
CommandX ships with a Dockerfile, meaning it can be deployed into existing cloud infrastructure in minutes. Whether running on a dedicated ground station server or a managed Kubernetes cluster, the containerized architecture allows DevOps and mission operations teams to integrate CommandX alongside other ground segment software without custom environment configuration. This lowers adoption cost, simplifies version management, and makes the platform straightforward to scale as operational demands increase.

---

<p align="center">
  <strong>CommandX</strong> — Mission control that operates at the speed of your ambition.
</p>
