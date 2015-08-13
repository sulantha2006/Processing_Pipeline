#!/usr/bin/python
__author__ = 'Seqian Wang'

# Parse ADNI Data Structure from Monica Download


class MonicaDownloadAdni:
    def __init__(self, root_folder):
        self.root_folder = root_folder

    def execute(self):
        # ls the root_folder
        # make sure that you reach the S000000 folder at the end
        # for each scan_folder, remove root_folder from string
        # split and parse the string to extract information
        # create new scan_session instance with valid information
        # check if folder contents is dcm, nii or mnc
        self.list_folder_contents()
        self.create_new_scan_session_instance()

    def create_new_scan_session_instance(self):
        pass

    def parse_path_info(self):
        pass

    def list_folder_contents(self, root_folder):
        pass