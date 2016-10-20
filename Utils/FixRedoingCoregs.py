__author__ = 'sulantha'
import glob, subprocess, re
from Utils.DbUtils import DbUtils
import os
from distutils import file_util, dir_util
import shutil

DBClient = DbUtils()

getAllTodoSQL = "SELECT XFM_NAME FROM Coregistration WHERE END = 0 AND SKIP = 0 AND START = 0 AND PET_SCANTYPE = 'AV45'"
res = DBClient.executeAllResults(getAllTodoSQL)
totalC = 0
done_c = 0
for xfm_name in res:
    xfm_id = xfm_name[0].split('_', 3)[-1]
    print(xfm_id)

    xfm_file = glob.glob('/data/data03/MANUAL_XFM/{0}.xfm'.format(xfm_name[0]))
    #checkSQL = "SELECT * FROM MANUAL_XFM WHERE XFM_UNIQUEID = '{0}'".format(xfm_id)
    #res2 = DBClient.executeAllResults(checkSQL)

    if len(xfm_file)>0:
        done_c +=1
        print('Already done.  - {0}'.format(xfm_id))
        markDoneSQL = "UPDATE Coregistration SET START=1, END=1, USER='admin' WHERE XFM_NAME LIKE '%{0}'".format(xfm_id)
        print(markDoneSQL)
        #DBClient.executeNoResult(markDoneSQL)
    else:
        print('Not done.  - {0}'.format(xfm_id))
    totalC +=1

    tag_file = '/data/data03/MANUAL_TAG/{0}.tag'.format(xfm_name[0])
    try:
        os.remove(tag_file)
    except OSError:
        pass


print('Total - {0}'.format(totalC))
print('Done - {0}'.format(done_c))