__author__ = 'sulantha'
xfmList = '/home/sulantha/Desktop/petMatch.csv'
outputpath = '/data/data03/MANUAL_XFM'
from Utils.DbUtils import DbUtils
import shutil


Dbclient = DbUtils()
with open(xfmList, 'r') as inf:
    for line in inf:
        row = line.split(',')
        if row[0].strip() == 'None' or row[2].strip() == 'None' or row[4].strip() == 'None':
            pass
        else:
            study = row[0].split('/')[-1].split('_')[0].upper()
            rid = row[0].split('/')[-1].split('_')[1][2:-2]
            petsid = row[2].split('.')[0].split('_')[-2]
            petiid = row[2].split('.')[0].split('_')[-1]
            t1sid = row[4].split('.')[0].split('_')[-2]
            t1iid = row[4].split('.')[0].split('_')[-1]
            uid = 'PET_{0}_{1}_T1_{2}_{3}'.format(petsid, petiid, t1sid, t1iid)
            path = '{0}/{1}_{2}_{3}.xfm'.format(outputpath, study, rid, uid)

            print(study, rid, uid, sep=', ')

            try:
                shutil.copyfile(row[0], path)
            except Exception as e:
                print('Error copy. {0}'.format(e))

            Dbclient.executeNoResult("INSERT IGNORE INTO MANUAL_XFM VALUES (Null, '{0}', '{1}', '{2}', '{3}')".format(study, rid, uid, path))
