__author__ = 'sulantha'
import subprocess
import os
import fnmatch
import distutils.dir_util
import distutils.file_util
import shutil
import glob
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
            copyMIncCmd = '/opt/minc-toolkit/bin/mincaverage -short {0} {1}'.format(mncList[0], outFile)
            p_t = subprocess.Popen(copyMIncCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out_t, err_t = p_t.communicate()
            PipelineLogger.log('converter', 'debug', 'Mincncopy Output : \n{0}'.format(out_t))
            PipelineLogger.log('converter', 'debug', 'Mincncopy Err : \n{0}'.format(err_t))
            PipelineLogger.log('converter', 'info',
                               'MINC Conversion success : {0} - {1} - {2} - {3}'.format(convertionObj.study,
                                                                                        convertionObj.rid,
                                                                                        convertionObj.scan_date,
                                                                                        convertionObj.scan_type))
            return 1
        else:
            PipelineLogger.log('converter', 'critical', 'More than 1 MINC file found for 3D scan. Please check {0}.'.format(mncList))
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
            PipelineLogger.log('converter', 'error', 'T1 Conversion MINC file as INPUT. Only 1 MINC found. Checking for time dimension ')
            checkTimeDimCmd = '/opt/minc-toolkit/bin/mincinfo {0} | grep time'.format(mncList[0])
            p_t = subprocess.Popen(checkTimeDimCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out_t, err_t = p_t.communicate()
            PipelineLogger.log('converter', 'debug', 'Check time dim Output : \n{0}'.format(out_t))
            PipelineLogger.log('converter', 'debug', 'Check time dim Err : \n{0}'.format(err_t))
            if 'time' in out_t.decode("utf-8")  or 'time' in err_t.decode("utf-8") :
                PipelineLogger.log('converter', 'info',
                               'T1 Conversion MINC file as INPUT. Only 1 MINC found. Time dimension found. Conversion failed ')
                return 0
            else:
                try:
                    os.remove(outFile)
                except:
                    pass
                try:
                    distutils.dir_util.mkpath(convertionObj.converted_folder)
                except:
                    pass
                copyMIncCmd = '/opt/minc-toolkit/bin/mincaverage -short {0} {1}'.format(mncList[0], outFile)
                p_t = subprocess.Popen(copyMIncCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out_t, err_t = p_t.communicate()
                PipelineLogger.log('converter', 'debug', 'Mincncopy Output : \n{0}'.format(out_t.decode("utf-8")))
                PipelineLogger.log('converter', 'debug', 'Mincncopy Err : \n{0}'.format(err_t.decode("utf-8")))
                if err_t.decode("utf-8") != '':
                    PipelineLogger.log('converter', 'error',
                                   '$$$$$ MINC Conversion failed : {0} - {1} - {2} - {3} - {4}'.format(convertionObj.study,
                                                                                            convertionObj.rid,
                                                                                            convertionObj.scan_date,
                                                                                            convertionObj.scan_type, err_t.decode("utf-8")))
                    return 0
                PipelineLogger.log('converter', 'info',
                                   'MINC Conversion success : {0} - {1} - {2} - {3}'.format(convertionObj.study,
                                                                                            convertionObj.rid,
                                                                                            convertionObj.scan_date,
                                                                                            convertionObj.scan_type))
                return 1
        else:
            PipelineLogger.log('converter', 'critical', 'More than 1 MINC file found. Please check {0}.'.format(mncList))
            return 0
