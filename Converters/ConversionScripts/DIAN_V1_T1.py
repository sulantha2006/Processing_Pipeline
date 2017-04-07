import subprocess
import os
import fnmatch
import distutils.dir_util
import distutils.file_util
import shutil
from Utils.PipelineLogger import PipelineLogger


class DIAN_V1_T1:
    def __init__(self):
        pass

    def convert_dicom(self, convertionObj):
        rawFile = '{0}/*.dcm'.format(convertionObj.raw_folder)
        outFile = '{0}/{1}_{2}{3}{4}{5}_{6}.mnc'.format(convertionObj.converted_folder, convertionObj.study,
                                                        convertionObj.rid, convertionObj.scan_date.replace('-', ''),
                                                        convertionObj.s_identifier, convertionObj.i_identifier,
                                                        convertionObj.scan_type)
        cmd = '/opt/minc-1.9.15/bin/dcm2mnc {0} {1}/../'.format(rawFile, convertionObj.converted_folder)
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
            copyMIncCmd = '/opt/minc-1.9.15/bin/mincaverage -short {0} {1}'.format(mncList[0], outFile)
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