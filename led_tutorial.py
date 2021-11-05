import RPi.GPIO as GPIO, time

LED = 14
INTERVAL = 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)

while True:
    GPIO.output(LED, GPIO.HIGH)
    time.sleep(INTERVAL)
    GPIO.output(LED, GPIO.LOW)
    time.sleep(INTERVAL)
