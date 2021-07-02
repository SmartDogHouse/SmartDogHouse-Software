# AWS MQTT client cert example for esp8266 or esp32 running MicroPython 1.9
from umqtt.robust import MQTTClient
import time
from machine import Pin, ADC
from secret import *
from pins import *
from static_values import *
import uasyncio as asyncio
from scheduler import Scheduler
from mqtt_manager import MQTTManager
from smart_water_bowl import SmartWaterBowl
from smart_food_bowl import SmartFoodBowl


def on_message_come(topic, msg):
    sc.scheduleOnce(on_message_come1(topic, msg))


async def on_message_come1(topic, msg):
    print(str(topic, "utf-8") + " " + ":" + str(msg, "utf-8"))


async def on_message_come3(topic, msg):
    pub_msg("{\"AWS-MQTT-8266-01\":" + str(time.time()) + "}s")


def pub_msg(msg):
    try:
        # mqtt_client.publish(MQTT_TOPIC, msg)
        print("Sent: " + msg)
    except Exception as e:
        print("Exception publish: " + str(e))
        raise


def mqttMessageHandler():
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
mqm = MQTTManager(key=KEY_FILE, cert=CERT_FILE, port=MQTT_PORT, client_id=MQTT_CLIENT_ID,
                  server=MQTT_HOST,
                  topic=MQTT_RECEIVE_TOPIC, callback=on_message_come)
try:
    mqm.connect()
except Exception as e:
    print('Cannot connect MQTT: ' + str(e))

svb = SmartWaterBowl(valve_pin=VALVE_PIN, water_pin=WATER_SENSOR_PIN, max_lvl=DEF_MAX_WATER_LVL,
                     min_lvl=DEF_MIN_WATER_LVL, mqtt_manager=mqm, topic=MQTT_RECEIVE_TOPIC).behaviour()

#sfb = SmartFoodBowl(scale_pin1=SCALE_PIN_1, scale_pin2=SCALE_PIN_2, bmotor_pinb=B_MOTOR_PIN, bmotor_pinf=B_MOTOR_PIN,
#                    motor_pin=MOTOR_PIN, sensor_pin=LIGHT_SENSOR_PIN, laser_pin=LASER_PIN, topic=MQTT_FOOD_TOPIC,
#                    mqtt_manager=mqm, min_lvl=DEF_MIN_FOOD_LVL, max_lvl=DEF_MAX_FOOD_LVL).behaviour()

print("Connecting MQTT")

tasks = [svb()]

sc = Scheduler()
sc.start(tasks)
