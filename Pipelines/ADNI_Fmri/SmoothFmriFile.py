__author__ = 'wang'

import Config.PipelineConfig as config
import subprocess


class SmoothFmriFile():
    def __init__(self, sqlObject):
        self.input_files, self.output_files, self.output_folders = self.parseSql(sqlObject)
        for input_file, output_file, output_folder in self.input_files, self.output_files, self.output_folders:
            self.execute(input_file, output_file, output_folder)

    def parseSql(self, sqlObject):
        pass
        return input_files, output_files, output_folders

    def execute(self, input_file, output_file, output_folder):
        command = "%s smoothFmri('%s', '%s', '%s', '%s', '%s')" %\
                  (config.matlab_call, config.niak_location,
                   input_file, output_file,
                   output_folder, config.fwhm_smoothing)
        outputStd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()
        return outputStd

        # Make sure output is at the right location