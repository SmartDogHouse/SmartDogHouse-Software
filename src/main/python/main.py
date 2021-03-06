from secret import MQTT_HOST
from pins import VALVE_PIN, WATER_SENSOR_PIN, SCALE_PIN_SCK, SCALE_PIN_DT, MOTOR_PIN, B_MOTOR_PIN, F_MOTOR_PIN, LIGHT_SENSOR_PIN
from pins import LASER_PIN, LIMIT_SWITCH_OPEN_PIN, LIMIT_SWITCH_CLOSE_PIN, DS18x20_PIN, HEARTBEAT_PIN
from static_values import CERT_FILE, KEY_FILE, MQTT_PORT, MQTT_CLIENT_ID, MQTT_FOOD_TOPIC, MQTT_RECEIVE_TOPIC
from static_values import DEF_MAX_FOOD_LVL_PERC, DEF_MAX_WATER_LVL_PERC, DEF_MIN_FOOD_LVL_PERC, DEF_MIN_WATER_LVL_PERC
from static_values import MQTT_SMARTCOLLAR_TOPIC
from scheduler import Scheduler
from mqtt_manager import MQTTManager
from smart_water_bowl_task import SmartWaterBowlTask
from smart_food_bowl_task import SmartFoodBowlTask
from check_bimotor_task import CheckBimotorTask
from smart_collar_temperature_task import SmartCollarTemperatureTask
from smart_collar_heartbeat_task import SmartCollarHeartbeatTask
from mqtt_message_checker_task import MqttMessageCheckerTask
from mqtt_message_handler_task import MqttMessageHandlerTask
import utime

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
swb_task = SmartWaterBowlTask(valve_pin=VALVE_PIN, water_pin=WATER_SENSOR_PIN,
                              max_water_lvl_perc=DEF_MAX_WATER_LVL_PERC,
                              min_water_lvl_perc=DEF_MIN_WATER_LVL_PERC, mqtt_manager=mqtt_manager,
                              topic=MQTT_RECEIVE_TOPIC)

sfb_task = SmartFoodBowlTask(scale_pin_sck=SCALE_PIN_SCK, scale_pin_dt=SCALE_PIN_DT, bmotor_pinb=B_MOTOR_PIN,
                             bmotor_pinf=F_MOTOR_PIN,
                             motor_pin=MOTOR_PIN, light_sensor_pin=LIGHT_SENSOR_PIN, laser_pin=LASER_PIN,
                             topic=MQTT_FOOD_TOPIC,
                             mqtt_manager=mqtt_manager, min_food_lvl_perc=DEF_MIN_FOOD_LVL_PERC,
                             max_food_lvl_perc=DEF_MAX_FOOD_LVL_PERC,
                             limit_switch_close_pin=LIMIT_SWITCH_CLOSE_PIN,
                             limit_switch_open_pin=LIMIT_SWITCH_OPEN_PIN)

mqtt_msg_chk_task = MqttMessageCheckerTask(mqtt_manager=mqtt_manager)

check_bimotor_task = CheckBimotorTask(bmotor_pinb=B_MOTOR_PIN,
                                      bmotor_pinf=F_MOTOR_PIN,
                                      limit_switch_close_pin=LIMIT_SWITCH_CLOSE_PIN,
                                      limit_switch_open_pin=LIMIT_SWITCH_OPEN_PIN)

#sct_task = SmartCollarTemperatureTask(mqtt_manager=mqtt_manager, topic=MQTT_SMARTCOLLAR_TOPIC, tmp_pin=DS18x20_PIN,
#                                      using_ds18x20=True)

#sch_task = SmartCollarHeartbeatTask(mqtt_manager=mqtt_manager, topic=MQTT_SMARTCOLLAR_TOPIC, hb_pin=HEARTBEAT_PIN)

# array of tasks
print("Creating array of tasks")
tasks = [swb_task.get_behaviour(), mqtt_msg_chk_task.get_behaviour()]  # array of coroutines

# create the scheduler and start with tasks
print("--- Starting Scheduler --- {}-{}-{} {}:{}".format(
    utime.localtime()[0], utime.localtime()[1],
    utime.localtime()[2], utime.localtime()[3], utime.localtime()[4]))
scheduler = Scheduler()
scheduler.start(tasks)
