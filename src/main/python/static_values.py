# Certs for ESP32s
# The certificates are .der format
CERT_FILE = "/flash/cert"
KEY_FILE = "/flash/key"

# if you change the ClientId make sure update AWS policy
MQTT_CLIENT_ID = "ClientID"
MQTT_PORT = 8883

# if you change the topic make sure update AWS policy
MQTT_RECEIVE_TOPIC = b"SmartCage1"
MQTT_FOOD_TOPIC = b"FOOD-OUT"
MQTT_WATER_TOPIC = b"WATER"
MQTT_NOTIFY_TOPIC = b"Notifications"
REFILL_TOPIC = b"FOOD-IN"
MQTT_SMARTCOLLAR_TOPIC = b"SMARTCOLLAR"
# food and water levels
DEF_MAX_WATER_LVL_PERC = 90/100
DEF_MIN_WATER_LVL_PERC = 10/100
DEF_MAX_FOOD_LVL_PERC = 90/100
DEF_MIN_FOOD_LVL_PERC = 10/100
