__author__ = 'sulantha'
import glob, subprocess, re
from Utils.DbUtils import DbUtils
import os
from distutils import file_util, dir_util
import shutil

DBClient = DbUtils()
IID_list = ['45WL3UA1MPRAGEv0020111115xDICOM']
for iid in IID_list:
    getDataFolderSQL = "SELECT RAW_FOLDER FROM Sorting WHERE I_IDENTIFIER = '{0}'".format(iid)
    res = DBClient.executeAllResults(getDataFolderSQL)
    if len(res) == 0:
        pass
    else:
        rawFolder = res[0][0]
        dataFolder = os.path.abspath(os.path.join(rawFolder, '../'))
        shutil.rmtree(dataFolder)
        print(dataFolder)
    delsql = "DELETE FROM Sorting WHERE I_IDENTIFIER = '{0}'".format(iid)
    DBClient.executeNoResult(delsql)

    delsql = "DELETE FROM Conversion WHERE I_IDENTIFIER = '{0}'".format(iid)
    DBClient.executeNoResult(delsql)

    getProSQL = "SELECT RECORD_ID, STUDY, MODALITY FROM Processing WHERE I_IDENTIFIER = '{0}'".format(iid)
    res2 = DBClient.executeAllResults(getProSQL)
    if len(res2) == 0:
       pass
    else:
        P_ID = res2[0][0]
        study = res2[0][1]
        mod = res2[0][2]
        print(P_ID)
        getPPSQL = "SELECT RECORD_ID FROM {1}_{2}_Pipeline WHERE PROCESSING_TID = '{0}'".format(P_ID, study, mod)
        res3 = DBClient.executeAllResults(getPPSQL)
        if len(res3) == 0:
            pass
        else:
            mt_ID = res3[0][0]
            print(mt_ID)
            delsql = "DELETE FROM {1}_{2}_Pipeline WHERE PROCESSING_TID = '{0}'".format(P_ID, study, mod)
            DBClient.executeNoResult(delsql)
            delsql = "DELETE FROM QC WHERE MODAL_TABLE = '{0}_{1}_Pipeline' AND MODAL_TABLE_ID = {2}".format(study, mod, mt_ID)
            DBClient.executeNoResult(delsql)


    delsql = "DELETE FROM Processing WHERE I_IDENTIFIER = '{0}'".format(iid)
    DBClient.executeNoResult(delsql)

    delsql = "DELETE FROM Coregistration WHERE XFM_NAME LIKE '%{0}%'".format(iid)
    DBClient.executeNoResult(delsql)

    delsql = "DELETE FROM externalWaitingJobs WHERE JOB_ID LIKE '%{0}%'".format(iid)
    DBClient.executeNoResult(delsql)

    delsql = "DELETE FROM MANUAL_MASK WHERE MASK_UNIQUEID LIKE '%{0}%'".format(iid)
    DBClient.executeNoResult(delsql)

    delsql = "DELETE FROM MANUAL_XFM WHERE XFM_UNIQUEID LIKE '%{0}%'".format(iid)
    DBClient.executeNoResult(delsql)

    delsql = "DELETE FROM MatchT1 WHERE MODALITY_ID LIKE '%{0}%'".format(iid)
    DBClient.executeNoResult(delsql)

    delsql = "DELETE FROM MatchT1 WHERE T1_ID LIKE '%{0}%'".format(iid)
    DBClient.executeNoResult(delsql)