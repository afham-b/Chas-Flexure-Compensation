import sys
import pyfirmata
import time

class ArduinoController:
    def __init__(self, port, pin):
        self.board = pyfirmata.Arduino(port)
        self.pin = pin
        time.sleep(2)  # Allow time for the board to initialize

        # default is to start with the light on
        self.board.digital[self.pin].write(1)

        self.light = True  # light is true :. light is on

    def keep_led_on(self):
        while True:
            try:
                self.board.digital[self.pin].write(1)
                self.light = True
                time.sleep(1)
            except KeyboardInterrupt:
                self.stop()
                break

    def stop(self):
        self.board.digital[self.pin].write(0)
        self.board.exit()
        sys.exit(0)

# Example usage:
if __name__ == "__main__":
    arduino = ArduinoController('COM5', 8)
    arduino.keep_led_on()
