__author__ = 'wang'

import fileinput, subprocess
import Config.FmriConfig as config

class SubjectToNiak():
    def __init__(self, sqlObject, outputFolder):

        self.niakTemplateFile = 'Pipelines/ADNI_Fmri/MatlabScripts/niakPreprocessingTemplate.m'
        self.patientInfo = self.parseSql(sqlObject)

        templateFileWithInformation = '';
        for line in fileinput.input(self.niakTemplateFile, inplace=True):
            templateFileWithInformation.append(line
                                               .replace('%{patient_information}', self.patientInfo)
                                               .replace('%{opt.folder_out}', outputFolder)
                                               .replace('%{niak_location}', config.niak_location)
                                               .replace('%{fwhm}', config.fwhm_smoothing)
                                               )

        # Execute script
        command = '%s -nodisplay << %s' % (config.matlab_location, templateFileWithInformation)
        outputStd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()
        print(outputStd) # Will have to implement a way that NIAK can output its running session to stdout

    def parseSql(self, sqlObject):
        pass