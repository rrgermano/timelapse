from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

def gauth(sourcePath):
    gauth = GoogleAuth()
    auth(gauth, sourcePath)
    drive = GoogleDrive(gauth)
    return gauth, drive

def auth(gauth, sourcePath):
    # Try to load saved client credentials
    gauth.LoadCredentialsFile(sourcePath + "mycreds.txt")
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile(sourcePath+"mycreds.txt")
    return gauth

def create_folder(name, parentid):
    global drive
    #print(type(parentid))
    folder_metadata = {'title' : name , 'mimeType' : 'application/vnd.google-apps.folder' , "parents": [{"kind": "drive#fileLink", "id": parentid}]}
    folder = drive.CreateFile(folder_metadata)
    #print (folder)
    folder.Upload()
    folderid = folder['id']
    return folderid

def upPhoto(sourcePath, name, parentid):
    flag=True
    while flag:
        file = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": parentid}]})
        file['title'] = name
        file.SetContentFile(sourcePath+'img/'+name)
        file.Upload()
        flag = compare(sourcePath, file, name)
        print ('Created file %s with mimeType %s\n' % (file['title'],file['mimeType']))

def compare(sourcePath, file, image):
    if (int(file['fileSize'])) == os.stat(sourcePath+'img/'+image).st_size:
        print ("ok")
        os.remove(sourcePath+'img/'+image)
        return False
    else:
        print ("Errado")
        return True

def pathid(drive, name, baseid = "root"):
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