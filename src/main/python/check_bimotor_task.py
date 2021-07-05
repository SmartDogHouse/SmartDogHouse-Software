from motor_bidirectional import MotorBidirectional
from machine import Pin
import uasyncio as asyncio

from task import Task


class CheckBimotorTask(Task):

    def __init__(self, bmotor_pinf: int, bmotor_pinb: int, limit_switch_open_pin: str, limit_switch_close_pin: str):
        """ constructor.
        """
        self.bidirectional_motor = MotorBidirectional(bmotor_pinb, bmotor_pinf)
        self.switch_open = Pin(limit_switch_open_pin, Pin.IN)
        self.switch_closed = Pin(limit_switch_close_pin, Pin.IN)
        # state variable holds the current state, this is the initial state
        self.state = self.closed_bimotor
        print("CheckBimotorTask Created")
        """
        bidirectional_motor = MotorBidirectional(12, 13)
        switch_open = Pin(33, Pin.IN)
        switch_closed = Pin(34, Pin.IN)
        """

    def __str__(self):
        """prints the object."""
        return "Check Bimotor"

    async def get_behaviour(self):
        """ async method called returns a coroutine"""
        while True:
            # executes the current state
            await self.state()

    # STATES
    async def closed_bimotor(self):
        print("STATE: closed bimotor")
        # evey X seconds
        await asyncio.sleep(5)
        print("\t\tInverting Bi-Motor")
        self.bidirectional_motor.on_direction_opposite()
        self.state = self.opening
        return

    async def opening(self):
        print("STATE: opening")
        # if open
        if self.switch_open.value():
            print("\t\tStop Bi-Motor")
            self.bidirectional_motor.off()
            self.state = self.opened_bimotor
            return

    async def closing(self):
        print("STATE: closing ")
        # if closed
        if self.switch_closed.value():
            print("\t\tStop Bi-Motor")
            self.bidirectional_motor.off()
            self.state = self.closed_bimotor
            return

    async def opened_bimotor(self):
        print("STATE: opened bimotor")
        # evey X seconds
        await asyncio.sleep(5)
        print("\t\tInverting Bi-Motor")
        self.bidirectional_motor.on_direction_opposite()
        self.state = self.closing


