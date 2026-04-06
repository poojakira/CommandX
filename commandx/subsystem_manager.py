import numpy as np

# --- REAL WORLD CONSTANTS ---
SOLAR_CONSTANT = 1361.0  # W/m^2 (Solar Flux at 1 AU)

class PowerThermalSubsystem:
    """
    Simulates the 'Lifeblood' of the satellite: Power and Heat.
    """
    def __init__(self):
        # --- HARDWARE SPECS (6U CubeSat) ---
        self.battery_capacity = 80.0    # Watt-hours (Wh)
        self.current_charge = 80.0      # Starts fully charged
        self.solar_efficiency = 0.28    # 28% efficient Triple-Junction Cells
        self.solar_area = 0.12          # m^2

        # --- POWER LOADS (Watts) ---
        self.base_load = 5.0            # Avionics
        self.heater_load = 12.0         # Heaters (Eclipse)
        self.thruster_load = 45.0       # Electric propulsion

        # --- THERMAL STATE ---
        self.temperature = 20.0         # Celsius

    def update(self, dt, is_eclipse, is_thrusting):
        # 1. Calculate Generation (Input)
        generation = 0.0
        if not is_eclipse:
            generation = SOLAR_CONSTANT * self.solar_area * self.solar_efficiency

        # 2. Calculate Consumption (Output)
        consumption = self.base_load
        if is_thrusting:
            consumption += self.thruster_load
        if is_eclipse:
            consumption += self.heater_load
            self.temperature -= (0.5 * dt)  # Cool down
        else:
            self.temperature += (0.2 * dt)  # Heat up

        # 3. Update Battery
        net_power = generation - consumption  # Watts
        energy_step = net_power * (dt / 3600.0)  # Watt-hours
        self.current_charge += energy_step
        self.current_charge = max(0.0, min(self.current_charge, self.battery_capacity))

        return {
            "charge_pct": (self.current_charge / self.battery_capacity) * 100,
            "temp_c": self.temperature,
            "power_draw": consumption
        }

    def simulate_cycle(self, dt=1.0, is_eclipse=False, is_thrusting=False):
        """
        Convenience wrapper called by test_smoke.py and app_dashboard.py.
        Delegates to update() with sensible defaults.
        """
        return self.update(dt=dt, is_eclipse=is_eclipse, is_thrusting=is_thrusting)
