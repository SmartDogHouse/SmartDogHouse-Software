from task import Task


class MqttMessageHandlerTask(Task):

    def __init__(self):
        """ constructor """

    def __str__(self):
        """prints the object."""
        return "Message Handler Task"

    async def get_behaviour(self, topic, msg):
        print(str(topic, "utf-8") + " " + ":" + str(msg, "utf-8"))
