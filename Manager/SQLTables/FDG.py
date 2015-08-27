__author__ = 'sulantha'
from Utils.DbUtils import DBUtils
from Manager.SQL.SQLBuilder import SQLBuilder
from Manager.SQLTables.T1Object import T1Object

class FDG:
    def __init__(self):
        self.tableName = 'FDG'
        self.DBClient = DBUtils()
        self.sqlBuilder = SQLBuilder()

    def insertToTable(self, objList):
        for obj in objList:
            self.DBClient.executeNoResult(
                self.sqlBuilder.getSQL_AddNewEntryToModalTable(obj.sqlInsert(), self.tableName))

    def insertFromConvertionObj(self, convertionObj):
        convertionValues = convertionObj.getValuesDict()
        self.insertToTable([T1Object(convertionValues)])