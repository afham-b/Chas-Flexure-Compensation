from pywinauto import Application
import time
import win32api
import win32con
import os
import threading
import socket
import time
import sys
import select
import math

# win32 import usually crashes the code, but its useful
# import win32com.client

# this is from MGListener.py file, which must be in the same directory as mg_track
# MGListener.py is located in program files x86 \ meta guide folder by default
from MGListener import MyListener, MGListener, MGMonitor


def main():
    idguide = win32api.RegisterWindowMessage("MG_RemoteGuide")

    # Start MetaGuide via the plain .exe
    # app = Application().start(r"C:\Program Files (x86)\MetaGuide\MetaGuide.exe")
    #time.sleep(10)  # Wait for MetaGuide to open

    # put in your metaguide setup file if its saved, ours is test1
    scope_setup_path = r'C:\Users\afham\Documents\MetaGuide\test1.mg'
    os.startfile(scope_setup_path)
    time.sleep(5)

    # start guide (uncomment if needed)
    # win32api.PostMessage(win32con.HWND_BROADCAST, idguide, 0, 0)

    #if you want to see monitoring graphs, no nessecary for code, just optional
    #monitor_path = r'C:\Program Files (x86)\MetaGuide\MetaMonitor.exe'
    #os.startfile(monitor_path)
    #time.sleep(5)

    # Start the listener and monitor threads
    listener = MyListener()
    listener.start()

    # Wait for the listener to receive the first message
    while not listener.isAlive():
        time.sleep(0.1)

    if listener.isAlive():
        print('Listener Live!')

    # listener.doit()

    # Print the initial x and y coordinates
    x, y, intens = listener.getXYI()
    print(f"Initial coordinates: x={x}, y={y}, intensity={intens}")


    # in metaguide, open the setup button (bottom bar)-> extra tab -> make sure Broadcast is checked
    # look at extra settings for port or ip settings, otherwise monitor may not work
    # you need to take your current connected router's ip4v address and its subnet mask to calculate the broadcast mask
    # for the current router in Lab the broadcast is 10.206.255.255

    monitor = MGMonitor(listener)
    monitor.start()
    while not monitor.is_alive():
        time.sleep(0.1)

    if monitor.is_alive():
        print('Monitor Live!')
        #monitor.dumpState()

    #try:
    #    while True:
    #        time.sleep(1)
    # except KeyboardInterrupt:
    #    listener.stop()
    #    listener.join()
    #    monitor.join()


if __name__ == "__main__":
    main()
