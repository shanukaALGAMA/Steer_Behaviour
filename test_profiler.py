import time
from driver_profiler import DriverProfiler

def test_profiler():
    print("--- Starting Driver Profiler Simulation ---")
    # Initialize profiler (force a fresh profile for the test)
    profiler = DriverProfiler("TEST_DRV_01", save_file="test_profile.json")
    
    # Simulate historical safe driving (150 safe observations)
    print("\n[Phase 1] Simulating 150 SAFE predictions (Building historical normal profile)...")
    for _ in range(150):
        notes = profiler.update("SAFE")
        if notes:
            for n in notes: print(f"  Alert: {n}")
            
    print(f"Current Rank: {profiler.last_rank}")
    print(f"Short-Term Mean: {profiler.st_mean:.1f}")
    print(f"Long-Term Mean: {profiler.lt_mean:.1f}")

    # Simulate concept drift - driver gets aggressive/fast (50 fast observations)
    print("\n[Phase 2] Simulating concept drift: 50 FAST predictions...")
    for _ in range(50):
        notes = profiler.update("FAST")
        if notes:
            for n in notes: print(f"  => {n}")

    # Simulate severe drift - driver gets unstable (20 unstable predictions)
    print("\n[Phase 3] Simulating severe drift: 20 UNSTABLE predictions...")
    for _ in range(20):
        notes = profiler.update("UNSTABLE")
        if notes:
            for n in notes: print(f"  => {n}")
            
    # Simulate recovering back to safe
    print("\n[Phase 4] Simulating recovery: 50 SAFE predictions...")
    for _ in range(50):
        notes = profiler.update("SAFE")
        if notes:
            for n in notes: print(f"  => {n}")

if __name__ == "__main__":
    test_profiler()
