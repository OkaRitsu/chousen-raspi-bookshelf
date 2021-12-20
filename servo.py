# -*- coding: utf-8 -*-

import logging
import time
import sys

import RPi.GPIO as GPIO

logger = logging.getLogger(__name__)


class Servo:
    def __init__(self, pin):
        # サーボモータのピン番号
        self.pin = pin
        # GPIOのピン番号をどうやって決めるかを設定
        # BORD: 左上から順番に数えたピン番号
        # BCM : GPIO〇〇みたいに決まってるピン番号
        GPIO.setmode(GPIO.BCM)
        # サーボモータのGPIOを出力モードに設定
        GPIO.setup(self.pin, GPIO.OUT)

        # サーボモータの設定
        # PWM(ポート番号, 周波数[Hz])
        self.servo = GPIO.PWM(pin, 50)
        self.servo.start(0)

    def servo_angle(self, angle):
        """指定した角度に回す
        Args:
            angle: サーボモータを回転させる角度
        """
        # 角度からデューティ比を求める
        duty = 2.5 + (12.0 - 2.5) * (angle + 90) / 180
        # サーボモータを回転
        self.servo.ChangeDutyCycle(duty)


    def up(self):
        logger.info({'action': 'up'})
        for theta in range(90, -30, -1):
            self.servo_angle(theta)
            time.sleep(0.02)

    def down(self):
        logger.info({'action': 'up'})
        logger.info({'action': 'down'})
        for theta in range(-30, 90, 1):
            self.servo_angle(theta)
            time.sleep(0.02)

    def stop(self):
        """後始末"""
        self.down()
        time.sleep(3)
        self.servo.stop()


if __name__ == '__main__':
    servo = Servo(12)
    try:
        while True:
            servo.up()
            time.sleep(2)
            servo.down()
    except KeyboardInterrupt:
        servo.stop()
        GPIO.cleanup()
        sys.exit()
