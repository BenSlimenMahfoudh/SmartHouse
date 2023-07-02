import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
PIR_PIN = 23#MOv
GPIO.setup(PIR_PIN, GPIO.IN)

MicPin = 3
RelayPin = 4

GPIO.setup(MicPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(RelayPin, GPIO.OUT, initial=GPIO.LOW)

def run():
    if GPIO.input(PIR_PIN):
        print('Motion Detected')
        return True
    else:
        print("Motion Not Detected !!")
        return False
