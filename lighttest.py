# before running make sure that a standard firmata is loaded onto the board
# Arudino IDE --> File--> Example --> Firmata --> Standard Firmata --> Load
# pip pyfirmata

import sys
import pyfirmata
import time

# # Set up the Arduino board and the pin
# board = pyfirmata.Arduino('COM7')
#
# # Allow time for the board to initialize
# time.sleep(2)
#
# # Main loop
# while True:
#     board.digital[8].write(1)
#     time.sleep(1)
#     board.digital[8].write(0)
#     time.sleep(3)

class ArduinoController:
    def __init__(self, port, pin):
        self.board = pyfirmata.Arduino(port)
        self.pin = pin
        time.sleep(2)  # Allow time for the board to initialize
        self.light = 0 # light is false :. light is off

    def toggle_led(self, on_time=1, off_time=1):
        while True:
            self.board.digital[self.pin].write(1)
            time.sleep(on_time)
            self.board.digital[self.pin].write(0)
            time.sleep(off_time)

    def stop(self):
        self.board.exit()
        sys.exit(0)

# Example usage:
if __name__ == "__main__":
    arduino = ArduinoController('COM7', 8)
    try:
        arduino.toggle_led(on_time=1, off_time=15)
    except KeyboardInterrupt:
        arduino.stop()
