# -*- coding: utf-8 -*-

import logging
import math
import time
import sys

import RPi.GPIO as GPIO

from servo import Servo
from distance_sensor import DistanceSensor
from stepping import Stepping

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# TODO: 以下のパラメータを調整

# 距離センサ―が測る最小の距離[cm]
MIN_DISTANCE = 5
# 距離センサーから測る最大の距離[cm]
MAX_DISTANCE = 100
# 距離を測る周期[s]
MEASURE_CYCLE = 0.1
# ステッピングモータにつけられたギアの半径[cm]
GEAR_RADIUS = 3
# ステッピングモータの速さ[cm/s]
SPEED = 1
# 本を取り終わるまで待つ時間[s]
TIME_TO_WAIT_TAKING = 5
# 装置の有効・無効を切り替えるために待つ時間[s]
TIME_TO_CHANGE_MODE = 2


class BookShelfManager:
    def __init__(self):
        self.dis_sensor = DistanceSensor(27, 17)
        self.servo = Servo(12)
        self.stepping = Stepping(18, 23, 24, 25)

        # 現在地
        self.current_location = 0
        # 装置が有効か
        self.is_valid = True

        # 装置の有効・無効を変更するときに使う
        self.timestamp = time.time()

    def __del__(self):
        self.servo.stop()
        self.stepping.back_home()
        GPIO.cleanup()
        sys.exit()

    def cm2step(self, cm):
        """cmをstepに変換する
        Args:
            cm: 変換前の値
        Returns:
            step: 変換後の値
        """
        # 1step = 2r * Pi * (0.9/360)
        cm_per_step = 2 * GEAR_RADIUS * math.pi * (0.9 / 360)
        step = cm / cm_per_step
        return step

    def get_duration(self, current, destination):
        """現在地から目的地までの移動時間を計算する
        Args:
            current: 現在地
            destination: 目的地
        Returns:
            duration: 移動時間
        """
        # 現在地から目的地までの距離
        difference = abs(current - destination)
        # 上で指定した速さ[cm/s]をstep/sに変換
        step_speed = self.cm2step(SPEED)
        # 移動時間を求める
        duration = difference / step_speed
        return duration

    def move_and_lift_up(self, position):
        """指定した位置まで移動し本を持ち上げる
        Args:
            position: 目的地[cm]
        """
        # 目的地をstepに変換
        step = self.cm2step(position)
        # 現在地から目的地まで何秒かかるか求める
        duration = self.get_duration(self.current_location, step)
        logger.info({'action': 'move_and_lift_up',
                     'step': step,
                     'duration': duration})
        # ステッピングモータを移動させる
        self.stepping.set_position(step, duration)
        # 現在地を更新
        self.current_location = step
        # 本を持ち上げる
        time.sleep(0.5)
        self.servo.up()
        # 本を取るまで待つ
        time.sleep(TIME_TO_WAIT_TAKING)
        # サーボモータを元に戻す
        self.servo.down()

    def start(self):
        """装置を動作させる"""
        while True:
            # 距離を測る
            distance = self.dis_sensor.read_distance()

            # 装置が有効で距離が範囲内の時
            if self.is_valid and \
                    distance > MIN_DISTANCE and distance < MAX_DISTANCE:
                logger.info({'status': 'valid',
                             'goto': distance})
                # 測定した位置まで移動し本を持ち上げる
                self.move_and_lift_up(distance)

            # 距離センサに手を近づけたら
            if distance < MIN_DISTANCE:
                current_time = time.time()
                diff_time = current_time - self.timestamp
                logger.warning({'countdown': TIME_TO_CHANGE_MODE - diff_time})

                # TIME_TO_CHANGE_MODE 秒以上距離センサに手を近づけたら
                if diff_time > TIME_TO_CHANGE_MODE:
                    # 有効・無効を切り替える
                    self.is_valid = not self.is_valid
                    logger.warning({
                        'action': 'change mode',
                        'is_valid': self.is_valid})
            else:
                # タイムスタンプをリセットする
                self.timestamp = time.time()
            time.sleep(MEASURE_CYCLE)


if __name__ == '__main__':
    manager = BookShelfManager()
    manager.start()