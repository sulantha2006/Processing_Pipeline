__author__ = 'sulantha'
import subprocess
import os
import fnmatch
import distutils.dir_util
import distutils.file_util
import shutil
import glob
from Utils.PipelineLogger import PipelineLogger


class ADNI_V1_PET:
    def __init__(self):
        pass

    def convert_nii(self, convertionObj):
        rawFile = '{0}/*.nii'.format(convertionObj.raw_folder)
        outFile = '{0}/{1}_{2}{3}{4}{5}_{6}.mnc'.format(convertionObj.converted_folder, convertionObj.study,
                                                        convertionObj.rid, convertionObj.scan_date.replace('-', ''),
                                                        convertionObj.s_identifier, convertionObj.i_identifier,
                                                        convertionObj.scan_type)
        outDynFile = '{0}/{1}_{2}{3}{4}{5}_{6}_Dyn.mnc'.format(convertionObj.converted_folder, convertionObj.study,
                                                        convertionObj.rid, convertionObj.scan_date.replace('-', ''),
                                                        convertionObj.s_identifier, convertionObj.i_identifier,
                                                        convertionObj.scan_type)
        cmd = '/opt/minc/bin/nii2mnc -short {0} {1}'.format(rawFile, outDynFile)
        PipelineLogger.log('converter', 'info',
                           'MINC conversion starting for : {0} - {1} - {2} - {3}'.format(convertionObj.study,
                                                                                         convertionObj.rid,
                                                                                         convertionObj.scan_date,
                                                                                         convertionObj.scan_type))
        PipelineLogger.log('converter', 'debug', 'Command : {0}'.format(cmd))
        try:
            os.remove(outDynFile)
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
        if self.avgTime(outDynFile, outFile):
            PipelineLogger.log('converter', 'info',
                               'MINC Conversion success : {0} - {1} - {2} - {3}'.format(convertionObj.study,
                                                                                        convertionObj.rid,
                                                                                        convertionObj.scan_date,
                                                                                        convertionObj.scan_type))
            return 1
        else:
            PipelineLogger.log('converter', 'error',
                               'MINC Conversion unsuccessful : Check log for : {0} - {1} - {2} - {3}'.format(
                                   convertionObj.study, convertionObj.rid, convertionObj.scan_date,
                                   convertionObj.scan_type))
            return 0

    def convert_v(self, convertionObj):
        rawFile = '{0}/*.v'.format(convertionObj.raw_folder)
        outFile = '{0}/{1}_{2}{3}{4}{5}_{6}.mnc'.format(convertionObj.converted_folder, convertionObj.study,
                                                        convertionObj.rid, convertionObj.scan_date.replace('-', ''),
                                                        convertionObj.s_identifier, convertionObj.i_identifier,
                                                        convertionObj.scan_type)
        outDynFile = '{0}/{1}_{2}{3}{4}{5}_{6}_Dyn.mnc'.format(convertionObj.converted_folder, convertionObj.study,
                                                        convertionObj.rid, convertionObj.scan_date.replace('-', ''),
                                                        convertionObj.s_identifier, convertionObj.i_identifier,
                                                        convertionObj.scan_type)
        cmd = '/opt/minc/bin/ecattominc -short {0} {1}'.format(rawFile, outDynFile)
        PipelineLogger.log('converter', 'info',
                           'MINC conversion starting for : {0} - {1} - {2} - {3}'.format(convertionObj.study,
                                                                                         convertionObj.rid,
                                                                                         convertionObj.scan_date,
                                                                                         convertionObj.scan_type))
        PipelineLogger.log('converter', 'debug', 'Command : {0}'.format(cmd))
        try:
            os.remove(outDynFile)
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
        if self.avgTime(outDynFile, outFile):
            PipelineLogger.log('converter', 'info',
                               'MINC Conversion success : {0} - {1} - {2} - {3}'.format(convertionObj.study,
                                                                                        convertionObj.rid,
                                                                                        convertionObj.scan_date,
                                                                                        convertionObj.scan_type))
            return 1
        else:
            PipelineLogger.log('converter', 'error',
                               'MINC Conversion unsuccessful : Check log for : {0} - {1} - {2} - {3}'.format(
                                   convertionObj.study, convertionObj.rid, convertionObj.scan_date,
                                   convertionObj.scan_type))
            return 0

    def convert_dicom(self, convertionObj):
        outFile = '{0}/{1}_{2}{3}{4}{5}_{6}.mnc'.format(convertionObj.converted_folder, convertionObj.study,
                                                        convertionObj.rid, convertionObj.scan_date.replace('-', ''),
                                                        convertionObj.s_identifier, convertionObj.i_identifier,
                                                        convertionObj.scan_type)
        outDynFile = '{0}/{1}_{2}{3}{4}{5}_{6}_Dyn.mnc'.format(convertionObj.converted_folder, convertionObj.study,
                                                        convertionObj.rid, convertionObj.scan_date.replace('-', ''),
                                                        convertionObj.s_identifier, convertionObj.i_identifier,
                                                        convertionObj.scan_type)

        cmd = 'source /opt/minc-toolkit/minc-toolkit-config.sh; Converters/ConversionScripts/BashScripts/ADNI_V1_PET_dicom {0} {1} {2} {3}'.format(convertionObj.raw_folder, convertionObj.converted_folder, outDynFile, outFile)
        PipelineLogger.log('converter', 'info',
                           'MINC conversion starting for : {0} - {1} - {2} - {3}'.format(convertionObj.study,
                                                                                         convertionObj.rid,
                                                                                         convertionObj.scan_date,
                                                                                         convertionObj.scan_type))
        PipelineLogger.log('converter', 'debug', 'Command : {0}'.format(cmd))
        try:
            shutil.rmtree('{0}/../'.format(convertionObj.converted_folder))
        except:
            pass
        try:
            distutils.dir_util.mkpath(convertionObj.converted_folder)
        except:
            pass
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable='/bin/bash')
        out, err = p.communicate()
        PipelineLogger.log('converter', 'debug', 'Conversion Log Output : \n{0}'.format(out))
        PipelineLogger.log('converter', 'debug', 'Conversion Log Err : \n{0}'.format(err))

        if self.avgTime(outDynFile, outFile):
            PipelineLogger.log('converter', 'info',
                               'MINC Conversion success : {0} - {1} - {2} - {3}'.format(convertionObj.study,
                                                                                        convertionObj.rid,
                                                                                        convertionObj.scan_date,
                                                                                        convertionObj.scan_type))
            return 1
        else:
            PipelineLogger.log('converter', 'error',
                               'MINC Conversion unsuccessful : Check log for : {0} - {1} - {2} - {3}'.format(
                                   convertionObj.study, convertionObj.rid, convertionObj.scan_date,
                                   convertionObj.scan_type))
            return 0

    def convertMinc(self, convertionObj):
        PipelineLogger.log('converter', 'info',
                           'MINC conversion starting for : {0} - {1} - {2} - {3}'.format(convertionObj.study,
                                                                                         convertionObj.rid,
                                                                                         convertionObj.scan_date,
                                                                                         convertionObj.scan_type))
        rawFile = '{0}/*.mnc'.format(convertionObj.raw_folder)
        mncList = glob.glob(rawFile)
        outFile = '{0}/{1}_{2}{3}{4}{5}_{6}.mnc'.format(convertionObj.converted_folder, convertionObj.study,
                                                        convertionObj.rid, convertionObj.scan_date.replace('-', ''),
                                                        convertionObj.s_identifier, convertionObj.i_identifier,
                                                        convertionObj.scan_type)
        if len(mncList) == 0:
            PipelineLogger.log('converter', 'error',
                               'MINC Conversion unsuccessful : Check log for : {0} - {1} - {2} - {3}'.format(
                                   convertionObj.study, convertionObj.rid, convertionObj.scan_date,
                                   convertionObj.scan_type))
            return 0
        elif len(mncList) == 1:
            PipelineLogger.log('converter', 'error',
                               'PET Conversion MINC file as INPUT. Only 1 MINC found. Checking for time dimension  - {0} - {1} - {2} - {3}'.format(convertionObj.study, convertionObj.rid, convertionObj.scan_date, convertionObj.scan_type))
            checkTimeDimCmd = '/opt/minc-toolkit/bin/mincinfo {0} | grep time'.format(mncList[0])
            p_t = subprocess.Popen(checkTimeDimCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out_t, err_t = p_t.communicate()
            PipelineLogger.log('converter', 'debug', 'Check time dim Output : \n{0}'.format(out_t))
            PipelineLogger.log('converter', 'debug', 'Check time dim Err : \n{0}'.format(err_t))
            if 'time' in out_t.decode("utf-8")  or 'time' in err_t.decode("utf-8") :
                PipelineLogger.log('converter', 'info',
                               'PET Conversion MINC file as INPUT. Only 1 MINC found. Time dimension found. Mincaverage on time. ')
                if self.avgTime(mncList[0], outFile):
                    PipelineLogger.log('converter', 'info',
                                       'MINC Conversion success : {0} - {1} - {2} - {3}'.format(convertionObj.study,
                                                                                                convertionObj.rid,
                                                                                                convertionObj.scan_date,
                                                                                                convertionObj.scan_type))
                    return 1
                else:
                    PipelineLogger.log('converter', 'error',
                                       'MINC Conversion unsuccessful : Check log for : {0} - {1} - {2} - {3}'.format(
                                           convertionObj.study, convertionObj.rid, convertionObj.scan_date,
                                           convertionObj.scan_type))
                    return 0
        else:
            PipelineLogger.log('converter', 'info', 'More than 1 MINC file found. Concat on time dimension.'.format(mncList))
            outDynFile = '{0}/{1}_{2}{3}{4}{5}_{6}_Dyn.mnc'.format(convertionObj.converted_folder, convertionObj.study,
                                                        convertionObj.rid, convertionObj.scan_date.replace('-', ''),
                                                        convertionObj.s_identifier, convertionObj.i_identifier,
                                                        convertionObj.scan_type)
            cmd = '/opt/minc/bin/mincconcat -short -concat_dimension time {0} {1}'.format(rawFile, outDynFile)
            PipelineLogger.log('converter', 'debug', 'Command : {0}'.format(cmd))
            try:
                os.remove(outDynFile)
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

            if self.avgTime(outDynFile, outFile):
                PipelineLogger.log('converter', 'info',
                                   'MINC Conversion success : {0} - {1} - {2} - {3}'.format(convertionObj.study,
                                                                                            convertionObj.rid,
                                                                                            convertionObj.scan_date,
                                                                                            convertionObj.scan_type))
                return 1
            else:
                PipelineLogger.log('converter', 'error',
                                   'MINC Conversion unsuccessful : Check log for : {0} - {1} - {2} - {3}'.format(
                                       convertionObj.study, convertionObj.rid, convertionObj.scan_date,
                                       convertionObj.scan_type))
                return 0

    def avgTime(self, inputMNC, outputMNC):
        avgCMD = '/opt/minc-toolkit/bin/mincaverage -short -avgdim time {0} {1}'.format(inputMNC, outputMNC)
        p = subprocess.Popen(avgCMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        PipelineLogger.log('converter', 'debug', 'Averaging Time Output : \n{0}'.format(out))
        PipelineLogger.log('converter', 'debug', 'Averaging Time Err : \n{0}'.format(err))
        if os.path.exists(outputMNC):
            return 1
        else:
            return 0
