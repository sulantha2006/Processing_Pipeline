__author__ = 'wang'
import os
import Config.LIB_PATH as libpath
from Utils.DbUtils import DbUtils
from Pipelines.ADNI_Fmri.ADNI_V1_FMRI import ADNI_V1_FMRI

def setEnvironmentVariables():
    os.environ['PATH'] = ':'.join(libpath.PATH)
    os.environ['LD_LIBRARY_PATH'] = ':'.join(libpath.LD_LIBRARY_PATH)
    os.environ['LD_LIBRARYN32_PATH'] = ':'.join(libpath.LD_LIBRARYN32_PATH)
    os.environ['PERL5LIB'] = ':'.join(libpath.PERL5LIB)
    os.environ['MNI_DATAPATH'] = ':'.join(libpath.MNI_DATAPATH)
    os.environ['ROOT'] = ';'.join(libpath.ROOT)
    os.environ['MINC_TOOLKIT_VERSION'] = libpath.MINC_TOOLKIT_VERSION
    os.environ['MINC_COMPRESS'] = libpath.MINC_COMPRESS
    os.environ['MINC_FORCE_V2'] = libpath.MINC_FORCE_V2

if __name__ == '__main__':
    processingPPDict = {'ADNI':{'V1':{'FMRI':ADNI_V1_FMRI()},
                             'V2':{'FMRI':ADNI_V1_FMRI()}}}

    study = 'ADNI'
    modality = 'FMRI'

    setEnvironmentVariables()
    toProcessinModalityPerStudy = DbUtils().executeAllResults("SELECT * FROM Processing INNER JOIN (SELECT * FROM {0}_{1}_Pipeline WHERE NOT (FINISHED OR SKIP)) as TMP ON Processing.RECORD_ID=TMP.PROCESSING_TID".format(study, modality))
    for processingItem in toProcessinModalityPerStudy:
        version = processingItem[10]
        # Calling on the process .section of given studies and modalities
        processingPPDict[study][version][modality].process(processingItem)