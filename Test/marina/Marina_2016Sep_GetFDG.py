__author__ = 'sulantha'
from datetime import datetime
import itertools
    
from Utils.DbUtils import DbUtils
import glob
DBClient = DbUtils()
outLines = []
count = 0
with open('/data/data02/sulantha/Marina_Sep_2016/Marina_2016Sep_Full_SQL_CSV_Bef_FDG_Scans.csv', 'r') as file:
    next(file)
    for line in file:
        print(count)
        row = line.split(',')
        rid = row[0]
        fdgdate = row[15].strip()
        dateT = datetime.strptime(fdgdate, '%Y-%m-%d')
        dateS = dateT.strftime('%Y-%m-%d')

        findSQLV2 = "SELECT * FROM Processing WHERE RID = {0} AND MODALITY = 'FDG' AND VERSION = '{2}' AND PROCESSED = 1 AND QCPASSED = 1".format(
            rid, dateS, 'V2')
        resv2 = DBClient.executeAllResults(findSQLV2)
        date_diff = ''
        closestFD = ''
        if len(resv2) > 0:
            sortedRecs = sorted(resv2,
                                key=lambda x: abs(datetime.strptime(x[4].strftime('%Y-%m-%d'), '%Y-%m-%d') - dateT))
            closestDate = [k for k, g in itertools.groupby(sortedRecs, key=lambda x: abs(
                datetime.strptime(x[4].strftime('%Y-%m-%d'), '%Y-%m-%d') - dateT))][0]
            closestMatchedRecs = [list(g) for k, g in itertools.groupby(sortedRecs, key=lambda x: abs(
                datetime.strptime(x[4].strftime('%Y-%m-%d'), '%Y-%m-%d') - dateT))][0]
            closestFD = closestMatchedRecs[0]
            date_diff = closestFD[4] - dateT.date()
        if date_diff == '':
            outLines.append([rid, '', ''])
        else:
            outLines.append([rid, abs(date_diff.days), closestFD[8]])
        count +=1
print('Writing...')
thefile = open('/data/data02/sulantha/Marina_Sep_2016/Marina_2016Sep_Full_SQL_CSV_FDG_Scans_2.csv', 'w')
for item in outLines:
  thefile.write("%s\n" % item)