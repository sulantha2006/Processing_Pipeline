__author__ = 'sulantha'
from Utils.PipelineLogger import PipelineLogger
from Utils.DbUtils import DbUtils

class QSubJobStatusReporter:
    def __init__(self):
        self.DBClient = DbUtils()

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