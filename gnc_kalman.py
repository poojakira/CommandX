import numpy as np

class ExtendedKalmanFilter:
    """
    Estimates true state [x, y, z, vx, vy, vz] from noisy measurements.
    """
    def __init__(self, initial_state, dt):
        self.state = initial_state.copy()
        self.dt = dt
        
        # State Transition Matrix (Newtonian Physics)
        self.F = np.eye(6)
        self.F[:3, 3:] = np.eye(3) * self.dt
        
        # Covariance Matrix (Initial Uncertainty)
        self.P = np.eye(6) * 0.1 
        
        # Process Noise (Physics isn't perfect)
        self.Q = np.eye(6) * 0.001
        
        # Measurement Matrix (We measure all 6 states)
        self.H = np.eye(6)
        
        # Measurement Noise (Sensor Specs)
        self.R = np.eye(6) * 0.1

    def predict(self, accel_command):
        # 1. Extrapolate State: x = Fx + Bu
        self.state = self.F @ self.state
        self.state[3:] += accel_command * self.dt
        self.state[:3] += accel_command * 0.5 * self.dt**2
        
        # 2. Extrapolate Uncertainty: P = FPF' + Q
        self.P = self.F @ self.P @ self.F.T + self.Q

    def update(self, measurement):
        # 1. Calculate Kalman Gain: K = PH' (HPH' + R)^-1
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        
        # 2. Update State Estimate: x = x + K(y - Hx)
        y = measurement - (self.H @ self.state)
        self.state = self.state + (K @ y)
        
        # 3. Update Uncertainty: P = (I - KH)P
        I = np.eye(6)
        self.P = (I - K @ self.H) @ self.P
        
        return self.state