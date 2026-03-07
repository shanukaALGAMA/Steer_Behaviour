import time
from instant_detector import InstantDetector

def test_instant():
    detector = InstantDetector(window_size=30, velocity_threshold=15.0, accel_threshold=8.0, oscillation_threshold=3)
    
    print("Simulating 1.5 seconds of SAFE driving...")
    for _ in range(30):
        res = detector.analyze(10.0) # Holding wheel at 10 deg
        if res: print(res)
        
    print("Simulating sudden severe swerve...")
    # Swerving from 10 to 45 degrees in 2 incoming samples (100ms)
    detector.analyze(20.0)
    res = detector.analyze(45.0)
    if res: print(res)
    
    # Wait for cooldown
    time.sleep(3.1)
    
    print("Simulating rapid oscillation (loss of control)...")
    # Swinging wheel left and right wildly
    angles = [30, -30, 30, -30, 30, -30, 30, -30]
    for a in angles:
        res = detector.analyze(a)
        if res: print(res)

if __name__ == "__main__":
    test_instant()
