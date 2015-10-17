__author__ = 'sulantha'

from Utils.DbUtils import DbUtils
import Config.PipelineConfig as pc
from Pipelines.ADNI_T1.ADNI_T1_Helper import ADNI_T1_Helper
from Utils.PipelineLogger import PipelineLogger
import distutils.dir_util
import distutils.file_util
import shutil
import subprocess
from Manager.QSubJob import QSubJob
from Manager.QSubJobHanlder import QSubJobHandler
import socket
import ast

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

class ADNI_V1_FDG:
    def __init__(self):
        self.DBClient = DbUtils()
        self.MatchDBClient = DbUtils(database=pc.ADNI_dataMatchDBName)

    def process(self, processingItem):
        processingItemObj = ProcessingItemObj(processingItem)
        if processingItemObj.manual_xfm == '':
            PipelineLogger.log('root', 'error', 'PET cannot be processed .. Manual XFM not found. {0} - {1} - {2} - {3} - {4}'.format(processingItemObj.subject_rid, processingItemObj.modality, processingItemObj.scan_date, processingItemObj.s_identifier, processingItemObj.i_identifier))
            return 0
        matching_t1 = ADNI_T1_Helper().getMatchingT1(processingItemObj)
        if not matching_t1:
            return 0

        processed = ADNI_T1_Helper().checkProcessed(matching_t1)
        if not processed:
            PipelineLogger.log('root', 'error', 'PET cannot be processed due to matching T1 not being processed. - {0} - {1}'.format(processingItemObj.subject_rid, processingItemObj.scan_date))
            return 0
        else:
            PipelineLogger.log('root', 'INFO', '+++++++++ PET ready to be processed. With check for xfm. - {0} - {1}'.format(processingItemObj.subject_rid, processingItemObj.scan_date))
            return 0
            if processingItemObj.manual_xfm == '':
                manualXFM = self.PETHelper.getManualXFM(processingItemObj, matching_t1)
                processingItemObj.manual_xfm = manualXFM
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
        paramStrd = ast.literal_eval(processingItemObj.parameters)
        paramStrt = ' '.join(['[\"{0}\"]=\"{1}\"'.format(k, v) for k,v in paramStrd.iteritems()])
        paramStr = '({0})'.format(paramStrt)
        petCMD = 'source /opt/minc-toolkit/minc-toolkit-config.sh; Pipelines/ADNI_FDG/ADNI_V1_FDG_Process {0} {1} {2} {3} {4} {5} {6} {7} {8}'.format(id, petFileName, processedFolder, matchT1Path, processingItemObj.manual_xfm, logDir, paramStr,socket.gethostname(), 50500)
        try:
            shutil.rmtree(processedFolder)
        except:
            pass
        try:
            distutils.dir_util.mkpath(processedFolder)
        except Exception as e:
            PipelineLogger.log('manager', 'error', 'Error in creating processing folder. \n {0}'.format(e))
            return 0

        PipelineLogger.log('manager', 'debug', 'Command : {0}'.format(petCMD))
        p = subprocess.Popen(petCMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable='/bin/bash')
        out, err = p.communicate()
        PipelineLogger.log('manager', 'debug', 'Conversion Log Output : \n{0}'.format(out))
        PipelineLogger.log('manager', 'debug', 'Conversion Log Err : \n{0}'.format(err))

        QSubJobHandler.submittedJobs[id] = QSubJob(id, '02:00:00', processingItemObj, 'av45')
        return 1


