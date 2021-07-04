from valve import Valve
from water_sensor import WaterSensor
from mqtt_manager import MQTTManager
from static_values import MQTT_ERROR_TOPIC
import uasyncio as asyncio
import math

ERROR_WAITING = 1
VALVE_INTERVAL = 2
ACTIVATION_SOIL = 0.05
AVERAGE_ESTIMATION = 3


class SmartWaterBowl:

    def __init__(self, valve_pin: int, water_pin: int, min_lvl: int, max_lvl: int, mqtt_manager: MQTTManager,
                 topic: bytes):
        """ constructor.
        """
        self.previous = 0
        self.actual = 0
        self.topic = topic
        self.mqm = mqtt_manager
        self.minLvl = min_lvl
        self.maxLvl = max_lvl
        self.valve = Valve(valve_pin)
        self.waterSensor = WaterSensor(water_pin)

    def __str__(self):
        """prints the object."""
        return "Water Bowl"

    async def __get_behaviour(self):
        while True:
            await asyncio.sleep(VALVE_INTERVAL)
            print("\t\t\tValvola chiamata")

            self.actual = self.__calculate_scale_average()
            diff = math.fabs(self.actual - self.previous)
            if diff >= ACTIVATION_SOIL:
                self.mqm.send_msg(self.topic, "Livello acqua" + " " + str(self.actual))
                self.previous = self.actual
            if self.actual < self.minLvl:
                self.mqm.send_msg(self.topic, "Livello acqua basso" + " " + str(self.actual))
                print("\t\t\t Livello acqua critico apertura valvola")
                self.valve.open()
                x = 0
                while self.actual < self.maxLvl:
                    print("\t\t\t Secondi attesa riempimento" + " " + str(x))
                    if x >= 10:
                        self.valve.close()
                        while True:
                            self.actual = self.__calculate_scale_average()
                            self.mqm.send_msg(MQTT_ERROR_TOPIC,
                                              "Eroor in water delivery" + " " + str(self.actual))
                            print("\t\t\t Errore" + " " + str(self.actual))
                            self.waterSensor.measure()
                            await asyncio.sleep(ERROR_WAITING)
                    x = x + 1
                    self.actual = self.__calculate_scale_average()
                    await asyncio.sleep(1)
                    self.waterSensor.measure()

                self.valve.close()
                print("\t\t\t Livello acqua ripristinato")

    def behaviour(self):
        return self.__get_behaviour

    def set_max_water_level(self, max_lvl):
        self.maxLvl = max_lvl

    def set_min_water_level(self, min_lvl):
        self.minLvl = min_lvl

    def __calculate_scale_average(self):
        for _ in range(AVERAGE_ESTIMATION):
            self.waterSensor.measure()
        return self.waterSensor.get_percentage()
