import sys
import os
import inspect
import time
import asyncio

# Import the .NET Common Language Runtime (CLR) to allow interaction with .NET
import clr
import numpy as np
from ctypes import byref, c_int

from pylablib.devices import Newport


class MotorOperations:
    def __init__(self, controller, motor):
        self.controller = controller
        self.motor = motor

    async def get_position(self):
        while True:
            try:
                if not self.controller.is_moving(self.motor):
                    break
            except Exception as e:
                print(f"Error checking if motor is moving: {e}")
            await asyncio.sleep(0.1)
        return self.controller.get_position(self.motor)

    async def jog_for_duration(self, direction, duration):
        address = self.controller.get_addr()
        self.controller.jog(self.motor, direction, address)
        await asyncio.sleep(duration)
        self.controller.stop(axis='all', immediate=True)  # Use 'all' for immediate stop

    async def move_to_position(self, position):
        self.controller.move_to(self.motor, position)
        return await self.get_position()

    async def move_by_steps(self, steps):
        self.controller.move_by(self.motor, steps)
        return await self.get_position()

    async def perform_operations(self, absolute_position, relative_steps, jog_direction, jog_duration):
        print(f'Motor {self.motor}')

        # Initial position
        position = await self.get_position()
        print("Initial Position: ", position)

        # Absolute movement
        position = await self.move_to_position(absolute_position)
        print("Absolute Position: ", position)

        # Relative movement
        position = await self.move_by_steps(relative_steps)
        print("Relative Position: ", position)

        # Jog movement
        await self.jog_for_duration(jog_direction, jog_duration)
        position = await self.get_position()
        print("Jog Position: ", position, "\n")


async def run():
    n = Newport.get_usb_devices_number_picomotor()

    if n == 0:
        return

    controller = Newport.Picomotor8742()

    # Motor 1 operations
    motor1_operations = MotorOperations(controller, motor=1)
    await motor1_operations.perform_operations(absolute_position=50, relative_steps=1000, jog_direction="-", jog_duration=3)

    # Motor 2 operations
    # motor2_operations = MotorOperations(controller, motor=2)
    # await motor2_operations.perform_operations(absolute_position=75, relative_steps=2000, jog_direction="+", jog_duration=2)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
