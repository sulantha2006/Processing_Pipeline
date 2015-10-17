__author__ = 'Sulantha'
from Utils.DbUtils import DbUtils

class QCHandler:
    def __init__(self):
        self.DBClient = DbUtils()

    def requestQC(self, study, modal_table, modal_tableId, qcField, qctype, qcFolder):
        qcsql = "INSERT IGNORE INTO QC VALUES (Null, '{0}', '{1}', '{2}', '{3}', '{4}','{5}' , 0, 0, 0, 0, Null)".format(study, modal_table,
                                                                                                                         modal_tableId,
                                                                                                                         qcField,
                                                                                                                         qctype, qcFolder)

        self.DBClient.executeNoResult(qcsql)
