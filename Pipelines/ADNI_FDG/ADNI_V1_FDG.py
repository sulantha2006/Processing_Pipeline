__author__ = 'sulantha'

class ADNI_V1_FDG:
    def __init__(self, study, version):
        self.study = study
        self.version = version

    def processNewData(self):
        print('ProcessDataCalled')