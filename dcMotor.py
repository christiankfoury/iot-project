import RPi.GPIO as GPIO

enable = 26
pin1 = 19
pin2 = 13

def runMotor():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(enable, GPIO.OUT)
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.setup(pin2, GPIO.OUT)

    GPIO.output(pin1, 1)
    GPIO.output(pin2, 0)
    GPIO.output(enable, 1)

def stopMotor():
    GPIO.output(enable, 0)