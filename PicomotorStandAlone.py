import sys
import time
import asyncio
import threading
import math
from datetime import datetime
import matplotlib.pyplot as plt
from pylablib.devices import Newport
from lighttest import ArduinoController

import socket

pico_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('127.0.0.1', 5002)  # Use the same address and port as MGListener
pico_sock.bind(server_address)

# file name of the calibration data
filename = 'calibration_data.txt' # microlens lenslets
#filename = 'calibration_data_nosecone.txt' #nosecone relay

log = open('pico_log.txt', 'a')

class MotorOperations:
    def __init__(self, controller, arduino, motor, default_speed=1750, close_speed=1000, very_close_speed=40):
        self.controller = controller
        self.address = self.controller.get_addr()
        self.motor = motor
        self.arduino = arduino
        self.default_speed = default_speed
        self.close_speed = close_speed
        self.very_close_speed = very_close_speed
        self.set_velocity(self.default_speed, acceleration=10000)
        self.calibrated = 0
        self.x_init = 0
        self.y_init = 0
        self.delt_x = 0
        self.delt_y = 0
        self.theta = 0

        self.controller.setup_velocity(1, speed=close_speed, accel=800)
        self.controller.setup_velocity(2, speed=close_speed, accel=800)

        self.calibration_files = ['calibration_data.txt', 'calibration_data_nosecone.txt']
        self.calibration_data = {file: {'theta': None, 'timestamp': None} for file in self.calibration_files}
        self.read_calibration_data()



        # when instance is initialized, retrieve the theta value from calibration_data.txt
        with open(filename, 'r') as file:
            lines = file.readlines()
            # Ensure there is at least one line in the file
            if not lines:
                self.theta = 0
                raise ValueError("The Calibration Data File is empty. Check File or Calibrate")


            # Get the latest theta value (last line)
            latest_theta = float(lines[-1].strip())

            self.theta = latest_theta


        # measure and modify the two parameters below for your magnification
        # distance in mm
        self.distance_lens_lightscourse = 118
        self.distance_lens_ccd = 83

        #if there is a lens on the camera use magnification calculation
        #self.magnification = self.distance_lens_ccd / self.distance_lens_lightscourse
        self.magnification = 1

        # pixel size (micrometer) can be found on camera specifications sheet
        # for asi290mini pixel size is 2.9 microns
        self.camera_pixel_size = 2.9
        #effective pixel size is ~ 4microns/pixel with a lens or 2.9 micron/pixel with no no lens
        self.effective_pixel_size = self.camera_pixel_size / self.magnification

        # set scale factor for picomotor motion from camera feedback
        #self.motion_scale = 0.75
        self.motion_scale_y = 0.8
        self.motion_scale_x = 0.8

        # the pico motor moves 20 nm per step, adjust this value based on the mas the motor moves
        #self.step_size = 0.02

        #is actuation forces for the motors are not eqivalent in both axis, you can set axis specific stepsizes
        self.step_size_y = 0.015
        self.step_size_x = 0.015

        # how close we want the picomotor to try to get to the home position
        self.margin_of_error = 2

    async def control_picomotors(self):
        print('control_picomotors output (x,y): ' + str(round(self.delt_x, 4)) + ', ' + str(round(self.delt_y, 4)))

        log.write('\n' + str(datetime.now()) + '    ' + 'control_picomotors output (x,y): ' + str(round(self.delt_x, 4)) + ', ' + str(round(self.delt_y, 4)))

        # using theta correction
        if self.theta != 0:
            corrected_delta_x = self.delt_x * math.cos(self.theta) - self.delt_y * math.sin(self.theta)
            corrected_delta_y = self.delt_x * math.sin(self.theta) + self.delt_y * math.cos(self.theta)
            #print("Corrected with theta (x,y)" + str(corrected_delta_x) + ' ' + str(corrected_delta_y))
        else:
            corrected_delta_x = self.delt_x
            corrected_delta_y = self.delt_y

        # not using theta correction
        # corrected_delta_x = self.delt_x
        # corrected_delta_y = self.delt_y

        # n pixels where motion scales need to be dynamic (i.e big steps need to reduce overshooting)
        motion_scale_switch_point = 10.0

        if abs(self.delt_x) > motion_scale_switch_point:
            self.motion_scale_x = 0.6
            self.controller.setup_velocity(2, speed=1200, accel=800)
        if abs(self.delt_y) > motion_scale_switch_point:
            self.motion_scale_y = 0.6
            self.controller.setup_velocity(1, speed=1200, accel=800)

        if abs(self.delt_x) < 4.0:
            self.controller.setup_velocity(2, speed=800, accel=800)
        if abs(self.delt_y) < 4.0:
            self.controller.setup_velocity(1, speed=800, accel=800)

        correction_scale_x = self.effective_pixel_size * self.motion_scale_x
        correction_scale_y = self.effective_pixel_size * self.motion_scale_y

        move_x = corrected_delta_x * correction_scale_x
        move_y = corrected_delta_y * correction_scale_y

        steps_x = move_x / self.step_size_x
        steps_y = move_y / self.step_size_y


        # move_x = self.delt_x * self.correction_scale
        # move_y = self.delt_y * self.correction_scale
        # # print(f"move_x and move_y: {move_x}, {move_y}")
        # await asyncio.sleep(0.1)
        #
        # # using theta
        # if self.theta != 0:
        #     corrected_move_x = move_x * math.cos(self.theta) - move_y * math.sin(self.theta)
        #     corrected_move_y = move_x * math.sin(self.theta) + move_y * math.cos(self.theta)
        #     #print(f"with theta move_x and move_y are {corrected_move_x} , {corrected_move_y}")
        # else:
        #     corrected_move_x = move_x
        #     corrected_move_y = move_y
        #     #print(f"theta is zero, move_x and move_y are {corrected_move_x} , {corrected_move_y}")
        #
        # # Convert microns to steps
        # steps_x = corrected_move_x / self.step_size
        # steps_y = corrected_move_y / self.step_size

        # direction: invert steps for x-axis correction on microlens array plate
        # direction: invert steps for x-axis correction on mirror plate
        invert = -1
        #steps_x = steps_x * invert
        #steps_y = steps_y * invert
        #print(f"Steps_x and y: {steps_x}, {steps_y}")

        self.motor = 1
        # this only include y axis

        # for testing
        #print("Correction Beginning, @Line 124")
        #print('Delta Y: ' + str(self.delt_y))
        #print('Delta X: ' + str(self.delt_x))


        if abs(self.delt_y) > self.margin_of_error:
            # print('delta y moving')
            # print('motor number is ' + str(self.motor))
            #print('about to await move by steps y')
            await self.move_by_steps(steps_y)
            #print('move by steps y awaited')
            await asyncio.sleep(0.001)
        else:
            # self.controller.stop(axis='all', immediate=True, addr=self.address)
            #self.controller.stop(axis='all', immediate=True)
            #print('stopped motion y')
            await asyncio.sleep(0.001)

        #await asyncio.sleep(0.001)
        moving = True
        while moving:
            try:
                moving = self.controller.is_moving(self.motor)
                if not moving:
                    break
            except Exception as e:
                print(f"Error checking if motor is moving: {e}")
                await asyncio.sleep(0.001)

        self.motor = 2
        # x axis motor
        if abs(self.delt_x) > self.margin_of_error:
            #print('delta x moving')
            # switch to motor 2 to move the x-axis since self by default is y
            #print('motor number is ' + str(self.motor))
            #print("steps x: " + str(steps_x))
            await self.move_by_steps(steps_x)
            await asyncio.sleep(0.001)
        else:
            #self.controller.stop(axis='all', immediate=True)
            await asyncio.sleep(0.001)

        #if abs(self.delt_x) > self.margin_of_error and abs(self.delt_y) > self.margin_of_error:
        #    self.controller.stop(axis='all', immediate=True)


        #return
        # switch back to motor 1 default


    async def calibration_data_stream(self):
        while True:
            data, _ = pico_sock.recvfrom(4096)  # Buffer size
            self.delt_x, self.delt_y, self.x_init, self.y_init= map(float, data.decode().split(','))
            if self.calibrated == 1:
                break
            await asyncio.sleep(0.01)


    async def calibrate(self, filename):

        print("Beginning Calibration")
        #print('Past Stored Theta Values:' + str(self.theta))
        await asyncio.sleep(1)
        print(f"Calibrate Picomotors: {self.delt_x}, {self.delt_y}")
        # print('Motor Number: ' + str(self.motor))

        try:
            await asyncio.sleep(2)
            # use for finding slope
            first_x = self.delt_x
            first_y = self.delt_y
            print(f"First x and y: {self.delt_x}, {self.delt_y}")

            await asyncio.sleep(3)

            # for the microlens array plate & mirror nosecone plate
            # move y motor in negative motor direction to get positive y shift to find slope
            invert = -1
            #calibration_steps = 5000*invert
            calibration_steps = 5000

            await self.move_by_steps(calibration_steps)
            await asyncio.sleep(3)

            print(f"Second x and y: {self.delt_x}, {self.delt_y}")
            second_y = self.delt_y
            second_x = self.delt_x

            if second_y != first_y and second_x != first_x:
                theta = math.asin((second_x - first_x) / (second_y - first_y))
                self.theta = theta
                print(f'Theta = {self.theta}')
                f = open(filename, 'a')
                f.write('\n'+str(datetime.now()) + '\n' + str(self.theta))
                f.close()
            elif second_x == first_x:
                self.theta = 0
                print("Calibration: No rotational offset detected (x)")
            elif second_y == first_y:
                print("Error In Calibration: No offset detected (y)")

        except Exception as e:
            print(f"Error during calibration: {e}")

        print("Moving y motor back to the original position")
        await self.move_by_steps(5000)
        await asyncio.sleep(1)
        print(f"Calibrated! Theta is {self.theta}")
        self.calibrated = 1
        await asyncio.sleep(0.001)

    async def calibration_process(self, filename):
        await asyncio.gather(self.calibration_data_stream(), self.calibrate(filename))

    def read_calibration_data(self):
        for file in self.calibration_files:
            try:
                with open(file, 'r') as f:
                    lines = f.readlines()
                    if lines:
                        latest_entry = lines[-2:]
                        timestamp = latest_entry[0].strip()
                        theta = float(latest_entry[1].strip())
                        self.calibration_data[file] = {'theta': theta, 'timestamp': timestamp}
            except FileNotFoundError:
                print(f"file {file} not found.")
            except Exception as e:
                print(f"Error reading file {file}: {e}")

    #async def start_sock_data(self, arduino):
    async def start_sock_data(self):
        loop_tracker = 0

        print("Last calibrated:")
        for file, data in self.calibration_data.items():
            print(f"    {file}: \n          Theta: {data['theta']}    \n          Time: {data['timestamp']}")

        while True:
            data, _ = pico_sock.recvfrom(4096)  # Buffer size
            self.delt_x, self.delt_y, self.x_init, self.y_init = map(float, data.decode().split(','))
            #print('Socket data received: ' + str(self.delt_x) + str(self.delt_y))

            #await asyncio.sleep(0.01)
            #print('X is : ' + str(self.delt_x+self.x_init))
            if (self.delt_x+self.x_init) != -1.00 and self.arduino.light:
            #if (self.delt_x+self.x_init) != -1.00 :
                await self.control_picomotors()

            #await self.control_picomotors()
            await asyncio.sleep(0.001)


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
        timeout = 10  # Timeout in n seconds

        moving = True

        while not (stop_event and stop_event.is_set()) and moving:
            await asyncio.sleep(0.001)
            elapsed_time = time.time() - start_time
            moving = self.controller.is_moving(self.motor)
            if elapsed_time > timeout:
                print("Move_by_Steps Timeout reached")
                # self.controller.stop(axis='all', immediate=True, addr=self.address)
                self.controller.stop(axis='all', immediate=True)
                moving = False
                # self.controller = controller # is this breaking the code?
                await self.start_sock_data()
                break
            try:
                if not self.controller.is_moving(self.motor):
                    break
            except Exception as e:
                print(f"Error checking if motor is moving: {e}")
                await asyncio.sleep(0.001)


            # time.sleep(0.001)
            await asyncio.sleep(0.001)

        await asyncio.sleep(0.001)  # Pause for n seconds
        # time.sleep(0.001)

    async def set_position_reference(self, position=0):
        # Set the current position as the reference position
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
        await self.move_by_steps((-1 * steps), stop_event=stop_event)
        print("Position: +0.02mm")

        # Move back home (0.00)
        await self.move_to_position(0, stop_event=stop_event)
        print("Position: Home (0.00mm)")

    async def jog_until(self, laser, target_distance, margin=0.1, stop_event=None):
        address = self.address
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
        address = self.address

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
        except asyncio.CancelledError or KeyboardInterrupt:
            pass
        finally:
            def end():
                stop_motors(controller)
                loop.close()
                controller.close()
            end()
            print("done")