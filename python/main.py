import RPi.GPIO as GPIO
import os
import paho.mqtt.client as mqtt
import base64
import water  as water
import camera as cam
import time
import math
import random, string
import json
from datetime import datetime
import tempSensor as temp
import motion as mouv
import lumier
import Gaz as gaz

packet_size = 3000
lightSet = False

def randomword(length):
    #Generate random string of given length
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("ctrl")

def on_message(client, userdata, msg):
    global flag
    message = str(msg.payload)
    print(msg.topic+" "+message)
    if message == "motionOn":
        print("Activate Motion")
        flag[0] = True
    elif message == "motionOff":
        print("Deactivated Motion")
        flag[0] = False
    elif message == "lightOn":
        print("Light On")
        flag[1] = True
    elif message == "lightOff":
        print("Light Off")
        flag[1] = False
    elif message == "picture":
        print("Taking Picture")
        flag[2] = True
    elif message == "video":
        print("Taking Video")
        flag[3] = True
    elif message == "waterON":
        print("Water Detector Activated")
        flag[4] = True
    elif message == "waterOFF":
        print("Water Detector Deactivated")
        flag[4] = False
    elif message == "temperature":
        flag[5] = True
    elif message == "gasON":
        print("gas on")
        flag[6]=True
    elif message == "gasOFF":
        print("gas off")
        flag[6]=False

def on_publish(client, userdata, mid):
    print("Publish Successful")

def convertImageToBase64(fileName):
    #Convert file to base64 for sending
    with open(fileName, "rb") as img:
        
        encoded1 = base64.b64encode(img.read())
        encoded=encoded1.decode('utf-8')
        return encoded

def publishEncodedImage(encoded,fileType):
    #Fragment and publish file
    end = packet_size
    start = 0
    length = len(encoded)
    picId = randomword(8)
    pos = 0
    no_of_packets = math.ceil(length/packet_size)
    while start <= len(encoded):
        data = {"data": encoded[start:end], "pic_id":picId, "pos": pos, "size": no_of_packets, "format":fileType}
        client.publish("data",json.JSONEncoder().encode(data))
        end += packet_size
        start += packet_size
        pos = pos +1

loopDelay = 0

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.username_pw_set("user1", "test")
#User authentication
client.connect("127.0.0.1", 1883, 120)
#Server IP

water.setup()
powerStatus = 0
#Flags set to True when devices is activated, each flag associated with one function
flag = [False,False,False,False,False,False,False]



client.loop_start()
while True:
    
    if flag[0] == True:#Detect motion
        for i in range(0,20):
            dect=mouv.run()
            if dect==True:
                client.publish("alert", "motion")
            time.sleep(1)
        flag[0]=False

    if flag[1] == True :#Turn outlet on 

        if lightSet == True:
            client.publish("alert", "lightOn")
            lightSet =False
        lumier.runLight()
        time.sleep(1)
        
        
    elif flag[1] == False:#Turn outlet off
        
        if lightSet == False:
            client.publish("alert", "lightOff")
            lightSet =True
        lumier.stopLight()
        time.sleep(1)
      
    if flag[2] == True:#Take and send picture
        cam.picture()
        encoded = convertImageToBase64("img1.jpg")
        publishEncodedImage(encoded, "jpg")
        flag[2] = False
    if flag[3] == True:#Take and send video
        cam.testVideo()
        os.system("MP4Box -add vid1.h264 vid1.mp4")
        encoded = convertImageToBase64("vid1.mp4")
        publishEncodedImage(encoded, "mp4")
        filename = datetime.now().strftime("%Y-%m-%d_%H.%M.%s.mp4")
        os.rename('vid1.mp4', filename)
        os.remove('vid1.h264')
        flag[3] = False
    if flag[4] == True:#Detect water leakage
        detection = water.run()
        if detection == False:
           client.publish("alert", "water")
        flag[4] = False
    if flag[5] == True:#Detect temperature and humidity
        humidity, temperature = temp.run()
        toSend = {"temp":temperature, "hum":humidity}
        client.publish("temp", json.JSONEncoder().encode(toSend))
        flag[5] = False
    time.sleep(loopDelay)
    if flag[6] == True:#Detect Gaz
        for i in range(0,20):
            decte=gaz.run()
            if decte==True:
                client.publish("alert", "gas")
            time.sleep(1)
        flag[6]=False
