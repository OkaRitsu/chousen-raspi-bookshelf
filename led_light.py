import time

import RPi.GPIO as GPIO

class Led:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def high(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def low(self):
        GPIO.output(self.pin, GPIO.LOW)

if __name__ == '__main__':
    led = Led(14)
    led.high()
    time.sleep(5)
    led.low()
    GPIO.cleanup()

