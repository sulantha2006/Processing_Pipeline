__author__ = 'sulantha'
import datetime
from Utils.DbUtils import DbUtils
import glob
DBClient = DbUtils()
outLines = []
with open('/data/data03/sulantha/Downloads/fdg_list.csv', 'r') as file:
    next(file)
    for line in file:
        row = line.split(',')
        rid = row[0]
        date = row[1].strip()
        dateT = datetime.datetime.strptime(date, '%Y-%m-%d')
        dateS = dateT.strftime('%Y-%m-%d')
        findSQLV1 = "SELECT * FROM Processing WHERE RID = {0} AND MODALITY = 'FDG' AND SCAN_DATE = '{1}' AND VERSION = '{2}'".format(rid, dateS, 'V1')
        resv1 = DBClient.executeAllResults(findSQLV1)
        findSQLV2 = "SELECT * FROM Processing WHERE RID = {0} AND MODALITY = 'FDG' AND SCAN_DATE = '{1}' AND VERSION = '{2}'".format(rid, dateS, 'V2')
        resv2 = DBClient.executeAllResults(findSQLV2)

        if len(resv1) is 0:
            v1Path = ''
        elif len(resv1) == 1:
            if resv1[0][12] == 1:
                v1Path = '{0}/processed/final/*tal_nlin_pbavg_ref_pons.mnc'.format(resv1[0][8])
                v1Path = glob.glob(v1Path)[0]
            else:
                v1Path = ''
        else:
            v1Path = ''
            for result in resv1:
                if result[12] == 1:
                    v1Path_t = '{0}/processed/final/*tal_nlin_pbavg_ref_pons.mnc'.format(result[8])
                    v1Path_t = glob.glob(v1Path_t)[0]
                    v1Path = v1Path.join(v1Path_t)

        if len(resv2) is 0:
            v2Path = ''
        elif len(resv2) == 1:
            if resv2[0][12] == 1:
                v2Path = '{0}/processed/final/*tal_nlin_pbavg_ref_pons.mnc'.format(resv2[0][8])
                v2Path = glob.glob(v2Path)[0]
            else:
                v2Path = ''
        else:
            v2Path = ''
            for result in resv2:
                if result[12] == 1:
                    v2Path_t = '{0}/processed/final/*tal_nlin_pbavg_ref_pons.mnc'.format(result[8])
                    v2Path_t = glob.glob(v2Path_t)[0]
                    if v2Path != '':
                        v2Path = v2Path.join(';')
                    v2Path = v2Path.join(v2Path_t)

        outLine = [rid, dateS, v1Path, v2Path]
        outLines.append(outLine)

thefile = open('/data/data03/sulantha/Downloads/fdg_list_newProcessed.csv', 'w')
for item in outLines:
  thefile.write("%s\n" % item)


