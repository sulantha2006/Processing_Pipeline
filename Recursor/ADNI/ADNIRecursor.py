__author__ = 'Seqian Wang'

import os
from Recursor.ADNI.ScanSession import ScanSession
import Config.ADNI_RecurserConfig as arc
import Config.StudyConfig as sc
from Utils.PipelineLogger import PipelineLogger

"""
Parse ADNI Data Structure from Monica Download and return a list of instances with scans' information
"""

class ADNIRecursor():
    def __init__(self, study, recurse_folder):
        self.study = study
        self.root_folder = recurse_folder

    def recurse(self):
        directories_list, filenames = self.listRootFolderContents()
        instancesList = []
        for directory, filename in zip(directories_list, filenames):
            newSession = self.createNewScanSession(directory, filename)
            if newSession:
                instancesList.append(newSession)
        return instancesList

    def createNewScanSession(self,down_most_folder, filelist):
        # Return parts of the folder path, the ones of interest
        folder = down_most_folder.replace(self.root_folder,"")
        folder_parts = folder.split("/")  # List containing each parts/folders of the full path
        filename_parts = filelist[0].split("_")  # Takes the first filename and create a list of its parts

        rid = folder_parts[1][-4:]  # Get the last 4 characters
        scan_type = self.determineScanType(folder_parts[-3])
        scan_date = folder_parts[-2].split('_')[0]
        scan_time = folder_parts[-2].split('_', 1)[-1].replace("_", ":")
        s_identifier = filename_parts[-2]
        i_identifier = filename_parts[-1].split('.', 1)[0]
        file_type = self.determineExtension(filename_parts)
        download_folder = down_most_folder
        raw_folder = '{0}/{1}/{2}/{3}/{4}_{5}_{6}/raw'.format(sc.studyDatabaseRootDict[self.study], self.study, scan_type, rid, scan_date, s_identifier, i_identifier)

        newScanSession = ScanSession\
            (self.study, rid, scan_type, scan_date, scan_time,
             s_identifier, i_identifier, download_folder, raw_folder, file_type)
        return newScanSession

    def determineExtension(self, filename):
        fileEnding = filename[-1].split('.')[-1]
        if fileEnding == "gz":
            fileEnding = filename[-1].split('.', 1)[-1]
        return arc.fileExtensionDict[fileEnding]

    def determineScanType(self, scanTypeRaw):
        try:
            return arc.scanTypeDict[scanTypeRaw]
        except KeyError:
            if 'FDG' in scanTypeRaw:
                PipelineLogger.log('root', 'error', 'Scan Type unidentified : {0} -> Close match FDG...'.format(scanTypeRaw))
                return 'FDG'
            if 'AV45' in scanTypeRaw:
                PipelineLogger.log('root', 'error', 'Scan Type unidentified : {0} -> Close match AV45...'.format(scanTypeRaw))
                return 'AV45'
            else:
                PipelineLogger.log('root', 'error', 'Scan Type unidentified : {0} -> No match...'.format(scanTypeRaw))
                return 'unknown'

    def listRootFolderContents(self):
        # Reach down-most directories and return a list
        down_most_directories_list = []
        filenames_list = []
        for dirpath, dirnames, filenames in os.walk(self.root_folder):
            if not dirnames: # Down-most directory
                down_most_directories_list.append(dirpath)
                filenames_list.append([x for x in filenames if x.endswith(arc.fileExtensionTuple)])
        return down_most_directories_list, filenames_list
