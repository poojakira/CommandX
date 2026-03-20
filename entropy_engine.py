import numpy as np
import random

class EntropyEngine:
    """
    Simulates Hardware Degradation, Radiation Effects, and Sensor Noise.
    'Honest Enough' Reality: Hardware is never perfect.
    """
    def __init__(self):
        self.imu_bias = np.array([0.001, -0.002, 0.0005]) # Fixed gyro drift
        self.radiation_counter = 0
        
    def inject_noise(self, true_state):
        """
        Corrupts the perfect 'Ground Truth' state with real-world sensor errors.
        """
        pos = true_state[:3]
        vel = true_state[3:]
        
        # 1. White Noise (Thermal noise in electronics)
        pos_noise = np.random.normal(0, 0.05, 3) # +/- 5cm jitter
        vel_noise = np.random.normal(0, 0.01, 3) # +/- 1cm/s jitter
        
        # 2. Random Walk / Bias (IMU Drift)
        # In reality, this grows over time until a Star Tracker resets it.
        vel_bias = self.imu_bias * np.random.uniform(0.9, 1.1)
        
        noisy_state = np.zeros(6)
        noisy_state[:3] = pos + pos_noise
        noisy_state[3:] = vel + vel_noise + vel_bias
        
        return noisy_state

    def check_for_failure(self):
        """
        Rolls the dice for catastrophic or transient failures.
        """
        roll = random.random()
        if roll < 0.0001: # 0.01% chance per step
            return "SEU" # Single Event Upset (Bit flip)
        return "NOMINAL"