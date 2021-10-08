# -*- coding: utf-8 -*-
import time

import RPi.GPIO as GPIO

from stepping import Stepping

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
