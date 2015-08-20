__author__ = 'wang'

import fileinput, subprocess
import Config.FmriConfig as config

class SubjectToNiak():
    def __init__(self, sqlObject, outputFolder):

        self.niakTemplateFile = 'Pipelines/ADNI_Fmri/MatlabScripts/niakPreprocessingTemplate.m'
        self.patientInfo = self.parseSql(sqlObject)

        templateFileWithInformation = None
        with open(self.niakTemplateFile, 'r') as templateFile:
            templateFileWithInformation = templateFile.read()
            templateFile.close()

        replacing_dict = {'%{patient_information}' : self.patientInfo,
                          '%'
                          }

        templateFileWithInformation = self.replaceString(templateFileWithInformation, replacing_dict)

        for line in fileinput.input(self.niakTemplateFile, inplace=True):
            templateFileWithInformation.append(line
                                               .replace('%{patient_information}', self.patientInfo)
                                               .replace('%{opt.folder_out}', outputFolder)
                                               .replace('%{niak_location}', config.niak_location)
                                               .replace('%{fwhm}', config.fwhm_smoothing)
                                               )

        # Execute script
        command = '%s %s' % (config.matlab_call, templateFileWithInformation)
        outputStd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()
        print(outputStd) # Will have to implement a way that NIAK can output its running session to stdout

    def parseSql(self, sqlObject):
        pass

    def replaceString(self, text, replacing_dict):
        pass