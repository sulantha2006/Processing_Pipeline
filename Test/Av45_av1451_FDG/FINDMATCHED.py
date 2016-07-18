from datetime import datetime
from Utils.DbUtils import DbUtils
import glob
import itertools

DBClient = DbUtils()
outLines = []
with open('/home/sulantha/Downloads/Av1451_V2.csv', 'r') as file:
    next(file)
    for line in file:
        row = line.split(',')
        rid = row[2]
        date = row[4].strip()
        dateT = datetime.strptime(date, '%Y-%m-%d')
        dateS = dateT.strftime('%Y-%m-%d')
        closestAV= ['']*20
        closestFD = ['']*20
        findAV45 = "SELECT * FROM Processing WHERE RID = {0} AND MODALITY = 'AV45' AND PROCESSED = 1 AND QCPASSED = 1 AND VERSION = 'V2'".format(
            rid)
        resvav45 = DBClient.executeAllResults(findAV45)
        if len(resvav45) > 0:
            sortedRecs = sorted(resvav45,
                                key=lambda x: abs(datetime.strptime(x[4].strftime('%Y-%m-%d'), '%Y-%m-%d') - dateT))
            closestDate = [k for k, g in itertools.groupby(sortedRecs, key=lambda x: abs(
                datetime.strptime(x[4].strftime('%Y-%m-%d'), '%Y-%m-%d') - dateT))][0]
            closestMatchedRecs = [list(g) for k, g in itertools.groupby(sortedRecs, key=lambda x: abs(
                datetime.strptime(x[4].strftime('%Y-%m-%d'), '%Y-%m-%d') - dateT))][0]
            closestAV = closestMatchedRecs[0]
        findFDG = "SELECT * FROM Processing WHERE RID = {0} AND MODALITY = 'FDG' AND PROCESSED = 1 AND QCPASSED = 1 AND VERSION = 'V2'".format(
            rid)
        resvFDG = DBClient.executeAllResults(findFDG)
        if len(resvFDG) > 0:
            sortedRecs = sorted(resvFDG,
                                key=lambda x: abs(datetime.strptime(x[4].strftime('%Y-%m-%d'), '%Y-%m-%d') - dateT))
            closestDate = [k for k, g in itertools.groupby(sortedRecs, key=lambda x: abs(
                datetime.strptime(x[4].strftime('%Y-%m-%d'), '%Y-%m-%d') - dateT))][0]
            closestMatchedRecs = [list(g) for k, g in itertools.groupby(sortedRecs, key=lambda x: abs(
                datetime.strptime(x[4].strftime('%Y-%m-%d'), '%Y-%m-%d') - dateT))][0]
            closestFD = closestMatchedRecs[0]
        try:
            print('{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}'.format(rid, 'AV1451', row[4], row[8], 'AV45', closestAV[4].strftime('%Y-%m-%d'), closestAV[8], 'FDG', closestFD[4].strftime('%Y-%m-%d'), closestFD[8]))
        except:
            pass