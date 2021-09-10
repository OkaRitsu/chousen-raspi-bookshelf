# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from time import sleep

class Stepping:
    """コンストラクタ"""
    def __init__(self, PinA1, PinA2, PinB1, PinB2):
        self.mPinA1 = PinA1     #GPIO Number
        self.mPinA2 = PinA2     #GPIO Number
        self.mPinB1 = PinB1     #GPIO Number
        self.mPinB2 = PinB2     #GPIO Number
        self.mStep = 0          #本当は1step = 0.9degだけど、簡略化のため100step = 360degとする

        self.SetWaitTime(0.01)

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.mPinA1, GPIO.OUT)
        GPIO.setup(self.mPinA2, GPIO.OUT)
        GPIO.setup(self.mPinB1, GPIO.OUT)
        GPIO.setup(self.mPinB2, GPIO.OUT)

        GPIO.output(self.mPinA2,GPIO.HIGH)
        GPIO.output(self.mPinB2,GPIO.HIGH)

    """ウエイト時間を設定する"""
    def SetWaitTime(self, wait):
        if wait < 0.01:
            self.mStep_wait = 0.005
        elif wait > 0.5:
            self.mStep_wait = 0.1
        else:
            self.mStep_wait = wait

    """CWに1Step移動する"""
    def Step_CW(self):
        GPIO.output(self.mPinA1,GPIO.HIGH)
        sleep(self.mStep_wait)
        GPIO.output(self.mPinB1,GPIO.HIGH)
        sleep(self.mStep_wait)
        GPIO.output(self.mPinA1,GPIO.LOW)
        sleep(self.mStep_wait)
        GPIO.output(self.mPinB1,GPIO.LOW)
        sleep(self.mStep_wait)

    """CCWに1Step移動する"""
    def Step_CCW(self):
        GPIO.output(self.mPinB1,GPIO.HIGH)
        sleep(self.mStep_wait)
        GPIO.output(self.mPinA1,GPIO.HIGH)
        sleep(self.mStep_wait)
        GPIO.output(self.mPinB1,GPIO.LOW)
        sleep(self.mStep_wait)
        GPIO.output(self.mPinA1,GPIO.LOW)
        sleep(self.mStep_wait)

    """目標ポジションに移動する"""
    def SetPosition(self, step, duration):
        diff_step = step - self.mStep
        if diff_step != 0:
            wait = abs(float(duration)/float(diff_step)/4)
            #wait = float2/25
            print("duration:"+str(duration))
            print("diff_step:"+str(diff_step))
            print("wait:"+str(wait))
            self.SetWaitTime(wait)
        for i in range(int(abs(diff_step))):
            if diff_step > 0:
                self.Step_CW()
            if diff_step < 0:
                self.Step_CCW()
        self.mStep = step
        return self.mStep

    """終了処理"""
    def Cleanup(self):
        GPIO.cleanup()

"""メイン関数"""
if __name__ == '__main__':
    StepMoter = Stepping(PinA1=18, PinA2=23, PinB1=24, PinB2=25)
    #Main loop
    try:
        while True:
            StepMoter.SetPosition(0,2)
            sleep(1)
            StepMoter.SetPosition(150,2)
            sleep(1)
            # StepMoter.SetPosition(50,2)
            # sleep(1)
            # StepMoter.SetPosition(75,3)
            # sleep(1)
    except KeyboardInterrupt  :         #Ctl+Cが押されたらループを終了
        print("\nCtl+C")
    except Exception as e:
        print(str(e))
    finally:
        StepMoter.Cleanup()
        print("\nexit program")
