from mqtt_manager import MQTTManager
from machine import Pin
import uasyncio as asyncio
import dht # for DHT11
import time, ds18x20 # for DS18B20

from task import Task

CHECK_COLLAR_INTERVAL = 5


class SmartCollarTask(Task):

    def __init__(self, mqtt_manager: MQTTManager, topic: str, tmp_pin: int, min_temp=30, max_temp=40, min_heartbeat=20, max_heartbeat=200):
        """ constructor.
        """
        self.mqtt_manager = mqtt_manager
        self.topic = topic
        self.tmp_pin = tmp_pin
        self.dht_temp = dht.DHT11(Pin(self.tmp_pin, Pin.IN))
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.max_heartbeat = max_heartbeat
        self.min_heartbeat = min_heartbeat
        # state variable holds the current state, this is the initial state
        self.state = self.check_food_consumption
        print("SmartCollarTask Created")

    def __str__(self):
        """prints the object."""
        return "Smart Collar"

    async def get_behaviour(self):
        """ async method called returns a coroutine"""
        while True:
            # executes the current state
            await self.state()

    def set_max_temperature(self, max_temp):
        self.max_temp = max_temp

    def set_min_temperature(self, min_temp):
        self.min_temp = min_temp

    def set_max_heartbeat(self, max_heartbeat):
        self.max_heartbeat = max_heartbeat

    def set_min_heartbeat(self, min_heartbeat):
        self.min_heartbeat = min_heartbeat

    # STATES
    async def check_food_consumption(self):
        print("STATE: check collar")
        # evey X seconds
        await asyncio.sleep(CHECK_COLLAR_INTERVAL)
        # measure temp
        self.dht_temp.measure()       # Measurement of temperature and humidity
        temp = self.dht_temp.temperature()  # Read Celsius temperature
        h = self.dht_temp.humidity()    # Read relative humidity
        print('Temperature=', temp, 'C', 'Humidity=', h, '%')
        # send notification
        #self.mqtt_manager.send_msg(self.topic, "Temperature: {}".format(temp))
        #if temp < self.min_temp or temp > self.max_temp:
            # send notification
            #self.mqtt_manager.send_msg(self.topic, "NOTIFICATION Temperature is abnormal: {}".format(temp))



    def check_ds18B20(self):
        from machine import Pin
        import onewire
        ow = onewire.OneWire(Pin(self.tmp_pin))  # create a OneWire bus on GPIO12
        ow.scan()               # return a list of devices on the bus
        import time, ds18x20
        ds = ds18x20.DS18X20(ow)
        roms = ds.scan()
        ds.convert_temp()
        time.sleep_ms(750)
        for rom in roms:
            print(ds.read_temp(rom))
