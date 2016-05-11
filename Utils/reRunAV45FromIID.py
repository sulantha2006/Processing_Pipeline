import csv
from Utils.DbUtils import DbUtils
inputFile = '/home/sulantha/reRUNAv45.csv'
DBC = DbUtils()
with open(inputFile, 'r') as inputFile:
    csvFile = csv.reader(inputFile)
    for line in csvFile:
        RID = line[0].split('/')[6]
        IID = line[0].split('/')[7].split('_')[-1]
        sql = "UPDATE ADNI_AV45_Pipeline SET FINISHED = 0, SKIP = 0 WHERE PROCESSING_TID IN (SELECT RECORD_ID FROM Processing WHERE RID = {0} AND I_IDENTIFIER = '{1}')".format(RID, IID)
        DBC.executeNoResult(sql)
