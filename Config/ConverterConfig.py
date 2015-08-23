__author__ = 'sulantha'

studyTypeForConvertionDict = {'ADNI':{'AV45': 'AV45',
                                      'FDG': 'FDG',
                                      'ext-rsfmri': 'rsfmri',
                                      'rsfmri': 'rsfmri'}}

dcmToMnc_exec = '/home/vfonov/quarantine/bin/dcm2mnc32'
dcmToNii_exec = ''
niiToMnc_exec = ''
mincSource_exec = 'source /opt/minc-toolkit/minc-toolkit-config.sh'