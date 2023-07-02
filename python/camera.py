from picamera import PiCamera
from datetime import datetime
import time

camera = PiCamera()

def testVideo():
    filename = "vid1.h264"
    camera.start_recording(filename)
    print ("Started Recording")
    time.sleep(5)
    camera.stop_recording()
    print ("Ended Recording")
def picture():
   # camera.rotation = 180
    camera.capture('img1.jpg', resize=(500,281))
