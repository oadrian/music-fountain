import RPi.GPIO as GPIO
import time

'''
  SERVO(pin)
     functions:
     * setup()
     * reset()
     * changeAngle(angle) 0.0 - 270.0
     * stop()
'''

MIN = 10.0
MAX = 70.0
FREQ = 300 #Hz

class Servo(object):
    def __init__(self, pin):
        self.pin = pin
        self.p = None

    def setup(self):
        GPIO.setup(self.pin, GPIO.OUT)
        self.p = GPIO.PWM(self.pin, FREQ)

        self.p.start(50)

    def reset(self):
        self.p.ChangeDutyCycle(MIN)

    def changeAngle(self, angle):
        if 0.0 <= angle and angle <= 270.0:
            pwm = MIN + (angle / 270.0) * (MAX - MIN)
            self.p.ChangeDutyCycle(pwm)
            time.sleep(1)        

    def stop():
        self.p.stop()

PIN1 = 38
PIN2 = 40

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

    s1 = Servo(PIN1)
    s2 = Servo(PIN2)

    angle = 50.0

    try:
        while True:
            angle = float(input(">>"))
            if 0.0 <= angle and angle <= 270.0:
                s1.changeAngle(angle)
                s2.changeAngle(angle)
                print("\n" + str(angle))
                time.sleep(1)
    except KeyboardInterrupt:
        s1.stop()
        s2.stop()
        GPIO.cleanup()

controlled()