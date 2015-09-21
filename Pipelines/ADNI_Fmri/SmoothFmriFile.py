__author__ = 'wang'

import Config.PipelineConfig as config
import subprocess


class SmoothFmriFile:
    def __init__(self):
        pass

    def process(self, processingItemObj):
        niakFolder = '{0}/niak'.format(processingItemObj.root_folder)
        fmri_file = niakFolder + '/fmri/fmri_subject1_session1_run1.mnc'
        outputFolder = niakFolder + '/fmri_s/'
        outputFile = niakFolder + '/fmri_s/fmri_subject1_session1_run1.mnc'

        command = self.setCommand(fmri_file, outputFile, outputFolder)
        self.execute(command)
        self.checkFileExists(outputFile)

    def execute(self, command):
        outputStd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()
        return outputStd

    def setCommand(self, input_file, output_file, output_folder):
        command = "%s smoothFmri('%s', '%s', '%s', '%s', '%s')" %\
                  (config.matlab_call, config.niak_location,
                   input_file, output_file,
                   output_folder, config.fwhm_smoothing)
        return command

    def checkFileExists(self, outputFile):
        pass
        # Make sure output is at the right location