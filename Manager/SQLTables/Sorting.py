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
        valuesDict = dict(study=tuple[0], rid=tuple[1], scan_type=tuple[2],
                          scan_date=tuple[3].strftime("%Y-%m-%d"), scan_time=str(tuple[4]),
                          s_identifier=tuple[5], i_identifier=tuple[6], file_type=tuple[7], download_folder=tuple[8],
                          raw_folder=tuple[9], moved=tuple[10])
        return SortingObject(valuesDict)

    def insertToTable(self, objList):
        for obj in objList:
            self.DBClient.executeNoResult(
                self.sqlBuilder.getSQL_AddNewEntryToSortingTable(obj.sqlInsert()))

    def getUnmovedFilesPerStudy(self, study):
        unmovedList = self.DBClient.executeAllResults(
            self.sqlBuilder.getSQL_getUnmovedFilesFromSortingTable(study, sc.ProcessingImagingModalities[study]))
        return [self.getObjectFromTuple(t) for t in unmovedList]

    def setMovedTrue(self, sortingObj):
        pass
