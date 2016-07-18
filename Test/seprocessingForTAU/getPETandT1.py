from datetime import datetime
from Utils.DbUtils import DbUtils
import glob, itertools

DBClient = DbUtils()
outLines = []
date_col = 10
type= 'AV45'
with open('/home/sulantha/Downloads/2016_July12_Tau_AV45_FDG.csv', 'r') as file:
    next(file)
    for line in file:
        row = line.split(',')
        rid = row[0].split('_')[-1]
        date = row[date_col].strip()
        dateT = datetime.strptime(date, '%m/%d/%Y')
        dateS = dateT.strftime('%Y-%m-%d')
        findSQLV2 = "SELECT CONVERTED_FOLDER FROM Processing WHERE RID = {0} AND MODALITY = '{3}' AND SCAN_DATE = '{1}' AND VERSION = '{2}' LIMIT 1".format(
            rid, dateS, 'V2', type.upper())
        resv2 = DBClient.executeSomeResults(findSQLV2, 1)

        if len(resv2) is 0:
            print(rid)
            v2Path = ''
        elif len(resv2) == 1:
            v2Path = '{0}/*_{1}.mnc'.format(resv2[0][0], type.upper())
            v2Path = glob.glob(v2Path)[0]

        findanyT1 = "SELECT ROOT_FOLDER FROM Processing WHERE RID = {0} AND MODALITY = '{1}' AND PROCESSED = 1 AND QCPASSED = 1 ORDER BY SCAN_DATE DESC LIMIT 1".format(
            rid, 'T1')
        t1 = DBClient.executeSomeResults(findanyT1, 1)
        if len(t1) is 0:
            t1_path = ''
        elif len(t1) == 1:
            t1_path = '{0}/civet'.format(t1[0][0])

        findanyT1 = "SELECT * FROM Processing WHERE RID = {0} AND MODALITY = '{1}' AND PROCESSED = 1 AND QCPASSED = 1".format(
            rid, 'T1')
        t1 = DBClient.executeAllResults(findanyT1)
        if len(t1) > 0:
            sortedRecs = sorted(t1,
                                key=lambda x: abs(datetime.strptime(x[4].strftime('%Y-%m-%d'), '%Y-%m-%d') - dateT))
            closestDate = [k for k, g in itertools.groupby(sortedRecs, key=lambda x: abs(
                datetime.strptime(x[4].strftime('%Y-%m-%d'), '%Y-%m-%d') - dateT))][0]
            closestMatchedRecs = [list(g) for k, g in itertools.groupby(sortedRecs, key=lambda x: abs(
                datetime.strptime(x[4].strftime('%Y-%m-%d'), '%Y-%m-%d') - dateT))][0]
            closestFD = closestMatchedRecs[0][8]
        else: closestFD = ''

        outLine = [v2Path, closestFD]
        outLines.append(outLine)

thefile = open('/data/data02/sulantha/TAU_AV45_FDG_12/AV45.csv', 'w')
for item in outLines:
    thefile.write("%s\n" % item)
