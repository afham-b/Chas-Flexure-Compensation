from pywinauto import Application
import time
import win32api
import win32con
import os


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

    # Start the listener and monitor threads
    listener = MyListener()
    listener.start()

    monitor = MGMonitor(listener)
    monitor.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        listener.stop()
        listener.join()
        monitor.join()


if __name__ == "__main__":
    main()