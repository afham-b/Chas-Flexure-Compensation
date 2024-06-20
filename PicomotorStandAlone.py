import sys
import time
import asyncio
import serial
import io
import datetime
import threading
import matplotlib.pyplot as plt
from pylablib.devices import Newport


class MotorOperations:
    def __init__(self, controller, motor, default_speed=1750, close_speed=800, very_close_speed=40):
        self.controller = controller
        self.motor = motor
        self.default_speed = default_speed
        self.close_speed = close_speed
        self.very_close_speed = very_close_speed
        self.set_velocity(self.default_speed, acceleration=10000)

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

    async def move_by_steps(self, steps, stop_event=None):
        """
        Move by a number of steps.
        """
        self.controller.move_by(self.motor, steps)
        while not (stop_event and stop_event.is_set()) and self.controller.is_moving(self.motor):
            await asyncio.sleep(0.001)
        await asyncio.sleep(5)  # Pause for 2 seconds

    async def set_position_reference(self, position=0):
        """
        Set the current position as the reference position.
        """
        self.controller.set_position_reference(self.motor, position)
        await asyncio.sleep(5)  # Small delay to ensure the command is processed

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


class LaserIO:
    def __init__(self, laser_port="COM5"):
        self.laser_port = laser_port
        self.ser = serial.Serial(self.laser_port, 9600, timeout=0.25)
        self.ser_io = io.TextIOWrapper(io.BufferedRWPair(self.ser, self.ser, 1),
                                       newline='\r',
                                       line_buffering=True)
        self.normal_mode()

    def normal_mode(self):
        print("normal mode")
        self.ser_io.write(u"R0\r")
        out = self.ser_io.readline()
        print(out)

    def measure(self, verbose=True):
        self.ser_io.write(u'M0\r')
        out = self.ser_io.readline()
        if verbose:
            print(out)

        i = out.rfind("M0,") + 3
        if i == -1:
            print("M0 measurement not found")
            return None
        j = out[i:].find(",")
        head_val = out[i:i + j]
        if verbose:
            print(f"Laser measurement: {head_val} mm")

        if self.isfloat(head_val):
            distance = float(head_val)
            return distance
        else:
            print("Laser head out of range")
            return None

    def isfloat(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def close(self):
        self.ser.close()
        return None


async def motor_operations_task(controller, stop_event):
    motor1_operations = MotorOperations(controller, motor=1)
    await motor1_operations.perform_operations(stop_event=stop_event, distance=0.02)


async def laser_logging_task(laser, logfile, stop_event, duration=None):
    start_time = time.time()
    measurements = []
    while not (stop_event and stop_event.is_set()):
        zlaser = laser.measure(verbose=True)
        line = str(time.time() - start_time) + "\t" + str(zlaser) + "\n"
        logfile.write(line)
        measurements.append((time.time() - start_time, zlaser))
        await asyncio.sleep(0.05)
    return measurements


def plot_measurements(measurements):
    times, distances = zip(*measurements)
    plt.figure()
    plt.plot(times, distances, label="Distance from Laser")
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

    laser = LaserIO()
    logfile = open("laser_log_" + str(datetime.date.today()) + '_' + str(time.time()) + ".txt", 'w')

    motor_task = motor_operations_task(controller, stop_event)
    laser_task = laser_logging_task(laser, logfile, stop_event, duration)

    laser_measurements = await asyncio.gather(motor_task, laser_task)
    logfile.close()
    laser.close()

    plot_measurements(laser_measurements[1])


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
