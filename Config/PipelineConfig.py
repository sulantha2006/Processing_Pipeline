__author__ = 'sulantha'
import os

defaultT1config = "{'n3Dist':'75', 'headHeight':'150'}"
defaultAV45config = "{'blur':'8'}"
defaultFDGconfig = "{'blur':'8'}"
defaultFMRIconfig = "{'nu_correct':'-75', 'fwhm_smoothing':'6'}"

# For Fmri
niak_location = '/data/data01/wang/references/niak-0.7.1-ammo'
fmristat_location = '/home/wang/Documents/MATLAB/fmristat'
emma_tools_location = '/home/wang/Documents/MATLAB/emma'
matlab_location = '/opt/matlab12b/bin/matlab'
matlab_scripts = os.path.dirname(__file__) + '/../Pipelines/ADNI_Fmri/MatlabScripts'
fwhm_smoothing = '6'
matlab_call = '%s -nodisplay -nosplash -r "addpath(\'%s\');' % (matlab_location, matlab_scripts)
sourcing = 'source /opt/minc-toolkit/minc-toolkit-config.sh'

T1TempDirForCIVETProcessing = '/data/data03/CIVETUPLOAD'
T1TempDirForCIVETDownload = '/data/data03/CIVETDOWNLOAD/2015-11-16'

ADNI_dataMatchDBName = 'Study_Data.ADNI'
ADNI_visitCode_Dict = {
    'ADNI1 Baseline': 'ad1_bl',
    'ADNI1/GO Month 6': 'adg_m6',
    'ADNI2 Year 1 Visit': 'ad2_m12',
    'ADNI2 Baseline-New Pt': 'ad2_bl',
    'ADNI1/GO Month 12': 'adg_m12',
    'ADNIGO Month 60': 'adg_m60',
    'ADNI1/GO Month 36': 'adg_m36',
    'ADNI1/GO Month 18': 'adg_m18',
    'ADNI2 Year 2 Visit': 'ad2_m24',
    'ADNI2 Initial Visit-Cont Pt': 'ad2_ini',
    'ADNI1/GO Month 24': 'adg_m24',
    'ADNI1/GO Month 48': 'adg_m48',
    'ADNI2 Year 3 Visit': 'ad2_m36',
    'ADNI2 Year 4 Visit}': 'ad2_m48',
    'ADNI1 Screening': 'ad1_sc',
    'ADNIGO Month 72': 'adg_m72',
    'Unscheduled': 'und',
    'No Visit Defined': 'und',
    'ADNI2 Year 4 Visit': 'ad2_m48',
    'ADNIGO Screening MRI': 'adg_sc',
    'ADNIGO Month 3 MRI': 'adg_m3',
    'ADNI2 Screening MRI-New Pt': 'ad2_sc',
    'ADNI2 Month 3 MRI-New Pt': 'ad2_m3',
    'ADNI2 Month 6-New Pt': 'ad2_m6'
}

ADNI_T1_match_accepted_scantypes = ['MPR-R_B1_N3', 'MPR_B1_N3S', 'MPR_B1_N3', 'MPR_B1', 'MPR_N3', 'MPR', 'MPR-R',
                                    'MPR-R_N3', 'MPR_N3S', 'MPR-R_N3S', 'MPR-R_N3S', 'MPR-R_B1', 'MPR-R_B1_N3S',
                                    'MPR-R_B1_N3S', 'MT1_G_N3m', 'MT1_N3m', 'T1-SNMN3C', 'MPR-R__N3', 'MPR__N3S',
                                    'MPR__N3S', 'MPR__N3', 'MPR_N3S', 'S_IR-SPGR', 'AS_IR-SPGR', 'AS_IR-FSPGR',
                                    'S_IR-FSPGR', 'AS_IR-SPGR', 'IR-FSPGR', 'IR-FSPGR_Rep', 'MPR__M', 'MPR-R__M', 'MPRAGE']

ADNI_T1_match_scantype_priorityList = ['MPR-R_B1_N3', 'MPR_B1_N3S', 'MPR_B1_N3', 'MT1_G_N3m', 'MPR-R_B1_N3S', 'MPR-R_B1_N3S', 'MPR-R_N3S',
                                       'MPR-R_B1',  'MPR-R_N3', 'MPR-R__N3', 'MPR__N3S', 'AS_IR-SPGR', 'AS_IR-FSPGR', 'T1-SNMN3C',
                                    'S_IR-FSPGR', 'AS_IR-SPGR', 'IR-FSPGR',
                                       'MT1_N3m', 'MPR_B1', 'MPR_N3', 'MPR', 'MPR-R',
                                    'MPR_N3S', 'MPR__N3', 'MPR_N3S', 'S_IR-SPGR',  'IR-FSPGR_Rep', 'MPR__M', 'MPR-R__M', 'MPRAGE']
