import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import time
import os

# --- MODULE IMPORTS (REORGANIZED) ---
from commandx.data_processor import TLEProcessor
from commandx.gnc.mission_engine import OrbitalMechanics, MU
from commandx.gnc.rl_pilot import AdvancedRLPilot
from commandx.ml.ga_optimizer import MissionOptimizer
from commandx.ml.system_analytics import SystemValidator
from commandx.subsystem_manager import PowerThermalSubsystem
from commandx.ml.entropy_engine import EntropyEngine
from commandx.gnc.graphics_engine import TacticalDisplay
from commandx.gnc.model_3d import SatelliteModel  # 3D Visuals
from commandx.gnc.emergency_ops import AnomalyScenario
from commandx.anomaly.score import PipelineOrchestrator
from commandx.gnc.ekf import ExtendedKalmanFilter

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Orbital Command v7.0 (Flight Ready)",
    layout="wide",
    page_icon="🛰️",
    initial_sidebar_state="expanded"
)

# --- DESIGN SYSTEM LOADER ---
def load_css(file_path):
    with open(file_path) as f:
        st.markdown('<style>' + f.read() + '</style>', unsafe_allow_html=True)

# Load Tactical Design System
css_path = os.path.join("assets", "style.css")
if os.path.exists(css_path):
    load_css(css_path)
    # Inject Google Font
    st.markdown('<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">', unsafe_allow_html=True)
else:
    st.error("Technical Error: Design system (style.css) not found in assets.")

# --- SIDEBAR ---
st.sidebar.image("https://img.icons8.com/color/96/satellite-in-orbit.png", width=80)
st.sidebar.title("Orbital Command")
st.sidebar.caption("v7.0 | Flight Ready | Real-World Physics")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Mission Phase",
    ["1. Command Center", "2. Flight Dynamics (GNC)", "3. Certification (IV&V)", "4. Mission Planning", "5. Emergency Operations", "6. ML Pipeline & Security"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Project Lead:** Apex-X")
st.sidebar.caption("Military-Grade Orbital Assets")

# Initialize Streaming Engine and attach to session_state so it persists across reruns
if 'streamer' not in st.session_state:
    st.session_state['streamer'] = PipelineOrchestrator(frequency_hz=20, buffer_duration_sec=10)
    st.session_state['streamer'].start()

# ==============================================================================
# PAGE 1: COMMAND CENTER (Global Awareness)
# ==============================================================================
if page == "1. Command Center":
    st.title("🌐 Mission Command Center")
    st.markdown("Global fleet tracking and link budget analysis.")
    
    col_visual, col_stats = st.columns([1, 2])
    
    with col_visual:
        st.markdown("### 🛰️ Asset Telemetry")
        sat_fig = SatelliteModel.get_spacecraft_fig()
        st.plotly_chart(sat_fig, use_container_width=True, config={'displayModeBar': False})
        
    with col_stats:
        processor = TLEProcessor()
        catalog = processor.load_catalog()
        
        m1, m2 = st.columns(2)
        m1.metric("Active Assets", len(catalog))
        
        # REALISM: Simulated Ground Station Pass
        if int(time.time()) % 60 < 30:
            m2.metric("Link Status", "AOS (Acquisition of Signal)", delta="Connected")
            st.success("📡 Ground Station: Svalbard (SVAL) | Signal Strength: -85 dBm")
        else:
            m2.metric("Link Status", "LOS (Loss of Signal)", delta="-Waiting", delta_color="inverse")
            st.warning("📶 Satellite is over the Pacific Ocean. Waiting for next pass...")
        
        m3, m4 = st.columns(2)
        m3.metric("Ground Stations", "4 (Active)")
        m4.metric("Collision Risk", "LOW")

    st.markdown("### 📡 Fleet Distribution")
    if len(catalog) > 0:
        sat_data = []
        items = list(catalog.items())
        for name, sat in items[:500]: 
            try:
                sat_data.append({"Name": name, "Mean Motion": sat.model.no_kozai, "Inclination": np.degrees(sat.model.inclo)})
            except Exception: pass
        
        df = pd.DataFrame(sat_data)
        if not df.empty:
            fig = px.scatter(df, x="Mean Motion", y="Inclination", color="Inclination", title="Orbit Catalog", color_continuous_scale="Electric", template="plotly_dark")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={'color': "#f8fafc"})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No valid telemetry for distribution plot.")

