# -*- coding: utf-8 -*-

import logging
import time
import sys

import RPi.GPIO as GPIO

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
        """
        多分こんな感じのことをしてる
        ・HighとLOWで超音波を出力する
        ・跳ね返ってきた音波を読み取る（HIGHとLOWそれぞれ）
        ・読み取れた時間を測って
        ・読み取った時間から距離をcmで計算する
        """
        GPIO.output(self.trig, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.trig, GPIO.LOW)

        while GPIO.input(self.echo) == GPIO.LOW:
            self.sig_off = time.time()
        while GPIO.input(self.echo) == GPIO.HIGH:
            self.sig_on = time.time()

        self.duration = self.sig_on - self.sig_off
        self.distance_cm = self.duration * 34000 / 2

        logging.info({'action': 'read_distance',
                      'distance': self.distance_cm})

        return self.distance_cm

    def finish(self):
        GPIO.cleanup()


# このスクリプトを実行したときだけ↓が呼ばれる
# importしたときは，ここは呼ばれない
if __name__ == '__main__':
    dis_sensor = DistanceSensor(27, 17)
    try:
        while True:
            cm = dis_sensor.read_distance()
            time.sleep(1)
            print(cm)
    # Ctrl+Cで中断したときに呼ばれる
    # 後片付け
    except KeyboardInterrupt:
        dis_sensor.finish()
        sys.exit()
