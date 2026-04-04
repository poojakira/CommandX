# CommandX: Technical Architecture Deep-Dive

CommandX is a high-frequency orbital asset management and security platform. This document outlines the internal data models, machine learning logic, and architectural patterns that drive the system’s performance and reliability.

## 1. System Architecture

CommandX uses a decoupled high-throughput pipeline architecture designed for asynchronous telemetry ingestion and real-time inference.

```mermaid
graph TD
    subgraph "Ingestion Layer"
        TS[Telemetry Source] -- "Synthetic @ 50Hz" --> IQ[Ingestion Queue (Blocking Queue)]
    end
    
    subgraph "Compute Layer"
        IQ -- "Batch (n=16)" --> BIE[Batch Inference Engine]
        BIE -- "Isolation Forest" --> TAD[Threat Detection]
        BIE -- "Ridge Regression" --> TCP[CPU Forecasting]
    end
    
    subgraph "Visualization Layer"
        BIE -- "Enriched Payload" --> OB[Output Buffer (Circular deque)]
        OB -- "st.rerun()" --> UI[Streamlit Dashboard]
    end
```

## 2. Data Models & Schemas

### 2.1 Telemetry Packet Schema
Each telemetry packet is a JSON-serializable object containing high-precision system health and network metrics.

| Field | Type | Description | Range/Distribution |
|-------|------|-------------|--------------------|
| `timestamp` | float | Unix epoch of the telemetry event. | N/A |
| `cpu_load` | float | CPU utilization percentage. | 0.0 - 100.0 |
| `memory_usage`| float | RAM utilization percentage. | 0.0 - 100.0 |
| `bus_temp` | float | Internal spacecraft bus temperature (°C). | Normal (µ=25, σ=2) |
| `network_tx` | float | Network transmission throughput (kbps). | Normal (µ=500, σ=100) |
| `ml_is_anomaly`| bool | True if flagged by the Isolation Forest. | N/A |
| `ml_predicted_cpu_t5` | float | Predicted CPU load in 5 seconds. | 0.0 - 100.0 |

### 2.2 Orbital Data (TLE)
The system uses the standard **NORAD Two-Line Element (TLE)** format for tracking orbital assets.
- **Line 1**: Satellite number, Classification, Launch Year, Epoch, etc.
- **Line 2**: Inclination, RAAN, Eccentricity, Argument of Perigee, Mean Anomaly, Mean Motion.

## 3. Anomaly Detection & Prediction Logic

### 3.1 Cyber Threat Detection: Isolation Forest
CommandX implements an unsupervised Anomaly Detection model using `sklearn.ensemble.IsolationForest`.
- **Approach**: It isolates observations by randomly selecting a feature and then randomly selecting a split value between the maximum and minimum values of the selected feature.
- **Why Isolation Forest?**: It is effective in high-dimensional spaces and does not require pre-labeled "attack" data.
- **Cold Start**: The model requires a baseline of **200 samples** before initializing online inference to avoid false positives during initialization.

### 3.2 Time-Series Forecasting: Ridge Regression
For predictive maintenance (CPU load forecasting), the system uses a **Ridge Regression** model.
- **Windowing**: Trained on a trailing circular buffer of the last 200 samples.
- **Forecasting**: Predicts $t+5$ seconds ahead based on the current system trend.
- **SLA**: Re-trained periodically or upon significant buffer shifts.

## 4. Performance Specifications

- **Pipeline Throughput**: Optimized for >50Hz telemetry updates.
- **Inference Latency**: <50ms per batch (including feature extraction and scoring).
- **Service Level Agreement (SLA)**: 99.9% uptime for the anomaly detection stream during flight operations.

---
*CommandX v7.0 | Engineering Documentation | Apex-X Aerospace*
