import paho.mqtt.client as mqtt
import numpy as np
import json
import time

BROKER = "localhost"
TOPIC = "vehicle/VEH_002/angle"

client = mqtt.Client()
client.connect(BROKER, 1883, 60)

print("Sending FAST steering data...")

# Large-amplitude, held sharp turn (FAST)
time_steps = np.arange(200)
angles = np.full(200, 35.0)
angles += np.random.randint(-3, 4, 200) # add human jitter

for a in angles:
    payload = {"angle": float(a)}
    client.publish(TOPIC, json.dumps(payload))
    time.sleep(0.03)

print("Done.")
