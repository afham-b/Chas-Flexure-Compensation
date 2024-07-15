import sys
import time
import asyncio
import threading
import matplotlib.pyplot as plt
from pylablib.devices import Newport

import socket
pico_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('127.0.0.1', 5002)  # Use the same address and port as MGListener
pico_sock.bind(server_address)

class MotorOperations:
    def __init__(self, controller, motor, default_speed=1750, close_speed=800, very_close_speed=40):
        self.controller = controller
        self.motor = motor
        self.default_speed = default_speed
        self.close_speed = close_speed
        self.very_close_speed = very_close_speed
        self.set_velocity(self.default_speed, acceleration=10000)
        self.delt_x = 0
        self.delt_y = 0

        # measure and modify the two parameters below for your magnification
        # distance in mm
        self.distance_lens_lightscourse = 118
        self.distance_lens_ccd = 83
        self.magnification = self.distance_lens_ccd/self.distance_lens_lightscourse

        # pixel size (micrometer) can be found on camera specifications sheet
        # for asi290mini pixel size is 2.9 microns, effective pixel size is ~ 4microns/pixel
        self.camera_pixel_size = 2.9
        self.effective_pixel_size = self.camera_pixel_size / self.magnification

        # set scale factor for picomotor motion from camera feedback
        self.motion_scale = 0.1
        self.correction_scale = self.effective_pixel_size * self.motion_scale

        # the pico motor moves 20 nm per step, adjust this value based on the mas the motor moves
        self.step_size = 0.019

        # how close we want the picomotor to try to get to the home position
        self.margin_of_error = 0.2

    async def control_picomotors(self):
        print('Control_picomotors output,' + str(self.delt_x) + ',' + str(self.delt_y))

        # Convert these deltas into microns * some arbitrary correction scale
        move_x = self.delt_y * self.correction_scale
        move_y = self.delt_y * self.correction_scale

        # Convert microns into steps, once picomotor step is 20 nm (default denominator is 0.02)
        steps_x = move_x / self.step_size
        steps_y = move_y / self.step_size

        #this only include y axis, needs other statement for x axis
        if abs(self.delt_y) >= self.margin_of_error:
            self.move_by_steps(steps_y)
        else:
            self.controller.stop(axis='all', immediate=True)

    async def start_sock_data(self):
        while True:
            data, _ = pico_sock.recvfrom(4096)  # Buffer size
            self.delt_x, self.delt_y = map(float, data.decode().split(','))
            #print('Socket data received: ' + str(self.delt_x) + str(self.delt_y))
            asyncio.create_task(self.control_picomotors())
            await asyncio.sleep(0.01)

    def set_velocity(self, speed, acceleration=10000):
        self.controller.setup_velocity(self.motor, speed=speed, accel=acceleration)

    async def get_position(self):
        while True:
            try:
                if not self.controller.is_moving(self.motor):
                    break
            except Exception as e:
                print(f"Error checking if motor is moving: {e}")
            await asyncio.sleep(0.005)
        return self.controller.get_position(self.motor)

    async def move_to_position(self, position, stop_event=None):
        """
        Move to an absolute position.
        """
        self.controller.move_to(self.motor, position)
        while not (stop_event and stop_event.is_set()) and self.controller.is_moving(self.motor):
            await asyncio.sleep(0.001)
        await asyncio.sleep(2)  # Pause for 2 seconds

    # async def move_by_steps(self, steps, stop_event=None):
    async def move_by_steps(self, steps, stop_event=None):
        """
        Move by a number of steps.
        """
        self.controller.move_by(self.motor, steps)

        start_time = time.time()
        timeout = 10  # Timeout in seconds

        while not (stop_event and stop_event.is_set()) and self.controller.is_moving(self.motor):
            # await asyncio.sleep(0.001)
            elapsed_time = time.time() - start_time
            if elapsed_time > timeout:
                print("Move_by_Steps Timeout reached")
                # await self.start_sock_data()
                self.controller = controller
                break
            time.sleep(0.05)

        # await asyncio.sleep(0.001)  # Pause for n seconds
        time.sleep(0.05)

    async def set_position_reference(self, position=0):
        """
        Set the current position as the reference position.
        """
        self.controller.set_position_reference(self.motor, position)
        await asyncio.sleep(3)  # Small delay to ensure the command is processed

    async def perform_operations(self, stop_event=None, distance=0.02):
        print(f'Motor {self.motor}')

        # for most masses below 1lb, the picomotor moves 20 nm per step
        steps = int((distance * 1e6) / 20)

        # Set the current position as the reference position
        await self.set_position_reference(position=0)

        # Move to initial home position (0.00)
        await self.move_to_position(0, stop_event=stop_event)
        print("Position: Home (0.00mm)")

        # Move to -0.02mm (1000 steps)
        await self.move_by_steps(steps, stop_event=stop_event)
        print("Position: -0.02mm")

        # Move to initial home position (0.00)
        await self.move_to_position(0, stop_event=stop_event)
        print("Position: Home (0.00mm)")

        # Move to +0.02mm (1000 steps from -0.02mm)
        await self.move_by_steps((-1*steps), stop_event=stop_event)
        print("Position: +0.02mm")

        # Move back home (0.00)
        await self.move_to_position(0, stop_event=stop_event)
        print("Position: Home (0.00mm)")

    async def jog_until(self, laser, target_distance, margin=0.1, stop_event=None):
        address = self.controller.get_addr()
        current_distance = laser.measure(verbose=True)
        if current_distance is None:
            print("Initial laser measurement failed. Aborting.")
            return

        direction = "+" if current_distance > target_distance else "-"
        self.controller.jog(self.motor, direction, address)

        while not (stop_event and stop_event.is_set()):
            distance = laser.measure(verbose=True)
            distance_to_target = distance - target_distance

            # Determine direction based on the current position and target distance
            new_direction = "+" if distance_to_target > 0 else "-"
            if new_direction != direction:
                print(f"Switching direction from {direction} to {new_direction}")
                self.controller.stop(axis='all', immediate=True)
                self.controller.jog(self.motor, new_direction, address)
                direction = new_direction

            # Adjust speed based on distance to target
            if abs(distance_to_target) < 0.001:
                self.set_velocity(1)
            elif abs(distance_to_target) < 0.005:
                self.set_velocity(3)
            elif abs(distance_to_target) < 0.01:
                self.set_velocity(self.very_close_speed)
            elif abs(distance_to_target) < 0.05:
                self.set_velocity(self.close_speed)
            elif abs(distance_to_target) < 0.1:
                self.set_velocity(1000)
            else:
                self.set_velocity(self.default_speed)

            if target_distance - margin <= distance <= target_distance + margin:
                self.controller.stop(axis='all', immediate=True)
                await asyncio.sleep(5)  # Pause for 5 seconds (this is for testing)
                break
            await asyncio.sleep(0.001)

        self.controller.stop(axis='all', immediate=True)

    async def joggin(self, target_distance=0, margin=0.1, stop_event=None):
        address = self.controller.get_addr()

        if self.delt_y is None:
            print("Initial laser measurement failed. Aborting.")
            return

        direction = "+" if self.delt_y > target_distance else "-"
        self.controller.jog(self.motor, direction, address)

        while not (stop_event and stop_event.is_set()):
            distance_to_target = self.delt_y - target_distance

            # Determine direction based on the current position and target distance
            new_direction = "+" if distance_to_target > 0 else "-"
            if new_direction != direction:
                print(f"Switching direction from {direction} to {new_direction}")
                self.controller.stop(axis='all', immediate=True)
                self.controller.jog(self.motor, new_direction, address)
                direction = new_direction

            # Adjust speed based on distance to target
            if abs(distance_to_target) < 0.001:
                self.set_velocity(1)
            elif abs(distance_to_target) < 0.005:
                self.set_velocity(3)
            elif abs(distance_to_target) < 0.01:
                self.set_velocity(self.very_close_speed)
            elif abs(distance_to_target) < 0.05:
                self.set_velocity(self.close_speed)
            elif abs(distance_to_target) < 0.1:
                self.set_velocity(1000)
            else:
                self.set_velocity(self.default_speed)

            if target_distance - margin <= self.delt_y <= target_distance + margin:
                self.controller.stop(axis='all', immediate=True)
                await asyncio.sleep(5)  # Pause for 5 seconds (this is for testing)
                break
            await asyncio.sleep(0.001)

        self.controller.stop(axis='all', immediate=True)

