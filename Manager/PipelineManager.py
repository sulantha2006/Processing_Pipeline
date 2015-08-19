__author__ = 'sulantha'
from Recursor.Recursor import Recursor
from Utils.DbUtils import DBUtils
from Config import StudyConfig as sc
from Manager.SQL.SQLBuilder import SQLBuilder
import distutils.dir_util
from Utils.PipelineLogger import PipelineLogger
from Manager.SQLTables.Sorting import Sorting
from Manager.SQLTables.SortingObject import SortingObject
from Manager.SQLTables.Conversion import Conversion


class PipelineManager:
    def __init__(self, studyList, version):
        self.DBClient = DBUtils()
        self.studyList = [i.upper() for i in studyList]
        self.version = version
        self.recursorList = []
        self._getRecursorList(studyList)
        self.sortingDataList = []
        self.sqlBuilder = SQLBuilder()
        self.moveSortingObjListDict = {}

        self.sortingTable = Sorting()
        self.conversionTable = Conversion()

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
        for sortingDataSet in self.sortingDataList: ##From the set of study specific recursors
            SortingObjList = [SortingObject(o.getValuesDict()) for o in sortingDataSet]
            self.sortingTable.insertToTable(SortingObjList)

    # This method will get the list of files need to be moved to study, subject specific folders.
    def getUnmovedRawDataList(self):
        for study in self.studyList:
            self.moveSortingObjListDict[study] = self.sortingTable.getUnmovedFilesPerStudy(study)

    # This method will move the downloaded raw files to the study, subject specific folders and add moved tag in sorting table.
    def moveRawData(self):
        def copyFile(sourceFolder, destFolder):
            try:
                PipelineLogger.log('manager', 'debug', 'Raw Data Copying : {0} -> {1}'.format(sourceFolder, destFolder))
                distutils.dir_util.copy_tree(sourceFolder, destFolder, update=True)
                PipelineLogger.log('manager', 'debug',
                                   'Raw Data Copy Done...... : {0} -> {1}'.format(sourceFolder, destFolder))
                return 1
            except Exception as exc:
                PipelineLogger.log('manager', 'error',
                                   'Raw Data Move Error : {0} -> {1}'.format(sourceFolder, destFolder))
                PipelineLogger.log('manager', 'exception', '')
                return 0
        for study in self.studyList:
            for sortingObj in self.moveSortingObjListDict[study]:
                copied = copyFile(sortingObj.download_folder, sortingObj.raw_folder)
                if copied:
                    self.conversionTable.insertFromSortingObj(sortingObj, self.version)
                    self.sortingTable.setMovedTrue(sortingObj)
                else:
                    PipelineLogger.log('manager', 'error', 'File Move Error : {0} -> {1}. Moving to next...'.format(sortingObj.download_folder, sortingObj.raw_folder))
