__author__ = 'wang'

from Utils.DbUtils import DbUtils
import ast
from Pipelines.ADNI_Fmri.Niak import Niak
import Pipelines.ADNI_Fmri.SmoothFmriFile as smoothing
from Utils.PipelineLogger import PipelineLogger

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
        self.table_id = processingItem[17] # From Processing_Pipeline import ADNI_FMRI_PIPELINE
        self.parameters = ast.literal_eval(processingItem[19])
        self.niak_sth = processingItem[20]
        self.qc = processingItem[21]
        self.finished = processingItem[22]
        self.skip = processingItem[23]
        self.additional_1 = processingItem[24]
        self.additional_2 = processingItem[25]

class ADNI_V1_FMRI:
    def __init__(self):
        self.DBClient = DbUtils()
        self.niak = Niak()

    def process(self, processingItem):
        processingItemObj = ProcessingItemObj(processingItem)
        self.runNiak(processingItemObj)


    def runNiak(self, processingItemObj):
        # Run Niak
        if not processingItemObj.skip:
            self.niak.process(processingItemObj)
        elif processingItemObj.skip:
            pass
        else:
            PipelineLogger.log('manager', 'error', 'Error handling obj for processing - {0}'.format(processingItemObj))
            return 0

    def runSmoothing(self, processingItemObj):
        if not processingItemObj.skip and processingItemObj.finished:
            smoothing.execute(processingItemObj)