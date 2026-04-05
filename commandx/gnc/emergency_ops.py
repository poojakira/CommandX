import time
import random

class AnomalyScenario:
    """
    Manages the 'Emergency Operations' scenario for the Mission Control System.
    """
    def __init__(self):
        self.is_active = False
        self.start_time = 0.0
        self.resolved = False
        self.failed = False
        self.failure_reason = ""
        self.time_limit = 30.0 # seconds
        
        # Scenario States
        self.payload_shutdown = False
        self.sun_shade_oriented = False
        
        # Telemetry
        self.base_temp = 25.0
        self.current_temp = 25.0

    def trigger(self):
        self.is_active = True
        self.start_time = time.time()
        self.resolved = False
        self.failed = False
        self.payload_shutdown = False
        self.sun_shade_oriented = False
        self.current_temp = self.base_temp

    def update(self):
        if not self.is_active or self.resolved or self.failed:
            return

        elapsed = time.time() - self.start_time
        
        # Simulate Temperature Spike
        # Rise faster if nothing is done
        heat_rate = 2.5 # degrees per second
        if self.payload_shutdown:
            heat_rate -= 1.0
        if self.sun_shade_oriented:
            heat_rate -= 1.2
            
        self.current_temp += heat_rate * 0.1 # Update every 100ms
        
        # Check for failure (timeout or critical temp)
        if elapsed > self.time_limit:
            self.failed = True
            self.failure_reason = "TIME EXPIRED: Operator failed to respond within 30s."
        
        if self.current_temp > 85.0:
            self.failed = True
            self.failure_reason = "CRITICAL THERMAL BREACH: Hardware melted."
            
        # Check for success
        if self.payload_shutdown and self.sun_shade_oriented and self.current_temp < 60.0:
            self.resolved = True
            self.is_active = False

    def execute_command(self, cmd):
        if cmd == "SHUTDOWN_PAYLOAD":
            self.payload_shutdown = True
            return "SUCCESS: Payload power cut."
        elif cmd == "ORIENT_SUN_SHADE":
            self.sun_shade_oriented = True
            return "SUCCESS: Satellite rotated to shade."
        return "ERROR: Unknown command."

    def get_status(self):
        elapsed = time.time() - self.start_time if self.is_active else 0
        return {
            "active": self.is_active,
            "resolved": self.resolved,
            "failed": self.failed,
            "failure_reason": self.failure_reason,
            "temp": self.current_temp,
            "elapsed": elapsed,
            "payload_off": self.payload_shutdown,
            "shade_on": self.sun_shade_oriented
        }
