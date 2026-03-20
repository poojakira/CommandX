import numpy as np
from gnc_kalman import ExtendedKalmanFilter
from mission_engine import OrbitalMechanics, MU

class AdvancedRLPilot:
    """
    Guidance, Navigation, and Control (GNC) System.
    """
    def __init__(self):
        # --- SPACECRAFT BUS PROPERTIES ---
        self.mass = 500.0      # kg
        self.max_thrust = 50.0 # N 
        self.dt = 0.1          # 10Hz
        
        # --- INITIAL STATE ---
        self.state = np.array([200.0, 50.0, -25.0, 0.0, 0.0, 0.0])
        self.target = np.array([0.0, 0.0, 0.0])
        
        # --- NAVIGATION SYSTEM (EKF) ---
        self.estimator = ExtendedKalmanFilter(self.state, self.dt)
        self.estimated_state = self.state.copy()
        
        # --- FUEL ACCOUNTING ---
        self.total_delta_v = 0.0
        
        # --- CONTROL LAWS (PID) ---
        self.settling_time = 70.0  
        self.damping = 0.9         
        wn = 4.0 / (self.damping * self.settling_time)
        
        # Gains
        self.Kp = (wn ** 2) * self.mass
        self.Kd = 2 * self.damping * wn * self.mass
        self.Ki = 0.5  # Integral Gain
        
        # Internal Logic
        self.integral_error = np.zeros(3)
        self.deadband = 0.01

    def get_control_effort(self, measurement):
        """
        Calculates thrust commands.
        Input: measurement (Noisy [x,y,z,vx,vy,vz])
        """
        # 1. Update Estimator
        self.estimated_state = self.estimator.update(measurement)
        
        # 2. Extract Logic Variables
        est_pos = self.estimated_state[:3]
        est_vel = self.estimated_state[3:]
        error = self.target - est_pos
        
        # 3. PHYSICS-AWARE CONTROL LAW
        # A. PID Terms
        self.integral_error += error * self.dt
        self.integral_error = np.clip(self.integral_error, -10, 10) # Anti-windup
        pid_force = (self.Kp * error) + (self.Ki * self.integral_error) - (self.Kd * est_vel)
        
        # B. Gravity & J2 Compensation (The "No Bluff" Hardening)
        # By calculating the expected gravitational pull, we can cancel it out
        # This allows the PID to focus only on the relative maneuvering.
        r_mag = np.linalg.norm(est_pos)
        if r_mag > 1000: # Ensure we are in orbit
            grav_comp = (MU / (r_mag**3)) * est_pos * self.mass
            j2_comp = -OrbitalMechanics.calculate_j2_accel(est_pos) * self.mass
        else:
            grav_comp = np.zeros(3)
            j2_comp = np.zeros(3)
            
        force = pid_force + grav_comp + j2_comp
        
        # 4. Actuator Saturation
        mag = np.linalg.norm(force)
        if mag > self.max_thrust:
            force = force * (self.max_thrust / mag)
            # Prevent integral windup when saturated
            self.integral_error -= error * self.dt 
            
        # 5. Deadband (Stay quiet if we are 'close enough')
        if np.linalg.norm(error) < self.deadband and np.linalg.norm(est_vel) < 0.01:
            return np.zeros(3)
        
        # 6. Predict next state for Kalman Filter
        accel_command = force / self.mass
        self.estimator.predict(accel_command)
            
        return force