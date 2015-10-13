__author__ = 'wang'
import glob, subprocess, re
from Utils.DbUtils import DbUtils
import os
from distutils import file_util, dir_util
import shutil

DBClient = DbUtils()

def recurseCivetFolder():
    # Recurse through the main folder
    fileList = []
    for mainFolder in glob.glob('/data/data03/ADNI/CBRAIN/civet_out/*/'):
        nativeFile = os.path.realpath(glob.glob(mainFolder + '/native/*t1.mnc')[0])
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
    sql = "SELECT TMP.*, ADNI_T1_Pipeline.ADDITIONAL_1 FROM (SELECT * FROM Processing WHERE S_IDENTIFIER = '{0}' AND I_IDENTIFIER = '{1}') as TMP INNER JOIN ADNI_T1_Pipeline ON TMP.RECORD_ID= ADNI_T1_Pipeline.PROCESSING_TID".format(s_id, i_id)
    res = DBClient.executeAllResults(sql)
    if len(res) == 0:
        return None
    else:
        return res[0]


def copyCivet(item, proc_entry):
    mainFolder = item[0]
    nativeFile = item[1]
    oldId = mainFolder.split('/')[-1]

    if os.path.exists('{0}/final/adni_{1}_t1_final.mnc'.format(mainFolder, oldId)):
        if proc_entry[17] == 'OLD_PROC':
            return 1
        new_path = proc_entry[8]
        newId = '{0}_{1}{2}{3}{4}'.format('ADNI', proc_entry[2], proc_entry[4].strftime('%Y-%m-%d').replace('-', ''), proc_entry[6], proc_entry[7])
        newCivetFolder = '{0}/civet'.format(new_path)

        if os.path.exists(newCivetFolder):
            try:
                shutil.move(newCivetFolder, '{0}/civetNewPipes_bkp'.format(new_path))
            except:
                pass

        for root, dirs, files in os.walk(mainFolder, topdown=True):
            if files:
                rootFolder = root.replace(mainFolder, '')
                if not os.path.exists('{0}/{1}'.format(newCivetFolder,rootFolder)):
                    os.makedirs('{0}/{1}'.format(newCivetFolder,rootFolder))
                for file in files:
                    newFilFolder = '{0}{1}'.format(newCivetFolder,rootFolder)
                    print('Copying - {0} -> {1}'.format('{0}/{1}'.format(root, file), '{0}/{1}'.format(newFilFolder, os.path.basename(file).replace('adni_{0}'.format(oldId), newId))))
                    file_util.copy_file('{0}/{1}'.format(root, file), '{0}/{1}'.format(newFilFolder, os.path.basename(file).replace('adni_{0}'.format(oldId), newId)))
        return 1
    else:
        print('Removing False entry : - {0}'.format(proc_entry))
        #new_path = proc_entry[8]
        #newBeaseFolder = '{0}/beast'.format(new_path)
        #os.removedirs(newBeaseFolder)
        sql = "UPDATE ADNI_T1_Pipeline SET BEAST_MASK = 0, BEAST_SKIP = 0, BEAST_QC = 0, ADDITIONAL_1 = NULL WHERE PROCESSING_TID = {0}".format(proc_entry[0])
        DBClient.executeNoResult(sql)
        return 0

def addToModalTable(proc_entry):
    sql = "UPDATE ADNI_T1_Pipeline SET BEAST_MASK = 1, BEAST_SKIP = 0, BEAST_QC = 1, ADDITIONAL_1 = 'OLD_PROC' WHERE PROCESSING_TID = {0}".format(proc_entry[0])
    DBClient.executeNoResult(sql)

if __name__ == '__main__':
    rid_list= []
    folderWithnativeList = recurseCivetFolder()
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

        if copyCivet(item, proc_entry):
            addToModalTable(proc_entry)

    print(rid_list)