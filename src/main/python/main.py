import time
from secret import MQTT_HOST
from pins import *
from static_values import CERT_FILE, KEY_FILE, MQTT_PORT, MQTT_CLIENT_ID, MQTT_FOOD_TOPIC, MQTT_RECEIVE_TOPIC
from static_values import DEF_MAX_FOOD_LVL, DEF_MAX_WATER_LVL, DEF_MIN_FOOD_LVL, DEF_MIN_WATER_LVL
from scheduler import Scheduler
from mqtt_manager import MQTTManager
from smart_water_bowl_task import SmartWaterBowlTask
from smart_food_bowl_task import SmartFoodBowlTask
from mqtt_message_checker_task import MqttMessageCheckerTask
from mqtt_message_handler_task import MqttMessageHandlerTask

print("Main Execution")


# callback for message received
def on_message_callback(topic, msg):
    """execution when a message is received, it schedules a task that reacts to that message"""
    scheduler.schedule_once(MqttMessageHandlerTask().get_behaviour(topic=topic, msg=msg))


# creating manager for MQTT connection and connect
mqtt_manager = MQTTManager(key=KEY_FILE, cert=CERT_FILE, port=MQTT_PORT, client_id=MQTT_CLIENT_ID,
                           server=MQTT_HOST,
                           topic=MQTT_RECEIVE_TOPIC, callback=on_message_callback)
try:
    mqtt_manager.connect()
except Exception as e:
    print('Cannot connect MQTT: ' + str(e))

# creating bowls
swb_task = SmartWaterBowlTask(valve_pin=VALVE_PIN, water_pin=WATER_SENSOR_PIN, max_lvl=DEF_MAX_WATER_LVL,
                              min_lvl=DEF_MIN_WATER_LVL, mqtt_manager=mqtt_manager,
                              topic=MQTT_RECEIVE_TOPIC)

sfb_task = SmartFoodBowlTask(scale_pin_sck=SCALE_PIN_SCK, scale_pin_dt=SCALE_PIN_DT, bmotor_pinb=B_MOTOR_PIN,
                             bmotor_pinf=F_MOTOR_PIN,
                             motor_pin=MOTOR_PIN, sensor_pin=LIGHT_SENSOR_PIN, laser_pin=LASER_PIN,
                             topic=MQTT_FOOD_TOPIC,
                             mqtt_manager=mqtt_manager, min_lvl=DEF_MIN_FOOD_LVL, max_lvl=DEF_MAX_FOOD_LVL,
                             limit_switch_close_pin=LIMIT_SWITCH_CLOSE_PIN,
                             limit_switch_open_pin=LIMIT_SWITCH_OPEN_PIN)

mqtt_msg_chk = MqttMessageCheckerTask(mqtt_manager=mqtt_manager)

# array of tasks
tasks = [sfb_task.get_behaviour(), mqtt_msg_chk.get_behaviour()]  # array of coroutines

# create the scheduler and start with tasks
scheduler = Scheduler()
scheduler.start(tasks)
