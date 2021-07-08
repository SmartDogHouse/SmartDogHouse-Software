from mqtt_manager import MQTTManager
import uasyncio as asyncio
import time
from machine import Pin

from task import Task
from pulse_sensor import PulseSensor

MAX_HISTORY = 250  # depends on the frequency of reading

TOTAL_BEATS = 30  # num last beats to calculate bmp

SECONDS_SENDING_HEARTBEAT = 30


class SmartCollarHeartbeatTask(Task):
    """ designed with pulse sensor MBCG-DX"""

    def __init__(self, mqtt_manager: MQTTManager, topic: str, hb_pin: int, min_heartbeat=20, max_heartbeat=200):
        """ constructor.
        """
        self.mqtt_manager = mqtt_manager
        self.topic = topic
        self.pulse_sensor = PulseSensor(hb_pin)
        # Maintains a log of previous values to determine min, max and threshold.
        self.history = []
        self.beats = []
        self.still_beat = False
        self.min_heartbeat = min_heartbeat
        self.max_heartbeat = max_heartbeat
        self.led = Pin(23, Pin.OUT)
        self.last_sent = time.time()
        # state variable holds the current state, this is the initial state
        self.state = self.check_heartbeat
        print("SmartCollarHeartbeatTask Created")

    def __str__(self):
        """prints the object."""
        return "Smart Collar Heartbeat"

    async def get_behaviour(self):
        """ async method called returns a coroutine"""
        while True:
            # executes the current state
            await self.state()

    def set_max_heartbeat(self, max_heartbeat):
        self.max_heartbeat = max_heartbeat

    def set_min_heartbeat(self, min_heartbeat):
        self.min_heartbeat = min_heartbeat

    # STATES
    async def check_heartbeat(self):
        # evey X seconds
        await asyncio.sleep_ms(10)
        # print("STATE: check collar heartbeat")
        # measure
        val = self.pulse_sensor.raw_measure()
        # add to history of values
        self.history.append(val)
        # crop to MAX_HISTORY length, getting the tail (last ones)
        self.history = self.history[-MAX_HISTORY:]
        # get min max in the history
        minima, maxima = min(self.history), max(self.history)
        # get thresholds
        threshold_on = (minima + maxima * 4) // 5  # 4/5
        threshold_off = (minima + maxima) // 2  # 1/2
        # print("{} {} {} {} {}".format(val, minima, maxima, threshold_on, threshold_off))
        # if val goes above beat threshold
        if val > threshold_on and self.still_beat == False:
            self.led.on()
            self.still_beat = True  # prevents multiple appends for all the measures during a beat
            # once every beat
            self.beats.append(time.time())
            self.beats = self.beats[-TOTAL_BEATS:]
            # calculate bpm
            beats_time = self.beats[-1] - self.beats[0]  # time difference between end and start of the queue
            if beats_time:
                bpm = (len(self.beats) / beats_time) * 60
                print("HeartBeat: {}".format(bpm))
                # if outside range
                if bpm < self.min_heartbeat or bpm > self.max_heartbeat:
                    # send notification now
                    self.mqtt_manager.send_msg(self.topic, "NOTIFICATION Heartbeat is abnormal: {}".format(bpm))
                    pass
                # if enough time (sec) passed since last sending
                if (time.time() - self.last_sent) > SECONDS_SENDING_HEARTBEAT:
                    self.last_sent = time.time()
                    # send data
                    self.mqtt_manager.send_msg(self.topic, "HeartBeat: {}".format(bpm))
        # if val goes below threshold
        if val < threshold_off and self.still_beat == True:
            self.led.off()
            self.still_beat = False  # current beat is no more active