async def motor_operations_task(controller, stop_event):
    motor1_operations = MotorOperations(controller, motor=1)
    await motor1_operations.perform_operations(stop_event=stop_event, distance=0.02)

def plot_measurements(measurements):
    times, distances = zip(*measurements)
    plt.figure()
    plt.plot(times, distances, label="Distance from Motor")
    plt.axhline(y=0.02, color='r', linestyle='--', label="Target Distance +0.02mm")
    plt.axhline(y=-0.02, color='b', linestyle='--', label="Target Distance -0.02mm")
    plt.xlabel("Time (s)")
    plt.ylabel("Distance (mm)")
    plt.legend()
    plt.title("Motor Position Data")
    plt.show()


async def run(controller):
    print("measuring")
    stop_event = asyncio.Event()
    duration = None
    if len(sys.argv) > 1:
        duration = int(sys.argv[1])
        asyncio.get_event_loop().call_later(duration, stop_event.set)

    motor_task = asyncio.create_task(motor_operations_task(controller, stop_event))
    await motor_task

def stop_motors(controller):
    controller.stop(axis='all', immediate=True)
    print("Motors stopped.")


def monitor_keyboard(controller, loop, stop_event):
    while True:
        key = input()
        if key.lower() == 'x':
            stop_motors(controller)
            stop_event.set()
            loop.stop()
            break


if __name__ == "__main__":
    n = Newport.get_usb_devices_number_picomotor()
    if n == 0:
        print("No Picomotor devices found.")
    else:
        controller = Newport.Picomotor8742()
        loop = asyncio.get_event_loop()
        stop_event = asyncio.Event()

        threading.Thread(target=monitor_keyboard, args=(controller, loop, stop_event)).start()

        try:
            loop.run_until_complete(run(controller))
        except asyncio.CancelledError:
            pass
        finally:
            loop.close()
            controller.close()
