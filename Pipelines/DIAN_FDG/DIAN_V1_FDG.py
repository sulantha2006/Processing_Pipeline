__author__ = 'sulantha'

from Utils.DbUtils import DbUtils
import Config.PipelineConfig as pc
from Pipelines.DIAN_T1.DIAN_T1_Helper import DIAN_T1_Helper
from Utils.PipelineLogger import PipelineLogger
import distutils.dir_util
import distutils.file_util
import shutil
import subprocess
from Manager.QSubJob import QSubJob
from Manager.QSubJobHanlder import QSubJobHandler
import socket, os
import ast
from Pipelines.Helpers.PETHelper import PETHelper

class ProcessingItemObj:
    def __init__(self, processingItem):
        self.processing_rid = processingItem[0]
        self.study = processingItem[1]
        self.subject_rid = processingItem[2]
        self.modality = processingItem[3]
        self.scan_date = processingItem[4].strftime("%Y-%m-%d")
        self.scan_time = str(processingItem[5])
        self.s_identifier = processingItem[6]
        self.i_identifier = processingItem[7]
        self.root_folder = processingItem[8]
        self.converted_folder = processingItem[9]
        self.version = processingItem[10]
        self.table_id = processingItem[17]
        self.parameters = processingItem[19]
        self.manual_xfm = processingItem[20]
        self.qc = processingItem[21]

