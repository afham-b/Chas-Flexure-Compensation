import sys
import time
import asyncio
import serial
import io
import datetime
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

    async def jog_until(self, laser, target_distance, margin=0.02):
        """
        Jog the motor until the laser measures the target distance within a given margin of error.
        Positive target_distance means moving the motor away from the laser (negative laser reading).
        Negative target_distance means moving the motor towards the laser (positive laser reading).
        """
        address = self.controller.get_addr()

        # Measure the current position
        current_distance = laser.measure(verbose=True)
        if current_distance is None:
            print("Initial laser measurement failed. Aborting.")
            return

        # Determine the direction based on the current position and target distance
        direction = "+" if current_distance > target_distance else "-"
        self.controller.jog(self.motor, direction, address)

        while True:
            distance = laser.measure(verbose=True)
            if target_distance - margin <= distance <= target_distance + margin:
                self.controller.stop(axis='all', immediate=True)
                break
            await asyncio.sleep(0.001)  # Increase sampling rate by reducing sleep duration

    async def perform_operations(self, laser):
        print(f'Motor {self.motor}')

        # Move to -1mm (laser reads -1.0, meaning motor at 81mm from laser)
        await self.jog_until(laser, -1.0)
        print("Position: 81mm from laser")

        # Move to +1mm (laser reads +1.0, meaning motor at 79mm from laser)
        await self.jog_until(laser, 1.0)
        print("Position: 79mm from laser")


class LaserIO(object):

    def __init__(self, laser_port="COM5"):  # Update with the correct COM port
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
        '''
        Get laser head measurement through serial
        '''
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


async def motor_operations_task(controller, laser):
    motor1_operations = MotorOperations(controller, motor=1)
    await motor1_operations.perform_operations(laser)


async def laser_logging_task(laser, logfile, duration=None):
    start_time = time.time()
    while duration is None or time.time() - start_time < duration:
        zlaser = laser.measure(verbose=True)
        line = str(time.time() - start_time) + "\t" + str(zlaser) + "\n"
        logfile.write(line)
        await asyncio.sleep(0.001)  # Increase sampling rate by reducing sleep duration


async def run():
    print("measuring")
    duration = None
    if len(sys.argv) > 1:
        duration = int(sys.argv[1])

    laser = LaserIO()
    logfile = open("laser_log_" + str(datetime.date.today()) + '_' + str(time.time()) + ".txt", 'w')

    n = Newport.get_usb_devices_number_picomotor()
    if n == 0:
        print("No Picomotor devices found.")
        laser.close()
        return

    controller = Newport.Picomotor8742()

    motor_task = motor_operations_task(controller, laser)
    laser_task = laser_logging_task(laser, logfile, duration)

    await asyncio.gather(motor_task, laser_task)

    logfile.close()
    laser.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
