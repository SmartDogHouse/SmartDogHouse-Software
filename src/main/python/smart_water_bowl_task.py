from valve import Valve
from water_sensor import WaterSensor
from mqtt_manager import MQTTManager
from static_values import MQTT_ERROR_TOPIC
import uasyncio as asyncio
from task import Task

CHECK_WATER_CONSUMPTION_INTERVAL = 2
WATER_SYSTEM_ERROR_NOTIFY_INTERVAL = 10
CHECK_FILL_WATER_BOWL_INTERVAL = 1

PERCENTAGE_CONSUMPTION_THRESHOLD = 10/100

SECONDS_BEFORE_ERROR_WATER_SYSTEM = 30


class SmartWaterBowlTask(Task):

    def __init__(self, valve_pin: int, water_pin: int, min_water_lvl_perc: int, max_water_lvl_perc: int, mqtt_manager: MQTTManager, topic: bytes):
        """ constructor.
        """
        self.valve = Valve(valve_pin)
        self.waterSensor = WaterSensor(water_pin)
        self.min_water_lvl_perc = min_water_lvl_perc
        self.max_water_lvl_perc = max_water_lvl_perc
        self.mqtt_manager = mqtt_manager
        self.topic = topic
        # initiate variables
        self.valve_present = True
        self.wait_before_water_error = SECONDS_BEFORE_ERROR_WATER_SYSTEM
        # initiate previous sent percentage to actual
        self.waterSensor.measure()
        self.previous_sent_perc = self.waterSensor.get_percentage()
        self.reduction_percentage = 0
        # state variable holds the current state, this is the initial state
        self.state = self.check_water_consumption
        print("SmartWaterBowlTask Created")

    def __str__(self):
        """prints the object."""
        return "Water Bowl"

    async def get_behaviour(self):
        """ async method called returns a coroutine"""
        while True:
            # executes the current state
            await self.state()

    def set_max_water_level(self, max_water_lvl_perc):
        self.max_water_lvl_perc = max_water_lvl_perc

    def set_min_water_level(self, min_water_lvl_perc):
        self.min_water_lvl_perc = min_water_lvl_perc

    # STATES
    async def check_water_consumption(self):
        print("STATE: check water consumption")
        # evey X seconds
        await asyncio.sleep(CHECK_WATER_CONSUMPTION_INTERVAL)
        # measure
        self.waterSensor.measure()
        print("\t\t\tWater Measure: {:.2f}".format(self.waterSensor.get_percentage()))
        # check empty
        if self.waterSensor.get_percentage() < self.min_water_lvl_perc:
            print("\t\t\tWater LOW: {:.2f} < {:.2f}".format(self.waterSensor.get_percentage(), self.min_water_lvl_perc))
            if self.valve_present:
                print("\t\t\tOpening Valve")
                self.valve.open()
                self.state = self.fill_water_bowl
                return
            else:  # water valve not present
                self.state = self.water_finished_notify
                return
        # check consumption
        self.reduction_percentage = self.previous_sent_perc - self.waterSensor.get_percentage()
        print("\t\t\tReduction Percentage: {:.2f}".format(self.reduction_percentage))
        if self.reduction_percentage >= PERCENTAGE_CONSUMPTION_THRESHOLD:
            self.state = self.send_water_consumption
            return

    async def send_water_consumption(self):
        print("STATE: send water consumption")
        # calculates consumption
        consumption = self.waterSensor.capacity * self.reduction_percentage
        # send msg consumption to database
        self.mqtt_manager.send_msg(self.topic, "Consumption Water: {:.2f} liters".format(consumption))
        # set percentage sent to actual percentage
        self.previous_sent_perc = self.waterSensor.get_percentage()
        # go to check water consumption again
        self.state = self.check_water_consumption
        return

    async def fill_water_bowl(self):
        print("STATE: filling water bowl")
        # evey X seconds
        await asyncio.sleep(CHECK_FILL_WATER_BOWL_INTERVAL)
        # measure
        self.waterSensor.measure()
        print("\t\t\tWater Measure: {:.2f} Time remaining: {}".format(self.waterSensor.get_percentage(), self.wait_before_water_error))
        # if water is refilled go back to check water consumption
        if self.waterSensor.get_percentage() > self.max_water_lvl_perc:
            print("\t\t\tClosing Valve")
            self.valve.close()
            # reset seconds
            self.wait_before_water_error = SECONDS_BEFORE_ERROR_WATER_SYSTEM
            # set percentage sent to actual percentage
            self.previous_sent_perc = self.waterSensor.get_percentage()
            self.state = self.check_water_consumption
            return
        # decrement time of period passed
        self.wait_before_water_error = self.wait_before_water_error - CHECK_FILL_WATER_BOWL_INTERVAL
        # if time expired close valve and go to water system error notify
        if self.wait_before_water_error < 0:
            print("\t\t\tClosing Valve")
            self.valve.close()
            self.wait_before_water_error = SECONDS_BEFORE_ERROR_WATER_SYSTEM
            self.state = self.water_system_error_notify
            return

    async def water_system_error_notify(self):
        print("STATE: water system error notify")
        # evey X seconds
        await asyncio.sleep(WATER_SYSTEM_ERROR_NOTIFY_INTERVAL)
        # send notification
        self.mqtt_manager.send_msg(self.topic, "NOTIFICATION ERROR WATER SYSTEM")

    async def water_finished_notify(self):
        print("STATE: water finished notify")
        # evey X seconds
        await asyncio.sleep(WATER_SYSTEM_ERROR_NOTIFY_INTERVAL)
        # measure
        self.waterSensor.measure()
        # send notification
        self.mqtt_manager.send_msg(MQTT_ERROR_TOPIC, "NOTIFICATION Water Low: {:.2f}".format(self.waterSensor.get_percentage()))
        # if water is refilled go back to check water consumption
        if self.waterSensor.get_percentage() > self.max_water_lvl_perc:
            # set percentage sent to actual percentage
            self.previous_sent_perc = self.waterSensor.get_percentage()
            self.state = self.check_water_consumption
            return