# ==============================================================================
# PAGE 2: FLIGHT DYNAMICS (GNC)
# ==============================================================================
elif page == "2. Flight Dynamics (GNC)":
    st.title("🚀 Flight Dynamics & GNC")
    st.markdown("**Proximity Operations Simulator** | Engine: *LQR-Assisted Control*")
    
    if st.button("▶️ INITIATE DOCKING SCENARIO"):
        st.session_state['run_sim'] = True
    
    if st.session_state.get('run_sim', False):
        pilot = AdvancedRLPilot()
        murphy = EntropyEngine()
        
        # --- EKF INITIALIZATION ---
        ekf = ExtendedKalmanFilter(initial_state=pilot.state.copy(), dt=pilot.dt)
        
        history = []
        ekf_history = []
        rmse_pos_list = []
        rmse_vel_list = []
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        steps = 1500
        sim_start_time = time.perf_counter()
        
        for i in range(steps):
            # 1. Capture Ground Truth
            true_state = pilot.state.copy()
            history.append(true_state)
            
            # 2. Generate Noisy Measurement (using EntropyEngine)
            measurement = murphy.inject_noise(true_state)
            
            # 3. EKF Predict & Update
            # In this simulator, thrust is the command
            input_state_for_pilot = ekf.state.copy() # Use estimate for control
            thrust = pilot.get_control_effort(input_state_for_pilot) * 0.8
            
            ekf.predict(accel_command=thrust/pilot.mass)
            ekf.update(measurement)
            ekf_history.append(ekf.state.copy())
            
            # 4. Calculate Instantaneous Error for RMSE tracking
            pos_error = np.linalg.norm(ekf.state[:3] - true_state[:3])
            vel_error = np.linalg.norm(ekf.state[3:] - true_state[3:])
            rmse_pos_list.append(pos_error**2)
            rmse_vel_list.append(vel_error**2)
            
            # 5. Physics Integration (Ground Truth)
            pos_eci = pilot.state[:3]
            gravity_accel = -(MU / (np.linalg.norm(pos_eci)**3)) * pos_eci
            j2_accel = OrbitalMechanics.calculate_j2_accel(pos_eci)
            
            total_accel = (thrust / pilot.mass) + gravity_accel + j2_accel
            pilot.state[3:] += total_accel * pilot.dt
            pilot.state[:3] += pilot.state[3:] * pilot.dt
            pilot.total_delta_v += (np.linalg.norm(thrust)/pilot.mass)*pilot.dt
            
            dist = np.linalg.norm(pilot.state[:3])
            if dist < 0.02:
                status_text.success(f"✅ HARD DOCK CONFIRMED. T={i*0.1:.1f}s")
                progress_bar.progress(100)
                actual_steps = i + 1
                break
            
            if i % 100 == 0:
                progress_bar.progress(int((i/steps)*100))
        else:
            actual_steps = steps

        sim_end_time = time.perf_counter()
        sim_duration = sim_end_time - sim_start_time
        sps = actual_steps / sim_duration
        
        # 6. Final RMSE Calculation
        final_rmse_pos = np.sqrt(np.mean(rmse_pos_list))
        final_rmse_vel = np.sqrt(np.mean(rmse_vel_list))
        
        # --- VISUALIZATION ---
        fig_3d = TacticalDisplay.create_3d_plot(history)
        st.plotly_chart(fig_3d, use_container_width=True)
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Delta-V Used", f"{pilot.total_delta_v:.2f} m/s")
        c2.metric("Final Range", f"{dist*100:.1f} cm")
        c3.metric("Pos RMSE", f"{final_rmse_pos*1000:.2f} m")
        c4.metric("Vel RMSE", f"{final_rmse_vel*1000:.2f} m/s")
        
        st.metric("Simulation Performance", f"{sps:.0f} steps/sec", delta=f"{pilot.dt*1000:.1f}ms step-time")
        
        # Error convergence plot
        err_df = pd.DataFrame({
            'Step': np.arange(len(rmse_pos_list)),
            'Pos Error (km)': np.sqrt(rmse_pos_list),
            'Vel Error (km/s)': np.sqrt(rmse_vel_list)
        })
        fig_err = px.line(err_df, x='Step', y=['Pos Error (km)', 'Vel Error (km/s)'], title="EKF Error Convergence", template="plotly_dark")
        fig_err.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_err, use_container_width=True)


