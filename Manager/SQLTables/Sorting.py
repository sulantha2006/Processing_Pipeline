__author__ = 'sulantha'
from Utils.DbUtils import DBUtils
from Manager.SQL.SQLBuilder import SQLBuilder
from Config import StudyConfig as sc
from Manager.SQLTables.SortingObject import SortingObject

class Sorting:
    def __init__(self):
        self.tableName = 'Sorting'
        self.DBClient = DBUtils()
        self.sqlBuilder = SQLBuilder()

    def getObjectFromTuple(self, tuple):
        valuesDict = dict(record_id=tuple[0], study=tuple[1], rid=tuple[2], scan_type=tuple[3],
                          scan_date=tuple[4].strftime("%Y-%m-%d"), scan_time=str(tuple[5]),
                          s_identifier=tuple[6], i_identifier=tuple[7], file_type=tuple[8], download_folder=tuple[9],
                          raw_folder=tuple[10], moved=tuple[11])
        return SortingObject(valuesDict)

    def insertToTable(self, objList):
        for obj in objList:
            self.DBClient.executeNoResult(
                self.sqlBuilder.getSQL_AddNewEntryToSortingTable(obj.sqlInsert()))

    def getUnmovedFilesPerStudy(self, study):
        unmovedList = self.DBClient.executeAllResults(
            self.sqlBuilder.getSQL_getUnmovedFilesFromSortingTable(study, tuple(sc.ProcessingModalityAndPipelineTypePerStudy[study].keys())))
        return [self.getObjectFromTuple(t) for t in unmovedList]

    def setMovedTrue(self, sortingObj):
        sortingObj.moved = 1
        self.saveObj(sortingObj)

    def saveObj(self, sortingObj):
        self.DBClient.executeNoResult(self.sqlBuilder.getSQL_saveObjSortingTable(sortingObj))

