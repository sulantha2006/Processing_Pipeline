__author__ = 'sulantha'
import datetime
from Utils.DbUtils import DbUtils
csvFile = '/data/data03/sulantha/Downloads/av45_list.csv'
MatchDBClient = DbUtils(database='Study_Data.ADNI')
with open(csvFile, 'r') as csv:
    next(csv)
    for line in csv:
        row = line.split(',')
        rid = row[0].strip()
        date = row[1].strip()
        dateT = datetime.datetime.strptime(date, '%m/%d/%Y')
        dateS = dateT.strftime('%Y-%m-%d')
        sql = "SELECT DISTINCT subject, visit FROM PET_META_LIST WHERE subject like '%_%_{0}' and scandate = '{1}' and origproc = 'Original'".format(rid, dateS)
        result = MatchDBClient.executeAllResults(sql)
        if len(result) == 0:
            print('No valid visit for {0} - {1}'.format(rid, dateS))
        else:
            print(result)


