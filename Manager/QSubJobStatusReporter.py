__author__ = 'sulantha'
from Utils.PipelineLogger import PipelineLogger
from Utils.DbUtils import DbUtils
from QC.QCHandler import QCHandler

class QSubJobStatusReporter:
    def __init__(self):
        self.DBClient = DbUtils()
        self.QCHandler = QCHandler()

    def setStatus(self, job, status):
        if job.jobType == 'beast':
            nestedJob = job.job
            table = '{0}_{1}_Pipeline'.format(nestedJob.study, nestedJob.modality)
            table_id = nestedJob.table_id
            if status == 'Success':
                setSql = 'UPDATE {0} SET BEAST_MASK = 1 WHERE RECORD_ID = {1}'.format(table, table_id)
            elif status == 'Fail':
                setSql = 'UPDATE {0} SET BEAST_MASK = -1, BEAST_SKIP = 1 WHERE RECORD_ID = {1}'.format(table, table_id)
            self.DBClient.executeNoResult(setSql)
            if status == 'Fail':
                PipelineLogger.log('manager', 'error','QSUB job Status Failed: - {0} - Processing Table ID : {1} - Modality Table ID : {2}'.format(job.jobType, nestedJob.processing_rid, nestedJob.table_id))

        if job.jobType == 'av45':
            nestedJob = job.job
            table = '{0}_{1}_Pipeline'.format(nestedJob.study, nestedJob.modality)
            table_id = nestedJob.table_id
            if status == 'Success':
                setSql = "UPDATE {0} SET FINISHED = 1, PROC_Failed = Null WHERE RECORD_ID = {1}".format(table, table_id)
                self.requestQC(nestedJob, 'av45')
            elif status == 'Fail':
                setSql = "UPDATE {0} SET PROC_Failed = 'Failed' , SKIP = 1 WHERE RECORD_ID = {1}".format(table, table_id)
            self.DBClient.executeNoResult(setSql)
            if status == 'Fail':
                PipelineLogger.log('manager', 'error','QSUB job Status Failed: - {0} - Processing Table ID : {1} - Modality Table ID : {2}'.format(job.jobType, nestedJob.processing_rid, nestedJob.table_id))

        if job.jobType == 'av1451':
            nestedJob = job.job
            table = '{0}_{1}_Pipeline'.format(nestedJob.study, nestedJob.modality)
            table_id = nestedJob.table_id
            if status == 'Success':
                setSql = "UPDATE {0} SET FINISHED = 1, PROC_Failed = Null WHERE RECORD_ID = {1}".format(table, table_id)
                self.requestQC(nestedJob, 'av1451')
            elif status == 'Fail':
                setSql = "UPDATE {0} SET PROC_Failed = 'Failed' , SKIP = 1 WHERE RECORD_ID = {1}".format(table,
                                                                                                         table_id)
            self.DBClient.executeNoResult(setSql)
            if status == 'Fail':
                PipelineLogger.log('manager', 'error',
                                   'QSUB job Status Failed: - {0} - Processing Table ID : {1} - Modality Table ID : {2}'.format(
                                       job.jobType, nestedJob.processing_rid, nestedJob.table_id))

        if job.jobType == 'fdg':
            nestedJob = job.job
            table = '{0}_{1}_Pipeline'.format(nestedJob.study, nestedJob.modality)
            table_id = nestedJob.table_id
            if status == 'Success':
                setSql = "UPDATE {0} SET FINISHED = 1, PROC_Failed = Null WHERE RECORD_ID = {1}".format(table, table_id)
                self.requestQC(nestedJob, 'fdg')
            elif status == 'Fail':
                setSql = "UPDATE {0} SET PROC_Failed = 'Failed' , SKIP = 1 WHERE RECORD_ID = {1}".format(table, table_id)
            self.DBClient.executeNoResult(setSql)
            if status == 'Fail':
                PipelineLogger.log('manager', 'error','QSUB job Status Failed: - {0} - Processing Table ID : {1} - Modality Table ID : {2}'.format(job.jobType, nestedJob.processing_rid, nestedJob.table_id))


    def requestQC(self, processingItemObj, qctype):
        qcFieldDict = dict(civet='QC', beast='BEAST_QC', av45='QC', fdg='QC', av1451='QC')
        qcFolderDict = { 'civet' : '{0}/civet'.format(processingItemObj.root_folder),
                         'beast' : '{0}/beast'.format(processingItemObj.root_folder),
                         'av45' : '{0}/processed'.format(processingItemObj.root_folder),
                         'av1451': '{0}/processed'.format(processingItemObj.root_folder),
                         'fdg' : '{0}/processed'.format(processingItemObj.root_folder)}
        self.QCHandler.requestQC(processingItemObj.study, '{0}_{1}_Pipeline'.format(processingItemObj.study,
                                                                                    processingItemObj.modality),
                                 processingItemObj.table_id, qcFieldDict[qctype], qctype, qcFolderDict[qctype])