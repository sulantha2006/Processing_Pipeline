__author__ = 'Seqian Wang'

import os
from Recursor.ADNI.ScanSession import ScanSession
import Config.ADNI_RecurserConfig as arc
import Config.StudyConfig as sc
from Utils.PipelineLogger import PipelineLogger
import re, glob
from xml.dom import minidom

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
        if filelist is None: # If no file in folder, ignore and skip
            return None
        try:
            folder_parts = folder.split("/")  # List containing each parts/folders of the full path
            filename_parts = filelist[0].split("_")  # Takes the first filename and create a list of its parts

            rid = folder_parts[1][-4:]  # Get the last 4 characters
            if re.search('[a-zA-Z]', rid) is not None:
                rid = filename_parts[3]
                if re.search('[a-zA-Z]', rid) is not None:
                    PipelineLogger.log('root', 'error', 'File recurse error on Folder RID cannot be identified. - {0}, \n Filelist - {1}'.format(folder, filelist))
                    return None

            s_identifier = filename_parts[-2]
            i_identifier = filename_parts[-1].split('.', 1)[0]
            scan_type = self.determineScanType(folder_parts[-3], self.study,rid, s_identifier, i_identifier)
            scan_date = folder_parts[-2].split('_')[0]
            scan_time = folder_parts[-2].split('_', 1)[-1].replace("_", ":")
            file_type = self.determineExtension(filename_parts)
            download_folder = down_most_folder
            raw_folder = '{0}/{1}/{2}/{3}/{4}_{5}_{6}/raw'.format(sc.studyDatabaseRootDict[self.study], self.study, scan_type, rid, scan_date, s_identifier, i_identifier)
        except:
            PipelineLogger.log('root', 'exception', 'File recurse error on Folder - {0}, \n Filelist - {1}'.format(folder, filelist))
            return None

        newScanSession = ScanSession\
            (self.study, rid, scan_type, scan_date, scan_time,
             s_identifier, i_identifier, download_folder, raw_folder, file_type)
        return newScanSession

    def determineExtension(self, filename):
        fileEnding = filename[-1].split('.')[-1]
        if fileEnding == "gz":
            fileEnding = filename[-1].split('.', 1)[-1]
        return arc.fileExtensionDict[fileEnding]

    def determineScanType(self, scanTypeRaw, study, rid, sid, iid):
        try:
            return arc.scanTypeDict[scanTypeRaw]
        except KeyError:
            if 'FDG' in scanTypeRaw:
                PipelineLogger.log('root', 'error', 'Scan Type unidentified : {0} -> Close match FDG...'.format(scanTypeRaw))
                return 'FDG'
            if 'PIB' in scanTypeRaw:
                PipelineLogger.log('root', 'error', 'Scan Type unidentified : {0} -> Close match PIB...'.format(scanTypeRaw))
                return 'PIB'
            if 'AV45' in scanTypeRaw or 'AV-45' in scanTypeRaw or 'AV_45' in scanTypeRaw:
                PipelineLogger.log('root', 'error', 'Scan Type unidentified : {0} -> Close match AV45...'.format(scanTypeRaw))
                return 'AV45'
            if 'MPRAGE' in scanTypeRaw.upper():
                PipelineLogger.log('root', 'error', 'Scan Type unidentified : {0} -> Close match MPRAGE...'.format(scanTypeRaw))
                return 'MPRAGE'
            else:
                typeFromXML = self.getScanTypeFromXMLs(sc.xmlPath, study, rid, sid, iid)
                if typeFromXML:
                    if 'FDG' in typeFromXML:
                        PipelineLogger.log('root', 'error', 'Scan Type unidentified : {0} -> Close match from XML - FDG...'.format(typeFromXML))
                        return 'FDG'
                    if 'PIB' in typeFromXML:
                        PipelineLogger.log('root', 'error', 'Scan Type unidentified : {0} -> Close match  from XML - PIB...'.format(typeFromXML))
                        return 'PIB'
                    if 'AV45' in typeFromXML or 'AV-45' in typeFromXML or 'AV_45' in typeFromXML:
                        PipelineLogger.log('root', 'error', 'Scan Type unidentified : {0} -> Close match  from XML - AV45...'.format(typeFromXML))
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

    def getScanTypeFromXMLs(self, xmlPath, study, rid, s_id, i_id):
        fileStr = '{0}_*_{1}_*_{2}_{3}.xml'.format(study, rid, s_id, i_id)
        file = glob.glob('{0}/{1}'.format(xmlPath, fileStr))
        if len(file) > 0:
            file = file[0]
            xmlDoc = minidom.parse(file)
            protocol = xmlDoc.getElementsByTagName('protocol')
            rad = None
            for element in protocol:
                if element.getAttribute('term') == 'Radiopharmaceutical':
                    try:
                        rad = element.firstChild.nodeValue
                        break
                    except:
                        pass
            return rad
        else:
            return None