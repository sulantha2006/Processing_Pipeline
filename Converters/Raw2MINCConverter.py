__author__ = 'sulantha'

import os
import Config.ConverterConfig as cc
from Converters.ConversionScripts.ADNI_V1_T1 import ADNI_V1_T1
from Converters.ConversionScripts.ADNI_V1_PET import ADNI_V1_PET
from Converters.ConversionScripts.ADNI_V1_Fmri import ADNI_V1_Fmri
from Converters.ConversionScripts.DIAN_V1_PET import DIAN_V1_PET
from Converters.ConversionScripts.DIAN_V1_T1 import DIAN_V1_T1
from Config import StudyConfig as sc
import Config.LIB_PATH as libpath

class Raw2MINCConverter:
    def __init__(self):
        self.convertionScriptsDict = {'ADNI':
                             {'AV45': {'V1': {'nifti': self.adni_v1_pet_nii,
                                              'dicom': self.adni_v1_pet_dicom,
                                              'v': self.adni_v1_pet_v,
                                              'minc': self.adni_v1_pet_minc},
                                       'V2': {'nifti': self.adni_v1_pet_nii,
                                              'dicom': self.adni_v1_pet_dicom,
                                              'v': self.adni_v1_pet_v,
                                              'minc': self.adni_v1_pet_minc}},
                              'AV1451': {'V1': {'nifti': self.adni_v1_pet_nii,
                                              'dicom': self.adni_v1_pet_dicom,
                                              'v': self.adni_v1_pet_v,
                                              'minc': self.adni_v1_pet_minc},
                                       'V2': {'nifti': self.adni_v1_pet_nii,
                                              'dicom': self.adni_v1_pet_dicom,
                                              'v': self.adni_v1_pet_v,
                                              'minc': self.adni_v1_pet_minc}},
                              'FDG': {'V1': {'nifti': self.adni_v1_pet_nii,
                                             'dicom': self.adni_v1_pet_dicom,
                                             'v': self.adni_v1_pet_v,
                                             'minc': self.adni_v1_pet_minc},
                                      'V2': {'nifti': self.adni_v1_pet_nii,
                                             'dicom': self.adni_v1_pet_dicom,
                                             'v': self.adni_v1_pet_v,
                                             'minc': self.adni_v1_pet_minc}},
                              'T1': {'V1': {'nifti': self.adni_v1_t1_nii,
                                            'dicom': self.adni_v1_t1_dicom,
                                            'v': self.adni_v1_t1_v,
                                            'minc': self.adni_v1_t1_minc},
                                     'V2': {'nifti': self.adni_v1_t1_nii,
                                            'dicom': self.adni_v1_t1_dicom,
                                            'v': self.adni_v1_t1_v,
                                            'minc': self.adni_v1_t1_minc}},
                              'FMRI': {'V1': {'nifti': self.adni_v1_rsfmri_nii,
                                            'dicom': self.adni_v1_rsfmri_dicom,
                                            'v': self.adni_v1_rsfmri_v,
                                            'minc': self.adni_v1_rsfmri_minc},
                                       'V2': {'nifti': self.adni_v1_rsfmri_nii,
                                            'dicom': self.adni_v1_rsfmri_dicom,
                                            'v': self.adni_v1_rsfmri_v,
                                            'minc': self.adni_v1_rsfmri_minc}}
                              }, 'DIAN':
                            {'T1':{'V1':{'dicom': self.dian_v1_t1_dicom}},
                             'FDG':{'V1':{'dicom': self.dian_v1_pet_dicom}},
                             'PIB':{'V1':{'dicom': self.dian_v1_pet_dicom}},
                             'AV1451':{'V1':{'dicom': self.dian_v1_pet_dicom}}
                            }}

        self.adni_v1_t1 = ADNI_V1_T1()
        self.adni_v1_pet = ADNI_V1_PET()
        self.adni_v1_fmri = ADNI_V1_Fmri()
        self.dian_v1_t1 = DIAN_V1_T1()
        self.dian_v1_pet = DIAN_V1_PET()

    def convert2minc(self, convertionObj):
        os.environ['PATH'] = ':'.join(libpath.PATH)
        os.environ['LD_LIBRARY_PATH'] = ':'.join(libpath.LD_LIBRARY_PATH)
        os.environ['LD_LIBRARYN32_PATH'] = ':'.join(libpath.LD_LIBRARYN32_PATH)
        os.environ['PERL5LIB'] = ':'.join(libpath.PERL5LIB)
        study = convertionObj.study
        scan_type = sc.ProcessingModalityAndPipelineTypePerStudy[study][convertionObj.scan_type]
        #scan_type = self.get_scanType_forConversion(convertionObj) # PET Conversion is done differently in ADNI
        file_type = convertionObj.file_type
        version = convertionObj.version

        converted = self.convertionScriptsDict[study][scan_type][version][file_type](convertionObj)

        return dict(converted=converted, obj=convertionObj)

    def get_scanType_forConversion(self, conversionObj):
        if conversionObj.scan_type not in cc.studyTypeForConvertionDict[conversionObj.study]:
            return 'T1'
        else:
            return conversionObj.scan_type

    def adni_v1_pet_nii(self, convertionObj):
        return self.adni_v1_pet.convert_nii(convertionObj)

    def adni_v1_pet_dicom(self, convertionObj):
        return self.adni_v1_pet.convert_dicom(convertionObj)

    def adni_v1_pet_v(self, convertionObj):
        return self.adni_v1_pet.convert_v(convertionObj)

    def adni_v1_t1_nii(self, convertionObj):
        return self.adni_v1_t1.convert_nii(convertionObj)

    def adni_v1_t1_dicom(self, convertionObj):
        return self.adni_v1_t1.convert_dicom(convertionObj)

    def adni_v1_t1_v(self, convertionObj):
        return self.adni_v1_t1.convert_v(convertionObj)

    def adni_v1_rsfmri_nii(self, convertionObj):
        return self.adni_v1_fmri.convert_nii(convertionObj)

    def adni_v1_rsfmri_dicom(self, convertionObj):
        return self.adni_v1_fmri.convert_dicom(convertionObj)

    def adni_v1_rsfmri_v(self, convertionObj):
        return self.adni_v1_fmri.convert_v(convertionObj)

    def adni_v1_rsfmri_minc(self, conversionObj):
        return self.adni_v1_fmri.convertMinc(conversionObj)

    def adni_v1_pet_minc(self, conversionObj):
        return self.adni_v1_pet.convertMinc(conversionObj)

    def adni_v1_t1_minc(self, conversionObj):
        return self.adni_v1_t1.convertMinc(conversionObj)

    def dian_v1_t1_dicom(self, conversionObj):
        return self.dian_v1_t1.convert_dicom(conversionObj)

    def dian_v1_pet_dicom(self, conversionObj):
        return self.dian_v1_pet.convert_dicom(conversionObj)
