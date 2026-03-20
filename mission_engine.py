import numpy as np

# WGS84 Constants
MU = 398600.4418      
R_EARTH = 6378.137    
J2 = 1.08262668e-3    

class OrbitalMechanics:
    @staticmethod
    def calculate_j2_accel(position_eci):
        """Calculates J2 Perturbation Acceleration."""
        r_vec = position_eci
        r_mag = np.linalg.norm(r_vec)
        x, y, z = r_vec
        
        k = (1.5 * J2 * MU * (R_EARTH**2)) / (r_mag**5)
        z_sq = z**2
        
        ax = k * x * (5 * z_sq / (r_mag**2) - 1)
        ay = k * y * (5 * z_sq / (r_mag**2) - 1)
        az = k * z * (5 * z_sq / (r_mag**2) - 3)
        
        return np.array([ax, ay, az])

    @staticmethod
    def calculate_period(semi_major_axis_km):
        return 2 * np.pi * np.sqrt(semi_major_axis_km**3 / MU)

    @staticmethod
    def hohmann_transfer(r1, r2):
        at = (r1 + r2) / 2
        v1 = np.sqrt(MU / r1)
        vt1 = np.sqrt(MU * (2/r1 - 1/at))
        vt2 = np.sqrt(MU * (2/r2 - 1/at))
        v2 = np.sqrt(MU / r2)
        return abs(vt1 - v1) + abs(v2 - vt2)