import Adafruit_DHT as DHT
import RPi.GPIO as GPIO
import json
GPIO.setup(21, GPIO.OUT)
def run():
    humidity, temperature = DHT.read_retry(11, 21)
    
    print ("humidity")
    print (humidity)
    
    print ("temperature")
    print (temperature)
    return humidity, temperature
