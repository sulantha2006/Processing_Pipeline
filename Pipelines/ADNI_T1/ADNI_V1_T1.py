__author__ = 'sulantha'

from Utils.PipelineLogger import PipelineLogger
from Utils.DbUtils import DbUtils
import distutils.dir_util
import shutil
import subprocess
from Manager.QSubJob import QSubJob
from Manager.QSubJobHanlder import QSubJobHandler
import socket
import Config.PipelineConfig as pc
import os
import distutils.file_util
from QC.QCHandler import QCHandler

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
        self.beast_mask = processingItem[20]
        self.beast_skip = processingItem[21]
        self.beast_qc = processingItem[22]
        self.manual_mask = processingItem[23]
        self.manual_skip = processingItem[24]
        self.civet = processingItem[25]
        self.civet_qc = processingItem[26]

class ADNI_V1_T1:
    def __init__(self):
        self.DBClient = DbUtils()
        self.QCHandler = QCHandler

    def process(self, processingItem):
        processingItemObj = ProcessingItemObj(processingItem)

        if processingItemObj.beast_skip and processingItemObj.manual_skip and not processingItemObj.civet:
            self.runCivet(processingItemObj, 'N')
        elif processingItemObj.manual_mask and not processingItemObj.manual_skip and not processingItemObj.civet:
            self.runCivet(processingItemObj, 'M')
        elif processingItemObj.beast_mask == 0 and not processingItemObj.beast_skip and processingItemObj.beast_qc == 0 and not processingItemObj.manual_mask:
            self.runBeast(processingItemObj)
        elif processingItemObj.beast_skip and not processingItemObj.manual_mask and not processingItemObj.manual_skip:
            PipelineLogger.log('manager', 'error', '$$$$$$$$$$$$$$$$$ Manual Mask Requested $$$$$$$$$$$$$$$$$$ - {0}'.format(processingItem))
            pass
        elif processingItemObj.beast_mask == 1 and not processingItemObj.beast_skip and processingItemObj.beast_qc == 1 and not processingItemObj.manual_mask and not processingItemObj.civet:
            self.runCivet(processingItemObj, 'B')
        elif processingItemObj.beast_mask == 1 and not processingItemObj.beast_skip and processingItemObj.beast_qc == 0 and not processingItemObj.manual_mask and not processingItemObj.manual_skip:
            self.requestQC(processingItemObj, 'beast')
        elif processingItemObj.civet == 1 and processingItemObj.civet_qc == 0:
            self.requestQC(processingItemObj, 'civet')
        else:
            PipelineLogger.log('manager', 'error', 'Error handling obj for processing - {0}'.format(processingItem))
            return 0

    def getScanType(self, processingItemObj):
        r = self.DBClient.executeAllResults("SELECT SCAN_TYPE FROM Conversion WHERE STUDY = '{0}' AND RID = '{1}' "
                                        "AND SCAN_DATE = '{2}' AND S_IDENTIFIER = '{3}' "
                                        "AND I_IDENTIFIER = '{4}'".format(processingItemObj.study,
                                                                          processingItemObj.subject_rid,
                                                                          processingItemObj.scan_date,
                                                                          processingItemObj.s_identifier,
                                                                          processingItemObj.i_identifier))
        return r[0][0]

    def checkNative(self, processingItemObj):
        orig_ScanType = self.getScanType(processingItemObj)
        converted_file = '{0}/{1}_{2}{3}{4}{5}_{6}.mnc'.format(processingItemObj.converted_folder, processingItemObj.study,
                                                        processingItemObj.subject_rid, processingItemObj.scan_date.replace('-', ''),
                                                        processingItemObj.s_identifier, processingItemObj.i_identifier,
                                                        orig_ScanType)
        nativeFolder = '{0}/native'.format(processingItemObj.root_folder)
        nativeFileName = '{0}/{1}_{2}{3}{4}{5}_{6}.mnc'.format(nativeFolder, processingItemObj.study,
                                                        processingItemObj.subject_rid, processingItemObj.scan_date.replace('-', ''),
                                                        processingItemObj.s_identifier, processingItemObj.i_identifier,
                                                        processingItemObj.modality.lower())
        if not os.path.exists(nativeFileName):
            try:
                distutils.dir_util.mkpath(nativeFolder)
                shutil.copyfile(converted_file, nativeFileName)
            except Exception as e:
                PipelineLogger.log('manager', 'error', 'Error in creating folders or copying native file. \n {0}'.format(e))
                return None
        return nativeFileName

    def runBeast(self, processingItemObj):
        nativeFileName = self.checkNative(processingItemObj)
        if not nativeFileName:
            return 0
        beastFolder = '{0}/beast'.format(processingItemObj.root_folder)
        logDir = '{0}/logs'.format(processingItemObj.root_folder)
        PipelineLogger.log('manager', 'info', 'BeAST starting for {0}'.format(nativeFileName))
        try:
            distutils.dir_util.mkpath(logDir)
        except Exception as e:
            PipelineLogger.log('manager', 'error', 'Error in creating log folder \n {0}'.format(e))
            return 0

        id = '{0}{1}{2}{3}'.format(processingItemObj.subject_rid, processingItemObj.scan_date.replace('-', ''), processingItemObj.s_identifier, processingItemObj.i_identifier)
        beastCMD = 'source /opt/minc-toolkit/minc-toolkit-config.sh; Pipelines/ADNI_T1/ADNI_V1_T1_BeAST {0} {1} {2} {3} {4} {5}'.format(id, nativeFileName, beastFolder, logDir, socket.gethostname(), 50500)
        try:
            shutil.rmtree(beastFolder)
        except:
            pass
        try:
            distutils.dir_util.mkpath(beastFolder)
        except Exception as e:
            PipelineLogger.log('manager', 'error', 'Error in creating BeAST folder. \n {0}'.format(e))
            return 0

        PipelineLogger.log('manager', 'debug', 'Command : {0}'.format(beastCMD))
        p = subprocess.Popen(beastCMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable='/bin/bash')
        out, err = p.communicate()
        PipelineLogger.log('manager', 'debug', 'Beast Log Output : \n{0}'.format(out.decode("utf-8")))
        PipelineLogger.log('manager', 'debug', 'Beast Log Err : \n{0}'.format(err.decode("utf-8")))

        QSubJobHandler.submittedJobs[id] = QSubJob(id, '02:00:00', processingItemObj, 'beast')
        return 1

    def runCivet(self, processingItemObj, maskStatus):
        nativeFileName = self.checkNative(processingItemObj)
        if not nativeFileName:
            return 0
        copyFolder = pc.T1TempDirForCIVETProcessing
        subjectFileName_base = '{0}_{1}{2}{3}{4}_{5}'.format(processingItemObj.study,
                                                        processingItemObj.subject_rid, processingItemObj.scan_date.replace('-', ''),
                                                        processingItemObj.s_identifier, processingItemObj.i_identifier,
                                                        processingItemObj.modality.lower())
        jobId = '{0}_{1}_{2}_{3}{4}{5}{6}_CIVETRUN'.format(processingItemObj.study, processingItemObj.modality,
                                                           processingItemObj.table_id, processingItemObj.subject_rid,
                                                           processingItemObj.scan_date.replace('-', ''),
                                                            processingItemObj.s_identifier, processingItemObj.i_identifier)
        checkJobPresentSql = "SELECT * FROM externalWaitingJobs WHERE JOB_ID = '{0}'".format(jobId)
        if len(self.DBClient.executeAllResults(checkJobPresentSql)) is 0:
            beastFileName = '{0}/beast/mask/{1}_skull_mask_native.mnc'.format(processingItemObj.root_folder, subjectFileName_base)
            beastMaskName_base = '{0}_{1}{2}{3}{4}_mask'.format(processingItemObj.study,
                                                            processingItemObj.subject_rid, processingItemObj.scan_date.replace('-', ''),
                                                            processingItemObj.s_identifier, processingItemObj.i_identifier)
            beastMaskName = '{0}/{1}.mnc'.format(copyFolder, beastMaskName_base)
            manualFileName = '{0}/manual/mask/{1}_skull_mask_native.mnc'.format(processingItemObj.root_folder, subjectFileName_base)
            manualMaskName_base = '{0}_{1}{2}{3}{4}_mask'.format(processingItemObj.study,
                                                            processingItemObj.subject_rid, processingItemObj.scan_date.replace('-', ''),
                                                            processingItemObj.s_identifier, processingItemObj.i_identifier)
            manualMaskName = '{0}/{1}.mnc'.format(copyFolder, manualMaskName_base)
            try:
                distutils.file_util.copy_file(nativeFileName, copyFolder)
                if maskStatus == 'B':
                    distutils.file_util.copy_file(beastFileName, beastMaskName)
                elif maskStatus == 'M':
                    distutils.file_util.copy_file(manualFileName, manualMaskName)
                elif maskStatus == 'N':
                    pass
                else:
                    PipelineLogger.log('manager', 'error', 'Unknown mask status - {0} Entry : Processing ID - {1}, Table ID - {3}'.format(maskStatus, processingItemObj.processing_rid, processingItemObj.table_id))

                addExternalJobSQL = "INSERT INTO externalWaitingJobs VALUES ('{0}', '{1}', '{2}', NULL, NULL, NULL)".format(jobId, '{0}_{1}_Pipeline'.format(processingItemObj.study, processingItemObj.modality), 'CIVET')
                self.DBClient.executeNoResult(addExternalJobSQL)
            except Exception as e:
                PipelineLogger.log('manager', 'error', 'Error copying for CIVET input. Rolling back... - Processing Table ID -> {0} Table ID -> {1}'.format( processingItemObj.processing_rid, processingItemObj.table_id))
                PipelineLogger.log('manager', 'exception', e)
                nativeFileOnCopyFolder = '{0}/{1}'.format(copyFolder, os.path.basename(nativeFileName))
                os.remove(nativeFileOnCopyFolder) if os.path.exists(nativeFileOnCopyFolder) else None
                os.remove(beastMaskName) if os.path.exists(beastMaskName) else None
                os.remove(manualMaskName) if os.path.exists(manualMaskName) else None

    def requestQC(self, processingItemObj, qctype):
        qcFieldDict = dict(civet='CIVET_QC', beast='BEAST_QC')
        qcFolderDict = { 'civet' : '{0}/civet'.format(processingItemObj.root_folder),
                         'beast' : '{0}/beast'.format(processingItemObj.root_folder)}
        self.QCHandler.requestQC(processingItemObj.study, '{0}_{1}_Pipeline'.format(processingItemObj.study,
                                                                                    processingItemObj.modality),
                                 processingItemObj.table_id, qcFieldDict[qctype], qctype, qcFolderDict[qctype])


