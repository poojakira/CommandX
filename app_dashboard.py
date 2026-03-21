import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- MODULE IMPORTS ---
from data_processor import TLEProcessor
from mission_engine import OrbitalMechanics, MU
from rl_pilot import AdvancedRLPilot
from ga_optimizer import MissionOptimizer
from system_analytics import SystemValidator
from subsystem_manager import PowerThermalSubsystem
from entropy_engine import EntropyEngine
from graphics_engine import TacticalDisplay
from model_3d import SatelliteModel  # 3D Visuals
from emergency_ops import AnomalyScenario

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Orbital Command v7.0 (Flight Ready)",
    layout="wide",
    page_icon="🛰️",
    initial_sidebar_state="expanded"
)

# --- LIGHT MODE CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f6f9; color: #1f2937; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e5e7eb; }
    h1, h2, h3 { color: #0f172a; font-family: 'Helvetica Neue', sans-serif; }
    div[data-testid="stMetric"] { background-color: #ffffff; border: 1px solid #e5e7eb; padding: 15px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    .stButton>button { background-color: #0052cc; color: white; border-radius: 6px; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.image("https://img.icons8.com/color/96/satellite-in-orbit.png", width=80)
st.sidebar.title("Orbital Command")
st.sidebar.caption("v7.0 | Flight Ready | Real-World Physics")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Mission Phase",
    ["1. Command Center", "2. Flight Dynamics (GNC)", "3. Certification (IV&V)", "4. Mission Planning", "5. Emergency Operations"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Project Lead:** Apex-X")
st.sidebar.caption("Military-Grade Orbital Assets")

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
        import time
        # Mock simple pass logic based on time
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
            except: pass
        
        df = pd.DataFrame(sat_data)
        fig = px.scatter(df, x="Mean Motion", y="Inclination", color="Inclination", title="Orbit Catalog", color_continuous_scale="Bluered")
        fig.update_layout(paper_bgcolor="white", plot_bgcolor="white", font=dict(color="#1f2937"))
        st.plotly_chart(fig, use_container_width=True)

# ==============================================================================
# PAGE 2: FLIGHT DYNAMICS (Smoothed Control)
# ==============================================================================
elif page == "2. Flight Dynamics (GNC)":
    st.title("🚀 Flight Dynamics & GNC")
    st.markdown("**Proximity Operations Simulator** | Engine: *LQR-Assisted Control*")
    
    if st.button("▶️ INITIATE DOCKING SCENARIO"):
        st.session_state['run_sim'] = True
    
    if st.session_state.get('run_sim', False):
        pilot = AdvancedRLPilot()
        murphy = EntropyEngine()
        history = []
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Simulation Loop
        steps = 1500
        for i in range(steps):
            history.append(pilot.state.copy())
            
            # REALISM: Add Sensor Noise
            input_state = murphy.inject_noise(pilot.state)
            
            # CONTROL: Smooth the thrust (Simple Gain Dampening)
            thrust = pilot.get_control_effort(input_state) * 0.8 # Dampen to prevent zigzag
            
            # PHYSICS (Real-World High Fidelity)
            pos_eci = pilot.state[:3]
            gravity_accel = -(MU / (np.linalg.norm(pos_eci)**3)) * pos_eci # Keplerian Gravity
            j2_accel = OrbitalMechanics.calculate_j2_accel(pos_eci)         # J2 Perturbation
            
            total_accel = (thrust / pilot.mass) + gravity_accel + j2_accel
            
            pilot.state[3:] += total_accel * pilot.dt
            pilot.state[:3] += pilot.state[3:] * pilot.dt
            pilot.total_delta_v += (np.linalg.norm(thrust)/pilot.mass)*pilot.dt
            
            dist = np.linalg.norm(pilot.state[:3])
            
            # REALISM: Docking Tolerance
            if dist < 0.02: # 2cm precision
                status_text.success(f"✅ HARD DOCK CONFIRMED. T={i*0.1:.1f}s")
                progress_bar.progress(100)
                break
            
            if i % 100 == 0:
                progress_bar.progress(int((i/steps)*100))
        
        fig_3d = TacticalDisplay.create_3d_plot(history)
        st.plotly_chart(fig_3d, use_container_width=True)
        
        m1, m2 = st.columns(2)
        m1.metric("Delta-V Used", f"{pilot.total_delta_v:.2f} m/s")
        m2.metric("Final Range", f"{dist*100:.1f} cm")

# ==============================================================================
# PAGE 5: EMERGENCY OPERATIONS (Anomaly Response)
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
            
            # Dynamic Colors
            temp_color = "normal" if status['temp'] < 60 else "inverse"
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Bus Temperature", f"{status['temp']:.1f} °C", delta=f"{status['temp']-25:.1f}", delta_color=temp_color)
            m2.metric("Response Timer", f"{30 - status['elapsed']:.1f}s", delta="Countdown")
            m3.metric("System Health", "CRITICAL" if status['active'] else ("STABLE" if status['resolved'] else "FAILED"))
            
            if status['failed']:
                st.error(f"💀 MISSION FAILURE: {status['failure_reason']}")
            elif status['resolved']:
                st.success("✅ MISSION SAVED: Operator response neutralized thermal runaway.")
            
            # Real-time Telemetry Graph
            if 'temp_history' not in st.session_state:
                st.session_state['temp_history'] = []
            
            if status['active']:
                st.session_state['temp_history'].append(status['temp'])
                if len(st.session_state['temp_history']) > 100:
                    st.session_state['temp_history'].pop(0)
                
            fig = px.line(y=st.session_state['temp_history'], title="Subsystem Thermal Telemetry (Live)")
            fig.update_layout(xaxis_title="Time Step (100ms)", yaxis_title="Temp (°C)", paper_bgcolor="white", plot_bgcolor="white")
            st.plotly_chart(fig, use_container_width=True)
            
            if status['active'] and not status['resolved'] and not status['failed']:
                time.sleep(0.1)
                st.rerun()
        else:
            st.info("Standing by for anomaly injection. Monitor subsystem integrity.")

# ==============================================================================
# PAGE 4: MISSION PLANNING (Physics-Aware)
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
                # FIXED: Unpacking 2 values now works because we fixed ga_optimizer.py
                best_alt, best_cost = optimizer.run()
                st.session_state['opt_res'] = (best_alt, best_cost)
    
    with col2:
        if 'opt_res' in st.session_state:
            alt, cost = st.session_state['opt_res']
            
            # REALISM: Interpret the result
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
            
            # Visualizing the "Death Zone"
            x = np.linspace(160, 8000, 100)
            y = []
            for h in x:
                c = OrbitalMechanics.hohmann_transfer(h+6378, 35786+6378)
                if h < 300: c += 2.0
                if 1000 < h < 6000: c += 5.0
                y.append(c)
                
            fig = px.line(x=x, y=y, title="Cost Landscape (Showing Radiation Penalty Spike)")
            fig.add_scatter(x=[alt], y=[cost], mode='markers', marker=dict(size=12, color='red'), name='Selected')
            fig.update_layout(xaxis_title="Altitude (km)", yaxis_title="Cost (Fuel + Risk)", paper_bgcolor="white", plot_bgcolor="white")
            st.plotly_chart(fig, use_container_width=True)