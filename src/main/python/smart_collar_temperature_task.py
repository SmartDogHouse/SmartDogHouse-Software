from mqtt_manager import MQTTManager
from machine import Pin
import uasyncio as asyncio
import time
import dht  # for DHT11
import ds18x20, onewire  # for DS18S20 and DS18B20 devices

from task import Task

CHECK_TEMPERATURE_INTERVAL = 5


class SmartCollarTemperatureTask(Task):

    def __init__(self, mqtt_manager: MQTTManager, topic: str, tmp_pin: int, using_ds18x20: bool, min_temp=20, max_temp=35):
        """ constructor.
        """
        self.mqtt_manager = mqtt_manager
        self.topic = topic
        self.tmp_pin = tmp_pin
        self.using_ds18x20 = using_ds18x20
        if self.using_ds18x20:
            ow_bus = onewire.OneWire(Pin(self.tmp_pin))  # create a OneWire bus
            ow_bus.scan()               # return a list of devices on the bus
            self.ds = ds18x20.DS18X20(ow_bus)
            self.roms = self.ds.scan()
        else:
            self.dht_temp = dht.DHT11(Pin(self.tmp_pin, Pin.IN))
        self.min_temp = min_temp
        self.max_temp = max_temp
        # state variable holds the current state, this is the initial state
        self.state = self.check_temperature
        print("SmartCollarTemperatureTask Created")

    def __str__(self):
        """prints the object."""
        return "Smart Collar Temperature"

    async def get_behaviour(self):
        """ async method called returns a coroutine"""
        while True:
            # executes the current state
            await self.state()

    def set_max_temperature(self, max_temp):
        self.max_temp = max_temp

    def set_min_temperature(self, min_temp):
        self.min_temp = min_temp

    # STATES
    async def check_temperature(self):
        # evey X seconds
        await asyncio.sleep(CHECK_TEMPERATURE_INTERVAL)
        print("STATE: check collar temperature")
        # measure temp
        if self.using_ds18x20:
            temp = self.check_ds18x20()
        else:
            temp = self.check_dht()
        # send notification
        self.mqtt_manager.send_msg(self.topic, "Temperature: {}".format(temp))
        if temp < self.min_temp or temp > self.max_temp:
            # send notification
            self.mqtt_manager.send_msg(self.topic, "NOTIFICATION Temperature is abnormal: {}".format(temp))


    def check_ds18x20(self):
        print("STATE: using DS18x20 sensor")
        self.ds.convert_temp()
        time.sleep_ms(750)
        temp = self.ds.read_temp(self.roms[0])
        #for rom in self.roms:
            #print(self.ds.read_temp(rom))
        return temp


    def check_dht(self):
        print("STATE: using DHT sensor")
        self.dht_temp.measure()       # Measurement of temperature and humidity
        temp = self.dht_temp.temperature()  # Read Celsius temperature
        h = self.dht_temp.humidity()    # Read relative humidity
        # print('Temperature=', temp, 'C', 'Humidity=', h, '%')
        return temp

