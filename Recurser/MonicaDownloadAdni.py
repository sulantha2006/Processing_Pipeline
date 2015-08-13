#!/usr/bin/python
__author__ = 'Seqian Wang'

import os

# Parse ADNI Data Structure from Monica Download


class MonicaDownloadAdni:
    def __init__(self, root_folder):
        self.root_folder = root_folder

    def execute(self):
        for subject_folder in os.walk(self.root_folder).next()[1]
        walk_in = os.walk(self.root_folder).next()
            if not walk_in[1]:
                folder_path = walk_in[1]
        # ls the root_folder
        # make sure that you reach the S000000 folder at the end
        # for each scan_folder, remove root_folder from string
        # split and parse the string to extract information
        # create new scan_session instance with valid information
        # check if folder contents is dcm, nii or mnc
        list_folder_contents()
        create_new_scan_session_instance()

    def check(self):
        data = None
        i = os.walk(self.root_folder).next()
        if not i[1]:  # If no subfolder, continue, else fail. Make sure that it is at the deepest level
            data = i[2][0].split("/")    # ['ADNI', '130', 'S', '2391', 'MR', 'Resting', 'State', 'fMRI', 'br', 'raw', '20110622150204096', '1', 'S112049', 'I240902.dcm']
            if len(data) >= 10:  # Make sure it's a proper DCM file
                data.append(i[0])  # i - ['<path>','<folders in the path>','<files in the path>']
        return data

    def create_new_scan_session_instance(self):
        pass

    def parse_path_info(self):
        pass

    def list_folder_contents(self, root_folder):
        pass