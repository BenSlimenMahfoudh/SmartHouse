import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(27,GPIO.OUT)

def runLight():
   
    GPIO.output(27,GPIO.HIGH)

def stopLight():
  
    GPIO.output(27,GPIO.LOW)

