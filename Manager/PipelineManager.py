__author__ = 'sulantha'
from Recursor.Recursor import Recursor
from Utils.DbUtils import DBUtils
from Config import StudyConfig as sc

class PipelineManager:
    def __init__(self, studyList):
        self.DBClient = DBUtils()
        self.recursorList = self._getRecursorList(studyList)

        self.sortingDataList=None

    ##This method will return a list of Recursor Objects based on the study list provided.
    def _getRecursorList(self, studyList):
        recursorList = []
        for study in studyList:
            if study == 'ADNI':
                recursorList.append(Recursor(study, sc.ADNIDownloadRoot))

    ##This method will recurse through the download folders.
    def recurseForNewData(self):
        for recursor in self.recursorList:
            self.sortingDataList.append(recursor.recurse())

    ##This method will add the new entries to the DB.
    def addNewDatatoDB(self):
        for sortingDataSet in self.sortingDataList:
            for sortingEntry in sortingDataSet:
                DBUtils.execute(
                    "If Not Exists (Select * from Sorting_Table where (studyID, rid, scan_type, study_date, s_identifider, i_identifier) = ({0},{1},{2},{3},{4})"
                    "Begin"
                    "Insert into Sorting {5} "
                    "End".format())

    ##This method will get the list of files need to be moved to study, subject specific folders.
    def getUnmovedRawDataList(self):
        pass

    ##This method will move the downloaded raw files to the study, subject specific folders and add moved tag in sorting table.
    def moveRawData(self):
        pass