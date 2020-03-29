#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dropbox
import os
from os.path import expanduser


def diff_files(local_files,local_files_path,remote_files,remote_files_path):
    """Check for which files to add and which ones to delete
    """
    files_folders_to_be_added=[]
    files_folders_to_be_deleted=[]
    files_folders_to_be_added_path=[]
    files_folders_to_be_deleted_path=[]
    for file in local_files:
        if file not in remote_files:
            files_folders_to_be_added.append(file)
            files_folders_to_be_added_path.append(local_files_path[local_files.index(file)])

    for file in remote_files:
        if file not in local_files:

            files_folders_to_be_deleted.append(file)
            files_folders_to_be_deleted_path.append(remote_files_path[remote_files.index(file)])

    return files_folders_to_be_added,files_folders_to_be_added_path, files_folders_to_be_deleted,files_folders_to_be_deleted_path

class TransferData:
    def __init__(self, access_token, folder_from, folder_to):
        self.dbx = dropbox.Dropbox(access_token)
        self.folder_from = folder_from
        self.folder_to = folder_to



    def get_files_list(self):
        """check the contents of a folder in Dropbox
        """
        files = []
        files_path=[]
        file_list = self.dbx.files_list_folder(self.folder_to)
        
        for file in file_list.entries:
            #print(file.path_lower)
            if file.name != 'test_dropbox':
                files.append(file.name)
                files_path.append(file.path_display)
        return files,files_path
    

    def upload_file(self,local_path,local_directory,drop_path):
        """upload a file to Dropbox using API v2
        """
        
        relative_path=os.path.relpath(local_path,local_directory)
        

        try:
           with open(local_path, 'rb') as f:
                self.dbx.files_upload(f.read(),drop_path+'/'+relative_path)
        except IsADirectoryError:
            for root, dirs, files in os.walk(local_path):

                for filename in files:
                    local_path = os.path.join(root, filename)
                    relative_path=os.path.relpath(local_path,local_directory)
                  
                    with open(local_path, 'rb') as f:
                        self.dbx.files_upload(f.read(),drop_path+'/'+relative_path)
                      
    
    def remove_file(self, file):
        """remove a file from Dropbox using API v2
        """
        self.dbx.files_delete(file)



class LocalFileSystem:
    def __init__(self, local_path):
        self.folder_path = local_path
    
    def get_files_list(self):
        lis_dir=os.listdir(self.folder_path)
        local_file_path=[]
        for i in lis_dir:
            local_file_path.append(os.path.join(self.folder_path,i))
        return lis_dir,local_file_path

def main():
    access_token = ''

    home = expanduser("~")
    
    #returns a string with the address of filefolder from
    file_folder_from=os.path.join(home,'new')

    #returns a list containing name of files(with extension) and folders
    localFileSystem=LocalFileSystem(file_folder_from)

    folder_to = '/test_dropbox'


    #returns the dbx ,path of file folder and path of folder to
    transferData=TransferData(access_token,file_folder_from,folder_to)

    remote_files,remote_files_path = transferData.get_files_list()


    local_files,local_files_path = localFileSystem.get_files_list()


    files_to_be_added,file_path, files_to_be_deleted,delete_path = diff_files(local_files,local_files_path,remote_files,remote_files_path)
 
    for file in file_path:
        transferData.upload_file(file,file_folder_from,folder_to)
    for file in delete_path:
        transferData.remove_file(file)


if __name__ == '__main__':
    main()
