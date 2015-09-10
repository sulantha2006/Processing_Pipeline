__author__ = 'wang'

import os
from Pipelines.ADNI_Fmri.Niak import Niak

class NiakOutput():
    def __init__(self, niakPreprocessingFolder):
        self.fmri_file = niakPreprocessingFolder + '/fmri/fmri_subject1_session1_run1.mnc'
        self.anat_ln_file = niakPreprocessingFolder + '/anat/anat_subject1_nuc_stereolin.mnc'
        self.anat_nl_file = niakPreprocessingFolder + '/anat/anat_subject1_nuc_stereonl.mnc'
        self.fmri_mean_file = niakPreprocessingFolder + '/anat/func_subject1_mean_stereonl.mnc'
        self.func_coregister = niakPreprocessingFolder + '/quality_control/group_coregistration/func_tab_qc_coregister_stereonl.csv'
        self.anat_ln_coregister = niakPreprocessingFolder + '/quality_control/group_coregistration/anat_tab_qc_coregister_stereolin.csv'
        self.anat_nl_coregister = niakPreprocessingFolder + '/quality_control/group_coregistration/anat_tab_qc_coregister_stereonl.csv'
        self.func_motion = niakPreprocessingFolder + '/quality_control/group_motion/qc_scrubbing_group.csv'


        # Need to wait for Niak to finish and loop a certain number of times
        while self.checkFiles([self.fmri_file, self.anat_ln_file, self.anat_nl_file, self.fmri_mean_file,
                               self.func_coregister, self.anat_ln_coregister, self.anat_nl_coregister,
                               self.func_motion]):
            Niak()

    def checkFiles(self, filesList):
        for path in filesList:
            if not os.path.isfile(path):
                return False
        return True

    def writeToSql(self):
        pass
        # Write results to SQL, as well as file locations