# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import sys

from servo import Servo
from distance_sensor import DistanceSensor
from stepping import Stepping

# 距離センサ―で測った距離[cm]を
# ステッピングモータで使うステップ数に変換する
def cmToStep(cm):
    """
    TODO: 1ステップは何cm?
    """
    step = cm
    return step

# 現在地から目的地までどれくらいかかる？
def howLongDoesItTake(current, destination):
    """
    TODO: 1秒間で何ステップ進ませたい?
    """
    # 現在地から目的地までの距離
    difference = abs(current - destination)
    # この距離を何秒かけて行く？
    duration = difference / 25
    return duration

def main():
    """
    TODO: 下の値の調整
    """
    # 距離センサ―が測る最小の距離[cm]
    MIN_DISTANCE = 5
    # 距離センサーから測る最大の距離[cm]
    MAX_DISTANCE = 100
    # 距離を測る周期[s]
    MEASURE_CYCLE = 1

    """
    TODO: 配線（GPIOは下にある通りに接続したらいいはず）
    """
    servo = Servo(12)
    dis_sensor = DistanceSensor(27, 17)
    stepping = Stepping(18, 23, 24, 25)

    # 現在地（ステップ）
    current_location = 0
    # 装置を動かすかどうか
    valid_flg = True


    try:
        while True:
            # 距離を測る
            distance = dis_sensor.read_distance()

            if valid_flg:
                #　測った距離が上で指定した範囲内なら
                if distance > MIN_DISTANCE and distance < MAX_DISTANCE:
                    # 距離をステップ数に変換
                    step = cmToStep(distance)
                    # 現在地からそこまでどのくらいかかる？
                    duration = howLongDoesItTake(current_location, step)
                    # 求めた時間でその場所まで移動（現在地の更新も）
                    current_location = stepping.SetPosition(step, duration)
                    # 一応ステッピングモータが動き終わってから待つ（必要ないかも）
                    time.sleep(1)
                    # サーボモーターで持ち上げる
                    servo.up()
                    # 本をとるのを待つ
                    time.sleep(5)
                    # 本をとり終わっただろうからサーボモーターを元に戻す
                    servo.down()
                # 測った距離が最小値よりも小さい（距離センサに手を近づけて装置を無効にする）
                elif distance < MIN_DISTANCE:
                    valid_flg = False
                    # ここでsleepしないとすぐに距離を測ってしまい，装置を有効に戻してしまう
                    time.sleep(3)
            else:
                # 装置が無効の状態で再び距離センサーに手を近づけると有効に戻す
                if distance < MIN_DISTANCE:
                    valid_flg = True
                    # ここも同じ
                    time.sleep(3)
            
            # 上で指定した時間待って，繰り返す
            time.sleep(MEASURE_CYCLE)

    except KeyboardInterrupt:
        servo.stop()
        GPIO.cleanup()
        sys.exit()

if __name__ == '__main__':
    main()
