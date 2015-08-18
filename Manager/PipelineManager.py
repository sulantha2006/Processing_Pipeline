__author__ = 'sulantha'
from Recursor.Recursor import Recursor
from Utils.DbUtils import DBUtils
from Config import StudyConfig as sc

class PipelineManager:
    def __init__(self, studyList):
        self.DBClient = DBUtils()
        self.recursorList = []
        self._getRecursorList(studyList)
        self.sortingDataList = []

    # This method will return a list of Recursor Objects based on the study list provided.
    def _getRecursorList(self, studyList):
        for study in studyList:
            if study == 'ADNI':
                self.recursorList.append(Recursor(study, sc.ADNIDownloadRoot))

    # This method will recurse through the download folders.
    def recurseForNewData(self):
        for recursor in self.recursorList:
            self.sortingDataList.append(recursor.recurse())

    # This method will add the new entries to the DB.
    def addNewDatatoDB(self):
        for sortingDataSet in self.sortingDataList:
            for sortingEntry in sortingDataSet:

                self.DBClient.insertIfNotExist(sortingEntry.sqlInsert(), sortingEntry.sqlUniqueFields(), sortingEntry.sqlUniqueValues())

    # This method will get the list of files need to be moved to study, subject specific folders.
    def getUnmovedRawDataList(self):
        pass

    # This method will move the downloaded raw files to the study, subject specific folders and add moved tag in sorting table.
    def moveRawData(self):
        pass