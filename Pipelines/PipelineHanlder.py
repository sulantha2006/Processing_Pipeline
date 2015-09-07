__author__ = 'sulantha'
import os
import Config.LIB_PATH as libpath
from Pipelines.ADNI_T1.ADNI_V1_T1 import ADNI_V1_T1
from Pipelines.ADNI_FDG.ADNI_V1_FDG import ADNI_V1_FDG
from Pipelines.ADNI_AV45.ADNI_V1_AV45 import ADNI_V1_AV45
from Pipelines.ADNI_Fmri.ADNI_V1_FMRI import ADNI_V1_FMRI

class PipelineHandler:
    def __init__(self):
        self.processingPPDict = {'ADNI':{'V1':{'T1':ADNI_V1_T1(), 'FMRI':ADNI_V1_FMRI(), 'AV45':ADNI_V1_AV45(), 'FDG':ADNI_V1_FDG()}}}

    def process(self, processingObj):
        os.environ['PATH'] = ':'.join(libpath.PATH)
        os.environ['LD_LIBRARY_PATH'] = ':'.join(libpath.LD_LIBRARY_PATH)
        os.environ['LD_LIBRARYN32_PATH'] = ':'.join(libpath.LD_LIBRARYN32_PATH)
        os.environ['PERL5LIB'] = ':'.join(libpath.PERL5LIB)

        study = processingObj.study
        modality = processingObj.modality
        version = processingObj.version

        processed = self.processingPPDict[study][version][modality].process(processingObj)

        return processed

