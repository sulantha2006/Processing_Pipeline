function compareSubjects(group1_files, group2_files, group1_covariates, group2_covariates, outputBase, fwhm_varatio)

addpath(genpath('/opt/matlab12b/toolbox/emma'),'-end');
addpath(genpath('/opt/matlab7.5/toolbox/fmristat'));

input_files_ef = [replaceCellSubstring(group1_files,'_t', '_ef') replaceCellSubstring(group2_files,'_t', '_ef')]';
input_files_sd = [replaceCellSubstring(group1_files,'_t', '_sd') replaceCellSubstring(group2_files,'_t', '_sd')]';


contrast = [1 -1 zeros(1, size(group1_covariates,2))];
X = [ones(length(group1_files),1) ; zeros(length(group2_files),1)];
Y = [zeros(length(group1_files),1) ; ones(length(group2_files),1)];
Z = [group1_covariates ; group2_covariates];
X = [X Y Z];

output_file_base{1} = outputBase;
which_stats = '_t';
if ~exist('fwhm_varatio','var'); fwhm_varatio = -100; end

my_multistat(input_files_ef,input_files_sd,[],[],X,contrast,output_file_base,which_stats,fwhm_varatio);
