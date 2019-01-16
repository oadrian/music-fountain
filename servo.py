import RPi.GPIO as GPIO
import time

PIN = 12
FREQ = 333 #Hz


def main():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PIN, GPIO.OUT)

    p = GPIO.PWM(PIN, FREQ)

    p.start(50)

    try:
        while True:
            p.ChangeDutyCycle(50)  # turn towards 90 degree
            time.sleep(5) # sleep 1 second
            p.ChangeDutyCycle(80)  # turn towards 0 degree
            time.sleep(5) # sleep 1 second
            p.ChangeDutyCycle(10) # turn towards 180 degree
            time.sleep(5) # sleep 1 second 
    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()
main()