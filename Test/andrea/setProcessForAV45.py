__author__ = 'sulantha'
import datetime
from Utils.DbUtils import DbUtils
DBClient = DbUtils()
with open('/data/data03/sulantha/Downloads/av45_list.csv', 'r') as file:
    next(file)
    for line in file:
        row = line.split(',')
        rid = row[0]
        date = row[1].strip()
        dateT = datetime.datetime.strptime(date, '%m/%d/%Y')
        dateS = dateT.strftime('%Y-%m-%d')
        findSQL = "SELECT * FROM Processing WHERE RID = {0} AND MODALITY = 'AV45' AND SCAN_DATE = '{1}'".format(rid, dateS)
        res = DBClient.executeAllResults(findSQL)
        print('{0}-{1} {2}'.format(rid, len(res), '############' if len(res) is 0 else '')) if len(res) is 0 else None
        processingSQL = "UPDATE Processing SET SKIP = 0 WHERE RID = {0} AND MODALITY = 'AV45' AND SCAN_DATE = '{1}'".format(rid, dateS)
        DBClient.executeNoResult(processingSQL)



