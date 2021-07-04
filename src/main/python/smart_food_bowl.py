from mqtt_manager import MQTTManager
from scale import Scale
from light_sensor import LightSensor
from motor_bidirectional import MotorBidirectional
from motor import Motor
from machine import Pin
import uasyncio as asyncio

from pins import LASER_PIN
from static_values import MQTT_ERROR_TOPIC

AVERAGE_ESTIMATION = 3
ERROR_WAITING = 10
CHECK_BOWL_BEFORE_ERROR = 10
FEEDING_TIME = 10
LASER_THRESHOLD = 10


class SmartFoodBowl:

    def __init__(self, scale_pin_sck: int, scale_pin_dt: int, motor_pin: int, bmotor_pinf: int, bmotor_pinb: int,
                 sensor_pin: int, laser_pin: int,
                 min_lvl: int, max_lvl: int, mqtt_manager: MQTTManager,
                 topic: str, limit_switch_open_pin: str, limit_switch_close_pin: str):
        """ constructor.
        """
        self.topic = topic
        self.mqm = mqtt_manager
        self.minLvl = min_lvl
        self.maxLvl = max_lvl
        self.scale = Scale(pin_sck=scale_pin_sck, pin_out_dt=scale_pin_dt)
        self.motor = Motor(motor_pin)
        self.bmotor = MotorBidirectional(bmotor_pinb, bmotor_pinf)
        self.sensor = LightSensor(sensor_pin)
        self.laserPin = Pin(laser_pin, Pin.OUT)
        self.switch_open = Pin(limit_switch_open_pin, Pin.IN)
        self.switch_closed = Pin(limit_switch_close_pin, Pin.IN)
        self.scale.tare()

    def __str__(self):
        """prints the object."""
        return "Food Bowl"

    async def __get_behaviour(self):
        self.bmotor.on_direction_opposite()
        while True:
            for _ in range(5):
                print("Misura " + str(self.switch_open.value()))
                if self.switch_open.value() == 1:
                    self.bmotor.on_direction_opposite()
                    break
            await asyncio.sleep(1)

            """await asyncio.sleep(10)
            print("Refill food")
            # Check food qta
            if self.__calculateScaleAverage() <= self.minLvl:
                print("Activate refill")
                self.motor.on()
                x = 0
                while self.__calculateScaleAverage() < self.maxLvl:
                    if x > CHECK_BOWL_BEFORE_ERROR:
                        self.motor.off()
                        self.__errorState()
                    await asyncio.sleep(1)
                    x = x + 1
                print("End refill")
                self.motor.off()
                # Check food remaining
                if self.__checkFoodReserve():
                    self.mqtt_manager.sendMsg(REFILL_TOPIC, "Food")
            # Check if is time for food
            if self.__CheckFoodTime:
                # Align bowl
                print("Food time")
                self.bmotor.on_direction(1)
                await asyncio.sleep(2)
                self.bmotor.off()
                # Feed time
                await asyncio.sleep(FEEDING_TIME)
                # Retrieve bowl
                self.bmotor.on_direction(2)
                await asyncio.sleep(2)
                self.bmotor.off()"""

    def behaviour(self):
        return self.__get_behaviour

    def set_max_food(self, max_lvl):
        self.maxLvl = max_lvl

    def set_min_food(self, min_lvl):
        self.minLvl = min_lvl

    def __calculate_scale_average(self):
        for _ in range(AVERAGE_ESTIMATION):
            self.scale.measure()
        return self.scale.weight()

    def __check_food_reserve(self):
        self.laserPin.on()
        if self.sensor.measure() > 10:
            self.laserPin.off()
            return True
        self.laserPin.off()
        return False

    def __check_food_time(self):
        return False

    def __error_state(self):
        while True:
            self.mqm.send_msg(MQTT_ERROR_TOPIC, "Eroor in food delivery")
            # await asyncio.sleep(ERROR_WAITING)
