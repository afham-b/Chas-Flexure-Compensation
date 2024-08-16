# before running make sure that a standard firmata is loaded onto the board
# Arudino IDE --> File--> Example --> Firmata --> Standard Firmata --> Load
# pip pyfirmata

import sys
import pyfirmata
import time
import asyncio

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
    def __init__(self, port, light_pin, relay_pin=2):
        self.board = pyfirmata.Arduino(port)
        self.pin = light_pin
        self.relay_pin = relay_pin
        time.sleep(1)  # Allow time for the board to initialize

        # default is to start with the light on
        self.board.digital[self.pin].write(1)
        #self.board.digital[self.relay_pin].write(1)


        # default is to start with the relay closed, meaning the pico control motors are on
        # this will activate the relay switch :. turning controller board off
        #self.board.digital[self.relay_pin].write(1)
        #print('Relay OFF! ')
        #time.sleep(5)

        #self.board.digital[self.pin].write(0)
        print('Relay ON! Picomotor Controller Powered')



        self.light = True  # light is true :. light is on
        self.relay = True   #the relay is open :. control board should have power

    async def toggle_led(self, on_time=1, off_time=1):
        while True:
            self.board.digital[self.pin].write(1)
            self.light = True
            #print(self.light)
            await asyncio.sleep(on_time)

            self.board.digital[self.pin].write(0)
            self.light = False
            #print(self.light)
            await asyncio.sleep(off_time)

    def light_on(self):
        self.board.digital[self.pin].write(1)
        self.light = True

    def light_off(self):
        self.board.digital[self.pin].write(0)
        self.light = False


    async def relay_off(self):
        try:
            self.board.digital[self.relay_pin].write(1)
            await asyncio.sleep(3)
            self.relay_pin = False
        except Exception as e:
            print(e)

    async def relay_on(self):
        try:
            self.board.digital[self.relay_pin].write(0)
            await asyncio.sleep(3)
            self.relay_pin = True
        except Exception as e:
            print(e)

    async def relay_restart(self):
        try:
            await self.relay_off()
            await asyncio.sleep(3)
            await self.relay_on()
        except Exception as e:
            print(e)


    def stop(self):
        self.board.digital[self.pin].write(0)
        self.board.digital[self.relay_pin].write(0)
        #sys.exit(0)

# Example usage:
if __name__ == "__main__":
    #ensure that you have the correct com port, check com ports in device manager to view
    arduino = ArduinoController('COM7', 8, 2)
    try:
        #arduino.toggle_led(on_time=1, off_time=15)
        pass
    except KeyboardInterrupt:
        arduino.stop()
