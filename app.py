#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dropbox
import os
from os.path import expanduser

def diff_files(local_files, remote_files):
    """Check for which files to add and which ones to delete
    """
    files_to_be_added = []
    files_to_be_deleted = []
    for file in local_files:
        if file not in remote_files:
            files_to_be_added.append(file)

    for file in remote_files:
        if file not in local_files:
            files_to_be_deleted.append(file)

    return files_to_be_added, files_to_be_deleted

class LocalFileSystem:
    def __init__(self, local_path):
        self.folder_path = local_path
    
    def get_files_list(self):
        return os.listdir(self.folder_path)

class TransferData:
    def __init__(self, access_token, folder_from, folder_to):
        self.dbx = dropbox.Dropbox(access_token)
        self.folder_from = folder_from
        self.folder_to = folder_to

    def upload_file(self, file):
        """upload a file to Dropbox using API v2
        """
        with open(os.path.join(self.folder_from, file), 'rb') as f:
            self.dbx.files_upload(f.read(), self.folder_to + '/' + file)

    def remove_file(self, file):
        """remove a file from Dropbox using API v2
        """
        self.dbx.files_delete(self.folder_to + '/' + file)
        

    def get_files_list(self):
        """check the contents of a folder in Dropbox
        """
        files = []
        file_list = self.dbx.files_list_folder(self.folder_to)
        for file in file_list.entries:
            if file.name != 'test_dropbox':
                files.append(file.name)
        return files
        

def main():
    access_token = ''

    home = expanduser("~")

    file_from = os.path.join(home, 'Desktop', 'dropbox')

    localFileSystem = LocalFileSystem(file_from)

    # file_to = '/test_dropbox/check.txt'  # The full path to upload the file to, including the file name

    folder_to = '/test_dropbox'
    transferData = TransferData(access_token, file_from, folder_to)

    # API v2
    # transferData.upload_file(file_from, file_to)
    remote_files = transferData.get_files_list()
    local_files = localFileSystem.get_files_list()
    files_to_be_added, files_to_be_deleted = diff_files(local_files, remote_files)

    for file in files_to_be_added:
        transferData.upload_file(file)

    for file in files_to_be_deleted:
        transferData.remove_file(file)
    

if __name__ == '__main__':
    main()