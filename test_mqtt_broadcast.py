import time
import json
import paho.mqtt.client as mqtt
import random
import socket

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
TOPIC = "vehicle/VEH_001/profile"

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker!")

client.on_connect = on_connect
client.connect(BROKER, PORT, 60)
client.loop_start()

def simulate():
    print("Simulating live Driver Profile stream...")
    st = 100.0
    lt = 100.0
    
    while True:
        # Simulate gentle variation
        st += random.uniform(-2.0, 2.0)
        if st > 100: st = 100
        
        # Occasional drift
        alerts = []
        if random.random() > 0.9:
            st -= 15.0
            alerts.append("Pattern Shift Detected! Driving has degraded.")
            
        lt = (0.05 * st) + (0.95 * lt)
        
        rank = "Rank S (Elite)"
        if lt < 90: rank = "Rank A (Excellent)"
        if lt < 80: rank = "Rank B (Good)"
        if lt < 65: rank = "Rank C (Average)"
        
        payload = {
            "device_id": "VEH_001",
            "st_mean": st,
            "lt_mean": lt,
            "rank": rank,
            "alerts": alerts
        }
        
        client.publish(TOPIC, json.dumps(payload))
        print(f"Published: {st:.1f} / {lt:.1f}")
        time.sleep(1)

if __name__ == "__main__":
    try:
        simulate()
    except KeyboardInterrupt:
        client.loop_stop()
        print("Disconnected")
