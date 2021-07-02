import machine
from mqtt_manager import MQTTManager
from scale import Scale
from light_sensor import LightSensor
from motor_bidirectional import MotorBidirectional
from motor import Motor
from machine import Pin
import uasyncio as asyncio

from pins import LASER_PIN
from static_values import *

AVERAGE_ESTIMATION = 3
ERROR_WAITING = 10
CHECK_BOWL_BEFORE_ERROR = 10
FEEDING_TIME = 10
LASER_THRESHOLD = 10


class SmartFoodBowl:

    def __init__(self, scale_pin1: int, scale_pin2: int, motor_pin: int, bmotor_pinf: int, bmotor_pinb: int,
                 sensor_pin: int, laser_pin: int,
                 min_lvl: int, max_lvl: int, mqtt_manager: MQTTManager,
                 topic: str):
        """ constructor.
        """
        self.topic = topic
        self.mqm = mqtt_manager
        self.minLvl = min_lvl
        self.maxLvl = max_lvl
        self.scale = Scale(scale_pin1, scale_pin2)
        self.motor = Motor(motor_pin)
        self.bmotor = MotorBidirectional(bmotor_pinf, bmotor_pinb)
        self.sensor = LightSensor(sensor_pin)
        self.laserPin = Pin(LASER_PIN, Pin.OUT)

    def __str__(self):
        """prints the object."""
        return "Motor bidirectional currently is running: {}, direction: {}"

    async def __getBehaviour(self):
        while True:
            await asyncio.sleep(10)
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
                    self.mqm.sendMsg(REFILL_TOPIC, "Food")
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
                self.bmotor.off()

    def behaviour(self):
        return self.__getBehaviour

    def setMaxFood(self, max_lvl):
        self.maxLvl = max_lvl

    def setMinFood(self, min_lvl):
        self.minLvl = min_lvl

    def __calculateScaleAverage(self):
        for _ in range(AVERAGE_ESTIMATION):
            self.scale.measure()
        return self.scale.get_average()

    def __checkFoodReserve(self):
        self.laserPin.on()
        if self.sensor.measure() > 10:
            self.laserPin.off()
            return True
        self.laserPin.off()
        return False

    def __CheckFoodTime(self):
        return False

    def __errorState(self):
        while True:
            self.mqm.sendMsg(MQTT_ERROR_TOPIC, "Eroor in food delivery")
            await asyncio.sleep(ERROR_WAITING)
