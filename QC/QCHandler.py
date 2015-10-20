__author__ = 'Sulantha'
from Utils.DbUtils import DbUtils

class QCHandler:
    def __init__(self):
        self.DBClient = DbUtils()

    def requestQC(self, study, modal_table, modal_tableId, qcField, qctype, qcFolder):
        qcsql = "INSERT IGNORE INTO QC VALUES (Null, '{0}', '{1}', '{2}', '{3}', '{4}','{5}' , 0, 0, 0, 0, Null)".format(study.upper(), modal_table,
                                                                                                                         modal_tableId,
                                                                                                                         qcField,
                                                                                                                         qctype, qcFolder)

        self.DBClient.executeNoResult(qcsql)

    def checkQCJobs(self, study, modality):
        sql = "SELECT * FROM {0}_{1}_Pipeline WHERE QC = 1 AND FINISHED = 1".format(study, modality)
        res = self.DBClient.executeAllResults(sql)
        if len(res) < 1:
            return 0
        else:
            for result in res:
                proc_id = result[1]
                setProcessedSQL = "UPDATE Processing SET PROCESSED = 1, QCPASSED = 1 WHERE RECORD_ID = {0}".format(proc_id)
                self.DBClient.executeNoResult(setProcessedSQL)

