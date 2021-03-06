# -*- coding: utf-8 -*-

import logging
import time

import RPi.GPIO as GPIO

logger = logging.getLogger(__name__)


class Stepping:
    def __init__(self, PinA1, PinA2, PinB1, PinB2):
        self.mPinA1 = PinA1     # GPIO Number
        self.mPinA2 = PinA2     # GPIO Number
        self.mPinB1 = PinB1     # GPIO Number
        self.mPinB2 = PinB2     # GPIO Number

        # 本当は1step = 0.9degだけど、
        # 簡略化のため100step = 360 degとする
        """
        !!!!! 1stepの長さの計算方法 !!!!!
        1step = 2r * Pi * (0.9/360)
        r: ギアの半径
        Pi: 円周率
        """
        self.mStep = 0

        self.set_wait_time(0.01)

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.mPinA1, GPIO.OUT)
        GPIO.setup(self.mPinA2, GPIO.OUT)
        GPIO.setup(self.mPinB1, GPIO.OUT)
        GPIO.setup(self.mPinB2, GPIO.OUT)

        GPIO.output(self.mPinA2, GPIO.HIGH)
        GPIO.output(self.mPinB2, GPIO.HIGH)

    def set_wait_time(self, wait):
        """ウエイト時間を設定する
        Args:
            wait: 設定する時間
        """
        if wait < 0.01:
            self.mStep_wait = 0.005
        elif wait > 0.5:
            self.mStep_wait = 0.1
        else:
            self.mStep_wait = wait
        logger.info({'action': 'SetWaitTime',
                     'wait_time': self.mStep_wait})

    def step_cw(self):
        """時計回りに1Step回転させる"""
        GPIO.output(self.mPinA1, GPIO.HIGH)
        time.sleep(self.mStep_wait)
        GPIO.output(self.mPinB1, GPIO.HIGH)
        time.sleep(self.mStep_wait)
        GPIO.output(self.mPinA1, GPIO.LOW)
        time.sleep(self.mStep_wait)
        GPIO.output(self.mPinB1, GPIO.LOW)
        time.sleep(self.mStep_wait)

    def step_ccw(self):
        """反時計回りに1Step回転させる"""
        GPIO.output(self.mPinB1, GPIO.HIGH)
        time.sleep(self.mStep_wait)
        GPIO.output(self.mPinA1, GPIO.HIGH)
        time.sleep(self.mStep_wait)
        GPIO.output(self.mPinB1, GPIO.LOW)
        time.sleep(self.mStep_wait)
        GPIO.output(self.mPinA1, GPIO.LOW)
        time.sleep(self.mStep_wait)

    def set_position(self, step, duration):
        """目標ポジションに移動する
        Args:
            step: 目標の位置
            duration: 移動する時間
        """
        diff_step = step - self.mStep
        if diff_step != 0:
            wait = abs(float(duration)/float(diff_step)/4)
            # wait = float2/25
            logger.info({'action': 'SetPosition',
                         'duration': duration,
                         'diff_step': diff_step})
            self.set_wait_time(wait)
        for _ in range(int(abs(diff_step))):
            if diff_step > 0:
                self.step_cw()
            if diff_step < 0:
                self.step_ccw()
        self.mStep = step

    def back_home(self):
        """元の位置に戻る"""
        self.set_position(0, 1)


if __name__ == '__main__':
    stepping = Stepping(PinA1=18, PinA2=23, PinB1=24, PinB2=25)
    try:
        while True:
            goto = input('どこまで行く？: ')
            stepping.set_position(goto, 2)
            # time.sleep(2)
    except KeyboardInterrupt:
        print("\nCtl+C")
    except Exception as e:
        print(str(e))
    finally:
        # stepping.back_home()
        GPIO.cleanup()
        print("\nexit program")
