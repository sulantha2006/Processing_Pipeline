__author__ = 'sulantha'
import os
import Config.LIB_PATH as libpath
from Utils.DbUtils import DbUtils
from Pipelines.ADNI_T1.ADNI_V1_T1 import ADNI_V1_T1
from Pipelines.ADNI_FDG.ADNI_V1_FDG import ADNI_V1_FDG
from Pipelines.ADNI_FDG.ADNI_V2_FDG import ADNI_V2_FDG
from Pipelines.ADNI_AV45.ADNI_V1_AV45 import ADNI_V1_AV45
from Pipelines.ADNI_AV45.ADNI_V2_AV45 import ADNI_V2_AV45
from Pipelines.ADNI_Fmri.ADNI_V1_FMRI import ADNI_V1_FMRI
from Config import PipelineConfig
from Utils.PipelineLogger import PipelineLogger
import glob
import shutil
from distutils import dir_util
from QC.QCHandler import QCHandler

class PipelineHandler:
    def __init__(self):
        self.processingPPDict = {'ADNI':{'V1':{'T1':ADNI_V1_T1(), 'FMRI':ADNI_V1_FMRI(), 'AV45':ADNI_V1_AV45(), 'FDG':ADNI_V1_FDG()},
                                         'V2':{'T1':ADNI_V1_T1(), 'FMRI':ADNI_V1_FMRI(), 'AV45':ADNI_V2_AV45(), 'FDG':ADNI_V2_FDG()}}}
        self.DBClient = DbUtils()
        self.QCH = QCHandler()

    def checkExternalJobs(self, study, modality):
        getExtJobSql = "SELECT * FROM externalWaitingJobs WHERE JOB_ID LIKE '{0}_{1}_%'".format(study, modality)
        extJobs = self.DBClient.executeAllResults(getExtJobSql)
        for job in extJobs:
            jobType = job[0].split('_')[-1]
            reportTable = job[1]
            tableID = job[0].split('_')[2]
            reportField = job[2]
            subjectScanID = job[0].split('_')[3]
            success = 0
            if jobType == 'CIVETRUN':
                if glob.glob('{0}/{1}_{2}_*'.format(PipelineConfig.T1TempDirForCIVETDownload, study, subjectScanID)):
                    getProccessRecSql = "SELECT * FROM Processing WHERE RECORD_ID IN (SELECT PROCESSING_TID FROM {0}_T1_Pipeline WHERE RECORD_ID = {1})".format(study, tableID)
                    processingEntry = self.DBClient.executeAllResults(getProccessRecSql)[0]

                    civetFolder = '{0}/civet'.format(processingEntry[8])

                    if os.path.exists(civetFolder):
                        shutil.rmtree(civetFolder)
                    try:
                        PipelineLogger.log('manager', 'info', 'Copying - {0} -> {1}'.format(glob.glob('{0}/{1}_{2}_*'.format(PipelineConfig.T1TempDirForCIVETDownload, study, subjectScanID))[0], civetFolder))
                        dir_util.copy_tree(glob.glob('{0}/{1}_{2}_*'.format(PipelineConfig.T1TempDirForCIVETDownload, study, subjectScanID))[0], civetFolder)
                        success = 1
                    except:
                        success = 0
                else:
                    continue
            else:
                PipelineLogger.log('manager', 'error', 'Unknown external job type - {}'.format(jobType))

            if success:
                updateSQL = "UPDATE {0} SET {1} = 1 WHERE RECORD_ID = {2}".format(reportTable, reportField, tableID)
                self.DBClient.executeNoResult(updateSQL)

                if jobType == 'CIVETRUN':
                    finishSQL = "UPDATE {0} SET FINISHED = 1 WHERE RECORD_ID = {1}".format(reportTable, tableID)
                    self.DBClient.executeNoResult(finishSQL)
                    modal_table = reportTable
                    modal_tableId = tableID
                    qcField = 'QC'
                    qctype = 'civet'
                    qcFolder = civetFolder
                    self.QCH.requestQC(study, modal_table, modal_tableId, qcField, qctype, qcFolder)


                rmSql = "DELETE FROM externalWaitingJobs WHERE JOB_ID LIKE '{0}_{1}_{2}_{3}_%'".format(study, modality, tableID, subjectScanID)
                self.DBClient.executeNoResult(rmSql)


    def process(self, study, modality):
        os.environ['PATH'] = ':'.join(libpath.PATH)
        os.environ['LD_LIBRARY_PATH'] = ':'.join(libpath.LD_LIBRARY_PATH)
        os.environ['LD_LIBRARYN32_PATH'] = ':'.join(libpath.LD_LIBRARYN32_PATH)
        os.environ['PERL5LIB'] = ':'.join(libpath.PERL5LIB)
        os.environ['MNI_DATAPATH'] = ':'.join(libpath.MNI_DATAPATH)
        os.environ['ROOT'] = ';'.join(libpath.ROOT)
        os.environ['MINC_TOOLKIT_VERSION'] = libpath.MINC_TOOLKIT_VERSION
        os.environ['MINC_COMPRESS'] = libpath.MINC_COMPRESS
        os.environ['MINC_FORCE_V2'] = libpath.MINC_FORCE_V2

        toProcessinModalityPerStudy = self.DBClient.executeAllResults("SELECT * FROM Processing INNER JOIN (SELECT * FROM {0}_{1}_Pipeline WHERE NOT (FINISHED OR SKIP)) as TMP ON Processing.RECORD_ID=TMP.PROCESSING_TID".format(study, modality))
        for processingItem in toProcessinModalityPerStudy:
            version = processingItem[10]
            self.processingPPDict[study][version][modality].process(processingItem)

        return 0


    def addToPipelineTable(self, processingObj):
        study = processingObj.study
        version = processingObj.version
        modality = processingObj.modality
        r_id = processingObj.record_id

        addToTableDict = dict(T1="INSERT IGNORE INTO {0}_T1_Pipeline VALUES (NULL, {1}, \"{2}\", 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL)".format(study, r_id, PipelineConfig.defaultT1config),
                              AV45="INSERT IGNORE INTO {0}_AV45_Pipeline VALUES (NULL, {1}, \"{2}\", '{3}', 0, 0, 0, NULL, NULL)".format(study, r_id, PipelineConfig.defaultAV45config, ''),
                              FDG="INSERT IGNORE INTO {0}_FDG_Pipeline VALUES (NULL, {1}, \"{2}\", '{3}', 0, 0, 0, NULL, NULL)".format(study, r_id, PipelineConfig.defaultFDGconfig, ''),
                              FMRI="INSERT IGNORE INTO {0}_FMRI_Pipeline VALUES (NULL, {1}, \"{2}\", '{3}', 0, 0, 0, NULL, NULL)".format(study, r_id, PipelineConfig.defaultFMRIconfig, 'NIAK_STH_COMESHERE'))

        self.DBClient.executeNoResult(addToTableDict[modality])

