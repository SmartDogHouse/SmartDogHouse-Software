from mqtt_manager import MQTTManager
import uasyncio as asyncio

from task import Task


class MqttMessageCheckerTask(Task):

    def __init__(self,  mqtt_manager: MQTTManager):
        """ constructor """
        self.mqtt_manager = mqtt_manager

    def __str__(self):
        """prints the object."""
        return "Message Checker Task"

    async def get_behaviour(self):
        while True:
            print('Checking')
            self.mqtt_manager.check_msg_come()
            await asyncio.sleep(2)
