__author__ = 'sulantha'
from Utils.DbUtils import DbUtils
from Manager.SQL.SQLBuilder import SQLBuilder
from Manager.SQLTables.ProcessingObject import ProcessingObject

from Config import StudyConfig as sc

class Processing:
    def __init__(self):
        self.DBClient = DbUtils()
        self.sqlBuilder = SQLBuilder()

    def getObjectFromTuple(self, tuple):
        valuesDict = dict(record_id=tuple[0], study=tuple[1], rid=tuple[2], modality=tuple[3],
                          scan_date=tuple[4].strftime("%Y-%m-%d"), scan_time=str(tuple[5]),
                          s_identifier=tuple[6], i_identifier=tuple[7], root_folder=tuple[8], converted_folder=tuple[9], version=tuple[10],
                          processed=tuple[12])
        return ProcessingObject(valuesDict)

    def insertToTable(self, objList):
        for obj in objList:
            self.DBClient.executeNoResult(
                self.sqlBuilder.getSQL_AddNewEntryToProcessingTable(obj.sqlInsert()))

    def insertFromConvertionObj(self, convertionObj):
        convertionValues = convertionObj.getValuesDict()
        convertionValues['modality'] = sc.ProcessingModalityAndPipelineTypePerStudy[convertionObj.study][convertionObj.scan_type]
        convertionValues['root_folder'] = '/'.join(convertionObj.converted_folder.split('/')[0:-2])
        self.insertToTable([ProcessingObject(convertionValues)])

    def getToProcessListPerStudy(self, study):
        toProcessList = self.DBClient.executeAllResults(
            self.sqlBuilder.getSQL_getToBeProcessedFromProcessingTable(study))
        return [self.getObjectFromTuple(t) for t in toProcessList]
