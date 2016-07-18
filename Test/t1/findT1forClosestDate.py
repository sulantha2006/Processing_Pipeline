from datetime import datetime
from Utils.DbUtils import DbUtils
import glob
import itertools

DBClient = DbUtils()
outLines = []
with open('/home/sulantha/GETCLOSET1.csv', 'r') as file:
    next(file)
    for line in file:
        row = line.split(',')
        rid = row[0]
        date = row[1].strip()
        dateT = datetime.strptime(date, '%Y-%m-%d')
        dateS = dateT.strftime('%Y-%m-%d')
        findSQLV1 = "SELECT * FROM Processing WHERE RID = {0} AND MODALITY = 'T1' AND PROCESSED = 1 AND QCPASSED = 1".format(rid, dateS, 'V1')
        resv1 = DBClient.executeAllResults(findSQLV1)
        if len(resv1) > 0:
            sortedRecs = sorted(resv1, key=lambda x: abs(datetime.strptime(x[4].strftime('%Y-%m-%d'), '%Y-%m-%d') - dateT))
            closestDate = [k for k, g in itertools.groupby(sortedRecs, key=lambda x: abs(
                datetime.strptime(x[4].strftime('%Y-%m-%d'), '%Y-%m-%d') - dateT))][0]
            closestMatchedRecs = [list(g) for k, g in itertools.groupby(sortedRecs, key=lambda x: abs(
                datetime.strptime(x[4].strftime('%Y-%m-%d'), '%Y-%m-%d') - dateT))][0]
            t1 = glob.glob('{0}/civet/final/*_t1_final.mnc'.format(closestMatchedRecs[0][8]))
            volumes = glob.glob('{0}/civet/classify/*.dat'.format(closestMatchedRecs[0][8]))
            if t1 and volumes:
                f = open(volumes[0],'r').read().splitlines()
                v=[i.split()[1] for i in f]
                print('{0}, {1}, {2}, {3}, {4}'.format(t1[0], closestDate.days, v[0], v[1], v[2]))
            else:
                print('')
        else:
            print('')