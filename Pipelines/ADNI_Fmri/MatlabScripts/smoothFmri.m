function smoothFmri(niakPath, input_file, output_file, outputFolder, fwhm)

addpath(genpath(niakPath));
opt.fwhm = fwhm;
opt.folder_out = outputFolder;
opt.flag_edge = 0;
niak_brick_smooth_vol(input_file, output_file, opt);