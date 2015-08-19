function combiningRuns(inputFolder, subjectID, sessionID)

addpath(genpath('/opt/matlab7.5/toolbox/fmristat')); addpath(genpath('/opt/matlab12b/toolbox/emma'),'-end');

filename = ['subject' subjectID '_session' sessionID];

input_ef = fMRIListDir([inputFolder '/data/' filename '*_mag_ef.mnc']);
input_sd = fMRIListDir([inputFolder '/data/' filename '*_mag_sd.mnc']);

X = ones(length(input_ef),1);
contrast = 1;
output_file_base{1} = [inputFolder '/data2/' filename '_multi'];
mkdir([inputFolder '/data2/']);
which_stats='_t _ef _sd';
fwhm_varatio = -10;

if exist([output_file_base{1} '_t.mnc'],'file'); return; end
my_multistat(input_ef,input_sd,1,[],X,contrast,output_file_base,which_stats,fwhm_varatio);
