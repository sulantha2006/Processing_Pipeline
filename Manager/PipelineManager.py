__author__ = 'sulantha'
import os
from multiprocessing import Pool
from Recursor.Recursor import Recursor
from Utils.DbUtils import DbUtils
from Config import StudyConfig as sc
from Manager.SQL.SQLBuilder import SQLBuilder
import distutils.dir_util
from Utils.PipelineLogger import PipelineLogger
from Manager.SQLTables.Sorting import Sorting
from Manager.SQLTables.SortingObject import SortingObject
from Manager.SQLTables.Conversion import Conversion
from Converters.Raw2MINCConverter import Raw2MINCConverter
from Manager.QSubJobHanlder import QSubJobHandler
from Pipelines.PipelineHandler import PipelineHandler
from Manager.SQLTables.Processing import Processing


class PipelineManager:
    def __init__(self, studyList, version):
        self.DBClient = DbUtils()
        self.studyList = [i.upper() for i in studyList]
        self.version = version
        self.recursorList = []
        self._getRecursorList(studyList)
        self.sortingDataList = []
        self.sqlBuilder = SQLBuilder()

        self.moveSortingObjListDict = {}
        self.toConvertObjListDict = {}

        self.sortingTable = Sorting()
        self.conversionTable = Conversion()

        self.raw2mincConverter = Raw2MINCConverter()
        self.pool = Pool(processes=12)
        self.qsubJobHandler = QSubJobHandler()
        self.qsubJobHandler.start()

        self.convertedListDict = {}

        self.processingTable = Processing()

        self.toProcessListDict = {}
        self.pipelineHanlder = PipelineHandler()

    # This method will return a list of Recursor Objects based on the study list provided.
    def _getRecursorList(self, studyList):
        for study in studyList:
            if study == 'ADNI':
                self.recursorList.append(Recursor(study, sc.ADNIDownloadRoot))
            elif study == 'ADNI_OLD':
                self.recursorList.append(Recursor(study, sc.ADNIOLDDownloadRoot))

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
        def removeCommaIfThere(destFolder):
            PipelineLogger.log('manager', 'debug',
                                   'Removing unsupported chars from file names...... :')
            for dpath, dnames, fnames in os.walk(destFolder):
                for f in fnames:
                    os.chdir(dpath)
                    if ',' in f:
                        os.rename(f, f.replace(',', ''))
            PipelineLogger.log('manager', 'debug',
                                   'Removing unsupported chars from file names done ...:')

        def copyFile(sourceFolder, destFolder):
            try:
                PipelineLogger.log('manager', 'debug', 'Raw Data Copying : {0} -> {1}'.format(sourceFolder, destFolder))
                distutils.dir_util.copy_tree(sourceFolder, destFolder, update=True)
                PipelineLogger.log('manager', 'debug',
                                   'Raw Data Copy Done...... : {0} -> {1}'.format(sourceFolder, destFolder))
                removeCommaIfThere(destFolder)
                return 1
            except Exception as exc:
                PipelineLogger.log('manager', 'error',
                                   'Raw Data Move Error : {0} -> {1}'.format(sourceFolder, destFolder))
                PipelineLogger.log('manager', 'exception', exc)
                return 0
        for study in self.studyList:
            totalToMove = len(self.moveSortingObjListDict[study])
            PipelineLogger.log('manager', 'info', 'Moving started for study {0} - Total to be moved : {1}'.format(study, totalToMove))
            count = 1
            for sortingObj in self.moveSortingObjListDict[study]:
                PipelineLogger.log('manager', 'info', 'Moving {0}/{1} - {2}'.format(count, totalToMove, sortingObj.download_folder))
                copied = copyFile(sortingObj.download_folder, sortingObj.raw_folder)
                count += 1
                if copied:
                    self.conversionTable.insertFromSortingObj(sortingObj, self.version)
                    self.sortingTable.setMovedTrue(sortingObj)
                else:
                    PipelineLogger.log('manager', 'error', 'File Move Error : {0} -> {1}. Moving to next...'.format(sortingObj.download_folder, sortingObj.raw_folder))

    def getConversionList(self):
        for study in self.studyList:
            self.toConvertObjListDict[study] = self.conversionTable.gettoBeConvertedPerStudy(study)

    def convertRawData(self):

        def addTODB(result):
            if result['converted']:
                #### Add to correspoing table
                #self.conversionTable.insertFromConvertionObj(convertionObj, self.version)
                self.conversionTable.setConvertedTrue(result['obj'])
            else:
                PipelineLogger.log('manager', 'error', 'File conversion Error : {0} -> {1}. Moving to next...'.format(result['obj'].raw_folder, result['obj'].converted_folder))
                self.conversionTable.setConvertedFailed(result['obj'])

        for study in self.studyList:
            totalToConv = len(self.toConvertObjListDict[study])
            PipelineLogger.log('manager', 'info', 'Convertion started for study {0} - Total to be converted : {1}'.format(study, totalToConv))
            results = []
            for convObj in self.toConvertObjListDict[study]:
                convertedResult = self.pool.apply_async(self.raw2mincConverter.convert2minc, args=(convObj,), callback=addTODB)
                results.append(convertedResult)
            for r in results:
                r.wait()

    def getConvertedList(self):
        for study in self.studyList:
            self.convertedListDict[study] = self.conversionTable.getConvertedListPerStudy(study)

    def refreshModalityTables(self):
        for study in self.studyList:
            for convertionObj in self.convertedListDict[study]:
                self.processingTable.insertFromConvertionObj(convertionObj)

    def getProcessList(self):
        for study in self.studyList:
            self.toProcessListDict[study] = self.processingTable.getToProcessListPerStudy(study)

    def fillPipelineTables(self):
        for study in self.studyList:
            for processingObj in self.toProcessListDict[study]:
                self.pipelineHanlder.addToPipelineTable(processingObj)

    def processModality(self, modality):
        PipelineLogger.log('manager', 'info', 'File processing started ... ###########')
        for study in self.studyList:
            self.pipelineHanlder.process(study, modality)






