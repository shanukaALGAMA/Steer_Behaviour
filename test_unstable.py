import paho.mqtt.client as mqtt
import numpy as np
import json
import time

BROKER = "localhost"
TOPIC = "vehicle/VEH_003/angle"

client = mqtt.Client()
client.connect(BROKER, 1883, 60)

print("Sending UNSTABLE steering data...")

# High-frequency sine + noise (UNSTABLE / Fishtailing)
time_steps = np.arange(200)
freq = 0.2
amplitude = 50.0
angles = amplitude * np.sin(freq * time_steps)
angles += np.random.randint(-10, 11, 200) # add jerky noise

for a in angles:
    payload = {"angle": float(a)}
    client.publish(TOPIC, json.dumps(payload))
    time.sleep(0.05)

print("Done.")
