# -*- coding: utf-8 -*-

import logging
from os import read
import time
import statistics
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

    def read_distance(self, read_num):
        """
        read_num（奇数）回距離を測定して中央値を返す
        """
        # read_numを奇数にする
        if read_num % 2 == 0:
            read_num += 1

        distances = []
        # read_num回測定する
        for _ in range(read_num):
            distances.append(self._read_distance())

        # 中央値求めて返す
        distance = statistics.median(distances)
        return distance

    def _read_distance(self):
        """距離を計測する
        Returns:
            distance_cm: 計測した距離（cm）
        """
        GPIO.output(self.trig, GPIO.HIGH)
        time.sleep(0.00001)
        self.sig_off = 0
        self.sig_on = 0
        GPIO.output(self.trig, GPIO.LOW)

        counter = 0
        while GPIO.input(self.echo) == GPIO.LOW:
            self.sig_off = time.time()
            counter += 1
            if counter > 1000:
                break
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
            dis_sensor.read_distance(11)
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit()
