import time
import sys
from commandx.gnc.emergency_ops import AnomalyScenario

def run_test():
    print("🛰️ COMMAND-X: EMERGENCY OPERATIONS TEST")
    print("-----------------------------------------")
    print("Simulating Critical Thermal Runaway...")
    time.sleep(1)
    
    scenario = AnomalyScenario()
    scenario.trigger()
    
    print(f"🚨 ANOMALY DETECTED! Current Temp: {scenario.current_temp:.1f} °C")
    print("Objective: Shutdown Payload and Orient Sun Shade within 30 seconds.")
    print("Hold tight for automated operator response...")
    
    # Simulate a delayed operator response (within time limit)
    time.sleep(5)
    print("\n[T+5s] Operator: Executing SHUTDOWN_PAYLOAD")
    print(scenario.execute_command("SHUTDOWN_PAYLOAD"))
    
    time.sleep(5)
    print("\n[T+10s] Operator: Executing ORIENT_SUN_SHADE")
    print(scenario.execute_command("ORIENT_SUN_SHADE"))
    
    # Wait for the scenario to resolve
    print("\nMonitoring system cooling...")
    while scenario.is_active and not scenario.resolved and not scenario.failed:
        scenario.update()
        print(f"Current Temp: {scenario.current_temp:.1f} °C | Status: {'Cooling' if scenario.payload_shutdown and scenario.sun_shade_oriented else 'Heating'}", end="\r")
        time.sleep(0.5)
        
    print("\n-----------------------------------------")
    if scenario.resolved:
        print("✅ MISSION SUCCESS: Anomaly neutralized.")
        print(f"Final Temperature: {scenario.current_temp:.1f} °C")
        sys.exit(0)
    else:
        print(f"❌ MISSION FAILURE: {scenario.failure_reason}")
        sys.exit(1)

if __name__ == "__main__":
    run_test()
