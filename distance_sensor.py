# -*- coding: utf-8 -*-

import logging
import time
import sys

import RPi.GPIO as GPIO

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class DistanceSensor:
    def __init__(self, trig, echo):
        self.trig = trig
        self.echo = echo

        # GPIOのモードをBCMに
        GPIO.setmode(GPIO.BCM)
        # GPIO.setmode(GPIO.BOAD)
        # trigで指定したピン番号を出力モードに
        GPIO.setup(self.trig, GPIO.OUT)
        # echoで指定したピン番号を入力モードに
        GPIO.setup(self.echo, GPIO.IN)

    def read_distance(self):
        """距離を計測する
        Returns:
            distance_cm: 計測した距離（cm）
        """
        GPIO.output(self.trig, GPIO.HIGH)
        time.sleep(0.00001)
        self.sig_off = 0
        self.sig_on = 0
        GPIO.output(self.trig, GPIO.LOW)

        while GPIO.input(self.echo) == GPIO.LOW:
            self.sig_off = time.time()
        while GPIO.input(self.echo) == GPIO.HIGH:
            self.sig_on = time.time()

        duration = self.sig_on - self.sig_off
        distance_cm = duration * 34000 / 2

        logging.info({'action': 'read_distance',
                      'distance': distance_cm})

        return distance_cm


if __name__ == '__main__':
    dis_sensor = DistanceSensor(27, 17)
    try:
        while True:
            dis_sensor.read_distance()
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit()
