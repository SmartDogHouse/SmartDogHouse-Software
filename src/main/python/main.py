import time
from secret import MQTT_HOST
from pins import *
from static_values import CERT_FILE, KEY_FILE, MQTT_PORT, MQTT_CLIENT_ID, MQTT_FOOD_TOPIC, MQTT_RECEIVE_TOPIC
from static_values import DEF_MAX_FOOD_LVL, DEF_MAX_WATER_LVL, DEF_MIN_FOOD_LVL, DEF_MIN_WATER_LVL
import uasyncio as asyncio
from scheduler import Scheduler
from mqtt_manager import MQTTManager
from smart_water_bowl import SmartWaterBowl
from smart_food_bowl import SmartFoodBowl


def on_message_come(topic, msg):
    """execution when a message is received"""
    scheduler.schedule_once(on_message_come1(topic, msg))


async def on_message_come1(topic, msg):
    print(str(topic, "utf-8") + " " + ":" + str(msg, "utf-8"))


async def on_message_come3(topic, msg):
    pub_msg("{\"AWS-MQTT-8266-01\":" + str(time.time()) + "}s")


def pub_msg(msg):
    try:
        # mqtt_client.publish(MQTT_TOPIC, msg)
        print("Sent: " + msg)
    except Exception as exception:
        print("Exception publish: " + str(exception))
        raise


async def mqtt_message_handler():
    while True:
        print('Checking')
        mqtt_manager.check_msg_come()
        await asyncio.sleep(2)


print("Main Execution")
# creating manager for MQTT connection and connect
mqtt_manager = MQTTManager(key=KEY_FILE, cert=CERT_FILE, port=MQTT_PORT, client_id=MQTT_CLIENT_ID,
                           server=MQTT_HOST,
                           topic=MQTT_RECEIVE_TOPIC, callback=on_message_come)
try:
    mqtt_manager.connect()
except Exception as e:
    print('Cannot connect MQTT: ' + str(e))

# creating bowls
swb = SmartWaterBowl(valve_pin=VALVE_PIN, water_pin=WATER_SENSOR_PIN, max_lvl=DEF_MAX_WATER_LVL,
                     min_lvl=DEF_MIN_WATER_LVL, mqtt_manager=mqtt_manager,
                     topic=MQTT_RECEIVE_TOPIC)

sfb = SmartFoodBowl(scale_pin_sck=SCALE_PIN_SCK, scale_pin_dt=SCALE_PIN_DT, bmotor_pinb=B_MOTOR_PIN,
                    bmotor_pinf=F_MOTOR_PIN,
                    motor_pin=MOTOR_PIN, sensor_pin=LIGHT_SENSOR_PIN, laser_pin=LASER_PIN,
                    topic=MQTT_FOOD_TOPIC,
                    mqtt_manager=mqtt_manager, min_lvl=DEF_MIN_FOOD_LVL, max_lvl=DEF_MAX_FOOD_LVL,
                    limit_switch_close_pin=LIMIT_SWITCH_CLOSE_PIN,
                    limit_switch_open_pin=LIMIT_SWITCH_OPEN_PIN)

# array of tasks
tasks = [sfb.get_behaviour(), mqtt_message_handler()]  # array of corutines

# create the scheduler and start with tasks
scheduler = Scheduler()
scheduler.start(tasks)
