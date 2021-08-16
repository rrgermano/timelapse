import cv2
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pydrive2.files import ApiRequestError
import os
from collections import Counter
import time

def avi(path, num, images, fps):
    # faz video (enumerado por 'num') de imagens .png de pasta('path') e a exclui
    image_folder = path
    video_name = 'videos/Frames_' + str(num) + '_FPS_'+str(fps)+'.avi'

    #images = sorted([img for img in os.listdir(image_folder) if img.endswith(".png")])
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    #print(images)

    #fourcc=cv2.VideoWriter_fourcc(*'4444')

    video = cv2.VideoWriter(video_name, 0, fps, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))
    video.release()
    cv2.destroyAllWindows()
    #shutil.copy((os.path.join(image_folder, images[0])), 'videos/imagem' + str(num) + '.png')
    #shutil.rmtree(path)
    return path[:-4]+video_name

def auth(gauth, sourcePath):
    # Try to load saved client credentials
    gauth.LoadCredentialsFile(sourcePath + "mycreds.txt")
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
        print("Autenticado via web")
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
        print ("atenticação atualizada")
    else:
        # Initialize the saved creds
        gauth.Authorize()
        print ("Autenticado via token")
    # Save the current credentials to a file
    gauth.SaveCredentialsFile(sourcePath+"mycreds.txt")

def mp4(images, output_name, fps,  bitrate):
    comand = "ffmpeg -r {ifps} -i '{input}' -ac 2 -b:v '{br}'k -c:a aac -c:v libx264 -b:a 160k -vprofile high -y -bf 0 -pix_fmt yuv420p -r {ofps} -strict experimental -f mp4 '{output}.mp4'".format(input = images, output = output_name, ifps = fps, ofps = fps, br= bitrate)
    os.popen(comand).read()
    return True

def create_folder(name, parentid):
    global drive
    #print(type(parentid))
    folder_metadata = {'title' : name , 'mimeType' : 'application/vnd.google-apps.folder' , "parents": [{"kind": "drive#fileLink", "id": parentid}]}
    folder = drive.CreateFile(folder_metadata)
    #print (folder)
    folder.Upload()
    folderid = folder['id']
    return folderid


def upVideo(videoName):
    flag = True
    flag_video = True
    parentid, file_list_video = pathid("Videos")

    if parentid is False:
        rootid = 'root'
        parentid = create_folder('Videos', rootid)
        file_list_video = drive.ListFile({'q': "'"+parentid+"' in parents"}).GetList()


    if fileRepeat(file_list_video, videoName[43:]):
        print ("Arquivo existente")
    else:
        file = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id":parentid}]})
        file['title'] = videoName[43:]
        file.SetContentFile(videoName)
        file.Upload()
        print('Created file %s with mimeType %s' % (file['title'], file['mimeType']))

def pathid(name, baseid = "root"):
    file_list = drive.ListFile({'q': "'"+baseid+"' in parents and trashed=false"}).GetList()
    for file in file_list:
        if file['title']== name:
            id = file['id']
    file_list = drive.ListFile({'q': "'" + id + "' in parents and trashed=false"}).GetList()
    return id, file_list

def fileRepeat(file_list, name=0,n='y'):
    if name !=0:
        for file in file_list:
            if file['title'] == name:
                print (file['title'])
                print (file['id'])
                return True
    else:
        for file in file_list:
            list.append(file['title'])

        list_duplicate = Counter(list)
        print("Duplicados: ")
        print(list_duplicate)
        res = [k for k, v in list_duplicate.items() if v > 1]

        for file in res:
            for file_rep in file_list:
                if file_rep['title'] == file and n=='y':
                    print("Arquivo apagado: " + file)
                    file_rep.Trash()
                    break


sourcePath = '/home/rafael/Área de Trabalho/video/'
gauth = GoogleAuth()
auth(gauth, sourcePath)
drive = GoogleDrive(gauth)
baixado = 0
repetido = 0
aquivos_drive = 0
repetido_drive = True
fps=60
bitrate = 2000
list = []

id, file_list = pathid("CAM1")
images = sorted([img for img in os.listdir(sourcePath+"/img/") if img.endswith(".png")])

#for file in file_list:
aquivos_drive = len(file_list)
if aquivos_drive > len(images):
    print ("Baixando imagens")
    print ("drive: "+str(aquivos_drive))
    print ("PC: "+str(len(images)))
try:
    for file in file_list:
        repetido_flag = True
        if aquivos_drive > len(images):
            for img in images:
                if file['title'] == img:
                    repetido_flag = False
                    break
            if repetido_flag:
                if gauth.access_token_expired: auth(gauth, sourcePath)
                file.GetContentFile(sourcePath + "img/" + file['title'])
                print ("Arquivo baixado: "+file['title'])
                images = sorted([img for img in os.listdir(sourcePath + "/img/") if img.endswith(".png")])
                baixado += 1
except ApiRequestError:
    print("dormindo")
    time.sleep(5)
    images = sorted([img for img in os.listdir(sourcePath + "/img/") if img.endswith(".png")])
    for file in file_list:
        if file['title']==images[-1] and (int(file['fileSize'])) != os.stat(sourcePath + '/img/' + images[-1]).st_size:
            os.remove(sourcePath+"/img/"+images[-1])
            images = sorted([img for img in os.listdir(sourcePath + "/img/") if img.endswith(".png")])



repetido = len(images) - baixado
print ("repetidos: " + str(repetido)+ ", Baixado: " + str(baixado)+", Total: "+str(len(images)))
#images = sorted([img for img in os.listdir(sourcePath+"/img/") if img.endswith(".png")])
video = sourcePath +'videos/Frames_' + str(len(images)) + '_FPS_'+str(fps)
#avi(sourcePath+'img/',len(images), images, fps)
mp4(sourcePath +'img/img_%5d.png', video, fps, bitrate)
#videos = sorted([vid for vid in os.listdir(sourcePath+"videos/") if vid.endswith(".mp4")])
#upVideo(video+".mp4")
