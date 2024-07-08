# import win32api
# import win32con
# from pywinauto import Application
import os
import time
import threading
import socket
import time
import sys
import select
import math
import psutil
import signal
import pyuac
import ctypes
import asyncio

# this is from MGListener.py file, which must be in the same directory as mg_track
# MGListener.py is located in program files x86 \ MetaGuide folder by default
from MGListener import MyListener, MGListener, MGMonitor

# make sure the PicomotorStandAlone.py file is in the same directory as this file
import PicomotorStandAlone
from pylablib.devices import Newport

# Run CMD as administrator to eliminate popups. If not running as admin, use run_as_admin()
# see below for main()
# however the popup still shows up...
"""def run_as_admin():
    if sys.platform == 'win32':
        try:
            # Elevate script's privileges using ShellExecuteW
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        except Exception as e:
            print(f"Failed to run as administrator: {e}")
            """
# alternative: use run_as_admin.bat

# measure and modify the two parameters below for your magnification
# distance in mm
distance_lens_lightsource = 118
distance_lens_ccd = 83
magnification = distance_lens_ccd / distance_lens_lightsource

#pixel size (micrometer) can be found on camera specifications sheet
# for asi290mini pixel size is 2.9 microns, effective pixel size is ~ 4microns/pixel
camera_pixel_size = 2.9
effective_pixel_size = camera_pixel_size / magnification

# set scale factor for picomotor motion from camera feedback
motion_scale = 0.01
correction_scale = effective_pixel_size * motion_scale

def handle_client_connection(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print("Received data:", data.decode())
    client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 9999))
    server.listen(5)
    print("Server started on port 9999")

    while True:
        client_sock, address = server.accept()
        print('Accepted connection from {}:{}'.format(address[0], address[1]))
        client_handler = threading.Thread(
            target=handle_client_connection,
            args=(client_sock,)
        )
        client_handler.start()


def main():
    # can start MetaGuide via the plain.exe
    # app = Application().start(r"C:\Program Files (x86)\MetaGuide\MetaGuide.exe")
    # time.sleep(10)  # Wait for MetaGuide to open

    # can also start MetaGuide this way:
    # idguide = win32api.RegisterWindowMessage("MG_RemoteGuide")
    # win32api.PostMessage(win32con.HWND_BROADCAST, idguide, 0, 0)

    # code below starts picomotor controller 8742 communication
    n = Newport.get_usb_devices_number_picomotor()
    if n == 0:
        print("No Picomotor devices found.")
        return

    if n > 0:
        print('ControllerFound')
    try:
        controller = Newport.Picomotor8742()
        print(controller)
    except Exception as e:
        print(f"Error connecting to the Picomotor controller: {e}")
        return

    # We're starting with a saved MetaGuide setup file: test1
    # remember to change to your own path!
    scope_setup_path = r'C:\Users\afham\Documents\MetaGuide\test1.mg'
    os.startfile(scope_setup_path)
    time.sleep(3)

    # if you want to see monitoring graphs, not necessary for code, just optional
    # monitor_path = r'C:\Program Files (x86)\MetaGuide\MetaMonitor.exe'
    # os.startfile(monitor_path)
    # time.sleep(5)


    # Start the listener and monitor threads
    listener = MyListener()
    listener.start()
    # Wait for the listener to receive the first message
    while not listener.isAlive():
        if listener.isAlive():
            print('Listener Live!')
            # Print the initial x and y coordinates
            # x, y, intens = listener.getXYI()
            # print(f"Initial coordinates: x={x}, y={y}, intensity={intens}")
        time.sleep(0.1)

    # Monitor stuff
    # in MetaGuide, open setup button (bottom bar)-> extra tab -> make sure Broadcast is checked
    # look at extra settings for port or ip settings, otherwise monitor may not work
    # you need to take your current connected router's ipv4 address and its subnet mask to calculate the broadcast mask
    # for the current router in Lab the broadcast is 10.206.255.255, it varies per router per device

    # you can use windows test loopback adapter for local network and bypasses need for router, use cmd ipconfig/all
    # to find ipv4 and subnet mask for the test loopback adapter once you've installed it from device manager.

    monitor = MGMonitor(listener)
    monitor.start()
    while not monitor.is_alive():
        if monitor.is_alive():
            print('Monitor Live!')
            # monitor.dumpState()
        time.sleep(0.1)

    def control_picomotors(delt_x, delt_y):
        # These deltas are in pixels
        print('Server output,' + str(delt_x) + ',' + str(delt_y))

        # Convert these deltas into microns * some arbitrary correction scale
        move_x = delt_x * correction_scale
        move_y = delt_y * correction_scale

        # Convert microns into steps, once picomotor step is 20 nm
        steps_x = move_x / 0.02
        steps_y = move_y / 0.02

        motor1_operations = PicomotorStandAlone.MotorOperations(controller, motor=1)
        print(motor1_operations)
        #motor1_operations.move_by_steps(steps_x)


    async def receive_data():
        # Set up UDP socket to listen
        XY_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('127.0.0.1', 5001)  # Use the same address and port as MGListener
        XY_sock.bind(server_address)

        while True:
            data, _ = XY_sock.recvfrom(4096)  # Buffer size
            delt_x, delt_y = map(float, data.decode().split(','))

            # Process received data to control the picomotors
            asyncio.create_task(control_picomotors(delt_x, delt_y))
            await asyncio.sleep(0.01)

    asyncio.run(receive_data())
    # receive_data()

    # Shut down MetaGuide using PIDs and signal
    def kill_processes(pids, sig=signal.SIGTERM):
        """
        Kill multiple processes given their PIDs using a signal (default: SIGTERM).
        """
        def get_program_name(pid):
            try:
                process = psutil.Process(pid)
                return process.name()
            except psutil.NoSuchProcess:
                print(f"No process found with PID {pid}.")
                return None

        for pid in pids:
            try:
                os.kill(pid, sig)
                print(f"Process with PID {pid} terminated: "+get_program_name(pid))
            except OSError as e:
                print(f"Error terminating process "+get_program_name(pid)+"with PID {pid}: {e} ")

    def get_pid(process_name):
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == process_name:
                return proc.info['pid']
        return None

    mgpid = get_pid('MetaGuide.exe')
    ascompid = get_pid('ASCOM.TelescopeSimulator.exe')

    input("Enter to close: ")
    pids_to_kill = [mgpid, ascompid]
    kill_processes(pids_to_kill)

    print("Now stopping threads")

    # need to end threads to end program!
    def end_threads():
        # Stop listener
        if listener.is_alive():
            listener.stop()
            listener.join()
        # Stop monitor
        if monitor.is_alive():
            monitor.join()

    end_threads()
    print("Done!")


# If you're using run_as_admin
"""if __name__ == "__main__":
    if ctypes.windll.shell32.IsUserAnAdmin() == 0:
        run_as_admin()
    else:
        main()"""

if __name__ == "__main__":
    main()