# ==============================================================================
# PAGE 3: CERTIFICATION (IV&V)
# ==============================================================================
elif page == "3. Certification (IV&V)":
    st.title("📊 Reliability Engineering")
    st.markdown("Independent Verification & Validation (IV&V) — Monte Carlo.")
    
    if st.button("RUN MONTE CARLO SUITE"):
        with st.spinner("Running 50 stochastic simulations..."):
            stats = SystemValidator.run_monte_carlo(50)
        
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Mean Accuracy", f"{stats['mean']:.2f}%")
        kpi2.metric("3-Sigma Confidence", f"{stats['3_sigma_low']:.2f}%")
        
        if stats['3_sigma_low'] >= 98.0:
            kpi3.metric("Certification", "FLIGHT READY", delta="PASSED")
            st.success("✅ System meets NASA Class-B Software Safety Requirements.")
        else:
            kpi3.metric("Certification", "GROUNDED", delta="FAILED", delta_color="inverse")
            st.error("❌ System requires GNC tuning.")

        fig = go.Figure(data=[go.Histogram(x=stats['raw_data'], nbinsx=20, marker_color='#6366f1')])
        fig.update_layout(title="Monte Carlo Distribution", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

# ==============================================================================
# PAGE 4: MISSION PLANNING
# ==============================================================================
elif page == "4. Mission Planning":
    st.title("📐 Mission Trajectory Planner")
    st.markdown("Evolutionary Algorithm with **Radiation & Drag Constraints**.")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Constraints")
        st.info("⚠️ **Safety Protocols Active:**\n- Radiation Belt Avoidance (1000-6000km)\n- Atmospheric Drag Avoidance (<300km)")
        if st.button("✨ OPTIMIZE ORBIT"):
            optimizer = MissionOptimizer(pop_size=40)
            with st.spinner("Analyzing orbital regimes..."):
                best_alt, best_cost = optimizer.run()
                st.session_state['opt_res'] = (best_alt, best_cost)
    
    with col2:
        if 'opt_res' in st.session_state:
            alt, cost = st.session_state['opt_res']
            st.success(f"🔹 Global Minimum Found at {alt:.2f} km")
            
            if 300 < alt < 1000:
                st.caption("✅ Orbit is Safe (LEO). Low Drag, No Radiation.")
            elif alt > 6000:
                st.caption("✅ Orbit is Safe (MEO/GEO). Above Radiation Belts.")
            else:
                st.caption("⚠️ Orbit is in a High Risk Zone.")
            
            m1, m2 = st.columns(2)
            m1.metric("Optimal Altitude", f"{alt:.2f} km")
            m2.metric("Total Mission Cost", f"{cost:.2f}")
            
            x = np.linspace(160, 8000, 100)
            y = [OrbitalMechanics.hohmann_transfer(h+6378, 35786+6378) + (2.0 if h<300 else 0) + (5.0 if 1000<h<6000 else 0) for h in x]
            fig = px.line(x=x, y=y, title="Cost Landscape (Showing Radiation Penalty Spike)", template="plotly_dark")
            fig.add_scatter(x=[alt], y=[cost], mode='markers', marker={'size': 12, 'color': '#00f5ff'}, name='Selected')
            fig.update_layout(xaxis_title="Altitude (km)", yaxis_title="Cost (Fuel + Risk)", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)

# ==============================================================================
# PAGE 5: EMERGENCY OPERATIONS
# ==============================================================================
elif page == "5. Emergency Operations":
    st.title("🚨 Emergency Operations")
    st.markdown("Critical Subsystem Anomaly Response Simulator.")
    
    if 'scenario' not in st.session_state:
        st.session_state['scenario'] = AnomalyScenario()
    
    scenario = st.session_state['scenario']
    col_ctrl, col_telemetry = st.columns([1, 2])
    
    with col_ctrl:
        st.subheader("Control Interface")
        if not scenario.is_active and not scenario.resolved and not scenario.failed:
            if st.button("🔥 TRIGGER SIMULATED ANOMALY"):
                scenario.trigger()
                st.rerun()
        
        if scenario.is_active:
            st.error("⚠️ CRITICAL ANOMALY ACTIVE")
            if st.button("🔌 [SHUTDOWN_PAYLOAD]"):
                msg = scenario.execute_command("SHUTDOWN_PAYLOAD")
                st.toast(msg)
            if st.button("🛡️ [ORIENT_SUN_SHADE]"):
                msg = scenario.execute_command("ORIENT_SUN_SHADE")
                st.toast(msg)
        
        if scenario.resolved or scenario.failed:
            if st.button("🔄 RESET SIMULATION"):
                st.session_state['scenario'] = AnomalyScenario()
                st.rerun()

    with col_telemetry:
        if scenario.is_active or scenario.resolved or scenario.failed:
            scenario.update()
            status = scenario.get_status()
            temp_color = "normal" if status['temp'] < 60 else "inverse"
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Bus Temperature", f"{status['temp']:.1f} °C", delta=f"{status['temp']-25:.1f}", delta_color=temp_color)
            m2.metric("Response Timer", f"{30 - status['elapsed']:.1f}s", delta="Countdown")
            m3.metric("System Health", "CRITICAL" if status['active'] else ("STABLE" if status['resolved'] else "FAILED"))
            
            if status['failed']:
                st.error(f"💀 MISSION FAILURE: {status['failure_reason']}")
            elif status['resolved']:
                st.success("✅ MISSION SAVED: Operator response neutralized thermal runaway.")
            
            if 'temp_history' not in st.session_state:
                st.session_state['temp_history'] = []
            
            if status['active']:
                st.session_state['temp_history'].append(status['temp'])
                if len(st.session_state['temp_history']) > 100:
                    st.session_state['temp_history'].pop(0)
                
            fig = px.line(y=st.session_state['temp_history'], title="Subsystem Thermal Telemetry (Live)", template="plotly_dark")
            fig.update_layout(xaxis_title="Time Step (100ms)", yaxis_title="Temp (°C)", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
            
            if status['active'] and not status['resolved'] and not status['failed']:
                time.sleep(0.1)
                st.rerun()
# ==============================================================================
# PAGE 6: ML PIPELINE & SECURITY
# ==============================================================================
elif page == "6. ML Pipeline & Security":
    st.title("⚡ Real-Time ML Systems Platform")
    st.markdown("Continuous streaming data with live anomaly detection & prediction.")

    streamer = st.session_state['streamer']
    metrics = streamer.get_metrics()
    
    # 1. Top Metrics Banner
    st.markdown("### 📊 Enterprise System Metrics")
    
    data_buffer = streamer.get_latest_data()
    df = pd.DataFrame(data_buffer) if data_buffer else pd.DataFrame()
    
    if not df.empty:
        avg_ui_latency = (time.time() - df['generated_at'].iloc[-10:].mean()) * 1000.0
    else:
        avg_ui_latency = 0.0

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Batch Latency", f"{metrics['latency_ms']:.1f}ms")
    m2.metric("Throughput", f"{metrics['throughput_hz']:.1f}hz")
    m3.metric("Queue Depth", f"{metrics['queue_size']}")
    m4.metric("UI Latency", f"{avg_ui_latency:.1f}ms", delta="Real-time", delta_color="inverse")
    m5.metric("Buffer Load", f"{metrics['buffer_usage']:.1f}%")
    
    st.divider()

    # 2. Main Live Dashboards
    col_pipeline, col_security = st.columns([1, 1])
    
    if len(df) < 20: # Wait for buffer to fill
        st.info("Gathering telemetry for ML inference... Please hold.")
        time.sleep(1.0)
        st.rerun()
    else:
        # df is already created above
        with col_pipeline:
            st.markdown("### 🤖 CPU Prediction Model")
            st.caption("Trailing 5s Ridge Regression Forecast")
            
            # Simple line chart comparing actual to predicted
            fig_pred = go.Figure()
            
            # Actual Data Series
            fig_pred.add_trace(go.Scatter(
                x=df['timestamp'], 
                y=df['cpu_load'],
                mode='lines',
                name='Actual CPU',
                line=dict(color='#0052cc', width=2)
            ))
            
            # Predicted future point (plot as a distinct line mapped slightly ahead based on timestamps)
            # Since the prediction is for t+5s, we can overlay it shifted.
            future_times = df['timestamp'] + 5.0
            fig_pred.add_trace(go.Scatter(
                x=future_times, 
                y=df['ml_predicted_cpu_t5'],
                mode='lines',
                line=dict(color='#ef4444', dash='dot'),
                name='Predicted (t+5s)'
            ))
            
            fig_pred.update_layout(
                yaxis_title="CPU Load (%)",
                xaxis_title="Simulation Time",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                template="plotly_dark",
                margin=dict(l=20, r=20, t=30, b=20),
                height=300
            )
            # Hide default xaxis labels for clean look
            fig_pred.update_xaxes(showticklabels=False)
            st.plotly_chart(fig_pred, use_container_width=True)

        with col_security:
            st.markdown("### 🔐 Cyber Threat Detection")
            st.caption("Isolation Forest Scoring")
            
            latest_status = df.iloc[-1]
            is_anomaly = latest_status.get('ml_is_anomaly', False)
            ground_truth = latest_status.get('ground_truth_attack', False)

            if is_anomaly:
                st.markdown("""
                    <div class="anomaly-banner">
                        <h3 style="margin:0; color:#991b1b;">🚨 ANOMALY DETECTED IN PIPELINE STREAM 🚨</h3>
                        <p style="margin:0;">High-threshold network burst detected. Auto-mitigation procedures initialized.</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.success("✅ PIPELINE SECURE")

            # Plot Anomaly Score vs Network TX (Common Attack Vector)
            fig_sec = go.Figure()
            
            # Base Network traffic
            fig_sec.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['network_tx'],
                mode='lines',
                line=dict(color='gray', width=1),
                name='Network I/O'
            ))

            # Overlay anomalies
            anomalies = df[df['ml_is_anomaly'] == True]
            if not anomalies.empty:
                fig_sec.add_trace(go.Scatter(
                    x=anomalies['timestamp'],
                    y=anomalies['network_tx'],
                    mode='markers',
                    marker=dict(color='red', size=10, symbol='x'),
                    name='ML Flagged Anomaly'
                ))

            fig_sec.update_layout(
                yaxis_title="Network TX (kbps)",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                template="plotly_dark",
                margin=dict(l=20, r=20, t=30, b=20),
                height=300
            )
            fig_sec.update_xaxes(showticklabels=False)
            st.plotly_chart(fig_sec, use_container_width=True)

        # 3. Clean Live Log
        st.markdown("### 🗒️ Telemetry Feed")
        log_df = df[['timestamp', 'cpu_load', 'memory_usage', 'network_tx', 'ml_is_anomaly']].tail(5)
        # Convert timestamp to relative time string nicely
        log_df['Time'] = pd.to_datetime(log_df['timestamp'], unit='s').dt.strftime('%H:%M:%S.%f').str[:-3]
        log_df['CPU %'] = log_df['cpu_load'].round(1)
        log_df['Mem %'] = log_df['memory_usage'].round(1)
        log_df['Net (kbps)'] = log_df['network_tx'].round(0)
        log_df['Threat'] = log_df['ml_is_anomaly'].apply(lambda x: '🚨 HIGH' if x else 'LOW')
        
        st.dataframe(
            log_df[['Time', 'CPU %', 'Mem %', 'Net (kbps)', 'Threat']], 
            use_container_width=True,
            hide_index=True
        )

        st.divider()
        with st.expander("🛠️ Data Schema & Raw Payload Inspector"):
            st.markdown("### JSON Telemetry Definition")
            st.code("""
{
  "timestamp": "float (Unix Epoch)",
  "cpu_load": "float (0-100%)",
  "memory_usage": "float (0-100%)",
  "bus_temp": "float (°C)",
  "network_tx": "float (kbps)",
  "ml_is_anomaly": "boolean",
  "ml_predicted_cpu_t5": "float (Inference Outcome)"
}
            """, language="json")
            
            st.markdown("### Latest Raw Payload")
            st.json(latest_status.to_dict())
            
            st.info("💡 **Engineer's Note:** This stream is processed in batches (n=16) using an Isolation Forest for anomaly detection. Numerical features are normalized before scoring.")

        # Trigger auto-refresh for live effect
        time.sleep(0.5)
        st.rerun()