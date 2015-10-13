__author__ = 'sulantha'
import datetime
from Utils.DbUtils import DbUtils
csvFile = '/data/data03/sulantha/Downloads/av45_list.csv'
MatchDBClient = DbUtils(database='Study_Data.ADNI')
DBClient = DbUtils()
with open(csvFile, 'r') as csv:
    next(csv)
    for line in csv:
        row = line.split(',')
        rid = row[0].strip()
        date = row[1].strip()
        dateT = datetime.datetime.strptime(date, '%m/%d/%Y')
        #dateT = datetime.datetime.strptime(date, '%Y-%m-%d')
        dateS = dateT.strftime('%Y-%m-%d')
        sql = "SELECT DISTINCT subject, visit, seriesid, imageid FROM PET_META_LIST WHERE subject like '%_%_{0}' and scandate = '{1}' and origproc = 'Original'".format(rid, dateS)
        result = MatchDBClient.executeAllResults(sql)
        checkDBSQL = "SELECT * FROM Conversion WHERE RID = '{0}' AND S_IDENTIFIER = '{1}' AND I_IDENTIFIER = '{2}'".format(rid, 'S{0}'.format(result[0][2]), 'I{0}'.format(result[0][3]))
        #print(checkDBSQL)
        resultN = DBClient.executeAllResults(checkDBSQL)
        if len(resultN) == 0:
            print('########################### Not in DB - {0} - {1}'.format(rid, date))
        else:
            pass





