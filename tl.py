import numpy as np
import picamera
import time
import RPi.GPIO as gpio
import json


gpio.setmode(gpio.BCM)

# Com pull-up interno
gpio.setup(26, gpio.IN, pull_up_down=gpio.PUD_UP)


def GPIO():
    if gpio.input(26) == gpio.LOW:
        print("Timer desligado")
        time.sleep(1)
        return False
    else:
        print("Timer ligado")
        return True
def maketxt(dic,path):
    name = path +'video.txt'
    with open(name, 'w') as file:
        file.write(json.dumps(dic)) # use `json.loads` to do the reverse
        file.close()
        
def extracttxt(path):
    with open(path+"video.txt", 'r') as file:
        x={}
        x = json.loads(file.read()) # use `json.dumps` to do the reverse
        file.close()
        return x

pasta = '/home/pi/Desktop/img/'
count = 0
intervalo = 450
awb = 'off'
red = .9
blue = 2.2
last_pic = time.time()
TXT = {'contador':count, 'lastPic':last_pic}


while True:
    TXT = extracttxt(pasta)
    count = TXT['contador']
    last_pic = TXT['lastPic']
    if time.time() - last_pic > intervalo:
        if GPIO():
            with picamera.PiCamera() as camera:
                time.sleep(.5)
                camera.awb_mode = awb
                camera.awb_gains = (red, blue)
                count_str = ''.join(np.repeat('0', 5 - len(str(count)))) + str(count)
                filename = pasta+'img_{}.png'.format(count_str)
                count += 1
                camera.capture(filename)
                print('shoot {}'.format(count_str))
                last_pic = time.time()
                TXT = {'contador': count, 'lastPic':last_pic}
                maketxt(TXT, pasta)
        else:
            last_pic = time.time()
            TXT['lastPic'] = last_pic
            maketxt(TXT,pasta)