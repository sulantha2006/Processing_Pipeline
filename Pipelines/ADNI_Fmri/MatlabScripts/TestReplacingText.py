__author__ = 'wang'


import Config.FmriConfig as config
import fileinput

niakTemplateFile = 'Pipelines/ADNI_Fmri/MatlabScripts/niakPreprocessingTemplate.m'

templateFileWithInformation = None
with open('niakTemplateFile', 'r') as templateFile:
    templateFileWithInformation = templateFile.read()
    templateFile.close()

# Replace the target string
templateFileWithInformation = templateFileWithInformation.replace('%{patient_information}', 'abcd')

for line in fileinput.input(niakTemplateFile, inplace=True):
    templateFileWithInformation.append(line
                                       .replace('%{patient_information}', "subject0007.session1.anat = 'bla.mnc'\n"
                                                                          "subject0007.session1.fmri = 'hi.mnc'")
                                       .replace('%{opt.folder_out}', '/data/data03/wang/output')
                                       .replace('%{niak_location}', config.niak_location)
                                       .replace('%{fwhm}', config.fwhm_smoothing)
                                       )
    # templateFileWithInformation.append(line
    #                                    .replace('%{patient_information}', "subject0007.session1.anat = 'bla.mnc'\n"
    #                                                                       "subject0007.session1.fmri = 'hi.mnc'")
    #                                    .replace('%{opt.folder_out}', '/data/data03/wang/output')
    #                                    .replace('%{niak_location}', config.niak_location)
    #                                    .replace('%{fwhm}', config.fwhm_smoothing)
    #                                    )

print(templateFileWithInformation)

def replaceInfo()