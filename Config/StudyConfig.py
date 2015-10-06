__author__ = 'Sulantha'

AllowedStudyList = ['ADNI', 'ADNI_OLD']
AllowedStepsList = ['Sort', 'Move', 'T1Beast', 'T1Process', 'ProcessAV45', 'ProcessFDG', 'ProcessFMRI', 'ProcessDTI']
AllowedVersions = ['1', '2', '3']
AllowedModalityList = ['T1', 'AV45', 'FDG', 'FMRI']


ProcessingModalityAndPipelineTypePerStudy = dict(ADNI={'AV45':'AV45',
                                            'FDG':'FDG',
                                            'T1':'T1',
                                            'MPR':'T1',
                                            'MPR_N3':'T1',
                                            'MPR_B1':'T1',
                                            'MPR_B1_N3':'T1',
                                            'MPR_B1_N3S':'T1',
                                            'MPR-R_B1_N3':'T1',
                                            'MPR-R':'T1',
                                            'MPR-R_N3':'T1',
                                            'MPR_N3S':'T1',
                                            'MPR-R_N3S':'T1',
                                            'MPR-R_B1':'T1',
                                            'MPR-R_B1_N3S':'T1',
                                            'MT1_G_N3m':'T1',
                                            'MT1_N3m':'T1',
                                            'T1-SNMN3C':'T1',
                                            'MPR-R__N3':'T1',
                                            'MPR__N3S':'T1',
                                            'MPR__N3':'T1',
                                            'S_IR-SPGR':'T1',
                                            'AS_IR-SPGR':'T1',
                                            'AS_IR-FSPGR':'T1',
                                            'S_IR-FSPGR':'T1',
                                            'IR-FSPGR':'T1',
                                            'IR-FSPGR_Rep':'T1',
                                            'MPRAGE':'T1',
                                            'ext-rsfmri':'FMRI',
                                            'rsfmri':'FMRI',
                                            'A_rsfmri_EO':'FMRI'
                                                })

#This versioning dict should have an entry if the default processing version is not V1 - Still in test.
defaultVersioningForStudy = dict(ADNI={'T1': 'V1', 'AV45': 'V1', 'FDG': 'V1', 'FMRI': 'V1'}, ADNI_OLD={'T1': 'V1', 'AV45': 'V1', 'FDG': 'V1', 'FMRI': 'V1'})

ADNIDownloadRoot = '/data/data03/sulantha/Downloads/ADNI/ADNI'
ADNIOLDDownloadRoot = '/data/data02/ADNI/raw/AD'


studyDatabaseRootDict = dict(ADNI='/data/data03/Database', ADNI_OLD='/data/data03/Database')
