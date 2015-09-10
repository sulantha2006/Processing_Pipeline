__author__ = 'sulantha'
import os
import Config.LIB_PATH as libpath
from Utils.DbUtils import DbUtils
from Pipelines.ADNI_T1.ADNI_V1_T1 import ADNI_V1_T1
from Pipelines.ADNI_FDG.ADNI_V1_FDG import ADNI_V1_FDG
from Pipelines.ADNI_AV45.ADNI_V1_AV45 import ADNI_V1_AV45
from Pipelines.ADNI_Fmri.ADNI_V1_FMRI import ADNI_V1_FMRI
from Config import PipelineConfig

class PipelineHandler:
    def __init__(self):
        self.processingPPDict = {'ADNI':{'V1':{'T1':ADNI_V1_T1(), 'FMRI':ADNI_V1_FMRI(), 'AV45':ADNI_V1_AV45(), 'FDG':ADNI_V1_FDG()}}}
        self.DBClient = DbUtils()

    def process(self, study, modality):
        os.environ['PATH'] = ':'.join(libpath.PATH)
        os.environ['LD_LIBRARY_PATH'] = ':'.join(libpath.LD_LIBRARY_PATH)
        os.environ['LD_LIBRARYN32_PATH'] = ':'.join(libpath.LD_LIBRARYN32_PATH)
        os.environ['PERL5LIB'] = ':'.join(libpath.PERL5LIB)

        toProcessinModalityPerStudy = self.DBClient.executeAllResults("SELECT * FROM Processing INNER JOIN (SELECT * FROM {0}_{1}_Pipeline WHERE NOT (FINISHED OR SKIP)) as TMP ON Processing.RECORD_ID=TMP.PROCESSING_TID".format(study, modality))
        for processingItem in toProcessinModalityPerStudy:
            version = processingItem[10]
            self.processingPPDict[study][version][modality].process(processingItem)

        return 0


    def addToPipelineTable(self, processingObj):
        study = processingObj.study
        version = processingObj.version
        modality = processingObj.modality
        r_id = processingObj.record_id

        addToTableDict = dict(T1="INSERT IGNORE INTO {0}_T1_Pipeline VALUES (NULL, {1}, \"{2}\", 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL)".format(study, r_id, PipelineConfig.defaultT1config),
                              AV45="INSERT IGNORE INTO {0}_AV45_Pipeline VALUES (NULL, {1}, \"{2}\", '{3}', 0, 0, 0, NULL, NULL)".format(study, r_id, PipelineConfig.defaultAV45config, 'MANUAL_XFM_COMESHERE'),
                              FDG="INSERT IGNORE INTO {0}_FDG_Pipeline VALUES (NULL, {1}, \"{2}\", '{3}', 0, 0, 0, NULL, NULL)".format(study, r_id, PipelineConfig.defaultFDGconfig, 'MANUAL_XFM_COMESHERE'),
                              FMRI="INSERT IGNORE INTO {0}_FMRI_Pipeline VALUES (NULL, {1}, \"{2}\", '{3}', 0, 0, 0, NULL, NULL)".format(study, r_id, PipelineConfig.defaultFMRIconfig, 'NIAK_STH_COMESHERE'))

        self.DBClient.executeNoResult(addToTableDict[modality])

