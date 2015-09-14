__author__ = 'sulantha'

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

class ADNI_V1_FMRI:
    def __init__(self):
        pass

    def process(self, processingItem):
        pass