__author__ = 'sulantha'
from Utils.DbUtils import DbUtils
DBClient = DbUtils()
RIDList = ['4225','4746','4799','4136','4142','4192','4713','4960','4387','0021','4827','4579','4580','4616','4668','4696','4809','4549','4680','5012','5019','4674','4757','4385','4721','4947','4714','4715','4736','4706','4720','4661','4728','4767','4739','4089','4379','0382','4732','0230','4586','4653','4671','4742','4369','4589','4730','4676','4689','4722','4723','4587','4631','4632','4672','4678','4756','4711','4764']

for rid in RIDList:
    sql1 = "DELETE FROM Sorting WHERE RID = {0} AND SCAN_TYPE NOT IN ('AV45', 'FDG')".format(rid)
    DBClient.executeNoResult(sql1)
    sql2 = "DELETE FROM Conversion WHERE RID = {0} AND SCAN_TYPE NOT IN ('AV45', 'FDG')".format(rid)
    DBClient.executeNoResult(sql2)
    sql3 = "SELECT RECORD_ID FROM Processing WHERE RID = {0} AND MODALITY NOT IN ('AV45', 'FDG')".format(rid)
    recs = DBClient.executeAllResults(sql3)
    for rec in recs:
        sql4 = "DELETE FROM ADNI_T1_Pipeline WHERE PROCESSING_TID = {0}".format(rec[0])
        DBClient.executeNoResult(sql4)
    sql5 = "DELETE FROM Processing WHERE RID = {0} AND MODALITY NOT IN ('AV45', 'FDG')".format(rid)
    DBClient.executeNoResult(sql5)