class DIAN_V1_FDG:
    def __init__(self):
        self.DBClient = DbUtils()
        self.MatchDBClient = DbUtils(database=pc.DIAN_dataMatchDBName)
        self.PETHelper = PETHelper()

    def process(self, processingItem):
        processingItemObj = ProcessingItemObj(processingItem)
        matching_t1 = DIAN_T1_Helper().getMatchingT1(processingItemObj)
        if not matching_t1:
            return 0

        processed = DIAN_T1_Helper().checkProcessed(matching_t1)
        if not processed:
            PipelineLogger.log('root', 'error', 'PET cannot be processed due to matching T1 not being processed. - {0} - {1}'.format(processingItemObj.subject_rid, processingItemObj.scan_date))
            return 0
        else:
            PipelineLogger.log('root', 'INFO', '+++++++++ PET ready to be processed. Will check for initial xfm. - {0} - {1}'.format(processingItemObj.subject_rid, processingItemObj.scan_date))
            if processingItemObj.manual_xfm == 'Req_man_reg':
                coregDone = self.PETHelper.checkIfAlreadyDone(processingItemObj, matching_t1)
                if coregDone:
                    manualXFM = coregDone
                    setPPTableSQL = "UPDATE {0}_{1}_Pipeline SET MANUAL_XFM = '{2}' WHERE RECORD_ID = {3}".format(processingItemObj.study, processingItemObj.modality, manualXFM, processingItemObj.table_id)
                    self.DBClient.executeNoResult(setPPTableSQL)
                    processingItemObj.manual_xfm = manualXFM
                    self.processPET(processingItemObj, processed)
                else:
                    self.PETHelper.requestCoreg(processingItemObj, matching_t1)
                    PipelineLogger.log('root', 'INFO', 'Manual XFM was not found. Request to create one may have added.  - {0} - {1}'.format(processingItemObj.subject_rid, processingItemObj.scan_date))
                    return 0
            else:
                self.processPET(processingItemObj, processed)

    def getScanType(self, processingItemObj):
        r = self.DBClient.executeAllResults("SELECT SCAN_TYPE FROM Conversion WHERE STUDY = '{0}' AND RID = '{1}' "
                                        "AND SCAN_DATE = '{2}' AND S_IDENTIFIER = '{3}' "
                                        "AND I_IDENTIFIER = '{4}'".format(processingItemObj.study,
                                                                          processingItemObj.subject_rid,
                                                                          processingItemObj.scan_date,
                                                                          processingItemObj.s_identifier,
                                                                          processingItemObj.i_identifier))
        return r[0][0]

    def set_new_param_str(self, table_name, table_id, param_str):
        sql = "UPDATE {0} SET PARAMETERS = \"{2}\" WHERE RECORD_ID = {1}".format(table_name, table_id, param_str)
        self.DBClient.executeNoResult(sql)

    def processPET(self, processingItemObj, matchT1Path):
        petFileName = '{0}/{1}_{2}{3}{4}{5}_{6}.mnc'.format(processingItemObj.converted_folder, processingItemObj.study,
                                                        processingItemObj.subject_rid, processingItemObj.scan_date.replace('-', ''),
                                                        processingItemObj.s_identifier, processingItemObj.i_identifier,
                                                        self.getScanType(processingItemObj))
        processedFolder = '{0}/processed'.format(processingItemObj.root_folder)
        logDir = '{0}/logs'.format(processingItemObj.root_folder)
        PipelineLogger.log('manager', 'info', 'PET processing starting for {0}'.format(petFileName))
        try:
            distutils.dir_util.mkpath(logDir)
        except Exception as e:
            PipelineLogger.log('manager', 'error', 'Error in creating log folder \n {0}'.format(e))
            return 0

        id = '{0}{1}{2}{3}'.format(processingItemObj.subject_rid, processingItemObj.scan_date.replace('-', ''), processingItemObj.s_identifier, processingItemObj.i_identifier)

        ### This section is new for ADNI Pre processing - Per scanner type blurring. Only required if
        ### the images are aquired from different scanners and need to get to same PSF.
        blur_x, blur_y, blur_z = self.PETHelper.getBlurringParams(processingItemObj)
        ### End pre processing.
        if not blur_x:
            PipelineLogger.log('manager', 'error',
                               'Error in identifying scanner specific blurring - {0}'.format(petFileName))
            return 0
        paramStrd = "{{'blur_x':'{0}', 'blur_y':'{1}', 'blur_z':'{2}'}}".format(blur_x, blur_y, blur_z)
        self.set_new_param_str('{0}_{1}_Pipeline'.format(processingItemObj.study, processingItemObj.modality), processingItemObj.table_id, paramStrd)
        paramStrd = ast.literal_eval(paramStrd)
        paramStrt = ' '.join(['[\"{0}\"]=\"{1}\"'.format(k, v) for k,v in paramStrd.items()])
        paramStr = '({0})'.format(paramStrt)
        petCMD = "source /opt/minc-1.9.15/minc-toolkit-config.sh; Pipelines/DIAN_FDG/DIAN_V1_FDG_Process {0} {1} {2} {3} {4} {5} '{6}' {7} {8}".format(id, petFileName, processedFolder, matchT1Path, 'auto' if processingItemObj.manual_xfm == '' else processingItemObj.manual_xfm, logDir, paramStr,socket.gethostname(), 50500)
        try:
            processedFolder_del = '{0}/processed_del'.format(processingItemObj.root_folder)
            os.rename(processedFolder, processedFolder_del)
            shutil.rmtree(processedFolder_del)
        except Exception as e:
            PipelineLogger.log('manager', 'error', 'Error in deleting old processing folder. \n {0}'.format(e))
        try:
            distutils.dir_util.mkpath(processedFolder)
        except Exception as e:
            PipelineLogger.log('manager', 'error', 'Error in creating processing folder. \n {0}'.format(e))
            return 0

        PipelineLogger.log('manager', 'debug', 'Command : {0}'.format(petCMD))
        p = subprocess.Popen(petCMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable='/bin/bash')
        out, err = p.communicate()
        PipelineLogger.log('manager', 'debug', 'Process Log Output : \n{0}'.format(out))
        PipelineLogger.log('manager', 'debug', 'Process Log Err : \n{0}'.format(err))

        QSubJobHandler.submittedJobs[id] = QSubJob(id, '23:00:00', processingItemObj, 'fdg')
        return 1


