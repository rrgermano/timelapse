import p3picam
import picamera
from datetime import datetime
motionState=False
time=0

while True:
    prev=datetime.now()
    motionState= p3picam.motion()
    time=datetime.now()-prev
    print (motionState)
    currentTime=datetime.now()
    picName = currentTime.strftime("%Y.%m.%d-%H%M%S") + '.jpg'
    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 720)
        camera.capture(picPath + picName)
    print("We have taken a picture.")
    print (time)