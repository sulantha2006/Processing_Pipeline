__author__ = 'sulantha'
from Utils.DbUtils import DbUtils
CSVFile = '/data/data03/sulantha/Downloads/missing_list_preprocessed.csv'
dbc = DbUtils()
with open(CSVFile, 'rU') as csv_file:
    for line in csv_file:
        lin = line.strip()

        rid = lin.split('/')[6]
        print(rid)
        s_id = lin.split('/')[7].split('_')[-2]
        i_id = lin.split('/')[7].split('_')[-1]
        sql = "UPDATE ADNI_AV45_Pipeline SET SKIP = 0, QC = 0, FINISHED = 0, PROC_Failed = NULL, MANUAL_XFM = 'Req_man_reg' WHERE PROCESSING_TID IN (SELECT RECORD_ID FROM Processing WHERE RID = '{0}' AND MODALITY = 'AV45' AND VERSION = 'V2' AND S_IDENTIFIER = '{1}' )".format(rid, s_id)
        dbc.executeNoResult(sql)
