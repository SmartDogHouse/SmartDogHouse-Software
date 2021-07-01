from umqtt.robust import MQTTClient


class MQTTManager:
    mqtt_client = None
    cert = ""
    key = ""
    client_id = ""
    server = ""
    port = ""
    topic = ""
    callback = ""

    def __init__(self, cert: str, key: str, client_id: str, server: str, port: int, topic: bytes, callback):
        """ constructor.
        """
        self.cert = cert
        self.key = key
        self.client_id = client_id
        self.server = server
        self.port = port
        self.topic = topic
        self.callback = callback

    def __str__(self):
        """prints the object."""
        return "Motor bidirectional currently is running: {}, direction: {}"

    def connect(self):
        with open(self.key, "r") as f:
            key = f.read()
        print("Got Key")

        with open(self.cert, "r") as f:
            cert = f.read()
        print("Got Cert")

        self.mqtt_client = MQTTClient(client_id=self.client_id, server=self.server, port=self.port, ssl=True,
                                      ssl_params={"cert": cert, "key": key, "server_side": False})

        self.mqtt_client.connect()
        self.mqtt_client.set_callback(self.callback)
        self.mqtt_client.subscribe(self.topic)
        print('MQTT Connected')

    def addTopic(self, topic):
        self.mqtt_client.subscribe(topic)

    def checkMsgCome(self):
        self.mqtt_client.check_msg()

    def sendMsg(self, topic, msg):
        self.mqtt_client.publish(topic, msg)
