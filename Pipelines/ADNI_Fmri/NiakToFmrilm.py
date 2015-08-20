__author__ = 'wang'
import Config.FmriConfig as config
import subprocess

class NiakToFmrilm():
    def __init__(self, sqlObject):
        self.input_files, self_output_files, self_unsmoothed_images, self_outputbases = self.parseSql()
        for input_file, output_file, unsmoothed_image, output_folder \
                in self.input_files, self.output_files, self.unsmoothed_images, self.output_folders:
            self.execute(input_file, output_file, unsmoothed_image, output_folder)

    def parseSql(self):
        pass
        return input_files, output_files, unsmoothed_images, output_bases

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