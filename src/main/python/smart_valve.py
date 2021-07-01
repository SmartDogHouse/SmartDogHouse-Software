import machine
from valve import Valve
from water_sensor import WaterSensor
from mqtt_manager import MQTTManager
import uasyncio as asyncio


class SmartValve:

    def __init__(self, valve_pin: int, water_pin: int, min_lvl: int, max_lvl: int, mqtt_manager: MQTTManager,
                 topic: str):
        """ constructor.
        """
        self.topic = topic
        self.mqm = mqtt_manager
        self.minLvl = min_lvl
        self.maxLvl = max_lvl
        self.valve = Valve(valve_pin)
        self.waterSensor = WaterSensor(water_pin)

    def __str__(self):
        """prints the object."""
        return "Motor bidirectional currently is running: {}, direction: {}"

    async def __getBehaviour(self):
        while True:
            await asyncio.sleep(2)
            print("Valvola chiamata")
            self.waterSensor.measure()
            self.mqm.sendMsg(self.topic, "Valore valvola" + str(self.waterSensor.get_average()))
            if self.waterSensor.get_average() < self.minLvl:
                self.mqm.sendMsg(self.topic, "RIempimento valvola" + str(self.waterSensor.get_average()))
                print("Livello acqua critico apertura valvola")
                self.valve.open()
                x = 0
                while self.waterSensor.get_average() < self.maxLvl:
                    if x >= 10:
                        self.valve.close()
                        self.mqm.sendMsg(self.topic, "Emergenza! valvola rotta")

                    x = x+1
                    await asyncio.sleep(1)
                    self.waterSensor.measure()
                self.valve.close()
                print("Livello acqua ripristinato")

    def behaviour(self):
        return self.__getBehaviour

    def setMaxWaterLevel(self, max_lvl):
        self.maxLvl = max_lvl

    def setMinWaterLevel(self, min_lvl):
        self.minLvl = min_lvl
