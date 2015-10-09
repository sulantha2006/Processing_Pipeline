__author__ = 'sulantha'
import glob, subprocess, re
from Utils.DbUtils import DbUtils
import os

DBClient = DbUtils()

def recurseBeastFolder():
    fileList = []
    for name in glob.glob('/data/data03/ADNI/BEAST/adni_*/t1/beast/*'):
        mainFolder = name
        nativeFile = os.path.realpath(glob.glob('{0}/native/*t1.mnc'.format(mainFolder))[0])
        if '\xef\xbb\xbf' in nativeFile:
            nativeFile = nativeFile.split('\xef\xbb\xbf')[1]
        if mainFolder and nativeFile:
            fileList.append((mainFolder, nativeFile))
    return fileList


def getSandIIDs(item):
    nativeFile = item[1]
    cmd = 'minchistory {0}'.format(nativeFile)
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



def copyBeast(item, proc_entry):
    pass


def addToModalTable(proc_entry):
    pass

if __name__ == '__main__':
    folderWithnativeList = recurseBeastFolder()
    for item in folderWithnativeList:
        print(item)
        s_id, i_id = getSandIIDs(item)
        proc_entry = getProcessingEntry(s_id, i_id)
        if proc_entry == None:
            print('Not found - {0} - {1} - {2}'.format(s_id, i_id, item))
        copyBeast(item, proc_entry)

        addToModalTable(proc_entry)

