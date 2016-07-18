__author__ = 'sulantha'

studyTypeForConvertionDict = {'ADNI':{'AV1451':'AV1451',
                                    'AV45': 'AV45',
                                      'FDG': 'FDG',
                                      'ext-rsfmri': 'rsfmri',
                                      'rsfmri': 'rsfmri'}}

dcmToMnc_exec = '/home/vfonov/quarantine/bin/dcm2mnc32'
dcmToNii_exec = '/home/wang/Documents/bin/references/dcm2nii'
niiToMnc_exec = '/opt/minc-toolkit/bin/nii2mnc'
mincSource_exec = 'source /opt/minc-toolkit/minc-toolkit-config.sh'