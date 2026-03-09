import time
import random
import socket
import paho.mqtt.client as mqtt
import json

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

BROKER = get_local_ip()
PORT = 1883
TOPIC = "vehicle/VEH_001/angle"
DELAY = 0.05  # 50ms, same as ESP32

def simulate_driving():
    client = mqtt.Client()
    
    try:
        print(f"Connecting to Broker at {BROKER}...")
        client.connect(BROKER, PORT, 60)
        client.loop_start()
        print(f"✅ Connected! Simulating live driving for VEH_001 on topic '{TOPIC}'.")
        print("Press Ctrl+C to stop.\n")
        
        while True:
            # Pick a driving phase randomly
            phase = random.choices(
                ["SAFE", "FAST", "SWERVE", "OSCILLATE", "STOPPED"], 
                weights=[60, 15, 5, 10, 10]
            )[0]
            
            if phase == "STOPPED":
                print("🛑 [STOPPED] Vehicle is stationary. Steering locked...")
                angle = random.uniform(-15, 15)
                # Hold the exact same angle for 5 seconds (100 samples)
                for _ in range(100):
                    payload = json.dumps({"angle": float(angle)})
                    client.publish(TOPIC, payload)
                    time.sleep(DELAY)
                    
            elif phase == "SAFE":
                print("🚙 [SAFE] Driving straight / gentle curves...")
                base_angle = random.uniform(-5, 5)
                # Stay in Safe mode for 4-8 seconds
                for _ in range(random.randint(80, 160)):
                    angle = base_angle + random.uniform(-2, 2)
                    payload = json.dumps({"angle": angle})
                    client.publish(TOPIC, payload)
                    time.sleep(DELAY)
                    
            elif phase == "FAST":
                print("🏎️ [FAST] Taking a sharp, fast turn...")
                base_angle = random.choice([-35, 35])
                # Stay in Fast mode for 2-4 seconds
                for _ in range(random.randint(40, 80)):
                    angle = base_angle + random.uniform(-5, 5)
                    payload = json.dumps({"angle": angle})
                    client.publish(TOPIC, payload)
                    time.sleep(DELAY)
                    
            elif phase == "SWERVE":
                print("💥 [SWERVE] Sudden extreme swerve!")
                angles = [0, 5, 20, 50, 80, 85, 70, 40, 10, -10, -20, -10, 0, 0]
                for angle in angles:
                    payload = json.dumps({"angle": float(angle)})
                    client.publish(TOPIC, payload)
                    time.sleep(DELAY)
                    
            elif phase == "OSCILLATE":
                print("⚠️ [OSCILLATION] Loss of control (fishtailing)...")
                # Mathematically correct 20Hz sine wave spanning ~3 seconds (60 samples)
                import numpy as np
                time_steps = np.arange(60)
                freq = random.uniform(0.1, 0.4)
                amplitude = random.uniform(30, 70)
                angles = amplitude * np.sin(freq * time_steps)
                angles += np.random.randint(-10, 11, 60) # jerkiness
                
                for angle in angles:
                    payload = json.dumps({"angle": float(angle)})
                    client.publish(TOPIC, payload)
                    time.sleep(DELAY)

    except KeyboardInterrupt:
        print("\nStopping simulation...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.loop_stop()
        client.disconnect()
        print("Disconnected.")

if __name__ == "__main__":
    simulate_driving()
