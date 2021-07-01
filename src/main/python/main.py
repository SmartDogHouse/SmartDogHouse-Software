# AWS MQTT client cert example for esp8266 or esp32 running MicroPython 1.9
from umqtt.robust import MQTTClient
import time
from machine import Pin, ADC
import secret
import pins
import static_values as values
import uasyncio as asyncio
from scheduler import Scheduler
from mqtt_manager import MQTTManager
from smart_valve import SmartValve


def on_message_come(topic, msg):
    sc.scheduleOnce(on_message_come1(topic, msg))


async def on_message_come1(topic, msg):
    print(str(topic,"utf-8") + " " + ":" + str(msg,"utf-8"))


async def on_message_come3(topic, msg):
    pub_msg("{\"AWS-MQTT-8266-01\":" + str(time.time()) + "}s")


def pub_msg(msg):
    try:
        # mqtt_client.publish(MQTT_TOPIC, msg)
        print("Sent: " + msg)
    except Exception as e:
        print("Exception publish: " + str(e))
        raise


def checkMsg():
    while True:
        mqm.checkMsgCome()
        await asyncio.sleep(2)
        print('Checking')


def sens0():
    while True:
        print('Sens0-A')
        await asyncio.sleep(2)
        print('Sens0-B')


def sens1():
    while True:
        print('Sens0-C')
        await asyncio.sleep(2)
        print('Sens0-D')


def foo():
    print('Start timeout coro foo()')


print("Crate objects")
mqm = MQTTManager(key=values.KEY_FILE, cert=values.CERT_FILE, port=values.MQTT_PORT, client_id=values.MQTT_CLIENT_ID,
                  server=secret.MQTT_HOST,
                  topic=values.MQTT_RECEIVE_TOPIC, callback=on_message_come)

svb = SmartValve(valve_pin=pins.VALVE_PIN, water_pin=pins.WATER_SENSOR_PIN, max_lvl=values.DEF_MAX_WATER_LVL,
                min_lvl=values.DEF_MIN_WATER_LVL, mqtt_manager=mqm, topic=values.MQTT_RECEIVE_TOPIC).behaviour()

print("Connecting MQTT")

try:
    mqm.connect()
except Exception as e:
    print('Cannot connect MQTT: ' + str(e))

tasks = [checkMsg(),svb()]
sc = Scheduler()
sc.start(tasks)
