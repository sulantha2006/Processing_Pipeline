__author__ = 'wang'

import subprocess
import Config.PipelineConfig as config

class FmrilmToCombinedRuns():

    
    def __init__(self, sqlObject):
        self.input_file, self.output_file, self.unsmoothed_image, self.output_folder = self.parseSql(sqlObject)
        self.execute(self.input_file, self.output_file, self.unsmoothed_image, self.output_folder)

    def parseSql(self, sqlObject):
        pass
        return input_file, output_file, unsmoothed_image, output_folder

    def execute(self, input_file, output_file, unsmoothed_image, output_folder):
        for x, y, z, voxelType in self.seedPoints():
            command = "%s runFmrilm('%s', '%s', '%s', '%s', '%s')" %\
                      (config.matlab_call, config.fmristat_location, config.emma_tools_location,
                       input_file, output_file, unsmoothed_image, output_folder, x, y, z, voxelType)
            outputStd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()
            return outputStd

    def seedPoints(self):
        pass
        # Figure out a way to structure desired seed points to be tested