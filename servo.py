import RPi.GPIO as GPIO
import time

PIN = 12
FREQ = 300 #Hz


def auto():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PIN, GPIO.OUT)

    p = GPIO.PWM(PIN, FREQ)

    p.start(50)

    try:
        while True:
            p.ChangeDutyCycle(50)  # turn towards 90 degree
            time.sleep(2) # sleep 1 second
            p.ChangeDutyCycle(80)  # turn towards 0 degree
            time.sleep(2) # sleep 1 second
            p.ChangeDutyCycle(10) # turn towards 180 degree
            time.sleep(2) # sleep 1 second 
    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()

def controlled():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PIN, GPIO.OUT)

    p = GPIO.PWM(PIN, FREQ)

    p.start(50)

    dc = 50.0

    try:
        while True:
            dc = float(input(">>"))
            if 0.0 <= dc and dc <= 100.0:
                p.ChangeDutyCycle(dc)
                print("\n" + str(dc))
                time.sleep(1)
    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()

controlled()