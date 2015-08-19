function combiningSubjects(outputBase, group_t, fwhm_varatio)

addpath(genpath('/opt/matlab7.5/toolbox/fmristat')); addpath(genpath('/opt/matlab12b/toolbox/emma'),'-end');

% Create the equivalent SD
input_ef = replaceCellSubstring(group_t,'_t.mnc','_ef.mnc');
input_sd = replaceCellSubstring(group_t,'_t.mnc','_sd.mnc');

X = ones(length(group_t),1);
input_ef = input_ef';
input_sd = input_sd';

contrast = 1;
which_stats='_t _fwhm';
output_file_base{1} = outputBase;

%% Getting the local computer's name
[~,gb_psom_localhost] = system('uname -n');
gb_psom_localhost = deblank(gb_psom_localhost);
display(gb_psom_localhost);

my_multistat(input_ef,input_sd,[],[],X,contrast,output_file_base,which_stats,fwhm_varatio);
