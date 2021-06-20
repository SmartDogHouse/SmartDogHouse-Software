# AWS MQTT client cert example for esp8266 or esp32 running MicroPython 1.9
from umqtt.robust import MQTTClient
import time
import machine
from machine import Pin, ADC
import secrets
# Certs for ESP32
# The certificates are .der format
CERT_FILE = "/flash/cert"
KEY_FILE = "/flash/key"

# if you change the ClientId make sure update AWS policy
MQTT_CLIENT_ID = "COGLIONE"
MQTT_PORT = 8883

# if you change the topic make sure update AWS policy
MQTT_TOPIC = b"TESTONE"

# Change the following three settings to match your environment
WIFI_SSID = secrets.WIFI_SSID
WIFI_PW = secrets.WIFI_PW
MQTT_HOST = secrets.MQTT_HOST

mqtt_client = None


def on_message_come(topic, msg):
    print(topic + " " + ":" + str(msg))
    print("sadsdasad")


def pub_msg(msg):
    global mqtt_client
    try:
        mqtt_client.publish(MQTT_TOPIC, msg)
        print("Sent: " + msg)
    except Exception as e:
        print("Exception publish: " + str(e))
        raise


def connect_mqtt():
    global mqtt_client
    try:
        with open(KEY_FILE, "r") as f:
            key = f.read()

        print("Got Key")

        with open(CERT_FILE, "r") as f:
            cert = f.read()

        print("Got Cert")

        mqtt_client = MQTTClient(client_id=MQTT_CLIENT_ID, server=MQTT_HOST, port=MQTT_PORT,  ssl=True,
                                 ssl_params={"cert": cert, "key": key, "server_side": False})

        mqtt_client.connect()
        mqtt_client.set_callback(on_message_come)
        mqtt_client.subscribe(MQTT_TOPIC)
        print('MQTT Connected')

    except Exception as e:
        print('Cannot connect MQTT: ' + str(e))

# start execution
try:

    print("Connecting MQTT")
    connect_mqtt()
    print("Publishing")
    #pub_msg("{\"AWS-MQTT-8266-01\":" + str(time.time()) + "}")
    print("OK")

    x = 0
    while True:
        #mqtt_client.wait_msg()
        print(x)
        mqtt_client.check_msg()
        x = x+1
        time.sleep(1)
except Exception as e:
    print(str(e))
