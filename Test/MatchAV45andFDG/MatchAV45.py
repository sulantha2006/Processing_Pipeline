from datetime import datetime
import sys
sys.path.append('/home/sulantha/PycharmProjects/Processing_Pipeline')
from Utils.DbUtils import DbUtils
import glob
import itertools
import argparse
parser = argparse.ArgumentParser(description='Match FDG to AV45.  ')
parser.add_argument('--csv', nargs=1, required=True,
                    help='CSV file with FDG files. and details. Column headers required. Column 1 - RID, Column 2 - FDG File, Column 3 - Date')
args = parser.parse_args()
csv_file = args.csv[0]

DBClient = DbUtils()
outLines = []

with open(csv_file, 'r') as file:
    next(file)
    for line in file:
        row = line.split(',')
        rid = row[0]
        date = row[2].strip()
        dateT = datetime.strptime(date, '%Y-%m-%d')
        dateS = dateT.strftime('%Y-%m-%d')
        closestAV= ['']*20

        findAV45 = "SELECT * FROM Processing WHERE RID = {0} AND MODALITY = 'AV45' AND PROCESSED = 1 AND QCPASSED = 1 AND VERSION = 'V2'".format(
            rid)
        resvav45 = DBClient.executeAllResults(findAV45)
        closestDate = ''
        noMatch = 0
        if len(resvav45) > 0:
            noMatch = 1
            sortedRecs = sorted(resvav45,
                                key=lambda x: abs(datetime.strptime(x[4].strftime('%Y-%m-%d'), '%Y-%m-%d') - dateT))
            closestDate = [k for k, g in itertools.groupby(sortedRecs, key=lambda x: abs(
                datetime.strptime(x[4].strftime('%Y-%m-%d'), '%Y-%m-%d') - dateT))][0]
            closestMatchedRecs = [list(g) for k, g in itertools.groupby(sortedRecs, key=lambda x: abs(
                datetime.strptime(x[4].strftime('%Y-%m-%d'), '%Y-%m-%d') - dateT))][0]
            closestAV = closestMatchedRecs[0]
        if noMatch:
            print('{0},{1},{2},{3},{4},{5},{6},{7}'.format(rid, 'FDG', row[1], dateS, 'AV45',  closestAV[8],closestAV[4].strftime('%Y-%m-%d'), closestDate.days))
        else:
            print(',,,,,,,')