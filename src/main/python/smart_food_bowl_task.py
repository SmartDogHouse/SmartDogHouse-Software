from mqtt_manager import MQTTManager
from scale import Scale
from light_sensor import LightSensor
from motor_bidirectional import MotorBidirectional
from motor import Motor
from machine import Pin
import uasyncio as asyncio

from task import Task
from static_values import MQTT_NOTIFY_TOPIC
import ujson

CHECK_FOOD_CONSUMPTION_INTERVAL = 5
FOOD_SYSTEM_ERROR_NOTIFY_INTERVAL = 10
CHECK_FILL_FOOD_BOWL_INTERVAL = 1

PERCENTAGE_CONSUMPTION_THRESHOLD = 10/100

SECONDS_BEFORE_ERROR_FOOD_SYSTEM = 30


class SmartFoodBowlTask(Task):

    def __init__(self, scale_pin_sck: int, scale_pin_dt: int, motor_pin: int, bmotor_pinf: int, bmotor_pinb: int,
                 light_sensor_pin: int, laser_pin: int,
                 min_food_lvl_perc: int, max_food_lvl_perc: int, mqtt_manager: MQTTManager,
                 topic: str, limit_switch_open_pin: str, limit_switch_close_pin: str, belt_present=True, motor_present=True):
        """ constructor.
        """
        self.scale = Scale(pin_sck=scale_pin_sck, pin_out_dt=scale_pin_dt)
        self.motor_belt = Motor(motor_pin)
        self.bidirectional_motor = MotorBidirectional(bmotor_pinb, bmotor_pinf)
        self.light_sensor = LightSensor(light_sensor_pin)
        self.laser = Pin(laser_pin, Pin.OUT)
        self.min_food_lvl_perc = min_food_lvl_perc
        self.max_food_lvl_perc = max_food_lvl_perc
        self.mqtt_manager = mqtt_manager
        self.topic = topic
        self.switch_open = Pin(limit_switch_open_pin, Pin.IN)
        self.switch_closed = Pin(limit_switch_close_pin, Pin.IN)
        # initiate variables
        self.belt_present = belt_present
        self.motor_present = motor_present
        self.food_desired = 350
        self.wait_before_food_error = SECONDS_BEFORE_ERROR_FOOD_SYSTEM
        # tare scale
        self.scale.tare()
        # initiate previous sent percentage to actual
        self.scale.measure()
        self.previous_sent_perc = self.scale.get_percentage()
        self.reduction_percentage = 0
        # state variable holds the current state, this is the initial state
        self.state = self.check_food_consumption
        print("SmartFoodBowlTask Created")
        self.food_time = True

    def __str__(self):
        """prints the object."""
        return "Food Bowl"

    async def get_behaviour(self):
        """ async method called returns a coroutine"""
        while True:
            # executes the current state
            await self.state()

    def set_max_food(self, max_food_lvl_perc):
        self.max_food_lvl_perc = max_food_lvl_perc

    def set_min_food(self, min_food_lvl_perc):
        self.min_food_lvl_perc = min_food_lvl_perc

    def set_food_desired(self, food_desired):
        self.food_desired = food_desired

    # STATES
    async def check_food_consumption(self):
        print("STATE: check food consumption")
        # evey X seconds
        await asyncio.sleep(CHECK_FOOD_CONSUMPTION_INTERVAL)
        # measure
        self.scale.measure()
        print("\t\tFood Measure: {:.2f}".format(self.scale.get_percentage()))
        # check empty
        if self.food_time and self.scale.get_percentage() < self.min_food_lvl_perc:
            print("\t\tFood LOW: {:.2f} < {:.2f}".format(self.scale.get_percentage(), self.min_food_lvl_perc))
            if self.belt_present:
                if self.motor_present:
                    print("\t\tInverting Bi-Motor")
                    self.bidirectional_motor.on_direction_opposite()
                    self.state = self.opening
                    return
                else:  # extracting motor not present
                    print("\t\tStarting Belt")
                    self.motor_belt.on()
                    print("\t\tLaser On")
                    self.laser.on()
                    self.state = self.fill_food_bowl
                    return
            else:  # belt not present
                self.state = self.food_finished_notify
                return
        # check consumption
        self.reduction_percentage = self.previous_sent_perc - self.scale.get_percentage()
        print("\t\tReduction Percentage: {:.2f}".format(self.reduction_percentage))
        if self.reduction_percentage >= PERCENTAGE_CONSUMPTION_THRESHOLD:
            self.state = self.send_food_consumption
            return

    async def send_food_consumption(self):
        print("STATE: send food consumption")
        # calculates consumption
        consumption = self.reduction_percentage * self.scale.range_max / self.scale.val_to_g_conversion
        # send msg consumption to database
        self.mqtt_manager.send_msg(self.topic, "Consumption Food: {:.2f} grams".format(consumption))
        # previous sent percentage to actual percentage
        self.previous_sent_perc = self.scale.get_percentage()
        # go to check food consumption again
        self.state = self.check_food_consumption
        return

    async def opening(self):
        # print("STATE: opening")
        # if open
        if self.switch_open.value():
            print("\t\tStop Bi-Motor")
            self.bidirectional_motor.off()
            print("\t\tStarting Belt")
            self.motor_belt.on()
            print("\t\tLaser On")
            self.laser.on()
            self.state = self.fill_food_bowl
            return

    async def closing(self):
        # print("STATE: closing ")
        # if closed
        if self.switch_closed.value():
            print("\t\tStop Bi-Motor")
            self.bidirectional_motor.off()
            self.state = self.check_food_consumption
            return

    async def fill_food_bowl(self):
        print("STATE: filling food bowl")
        # evey X seconds
        await asyncio.sleep(CHECK_FILL_FOOD_BOWL_INTERVAL)
        # measure
        self.scale.measure()
        print("\t\tFood Measure: {:.2f} corresponds: {:.2f} grams Time remaining: {}".format(self.scale.get_percentage(), self.scale.weight(), self.wait_before_food_error))
        # if food is the amount desired
        if self.scale.weight() > self.food_desired:
            print("\t\tStop Belt")
            self.motor_belt.off()
            print("\t\tLaser OFF")
            self.laser.off()
            # reset seconds
            self.wait_before_food_error = SECONDS_BEFORE_ERROR_FOOD_SYSTEM
            # set percentage sent to actual percentage
            self.previous_sent_perc = self.scale.get_percentage()
            if self.motor_present:
                print("\t\tInverting Bi-Motor")
                self.bidirectional_motor.on_direction_opposite()
                self.state = self.closing
                return
            else:
                self.state = self.check_food_consumption()
                return
        # decrement time of period passed
        self.wait_before_food_error = self.wait_before_food_error - CHECK_FILL_FOOD_BOWL_INTERVAL
        # if time expired stop belt and go to water system error notify
        if self.wait_before_food_error < 0:
            print("\t\tStop Belt")
            self.motor_belt.off()
            print("\t\tLaser OFF")
            self.laser.off()
            self.wait_before_food_error = SECONDS_BEFORE_ERROR_FOOD_SYSTEM
            self.state = self.food_system_error_notify
            return
        # if light reaches sensor
        if self.light_sensor.is_light():
            # send notification
            self.mqtt_manager.send_msg(MQTT_NOTIFY_TOPIC, ujson.dumps({"Notify":"Food Storage for recharge bowl is LOW!"}))
            print("\t\tLaser OFF")
            self.laser.off()

    async def food_system_error_notify(self):
        print("STATE: food system error notify")
        # evey X seconds
        await asyncio.sleep(FOOD_SYSTEM_ERROR_NOTIFY_INTERVAL)
        # send notification
        self.mqtt_manager.send_msg(MQTT_NOTIFY_TOPIC, ujson.dumps({"Notify":"ERROR FOOD SYSTEM"}))

    async def food_finished_notify(self):
        print("STATE: food finished notify")
        # evey X seconds
        await asyncio.sleep(FOOD_SYSTEM_ERROR_NOTIFY_INTERVAL)
        # measure
        self.scale.measure()
        # send notification
        self.mqtt_manager.send_msg(MQTT_NOTIFY_TOPIC, ujson.dumps({"Notify":"Food Low: {:.2f}".format(self.scale.get_percentage())}))
        # if food is refilled go back to check food consumption
        if self.scale.get_percentage() > self.max_food_lvl_perc:
            # set percentage sent to actual percentage
            self.previous_sent_perc = self.scale.get_percentage()
            self.state = self.check_food_consumption
            return
