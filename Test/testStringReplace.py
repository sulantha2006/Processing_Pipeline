__author__ = 'wang'

# Testing Pipelines.ADNI_Fmri.Niak.replaceString function

from Pipelines.ADNI_Fmri.Niak import Niak

if __name__ == "__main__":
    niakTemplateFile = '/home/wang/Documents/bin/PyCharmProjects/Processing_Pipeline/Pipelines/ADNI_Fmri/MatlabScripts/niakPreprocessingTemplate.m'
    with open(niakTemplateFile, 'r') as templateFile:
        templateFileWithInformation = templateFile.read()
        templateFile.close()
    replacing_dict = {'%{patient_information}': '2453',
                      '%{opt.folder_out}': '/data/data03/wang/NiakFolder',
                      '%{niak_location}': '/data/data01/wang/references/niak-0.7.1-ammo/',
                      '%{nu_correct}': '6'
                      }
    new_text = Niak.replaceString(templateFileWithInformation, replacing_dict)
    print(new_text)