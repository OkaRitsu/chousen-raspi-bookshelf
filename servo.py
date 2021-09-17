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
        """本を持ち上げる"""
        for theta in range(90, -90, -1):
            self.servo_angle(theta)
            logger.info({'action': 'up'})
            time.sleep(0.01)

    def down(self):
        """本を持ち上げるために回転させたステッピングモータを元に戻す"""
        for theta in range(-90, 90, 1):
            self.servo_angle(theta)
            logger.info({'action': 'down'})
            time.sleep(0.01)

    def stop(self):
        """後始末"""
        self.down()
        time.sleep(3)
        self.servo.stop()


if __name__ == '__main__':
    servo = Servo(12)
    try:
        while True:
            print('up')
            servo.up()
            time.sleep(2)
            print('down')
            servo.down()

    except KeyboardInterrupt:
        servo.stop()
        GPIO.cleanup()
        sys.exit()
