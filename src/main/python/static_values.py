# Certs for ESP32s
# The certificates are .der format
CERT_FILE = "/flash/cert"
KEY_FILE = "/flash/key"

# if you change the ClientId make sure update AWS policy
MQTT_CLIENT_ID = "COGLIONE"
MQTT_PORT = 8883

# if you change the topic make sure update AWS policy
MQTT_RECEIVE_TOPIC = b"SmartCage1"
MQTT_FOOD_TOPIC = b"FOOD-OUT"
MQTT_WATER_TOPIC = b"WATER"
MQTT_ERROR_TOPIC = b"ERROR"
REFILL_TOPIC = b"FOOD-IN"
DEF_MAX_WATER_LVL = 0.9
DEF_MIN_WATER_LVL = 0.3
DEF_MAX_FOOD_LVL = 10000
DEF_MIN_FOOD_LVL = 1000
