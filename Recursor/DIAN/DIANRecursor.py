import os, re
import subprocess
from multiprocessing import Pool
import Config.ADNI_RecurserConfig as arc
import Config.StudyConfig as sc
from Recursor.ScanSession import ScanSession
from Utils.PipelineLogger import PipelineLogger



class DIANRecursor:
    def __init__(self, study, recurse_folder):
        self.study = study
        self.root_folder = recurse_folder
        self.only_allowed_scan_types_to_move = ['MPR', 'MPRAGE', 'PIB', 'FDG', 'TAU', 'IRFSPGR', 'FSPGR']
        self.pool = Pool()

    def __getstate__(self):
        self_dict = self.__dict__.copy()
        del self_dict['pool']
        return self_dict

    def __setstate__(self, state):
        self.__dict__.update(state)

    def recurse(self):
        directories_list, filenames = self.listRootFolderContents()
        instancesList = []

        sessions = self.pool.map(self.createNewScanSession, zip(directories_list, filenames))
        for newSession in sessions:
            if newSession:
                instancesList.append(newSession)
        return instancesList

    def get_visit_info(self, file_name):
        cmd = "/data/data02/sulantha/bin/gdcmbin/bin/gdcmdump {0} ".format(file_name)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        tmp = proc.stdout.read().decode("utf-8")
        for line in tmp.split("\n"):
            if '(0010,0020)' in line:
                pid = line[line.find('[') + len('['):line.find(']')]
                visit = pid.split('_')[1]
                if len(visit) is 3 and visit.startswith('v'):
                    return visit
                else:
                    return None

    def getScanDateTimeDCMHeader(self, file_name):
        cmd = "/data/data02/sulantha/bin/gdcmbin/bin/gdcmdump {0} ".format(file_name)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        tmp = proc.stdout.read().decode("utf-8")
        time_str = None
        date_str = None
        for line in tmp.split("\n"):
            if '(0008,0020)' in line:
                date_str = line[line.find('[') + len('['):line.find(']')]
        for line in tmp.split("\n"):
            if '(0008,0030)' in line:
                time_str = line[line.find('[') + len('['):line.find(']')]
                time_str = time_str.strip().split('.')[0]
        return  date_str, time_str
        
    def createNewScanSession(self, tup):
        down_most_folder, filelist = tup
        # Return parts of the folder path, the ones of interest
        folder = down_most_folder.replace(self.root_folder,"")
        filelist = [ x for x in filelist if 'xml' not in x ]
        if len(filelist) == 0: # If no file in folder, ignore and skip
            return None
        try:
            folder_parts = folder.split("/")  # List containing each parts/folders of the full path
            filename_parts = filelist[0].split(".")  # Takes the first filename and create a list of its parts

            rid = filename_parts[0]
            file_type = self.determineExtension(filename_parts)

            scan_date_str, scan_time_str = self.getScanDateTimeDCMHeader('{0}/{1}'.format(down_most_folder, filelist[0]))

            scan_date = '{0}-{1}-{2}'.format(scan_date_str[:4], scan_date_str[4:6], scan_date_str[6:8])
            scan_time = '{0}:{1}:{2}'.format(scan_time_str[:2], scan_time_str[2:4], scan_time_str[4:6])
            visit = self.get_visit_info('{0}/{1}'.format(down_most_folder, filelist[0]))
            if not visit:
                return None
            scan_type = self.determineScanType('{0}/{1}'.format(down_most_folder, filelist[0]))
            if not scan_type or scan_type not in self.only_allowed_scan_types_to_move:
                return None
            i_identifier = '{0}{1}{2}{3}x{4}'.format(rid, scan_type, visit, scan_date_str,
                                                     re.sub(r'[\W_]+', '', folder_parts[-2]))
            s_identifier = 'ySy'
            download_folder = down_most_folder
            raw_folder = '{0}/{1}/{2}/{3}/{4}_{5}_{6}/raw'.format(sc.studyDatabaseRootDict[self.study], self.study, scan_type, rid, scan_date, s_identifier, i_identifier)
        except Exception as e:
            PipelineLogger.log('root', 'exception', 'File recurse error on Folder - {0}, \n Filelist - {1}'.format(folder, filelist))
            PipelineLogger.log('root', 'exception', 'Exception - {0}'.format(e))
            return None

        newScanSession = ScanSession(self.study, rid, scan_type, scan_date, scan_time,
             s_identifier, i_identifier, download_folder, raw_folder, file_type)
        return newScanSession

    def determineExtension(self, filename):
        fileEnding = filename[-1].split('.')[-1]
        if fileEnding == "gz":
            fileEnding = filename[-1].split('.', 1)[-1]
        return arc.fileExtensionDict[fileEnding]

    def getScanTypeFromPID(self, pid):
        try:
            st = pid.lower().split('_')[2]
            if st in ['fdg', 'pib', 'tau']:
                return st.upper()
            else:
                return 'unknown'
        except:
            return 'unknown'

    def getDIAN_MR_ScanType(self, st):
        if 'dti' in st.lower():
            return 'DTI'
        if 'mprage' in st.lower():
            return 'MPRAGE'
        if 'rsfmri' in st.lower() or 'rsf mri' in st.lower():
            return 'rsFMRI'
        if 'fmri' in st.lower():
            return 'FMRI'
        if 'ir-fspgr' in st.lower():
            return 'IRFSPGR'
        if 'fspgr' in st.lower():
            return 'FSPGR'
        if 't2' in st.lower():
            return 'T2'
        if 'perfusion_weighted' in st.lower():
            return 'DTI'
        if 'resting_state' in st.lower():
            return 'rsFMRI'
        if 'dwi' in st.lower():
            return 'DTI'
        if 'mpr' in st.lower():
            return 'MPR'

    def determineScanType(self, file_name):
        cmd = "/data/data02/sulantha/bin/gdcmbin/bin/gdcmdump {0} ".format(file_name)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        tmp = proc.stdout.read().decode("utf-8")
        scanTypeRaw='unknown'
        for line in tmp.split("\n"):
            if '(0008,0060)' in line:
                modality = line[line.find('[')+len('['):line.find(']')]
                break
        for line in tmp.split("\n"):
            if '(0008,0008)' in line:
                img_type = line[line.find('[')+len('['):line.find(']')]
                break

        for line in tmp.split("\n"):
            if '(0010,0020)' in line:
                pid = line[line.find('[')+len('['):line.find(']')]
                if 'fdg' in pid.lower() or 'pib' in pid.lower() or 'tau' in pid.lower():
                    if (modality == 'CT' or modality == 'PT') and img_type == r'ORIGINAL\PRIMARY':
                        return self.getScanTypeFromPID(pid)
                    else:
                        if modality == 'MR':
                            break
                        else:
                            return None
        for line in tmp.split("\n"):
            if '(0008,103e)' in line:
                scanTypeRaw = line[line.find('[')+len('['):line.find(']')]
                break
        return self.getDIAN_MR_ScanType(scanTypeRaw)

    def listRootFolderContents(self):
        # Reach down-most directories and return a list
        down_most_directories_list = []
        filenames_list = []
        for dirpath, dirnames, filenames in os.walk(self.root_folder):
            if not dirnames: # Down-most directory
                down_most_directories_list.append(dirpath)
                filenames_list.append([x for x in filenames if x.endswith(arc.fileExtensionTuple)])
        return down_most_directories_list, filenames_list

if __name__ == '__main__':
    c = DIANRecursor('DIAN', '/data/data02/sulantha/DIAN_EXT_MR_DICOM/DIANDF')
    k = c.recurse()
    print(len(k))
    s = set(k)
    print(len(s))
