__author__ = 'sulantha'
import subprocess
import os
import fnmatch
import distutils.dir_util
import distutils.file_util
import shutil
from Utils.PipelineLogger import PipelineLogger
import Config.ConverterConfig as cc

class ADNI_V1_T1:
    def __init__(self):
        pass

    def convert_nii(self, convertionObj):
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
            return 0


    def convert_v(self, convertionObj):
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
            return 0


    def convert_dicom(self, convertionObj):
        rawFile = '{0}/*.dcm'.format(convertionObj.raw_folder)
        outFile = '{0}/{1}_{2}{3}{4}{5}_{6}.mnc'.format(convertionObj.converted_folder, convertionObj.study,
                                                        convertionObj.rid, convertionObj.scan_date.replace('-', ''),
                                                        convertionObj.s_identifier, convertionObj.i_identifier,
                                                        convertionObj.scan_type)
        cmd = '/home/vfonov/quarantine/bin/dcm2mnc32 {0} {1}/../'.format(rawFile, convertionObj.converted_folder)
        PipelineLogger.log('converter', 'info', 'MINC conversion starting for : {0} - {1} - {2} - {3}'.format(convertionObj.study, convertionObj.rid, convertionObj.scan_date, convertionObj.scan_type))
        PipelineLogger.log('converter', 'debug', 'Command : {0}'.format(cmd))
        try:
            shutil.rmtree('{0}/../'.format(convertionObj.converted_folder))
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
        for root, dirnames, filenames in os.walk('{0}/../'.format(convertionObj.converted_folder)):
            for filename in fnmatch.filter(filenames, '*.mnc'):
                distutils.file_util.copy_file(os.path.join(root, filename), convertionObj.converted_folder)
                mincPresent = 1

        if mincPresent:
            PipelineLogger.log('converter', 'info', 'MINC Conversion success : {0} - {1} - {2} - {3}'.format(convertionObj.study, convertionObj.rid, convertionObj.scan_date, convertionObj.scan_type))
            return 1
        else:
            PipelineLogger.log('converter', 'error', 'MINC Conversion unsuccessful : Check log for : {0} - {1} - {2} - {3}'.format(convertionObj.study, convertionObj.rid, convertionObj.scan_date, convertionObj.scan_type))
            return 0


    def convertMinc(self, convertionObj):
        pass
