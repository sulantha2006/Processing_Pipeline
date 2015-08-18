__author__ = 'Sulantha'

AllowedStudyList = ['ADNI']
AllowedStepsList = ['Sort', 'Move', 'T1Beast', 'T1Process', 'ProcessAV45', 'ProcessFDG', 'ProcessFMRI', 'ProcessDTI']
AllowedVersions = ['1', '2', '3']

#This dictionary will have the list of modalities for each study type, where only these type of images be moved and processed.
ProcessingImagingModalities = {'ADNI':['AV45', 'FDG', 'MT1__GradWarp__N3m', 'MT1__N3m']}

ADNIDownloadRoot = '/data/backup-data02/ADNI/downloads/New2'
