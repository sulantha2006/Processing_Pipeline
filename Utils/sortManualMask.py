__author__ = 'sulantha'

maskList = '/home/sulantha/Desktop/ManualMaskMatch.csv'
outputpath = '/data/data03/MANUAL_MASK'
from Utils.DbUtils import DbUtils
import shutil


Dbclient = DbUtils()
with open(maskList, 'r') as inf:
    for line in inf:
        row = line.split(',')
        if row[0].strip() == 'None' or row[1].strip() == 'None' or row[2].strip() == 'None':
            pass
        else:
            study = row[1].split('/')[-1].split('_')[0].upper()
            rid = row[2].split('_')[3]
            t1sid = row[2].split('.')[0].split('_')[-2]
            t1iid = row[2].split('.')[0].split('_')[-1]
            uid = 'SKULLMASK_{0}_{1}_{2}_{3}'.format(study, rid, t1sid, t1iid)
            path = '{0}/{1}.mnc'.format(outputpath, uid)

            print(study, rid, uid, sep=', ')

            try:
                shutil.copyfile(row[0], path)
                Dbclient.executeNoResult("INSERT IGNORE INTO MANUAL_MASK VALUES (Null, '{0}', '{1}', '{2}', '{3}')".format(study, rid, uid, path))

                sql2 = "UPDATE ADNI_T1_Pipeline SET MANUAL_MASK = 1 WHERE PROCESSING_TID IN (SELECT RECORD_ID FROM Processing WHERE RID = {0} AND S_IDENTIFIER = {1} AND I_IDENTIFIER = {2})".format(rid, t1sid, t1iid)
            except Exception as e:
                print('Error copy. {0}'.format(e))


