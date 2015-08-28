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

    def getSQL_saveObjSortingTable(self, sortingObj):
        return "UPDATE Sorting SET STUDY='{0}', RID='{1}', SCAN_TYPE='{2}', SCAN_DATE='{3}', SCAN_TIME='{4}', " \
               "S_IDENTIFIER='{5}', I_IDENTIFIER='{6}', FILE_TYPE='{7}', DOWNLOAD_FOLDER='{8}', RAW_FOLDER='{9}', " \
               "MOVED={10} WHERE RECORD_ID={11}".format(sortingObj.study, sortingObj.rid, sortingObj.scan_type,
                                                          sortingObj.scan_date, sortingObj.scan_time,
                                                          sortingObj.s_identifier, sortingObj.i_identifier,
                                                          sortingObj.file_type, sortingObj.download_folder,
                                                          sortingObj.raw_folder, sortingObj.moved,
                                                          sortingObj.record_id)

    def getSQL_saveObjConversionTable(self, conversionObj):
        return "UPDATE Conversion SET STUDY='{0}', RID='{1}', SCAN_TYPE='{2}', SCAN_DATE='{3}', SCAN_TIME='{4}', " \
               "S_IDENTIFIER='{5}', I_IDENTIFIER='{6}', FILE_TYPE='{7}', RAW_FOLDER='{8}', CONVERTED_FOLDER='{9}', " \
               "VERSION='{10}', CONVERTED={11} WHERE RECORD_ID={12}".format(conversionObj.study, conversionObj.rid,
                                                                              conversionObj.scan_type,
                                                                              conversionObj.scan_date,
                                                                              conversionObj.scan_time,
                                                                              conversionObj.s_identifier,
                                                                              conversionObj.i_identifier,
                                                                              conversionObj.file_type,
                                                                              conversionObj.raw_folder,
                                                                              conversionObj.converted_folder,
                                                                              conversionObj.version,
                                                                              conversionObj.converted,
                                                                              conversionObj.record_id)

    def getSQL_getRecordIDFromSorting(self, sortingObj):
        return "SELECT RECORD_ID FROM Sorting WHERE STUDY='{0}', RID='{1}', SCAN_TYPE='{2}', SCAN_DATE='{3}', SCAN_TIME='{4}', " \
               "S_IDENTIFIER='{5}', I_IDENTIFIER='{6}', FILE_TYPE='{7}', DOWNLOAD_FOLDER='{8}', RAW_FOLDER='{9}', " \
               "MOVED={10}".format(sortingObj.study, sortingObj.rid, sortingObj.scan_type,
                                                          sortingObj.scan_date, sortingObj.scan_time,
                                                          sortingObj.s_identifier, sortingObj.i_identifier,
                                                          sortingObj.file_type, sortingObj.download_folder,
                                                          sortingObj.raw_folder, sortingObj.moved)

    def getSQL_getToBeConvertedFileFromConversionTable(self, studyID):
        return "SELECT * FROM Conversion WHERE STUDY='{0}' AND NOT (CONVERTED OR SKIP)".format(studyID.upper())

    def getSQL_getAllConvertedFromConvertionTable(self, studyID):
        return "SELECT * FROM Conversion WHERE STUDY='{0}' AND CONVERTED".format(studyID.upper())

    def getSQL_AddNewEntryToProcessingTable(self, values):
        return "INSERT IGNORE INTO Processing VALUES ({0}) ".format(values)

    def getSQL_getToBeProcessedFromProcessingTable(self, studyID):
        return "SELECT * FROM Processing WHERE STUDY='{0}' AND NOT (PROCESSED OR SKIP)".format(studyID.upper())
