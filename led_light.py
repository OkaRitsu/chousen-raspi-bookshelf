# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import sys


class Led:
    def __init__(self,LED_PIN,SWITCH_PIN):
        self.LED_PIN = LED_PIN
        self.SWITCH_PIN = SWITCH_PIN 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(LED_PIN, GPIO.OUT)
        self.is_led_high = False

    def led_on(self):
        GPIO.output(self.LED_PIN, GPIO.HIGH)

    def led_off(self):
        GPIO.output(self.LED_PIN, GPIO.LOW)

    def get_btn_status(self):
        status = GPIO.input(self.SWITCH_PIN)
        return status

if __name__ == '__main__':
    led = Led(21,15)
    try:
        while True:
            led.led_switch()
    except KeyboardInterrupt:
        GPIO.cleanup()
