__author__ = 'sulantha'
import subprocess
import os
import fnmatch
import distutils.dir_util
import distutils.file_util
import shutil
from Utils.PipelineLogger import PipelineLogger

class Raw2MINCConverter:
    def __init__(self):
        self.convertionScriptsDict = {'ADNI':
                             {'AV45': {'V1': {'nifti': self.adni_v1_pet_nii,
                                              'dicom': self.adni_v1_pet_dicom,
                                              'v': self.adni_v1_pet_v}},
                              'FDG': {'V1': {'nifti': self.adni_v1_pet_nii,
                                             'dicom': self.adni_v1_pet_dicom,
                                             'v': self.adni_v1_pet_v}},
                              'T1': {'V1': {'nifti': self.adni_v1_t1_nii,
                                            'dicom': self.adni_v1_t1_dicom,
                                            'v': self.adni_v1_t1_v}},
                              'rsfmri': {'V1': {'nifti': self.adni_v1_rsfmri_nii,
                                            'dicom': self.adni_v1_rsfmri_dicom,
                                            'v': self.adni_v1_rsfmri_v}}
                              }}

    def convert2minc(self, convertionObj):
        converted = 0
        study = convertionObj.study
        scan_type = convertionObj.scan_type
        file_type = convertionObj.file_type
        version = convertionObj.version

        # PET Conversion is done differently in ADNI
        if study == 'ADNI' and (scan_type != 'AV45' or scan_type != 'FDG' or scan_type != 'ext-rsfmri' or scan_type != 'rsfmri'):
            scan_type = 'T1'

        if study == 'ADNI' and (scan_type == 'ext-rsfmri' or 'rsfmri'):
            scan_type = 'rsfmri'

        if file_type != 'minc':
            converted = self.convertionScriptsDict[study][scan_type][version][file_type](convertionObj)
        return converted

    def adni_v1_pet_nii(self, convertionObj):
        pass

    def adni_v1_pet_dicom(self, convertionObj):
        pass

    def adni_v1_pet_v(self, convertionObj):
        pass

    def adni_v1_t1_nii(self, convertionObj):
        rawFile = '{0}/*.nii'.format(convertionObj.raw_folder)
        outFile = '{0}/{1}_{2}{3}{4}{5}_{6}.mnc'.format(convertionObj.converted_folder, convertionObj.study,
                                                        convertionObj.rid, convertionObj.scan_date.replace('-', ''),
                                                        convertionObj.s_identifier, convertionObj.i_identifier,
                                                        convertionObj.scan_type)
        cmd = '/opt/minc/bin/nii2mnc -short {0} {1}'.format(rawFile, outFile)
        PipelineLogger.log('converter', 'info', 'MINC conversion starting for : {0} - {1} - {2} - {3}'.format(convertionObj.study, convertionObj.rid, convertionObj.scan_date, convertionObj.scan_type))
        PipelineLogger.log('converter', 'debug', 'Command : {0}'.format(cmd))
        try:
            os.remove(outFile)
        except:
            pass
        try:
            distutils.dir_util.mkpath(convertionObj.converted_folder)
        except:
            pass
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        PipelineLogger.log('converter', 'debug', 'Conversion Log Output : \n{0}'.format(out))
        PipelineLogger.log('converter', 'debug', 'Conversion Log Err : \n{0}'.format(err))
        if os.path.exists(outFile):
            PipelineLogger.log('converter', 'info', 'MINC Conversion success : {0} - {1} - {2} - {3}'.format(convertionObj.study, convertionObj.rid, convertionObj.scan_date, convertionObj.scan_type))
            return 1
        else:
            PipelineLogger.log('converter', 'error', 'MINC Conversion unsuccessful : Check log for : {0} - {1} - {2} - {3}'.format(convertionObj.study, convertionObj.rid, convertionObj.scan_date, convertionObj.scan_type))


    def adni_v1_t1_dicom(self, convertionObj):
        rawFile = '{0}/*.dcm'.format(convertionObj.raw_folder)
        outFile = '{0}/{1}_{2}{3}{4}{5}_{6}.mnc'.format(convertionObj.converted_folder, convertionObj.study,
                                                        convertionObj.rid, convertionObj.scan_date.replace('-', ''),
                                                        convertionObj.s_identifier, convertionObj.i_identifier,
                                                        convertionObj.scan_type)
        cmd = '/home/vfonov/quarantine/bin/dcm2mnc32 {0} {1}/../'.format(rawFile, convertionObj.converted_folder)
        PipelineLogger.log('converter', 'info', 'MINC conversion starting for : {0} - {1} - {2} - {3}'.format(convertionObj.study, convertionObj.rid, convertionObj.scan_date, convertionObj.scan_type))
        PipelineLogger.log('converter', 'debug', 'Command : {0}'.format(cmd))
        try:
            shutil.rmtree('{1}/../'.format(convertionObj.converted_folder))
        except:
            pass
        try:
            distutils.dir_util.mkpath(convertionObj.converted_folder)
        except:
            pass
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        PipelineLogger.log('converter', 'debug', 'Conversion Log Output : \n{0}'.format(out))
        PipelineLogger.log('converter', 'debug', 'Conversion Log Err : \n{0}'.format(err))

        mincPresent = 0
        for root, dirnames, filenames in os.walk('{1}/../'.format(convertionObj.converted_folder)):
            for filename in fnmatch.filter(filenames, '*.mnc'):
                distutils.file_util.copy_file(os.path.join(root, filename), convertionObj.converted_folder)
                mincPresent = 1

        if mincPresent:
            PipelineLogger.log('converter', 'info', 'MINC Conversion success : {0} - {1} - {2} - {3}'.format(convertionObj.study, convertionObj.rid, convertionObj.scan_date, convertionObj.scan_type))
            return 1
        else:
            PipelineLogger.log('converter', 'error', 'MINC Conversion unsuccessful : Check log for : {0} - {1} - {2} - {3}'.format(convertionObj.study, convertionObj.rid, convertionObj.scan_date, convertionObj.scan_type))

    def adni_v1_t1_v(self, convertionObj):
        rawFile = '{0}/*.v'.format(convertionObj.raw_folder)
        outFile = '{0}/{1}_{2}{3}{4}{5}_{6}.mnc'.format(convertionObj.converted_folder, convertionObj.study,
                                                        convertionObj.rid, convertionObj.scan_date.replace('-', ''),
                                                        convertionObj.s_identifier, convertionObj.i_identifier,
                                                        convertionObj.scan_type)
        cmd = '/opt/minc/bin/ecattominc -short {0} {1}'.format(rawFile, outFile)
        PipelineLogger.log('converter', 'info', 'MINC conversion starting for : {0} - {1} - {2} - {3}'.format(convertionObj.study, convertionObj.rid, convertionObj.scan_date, convertionObj.scan_type))
        PipelineLogger.log('converter', 'debug', 'Command : {0}'.format(cmd))
        try:
            os.remove(outFile)
        except:
            pass
        try:
            distutils.dir_util.mkpath(convertionObj.converted_folder)
        except:
            pass
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        PipelineLogger.log('converter', 'debug', 'Conversion Log Output : \n{0}'.format(out))
        PipelineLogger.log('converter', 'debug', 'Conversion Log Err : \n{0}'.format(err))
        if os.path.exists(outFile):
            PipelineLogger.log('converter', 'info', 'MINC Conversion success : {0} - {1} - {2} - {3}'.format(convertionObj.study, convertionObj.rid, convertionObj.scan_date, convertionObj.scan_type))
            return 1
        else:
            PipelineLogger.log('converter', 'error', 'MINC Conversion unsuccessful : Check log for : {0} - {1} - {2} - {3}'.format(convertionObj.study, convertionObj.rid, convertionObj.scan_date, convertionObj.scan_type))

    def adni_v1_rsfmri_nii(self, convertionObj):
        pass

    def adni_v1_rsfmri_dicom(self, convertionObj):
        pass

    def adni_v1_rsfmri_v(self, convertionObj):
        pass