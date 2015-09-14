__author__ = 'sulantha'

defaultT1config = "{'n3Dist':'75', 'headHeight':'150'}"
defaultAV45config = "{'blur':'8'}"
defaultFDGconfig = "{'blur':'8'}"
defaultFMRIconfig = "{'blur':'6', }"

# For Fmri
niak_location = '/data/data01/wang/references/niak-0.7.1-ammo'
fmristat_location = '/home/wang/Documents/MATLAB/fmristat'
emma_tools_location = '/home/wang/Documents/MATLAB/emma'
matlab_location = '/opt/matlab12b/bin/matlab'
matlab_scripts = 'Pipelines/ADNI_Fmri/MatlabScripts'
fwhm_smoothing = '6'
matlab_call = '%s -nodisplay << addpath(%s)' % (matlab_location, matlab_scripts)

T1TempDirForCIVETProcessing = '/data/data03/CIVETUPLOAD'