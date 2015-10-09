__author__ = 'wang'
import glob, subprocess, re, os, shutil
from Utils.DbUtils import DbUtils

DBClient = DbUtils()

def recurseCivetFolder():
    # Recurse through the main folder
    fileList = []
    for mainFolder in glob.glob('/data/data03/ADNI/CBRAIN/civet_out/*/'):
        nativeFile = os.path.realpath(glob.glob(mainFolder + '/native/*t1.mnc')[0])
        if '\xef\xbb\xbf' in nativeFile:
            nativeFile = nativeFile.split('\xef\xbb\xbf')[1]
        if mainFolder and nativeFile:
            fileList.append((mainFolder, nativeFile))
    return fileList

def getSandIIDs(item):
    nativeFile = item[1]
    cmd = 'source /opt/minc/init.sh; minchistory {0}'.format(nativeFile)
    readRes, err = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    for strItem in str(readRes).strip().split('/'):
        if re.search(r'_S\d+_I\d+', strItem):
            match = re.search(r'_S\d+_I\d+', strItem)
            s = match.group().split('_')[1]
            i = match.group().split('_')[2]
            return s, i


def getProcessingEntry(s_id, i_id):
    sql = "SELECT * FROM Processing WHERE S_IDENTIFIER = '{0}' AND I_IDENTIFIER = '{1}'".format(s_id, i_id)
    res = DBClient.executeAllResults(sql)
    if len(res) == 0:
        return None
    else:
        return res

def renameFiles(file, proc_entry):
    id = proc_entry[0][2] #### Need to figure which newID to use
    newFilename = re.sub(r"\d+", id, file)
    return newFilename

def copyCivet(item, proc_entry):
    nativeFolder = item[0]
    outputFolder = proc_entry[0][8]

    # Copy structure tree with folders without files
    for dirpath, dirnames, filenames in os.walk(nativeFolder):
        # Create folder if not exist
        newFolder = os.path.join(outputFolder, dirpath[len(nativeFolder):])
        if not os.path.isdir(newFolder):
            pass
            # os.mkdir(newFolder)
        # Copy files with new naming
        for file in filenames:
            shutil.copy2(dirpath + '/' + file, newFolder + '/' + renameFiles(file, proc_entry))

def addToModalTable(proc_entry):
    pass

if __name__ == '__main__':
    folderWithnativeList = recurseCivetFolder()
    for item in folderWithnativeList:
        print(item)
        s_id, i_id = getSandIIDs(item)
        proc_entry = getProcessingEntry(s_id, i_id)
        if proc_entry == None:
            print('Not found - {0} - {1} - {2}'.format(s_id, i_id, item))
        copyCivet(item, proc_entry)

        addToModalTable(proc_entry)