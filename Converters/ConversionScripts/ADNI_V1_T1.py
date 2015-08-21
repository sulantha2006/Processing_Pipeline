__author__ = 'sulantha'
import subprocess
import os
import fnmatch
import distutils.dir_util
import distutils.file_util
import shutil
from Utils.PipelineLogger import PipelineLogger


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
        PipelineLogger.log('converter', 'info',
                           'MINC conversion starting for : {0} - {1} - {2} - {3}'.format(convertionObj.study,
                                                                                         convertionObj.rid,
                                                                                         convertionObj.scan_date,
                                                                                         convertionObj.scan_type))
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
        cmd = '/opt/minc/bin/ecattominc -short {0} {1}'.format(rawFile, outFile)
        PipelineLogger.log('converter', 'info',
                           'MINC conversion starting for : {0} - {1} - {2} - {3}'.format(convertionObj.study,
                                                                                         convertionObj.rid,
                                                                                         convertionObj.scan_date,
                                                                                         convertionObj.scan_type))
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
        rawFile = '{0}/*.dcm'.format(convertionObj.raw_folder)
        outFile = '{0}/{1}_{2}{3}{4}{5}_{6}.mnc'.format(convertionObj.converted_folder, convertionObj.study,
                                                        convertionObj.rid, convertionObj.scan_date.replace('-', ''),
                                                        convertionObj.s_identifier, convertionObj.i_identifier,
                                                        convertionObj.scan_type)
        cmd = '/home/vfonov/quarantine/bin/dcm2mnc32 {0} {1}/../'.format(rawFile, convertionObj.converted_folder)
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
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        PipelineLogger.log('converter', 'debug', 'Conversion Log Output : \n{0}'.format(out))
        PipelineLogger.log('converter', 'debug', 'Conversion Log Err : \n{0}'.format(err))

        mncList = []
        for root, dirnames, filenames in os.walk('{0}/../'.format(convertionObj.converted_folder)):
            for filename in fnmatch.filter(filenames, '*.mnc'):
                mncList.append(os.path.join(root, filename))
        if len(mncList) == 0:
            PipelineLogger.log('converter', 'error',
                               'MINC Conversion unsuccessful : Check log for : {0} - {1} - {2} - {3}'.format(
                                   convertionObj.study, convertionObj.rid, convertionObj.scan_date,
                                   convertionObj.scan_type))
            return 0
        elif len(mncList) == 1:
            distutils.file_util.copy_file(mncList[0], outFile)
            PipelineLogger.log('converter', 'info',
                               'MINC Conversion success : {0} - {1} - {2} - {3}'.format(convertionObj.study,
                                                                                        convertionObj.rid,
                                                                                        convertionObj.scan_date,
                                                                                        convertionObj.scan_type))
            return 1
        else:
            checkTimeDimCmd = '/opt/minc-toolkit/bin/mincinfo {0} | grep time'.format(mncList[0])
            p_t = subprocess.Popen(checkTimeDimCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out_t, err_t = p_t.communicate()
            PipelineLogger.log('converter', 'debug', 'Check time dim Output : \n{0}'.format(out_t))
            PipelineLogger.log('converter', 'debug', 'Check time dim Err : \n{0}'.format(err_t))
            if 'time' in out_t or 'time' in err_t:
                concatCMD = '/opt/minc/bin/mincconcat -short -concat_dimension time {0}/*.mnc {1}'.format(convertionObj.converted_folder, outFile)
                p_c = subprocess.Popen(concatCMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out_c, err_c = p_c.communicate()
                PipelineLogger.log('converter', 'debug', 'MincConcat Output : \n{0}'.format(out_c))
                PipelineLogger.log('converter', 'debug', 'MincConcat Err : \n{0}'.format(err_c))
            else:
                PipelineLogger.log('converter', 'error', 'T1 - dicom conversion failed : Many unlinked MINC files')
                PipelineLogger.log('converter', 'error',
                               'MINC Conversion unsuccessful : Check log for : {0} - {1} - {2} - {3}'.format(
                                   convertionObj.study, convertionObj.rid, convertionObj.scan_date,
                                   convertionObj.scan_type))
                return 0

        if os.path.exists(outFile):
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
        pass
