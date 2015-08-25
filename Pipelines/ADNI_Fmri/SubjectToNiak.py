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

        # Replacing
        replacing_dict = {'%{patient_information}': self.patientInfo,
                          '%{opt.folder_out}': outputFolder,
                          '%{niak_location}': config.niak_location,
                          '%{fwhm}': config.fwhm_smoothing
                          }
        templateFileWithInformation = self.replaceString(templateFileWithInformation, replacing_dict)

        # Execute script
        command = '%s %s' % (config.matlab_call, templateFileWithInformation)
        outputStd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()
        print(outputStd) # Will have to implement a way that NIAK can output its running session to stdout

    def parseSql(self, sqlObject):
        pass

    def replaceString(self, text, replacing_dict):
        for query, replacedInto in replacing_dict:
            text = text.replace(query, replacedInto)
        return text