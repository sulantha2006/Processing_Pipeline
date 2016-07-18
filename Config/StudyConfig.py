__author__ = 'Sulantha'

AllowedStudyList = ['ADNI', 'ADNI_OLD']
AllowedStepsList = ['Sort', 'Move', 'T1Beast', 'T1Process', 'ProcessAV45', 'ProcessFDG', 'ProcessFMRI', 'ProcessDTI', 'ProcessAV1451']
AllowedVersions = ['V1', 'V2', 'V3']
AllowedModalityList = ['T1', 'AV45', 'FDG', 'FMRI', 'BLUFF', 'AV1451']


ProcessingModalityAndPipelineTypePerStudy = dict(ADNI={'AV1451':'AV1451',
                                            'AV45':'AV45',
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
                                            'HHP6MPRAGE':'T1',
                                            'ext-rsfmri':'FMRI',
                                            'rsfmri':'FMRI',
                                            'A_rsfmri_EO':'FMRI'
                                                })

#This versioning dict should have an entry if the default processing version is not V1 - Still in test.
defaultVersioningForStudy = dict(ADNI={'T1': 'V1', 'AV45': 'V1', 'FDG': 'V1', 'FMRI': 'V1', 'BLUFF': 'V1', 'AV1451': 'V1'}, ADNI_OLD={'T1': 'V1', 'AV45': 'V1', 'FDG': 'V1', 'FMRI': 'V1', 'AV1451': 'V1'})

ADNIDownloadRoot = '/data/data02/sulantha/ADNI_DL'
# ADNIDownloadRoot = '/data/data02/ADNI/raw' # /data/data02/ADNI/new_raw
xmlPath = '/data/data03/RawArchive/XMLProcessedArchive'

ADNIOLDDownloadRoot = '/data/data02/ADNI/raw/AD'


studyDatabaseRootDict = dict(ADNI='/data/data03/Database', ADNI_OLD='/data/data03/Database')
