#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

/* CONFIG */

const char* WIFI_SSID = "Galaxy A05 AL";
const char* WIFI_PASS = "whywifi1";

const char* MQTT_BROKER = "10.222.114.50";
const int   MQTT_PORT   = 1883;

const char* DEVICE_ID  = "VEH_001";
const char* MQTT_TOPIC = "vehicle/VEH_001/angle";

/*  ENCODER CONFIG */

#define PIN_S1 18
#define PIN_S2 19

const int   STEPS_PER_REV = 360;     // adjust to your pattern
const float DEG_PER_STEP = 360.0 / STEPS_PER_REV;

/*  OBJECTS */

WiFiClient espClient;
PubSubClient mqttClient(espClient);

/*  ENCODER STATE */

volatile int stepCount = 0;
volatile int lastState = 0b11;   // assume ON-ON is zero at start

portMUX_TYPE mux = portMUX_INITIALIZER_UNLOCKED;

/*  TIMING */

unsigned long lastPublishTime = 0;
const unsigned long PUBLISH_INTERVAL = 50; // 20 Hz

/*  ENCODER ISR */

void IRAM_ATTR encoderISR() {
  int s1 = digitalRead(PIN_S1);
  int s2 = digitalRead(PIN_S2);
  int currentState = (s1 << 1) | s2;

  portENTER_CRITICAL_ISR(&mux);

  if (currentState != lastState) {

    //  CLOCKWISE (RIGHT) --------
    if (
      (lastState == 0b11 && currentState == 0b10) ||
      (lastState == 0b10 && currentState == 0b00) ||
      (lastState == 0b00 && currentState == 0b01) ||
      (lastState == 0b01 && currentState == 0b11)
    ) {
      stepCount++;
    }

    // COUNTER-CLOCKWISE (LEFT) --------
    else if (
      (lastState == 0b11 && currentState == 0b01) ||
      (lastState == 0b01 && currentState == 0b00) ||
      (lastState == 0b00 && currentState == 0b10) ||
      (lastState == 0b10 && currentState == 0b11)
    ) {
      stepCount--;
    }

    lastState = currentState;
  }

  portEXIT_CRITICAL_ISR(&mux);
}

/*  WIFI */

void setupWiFi() {
  Serial.print("Connecting to WiFi");
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

/* MQTT */

void reconnectMQTT() {
  while (!mqttClient.connected()) {
    Serial.print("Connecting to MQTT...");
    if (mqttClient.connect(DEVICE_ID)) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(mqttClient.state());
      delay(2000);
    }
  }
}

/*  SETUP */

void setup() {
  Serial.begin(115200);

  pinMode(PIN_S1, INPUT_PULLUP);
  pinMode(PIN_S2, INPUT_PULLUP);

  int s1 = digitalRead(PIN_S1);
  int s2 = digitalRead(PIN_S2);
  lastState = (s1 << 1) | s2;

  // Force zero if start at ON-ON
  if (lastState == 0b11) {
    stepCount = 0;
  }

  attachInterrupt(digitalPinToInterrupt(PIN_S1), encoderISR, CHANGE);
  attachInterrupt(digitalPinToInterrupt(PIN_S2), encoderISR, CHANGE);

  setupWiFi();
  mqttClient.setServer(MQTT_BROKER, MQTT_PORT);

  Serial.println("System started (ON-ON = ZERO)");
}



void loop() {
  if (!mqttClient.connected()) {
    reconnectMQTT();
  }
  mqttClient.loop();

  unsigned long now = millis();
  if (now - lastPublishTime >= PUBLISH_INTERVAL) {
    lastPublishTime = now;

    int steps;
    portENTER_CRITICAL(&mux);
    steps = stepCount;
    portEXIT_CRITICAL(&mux);

    float angle = steps * DEG_PER_STEP;
    angle = constrain(angle, -180.0, 180.0);

    StaticJsonDocument<64> doc;
    doc["angle"] = angle;

    char payload[64];
    serializeJson(doc, payload);

    mqttClient.publish(MQTT_TOPIC, payload);

    Serial.print("Published angle: ");
    Serial.println(angle, 2);
  }
}
