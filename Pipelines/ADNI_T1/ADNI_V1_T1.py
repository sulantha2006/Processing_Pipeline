__author__ = 'sulantha'

from Utils.PipelineLogger import PipelineLogger
from Utils.DbUtils import DbUtils
import distutils.dir_util
import shutil
import subprocess
from Manager.QSubJob import QSubJob
from Manager.QSubJobHanlder import QSubJobHandler
import socket

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

    def process(self, processingItem):
        processingItemObj = ProcessingItemObj(processingItem)

        if processingItemObj.beast_skip and processingItemObj.manual_skip:
            #RUN CIVET WITH NO MASK
            pass
        elif processingItemObj.manual_mask and not processingItemObj.manual_skip:
            #RUN CIVET WITH MANUAL MASK
            pass
        elif processingItemObj.beast_mask == 0 and not processingItemObj.beast_skip and not processingItemObj.beast_qc and not processingItemObj.manual_mask:
            self.runBeast(processingItemObj)
        elif processingItemObj.beast_skip and not processingItemObj.manual_mask and not processingItemObj.manual_skip:
            #Request Manual Mask
            pass
        elif processingItemObj.beast_mask == 1 and not processingItemObj.beast_skip and processingItemObj.beast_qc and not processingItemObj.manual_mask:
            #RUN CIVET BEAST MASK
            pass
        elif processingItemObj.beast_mask == 1 and not processingItemObj.beast_skip and not processingItemObj.beast_qc and not processingItemObj.manual_mask and not processingItemObj.manual_skip:
            #Request QC on Beast Mask
            pass
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

    def runBeast(self, processingItemObj):
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
        beastFolder = '{0}/beast'.format(processingItemObj.root_folder)
        logDir = '{0}/logs'.format(processingItemObj.root_folder)
        PipelineLogger.log('manager', 'info', 'BeAST starting for {0}'.format(nativeFileName))
        try:
            distutils.dir_util.mkpath(nativeFolder)
            distutils.dir_util.mkpath(logDir)
            shutil.copyfile(converted_file, nativeFileName)
        except Exception as e:
            PipelineLogger.log('manager', 'error', 'Error in creating folders or copying native file. \n {0}'.format(e))
            return 0

        id = '{0}{1}{2}{3}'.format(processingItemObj.subject_rid, processingItemObj.scan_date.replace('-', ''), processingItemObj.s_identifier, processingItemObj.i_identifier)
        beastCMD = 'source /opt/minc-toolkit/minc-toolkit-config.sh; Pipelines/ADNI_T1/ADNI_V1_T1_BeAST {0} {1} {2} {3} {4} {5}'.format(id, nativeFileName, beastFolder, logDir, socket.gethostname(), 50500)
        print(beastCMD)
        try:
            shutil.rmtree(beastFolder)
        except:
            pass
        try:
            distutils.dir_util.mkpath(beastFolder)
        except Exception as e:
            PipelineLogger.log('manager', 'error', 'Error in creating BeAST folder. \n {0}'.format(e))
            return 0

        PipelineLogger.log('converter', 'debug', 'Command : {0}'.format(beastCMD))
        p = subprocess.Popen(beastCMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable='/bin/bash')
        out, err = p.communicate()
        PipelineLogger.log('converter', 'debug', 'Conversion Log Output : \n{0}'.format(out))
        PipelineLogger.log('converter', 'debug', 'Conversion Log Err : \n{0}'.format(err))

        QSubJobHandler.submittedJobs[id] = QSubJob(id, '00:20:00', processingItemObj, 'beast')
        return 1





