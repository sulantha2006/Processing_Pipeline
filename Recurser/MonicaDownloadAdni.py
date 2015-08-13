__author__ = 'Seqian Wang'

import os
from Recurser.ScanSession import ScanSession
import Config.ADNI_RecurserConfig as arc

# Parse ADNI Data Structure from Monica Download


class MonicaDownloadAdni:
    def __init__(self, root_folder):
        self.root_folder = root_folder

    def execute(self):
        directories_list, filenames = self.list_root_folder_contents()
        instancesList = []
        for directory, filename in zip(directories_list, filenames):
            instancesList.append(self.create_new_scan_session_instance(directory, filename))
        return instancesList
        # check if folder contents is dcm, nii or mnc

    def create_new_scan_session_instance(self,down_most_folder, filename):
        # Return parts of the folder path, the ones of interest
        folder = down_most_folder.replace(self.root_folder,"")
        folder_parts = folder.split("/")
        filename_parts = filename[0].split("_")
        study = 'ADNI'
        rid = folder_parts[1][-4:] # Get the last 4 characters
        scan_type = arc.scanTypeDict[folder_parts[2]]
        scan_date = folder_parts[-2].split('_')[0]
        scan_time = folder_parts[-2].split('_', 1)[-1].replace("_",":")
        s_identifier = folder_parts[-1]
        i_identifier = filename_parts[-1].split('.', 1)[0]
        download_folder = down_most_folder
        raw_folder = '{0}/{1}/{2}/{3}/{4}/{5}/{6}/{7}/{8}/{9}/{10}'.format(arc.databaseRoot, study, scan_type, rid, scan_date, scan_time, 'raw')
        file_type = arc.fileExtensionDict[filename_parts[-1].split('.', 1)[-1]]

        newScanSession = ScanSession\
            (study, rid, scan_type, scan_date, scan_time,
             s_identifier, i_identifier, download_folder, raw_folder, file_type)
        return newScanSession


    def list_root_folder_contents(self):
        # Reach down-most directories and return a list
        down_most_directories_list = []
        filenames_list = []
        for dirpath, dirnames, filenames in os.walk(self.root_folder):
            if not dirnames: # Down-most directory
                down_most_directories_list.append(dirpath)
                filenames_list.append([x for x in filenames if x.endswith(('.nii', '.dcm', '.mnc', '.nii.gz', '.dcm.gz', '.mnc.gz'))])
        return down_most_directories_list, filenames_list
