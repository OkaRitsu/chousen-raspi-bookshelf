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

    def led_switch(self):
        Status = 0
        while True:
            print(Status)
            try:
                if(Status == 1):
                    GPIO.output(self.LED_PIN, GPIO.HIGH)     #GPIO25の出力をHigh(3.3V)にする
                    Status = 0                          #変数"Status"に0を代入
                else:
                    GPIO.output(self.LED_PIN, GPIO.LOW)      #GPIO25の出力をLow(0V)にする
                    Status = 1
                                              #変数"Status"に1を代入
                time.sleep(1)                           #1秒間待つ
                while(GPIO.input(self.SWITCH_PIN) == 0):
                    time.sleep(0.1)                     #0.1秒間待つ

            except KeyboardInterrupt:                   #Ctrl+Cキーが押された
                GPIO.cleanup()                          #GPIOをクリーンアップ
                sys.exit()

    def get_btn_status(self):
        status = GPIO.input(self.SWITCH_PIN)
        # if status == 1:
        #      self.is_led_high = not self.is_led_high
        #      GPIO.output(self.LED_PIN, self.is_led_high)
        return status

if __name__ == '__main__':
    led = Led(21,15)
    try:
        while True:
            led.led_switch()
    except KeyboardInterrupt:
        GPIO.cleanup()
    #    pass
    #finally:
    #    GPIO.cleanup()