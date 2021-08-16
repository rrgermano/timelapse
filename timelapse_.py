import picamera
import p3picam
import os
from datetime import datetime
from time import time, sleep
import _thread
import cv2
import shutil
from multiprocessing import Pool

#Função que faz o vídeo / Carrega todas imagens em um AVI e copia a primeira imagem
#para a mesma pasta do vídeo, e excluí todas as imagens usadas para fazer o vídeo
'''def makeVideo(path, num, fps=1):
    #faz video (enumerado por 'num') de imagens .png de pasta('path') e a exclui
    image_folder = path
    video_name = 'videos/video'+str(num)+'.avi'
    

    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    print (images)

    #fourcc=cv2.VideoWriter_fourcc(*'avc1')
    
    video = cv2.VideoWriter(video_name, 0, fps, (width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))
    video.release()
    cv2.destroyAllWindows()
    shutil.copy((os.path.join(image_folder, images[0])),'videos/imagem'+str(num)+'.png')
    shutil.rmtree(path)'''
    
#Pasta onde salva as imagens
picPath = "/home/pi/Desktop/motiontl/testes/"
#Variável que conta quantos vídeos foram feitos
videoCounter = 0
#Se a pasta já contem imagens, deleta todos anteriores (apenas para teste)
if os.listdir(picPath):
    shutil.rmtree(picPath)
    os.mkdir(picPath)
#Cria pasta para separar as imagens por vídeos
picPath = picPath + str(videoCounter)+"/"
os.mkdir(picPath)
#Intervalo entre fotos (Ainda é somado cerca de 6s para analizar o motion)
intervalo=0.001
resolution=(1960, 1080)
contraste = 90
brilho = 80
#Variável que analisa o movimento
motion = True
lastpictime = time() - intervalo
testmotion = False
testVideo = False
while True:
    #Analisa se passou 3 ciclos de fotos e se fez vídeo no ultimo tempo 
    if (time() - lastpictime) > 3*intervalo and testVideo :
        #Atera a pasta para novas imagens
        _thread.start_new_thread(makeVideo, (picPath, videoCounter))
        videoCounter += 1
        picPath = "/home/pi/Desktop/motiontl/testes/" + str(videoCounter)+"/"
        lastpictime = time() - intervalo
        os.mkdir(picPath)
        testVideo = False
    #testa se houve movimento
    motion = p3picam.motion()
    if motion:
        testmotion = True
    print (motion)
    #Tira a foto
    if ((time() - lastpictime) > intervalo) and testmotion :
        currentTime=datetime.now()
        picName = currentTime.strftime("%d.%m.%Y-%H:%M:%S") + '.png'
        with picamera.PiCamera() as camera:
            camera.resolution = resolution
            camera.brightness = brilho
            camera.contrast = contraste
            camera.capture(picPath + picName)
        testVideo = True
        testmotion = False
        lastpictime = time()
    print ("Intervalo")


 

 

