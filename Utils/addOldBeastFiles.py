__author__ = 'sulantha'
import glob, subprocess, re
from Utils.DbUtils import DbUtils
import os
from distutils import file_util, dir_util
import shutil

DBClient = DbUtils()

def recurseBeastFolder():
    fileList = []
    for name in glob.glob('/data/data03/ADNI/BEAST/adni_*/t1/beast/*'):
        mainFolder = name
        nativeFile = os.path.realpath(glob.glob('{0}/native/*t1.mnc'.format(mainFolder))[0])
        if '/data/data02' in nativeFile:
            nativeFile = '/data/data02{0}'.format(nativeFile.split('/data/data02')[1])
        if mainFolder and nativeFile:
            fileList.append((mainFolder, nativeFile))
    return fileList


def getSandIIDs(item):
    if not item:
        print('Stupid - {0}'.format(item))
        return None

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
    sql = "SELECT TMP.*, ADNI_T1_Pipeline.ADDITIONAL_1 FROM (SELECT * FROM Processing WHERE S_IDENTIFIER = '{0}' AND I_IDENTIFIER = '{1}') as TMP INNER JOIN ADNI_T1_Pipeline ON TMP.RECORD_ID= ADNI_T1_Pipeline.PROCESSING_TID".format(s_id, i_id)
    res = DBClient.executeAllResults(sql)
    if len(res) == 0:
        return None
    else:
        return res[0]



def copyBeast(item, proc_entry):
    mainFolder = item[0]
    nativeFile = item[1]
    oldId = mainFolder.split('/')[-1]

    if os.path.exists('{0}/final/adni_{1}_t1_tal_lin.mnc'.format(mainFolder, oldId)) and os.path.exists('{0}/mask/adni_{1}_t1_skull_mask_native.mnc'.format(mainFolder, oldId) and os.path.exists('{0}/mask/adni_{1}_t1_tal_lin_skull_mask.mnc'.format(mainFolder, oldId))):
        if proc_entry[17] == 'OLD_PROC':
            return 1
        new_path = proc_entry[8]
        newId = '{0}_{1}{2}{3}{4}'.format('ADNI', proc_entry[2], proc_entry[4].strftime('%Y-%m-%d').replace('-', ''), proc_entry[6], proc_entry[7])
        newBeaseFolder = '{0}/beast'.format(new_path)

        if os.path.exists(newBeaseFolder):
            try:
                shutil.move(newBeaseFolder, '{0}/beastNewPipes_bkp'.format(new_path))
            except:
                pass

        exclude = set(['native'])
        if not os.path.exists('{0}/native'.format(newBeaseFolder)):
            os.makedirs('{0}/native'.format(newBeaseFolder))
        if not os.path.exists('{0}/native/{1}'.format(newBeaseFolder, os.path.basename(nativeFile).replace('adni_{0}'.format(oldId), newId))):
            file_util.copy_file(nativeFile, '{0}/native/{1}'.format(newBeaseFolder, os.path.basename(nativeFile).replace('adni_{0}'.format(oldId), newId)))

        for root, dirs, files in os.walk(mainFolder, topdown=True):
            dirs[:] = [d for d in dirs if d not in exclude]
            if files:
                rootFolder = root.replace(mainFolder, '')
                if not os.path.exists('{0}/{1}'.format(newBeaseFolder,rootFolder)):
                    os.makedirs('{0}/{1}'.format(newBeaseFolder,rootFolder))
                for file in files:
                    newFilFolder = '{0}{1}'.format(newBeaseFolder,rootFolder)
                    print('Copying - {0} -> {1}'.format('{0}/{1}'.format(root, file), '{0}/{1}'.format(newFilFolder, os.path.basename(file).replace('adni_{0}'.format(oldId), newId))))
                    file_util.copy_file('{0}/{1}'.format(root, file), '{0}/{1}'.format(newFilFolder, os.path.basename(file).replace('adni_{0}'.format(oldId), newId)))
        return 1
    else:
        print('Removing False entry : - {0}'.format(proc_entry))
        new_path = proc_entry[8]
        newBeaseFolder = '{0}/beast'.format(new_path)
        os.removedirs(newBeaseFolder)
        return 0




def addToModalTable(proc_entry):
    sql = "UPDATE ADNI_T1_Pipeline SET BEAST_MASK = 1, BEAST_SKIP = 0, BEAST_QC = 1, ADDITIONAL_1 = 'OLD_PROC' WHERE PROCESSING_TID = {0}".format(proc_entry[0])
    DBClient.executeNoResult(sql)

if __name__ == '__main__':
    rid_list= []
    folderWithnativeList = recurseBeastFolder()
    for item in folderWithnativeList:
        s_id, i_id = getSandIIDs(item)
        proc_entry = getProcessingEntry(s_id, i_id)
        if proc_entry == None:
            if item[1].split('/')[5] != 'SMC':
                rid = item[1].split('/')[6].split('_')[1]
                if rid not in rid_list:
                    rid_list.append(rid)

            continue
        #if proc_entry[17] == 'OLD_PROC':
            #continue

        if copyBeast(item, proc_entry):
            addToModalTable(proc_entry)

    print(rid_list)

