__author__ = 'sulantha'
import os

from Utils.DbUtils import DbUtils
import glob

DBClient = DbUtils()
outLines = []
count = 0
with open('/data/data02/sulantha/VBM_FDG/FDG_FULLPAT', 'r') as file:
    for line in file:

        row = line.split('/')
        rid = row[6]
        dirname = os.path.dirname(line)
        native_t1 = glob.glob('{0}/../t1/*t1.mnc'.format(dirname))[0]
        t1_base = os.path.basename(native_t1)
        t1_sid = t1_base.split('S')[1].split('I')[0]
        t1_iid = t1_base.split('S')[1].split('I')[1].split('_')[0]

        findSQLV2 = "SELECT ROOT_FOLDER FROM Processing WHERE RID = {0} AND MODALITY = 'T1' AND S_IDENTIFIER = 'S{1}' AND I_IDENTIFIER = 'I{2}' ".format(
            rid, t1_sid, t1_iid)
        resv2 = DBClient.executeAllResults(findSQLV2)

        if len(resv2) > 0:
            outLines.append(resv2[0])
        else:
            outLines.append('')
        count += 1
print('Writing...')
thefile = open('/data/data02/sulantha/VBM_FDG/FDG_FULLPAT_T1_Civet', 'w')
for item in outLines:
    thefile.write("%s\n" % item)