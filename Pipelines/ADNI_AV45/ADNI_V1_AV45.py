__author__ = 'sulantha'

from Utils.DbUtils import DbUtils
import Config.PipelineConfig as pc
from Pipelines.ADNI_T1.ADNI_T1_Helper import ADNI_T1_Helper


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

class ADNI_V1_AV45:
    def __init__(self):
        self.DBClient = DbUtils()
        self.MatchDBClient = DbUtils(database=pc.ADNI_dataMatchDBName)

    def process(self, processingItem):
        processingItemObj = ProcessingItemObj(processingItem)
        mathcnig_t1 = ADNI_T1_Helper().getMatchingT1(processingItemObj)

        print(mathcnig_t1)
