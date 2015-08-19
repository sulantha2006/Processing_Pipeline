__author__ = 'sulantha'

class SQLBuilder:
    def __init__(self):
        pass

    def getSQL_AddNewEntryToSortingTable(self, values):
        return "INSERT IGNORE INTO Sorting VALUES ({0}) ".format(values)

    def getSQL_getUnmovedFilesFromSortingTable(self, studyID, allowedScanTypes):
        return "SELECT * FROM Sorting WHERE STUDY='{0}' AND SCAN_TYPE IN {1} AND MOVED=0".format(studyID.upper(), str(allowedScanTypes))

    def getSQL_AddNewEntryToConversionTable(self, values):
        return "INSERT IGNORE INTO Conversion VALUES ({0}) ".format(values)