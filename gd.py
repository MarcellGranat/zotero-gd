from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import GoogleDriveFileList

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

def gd_file(filename = None):
    '''Multiple files can have the same name, but they have different ids'''
    files = drive.ListFile({'q': "title='{}' and trashed=false".format(filename)}).GetList()
    return files

def subfolders_of_folder(folder_id):
    return drive.ListFile({'q': "mimeType='application/vnd.google-apps.folder'\
     and '{}' in parents and trashed=false".format(folder_id)}).GetList()

def create_subfolder(folder_name, parent_folder_id):
    '''Create a subfolder in Google Drive'''
    file_metadata = {
        'title': [folder_name],
        'parents': [{'id': parent_folder_id}],
        'mimeType': 'application/vnd.google-apps.folder'
    }   

    folder = drive.CreateFile(file_metadata)
    folder.Upload()
    print('Created folder: %s' % folder_name)
    return folder['id']

def gd_path(path, root_folder_id = "1xNRiSJ9oQiUKbmugDz7bSUijKs9soIxe"):
    '''Get the id of a folder from its path'''
    path = path.split("/")
    folder_id = root_folder_id
    for folder in path:
        subfolders = subfolders_of_folder(folder_id)
        print(subfolders)
        prev_subfolder_id = folder_id
        folder_id = None
        for subfolder in subfolders:
            if subfolder['title'] == folder:
                folder_id = subfolder['id']
                break
        if folder_id is None:
            folder_id = create_subfolder(folder, prev_subfolder_id)
    return folder_id

def upload_file(name_of_file: str, folder_path, local_path = "literature_pdfs"):
    '''Upload a file to Google Drive'''
    folder_id = gd_path(folder_path)
    file = drive.CreateFile({'title': name_of_file,'parents': [{'id': folder_id}]})
    file.SetContentFile(local_path + "/" + name_of_file)
    file.Upload()

def download_file(gfile, path):
    '''Download a file from Google Drive'''
    gfile.GetContentFile(path)

