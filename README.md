# 🛰️ CommandX: Advanced Orbital Dynamics & Mission Planning

[![Version](https://img.shields.io/badge/version-v7.0-blue.svg?style=flat-square)](https://github.com/yourusername/CommandX)
[![Status](https://img.shields.io/badge/status-Flight--Ready-green.svg?style=flat-square)](https://github.com/yourusername/CommandX)
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg?style=flat-square)](LICENSE)

CommandX is a high-fidelity orbital mechanics platform designed for satellite constellation management, proximity operations, and mission trajectory optimization. It integrates real-world Space-Track TLE data with advanced GNC (Guidance, Navigation, and Control) algorithms to provide a production-grade simulation environment.

---

## ⚡ The Problem: Orbital Congestion
As of 2024, there are over 17,000 active satellites and hundreds of thousands of debris particles in Low Earth Orbit (LEO). Legacy mission planning tools often:
- **Ignore Live Traffic**: Planning in a vacuum leads to conjunction risks.
- **Simplistic Physics**: Failing to account for J2 perturbations or atmospheric drag.
- **Manual Optimization**: Relying on human intuition for complex multi-constraint transfers.

## 🚀 The Solution: CommandX
CommandX addresses these challenges by automating the "Sense-Analyze-Act" loop for orbital assets:
- **Live Traffic Awareness**: Automatically parses live `3LE` catalogs to map orbital density.
- **Physics-First Optimization**: Uses Genetic Algorithms to find fuel-efficient trajectories that avoid radiation belts and high-drag zones.
- **Robust Estimation**: Implements an Extended Kalman Filter (EKF) to maintain state awareness even with noisy sensor telemetry.

---

## 🏗️ Project Structure

```text
CommandX/
├── app_dashboard.py      # Streamlit UI & Mission Control Center
├── mission_engine.py      # Orbital Physics (J2, Hohmann, Keplerian)
├── ga_optimizer.py       # Trajectory Planning via Genetic Algorithms
├── gnc_kalman.py         # Guidance & Navigation (Extended Kalman Filter)
├── rl_pilot.py           # Actuator Control & PID Logic
├── system_analytics.py   # Monte Carlo IV&V Simulation Suite
├── data_processor.py      # TLE Parsing & Catalog Management
├── graphics_engine.py    # 3D Plotly Tactical Visuals
├── model_3d.py           # Spacecraft Geometry Models
└── requirements.txt      # Project Dependencies
```

---

## 🔄 Workflow Diagram

```mermaid
graph TD
    A[Space-Track TLE Data] --> B[data_processor.py]
    B --> C{Catalog Mapping}
    C -->|Density Map| D[ga_optimizer.py]
    E[Mission Constraints] --> D
    D -->|Optimal Trajectory| F[app_dashboard.py]
    
    subgraph "Flight Loop"
    G[Sensor Noise] --> H[gnc_kalman.py EKF]
    H -->|Estimated State| I[rl_pilot.py PID]
    I -->|Actuator Command| J[Physics Engine]
    J --> G
    end
    
    F -->|Command Execution| G
```

---

## 🛠️ Getting Started

### Prerequisites
- Python 3.9+
- Pip (Python Package Manager)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/CommandX.git
   cd CommandX
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Locally
Launch the Mission Control dashboard natively using Python:
```bash
streamlit run app_dashboard.py
```

## 🌐 Deployment Pipeline

### Deploying with Docker
You can containerize the CommandX pipeline using the provided `Dockerfile`.
1. Build the Docker image:
   ```bash
   docker build -t commandx:latest .
   ```
2. Run the container:
   ```bash
   docker run -d -p 8501:8501 --name commandx commandx:latest
   ```
Access the application at `http://localhost:8501`.

### Deploying with Kubernetes
We provide Kubernetes manifests in the `k8s/` directory.

**(Verified Locally on Minikube)**
1. If using [Minikube](https://minikube.sigs.k8s.io/), ensure your local Docker daemon is running and execute:
   ```bash
   minikube start --driver=docker
   # Build the image and load it into minikube
   docker build -t commandx:latest .
   minikube image load commandx:latest
   ```
2. Apply the deployment and service configurations:
   ```bash
   kubectl apply -f k8s/
   ```
3. Retrieve the external IP (or map to localhost via minikube service alias):
   ```bash
   kubectl get svc commandx-service
   # For Minikube users:
   minikube service commandx-service --url
   ```
### Deploying to Amazon EC2
We provide an `ec2-user-data.sh` script to auto-provision an EC2 instance.
1. Launch an EC2 instance (Amazon Linux or Ubuntu) and paste the contents of `ec2-user-data.sh` into the **User Data** field under Advanced Details.
2. Ensure your Security Group allows inbound HTTP traffic on **Port 80**.
3. Once provisioned, SSH into the instance and follow the instructions in the script comments to build and run the Docker image.

---

## 📊 Verification & Validation (IV&V)
CommandX includes a professional verification suite to ensure flight readiness. You can run a standalone Monte Carlo analysis to verify GNC robustness:
```bash
python system_analytics.py
```
This will execute 1,000 stochastic docking simulations and report 3-sigma accuracy confidence intervals.

---

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
