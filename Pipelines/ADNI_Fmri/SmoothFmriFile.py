__author__ = 'wang'

import Config.FmriConfig as config
import subprocess


class SmoothFmriFile():
    def __init__(self, sqlObject):
        self.input_file, self.output_file, self.outputFolder = self.parseSql(sqlObject)
        command = "%s -nodisplay << smoothFmri('%s', '%s', '%s', '%s', '%s')" %\
                  (config.matlab_location, config.niak_location,
                   self.input_file, self.output_file,
                   self.output_Folder, config.fwhm_smoothing)
        outputStd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()
        # Make sure output is at the right location

    def parseSql(self, sqlObject):
        pass
