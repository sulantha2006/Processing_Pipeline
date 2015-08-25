__author__ = 'wang'
import subprocess
import os
import fnmatch
import distutils.dir_util
import distutils.file_util
import shutil
import glob
from Utils.PipelineLogger import PipelineLogger
import Config.ConverterConfig


class ADNI_V1_Fmri:
    def __init__(self):
        pass

    def convert_nii(self, convertionObj):
        rawFile = '{0}/*.nii*'.format(convertionObj.raw_folder)
        outFile = '{0}/{1}_{2}{3}{4}{5}_{6}.mnc'.format(convertionObj.converted_folder, convertionObj.study,
                                                        convertionObj.rid, convertionObj.scan_date.replace('-', ''),
                                                        convertionObj.s_identifier, convertionObj.i_identifier,
                                                        convertionObj.scan_type)
        # Run nii2mnc
        cmd = '{0} {1} {2}/../'.format('mv ' + rawFile + ' outFile')
        PipelineLogger.log('converter', 'info',
                           'nii2mnc conversion starting for : {0} - {1} - {2} - {3}'.format(convertionObj.study,
                                                                                         convertionObj.rid,
                                                                                         convertionObj.scan_date,
                                                                                         convertionObj.scan_type))
        PipelineLogger.log('converter', 'debug', 'Command : {0}'.format(cmd))

        cmd = '%s %s %s' % (Config.ConverterConfig.niiToMnc_exec, rawFile, outFile)
        self.runShellCommand(cmd)
        self.checkMncFile(outFile) # Check whether the fMRI file has a time component/axis

    def convert_v(self, convertionObj):
        pass

    def convert_dicom(self, convertionObj):
        rawFolder = convertionObj.raw_folder
        outFile = '{0}/{1}_{2}{3}{4}{5}_{6}.mnc'.format(convertionObj.converted_folder, convertionObj.study,
                                                        convertionObj.rid, convertionObj.scan_date.replace('-', ''),
                                                        convertionObj.s_identifier, convertionObj.i_identifier,
                                                        convertionObj.scan_type)

        self.createNewFolder(convertionObj.converted_folder) # Create output folder
        tempFolder = convertionObj.converted_folder + '/../temp'  # Generate path for temp folder
        self.createNewFolder(tempFolder)  # Create temp folder

        # Move all the non-dicom stuff out of the original folder into tempFolder
        otherFiles = self.removeOtherFilesInFolder(rawFolder, '.dcm', tempFolder)
        # Run dcm2nii
        cmd = Config.ConverterConfig.dcmToNii_exec + ' -a N -e N -p N -g N -o ' + tempFolder + '/ -v Y ' + rawFolder
        PipelineLogger.log('converter', 'info',
                           'dcm2nii conversion starting for : {0} - {1} - {2} - {3}'.format(convertionObj.study,
                                                                                         convertionObj.rid,
                                                                                         convertionObj.scan_date,
                                                                                         convertionObj.scan_type))
        PipelineLogger.log('converter', 'debug', 'Command : {0}'.format(cmd))
        self.runShellCommand(cmd)
        # Move all the non-dicom stuff back into the original folder
        self.addBackOtherFiles(rawFolder, otherFiles, tempFolder)

        # Run nii2mnc
        cmd = '{0} {1} {2}/../'.format(Config.ConverterConfig.niiToMnc_exec, rawFolder, convertionObj.converted_folder)		
        PipelineLogger.log('converter', 'info',
                           'nii2mnc conversion starting for : {0} - {1} - {2} - {3}'.format(convertionObj.study,
                                                                                         convertionObj.rid,
                                                                                         convertionObj.scan_date,
                                                                                         convertionObj.scan_type))
        PipelineLogger.log('converter', 'debug', 'Command : {0}'.format(cmd))
        iterator = 1
        for niiFile in glob.glob(tempFolder + '/*.nii'):
            tempOutFile = outFile.replace('.mnc', '_run' + str(iterator) + '.mnc')
            cmd = '%s %s %s' % (Config.ConverterConfig.niiToMnc_exec, niiFile, tempOutFile)
            self.runShellCommand(cmd)
            self.checkMncFile(tempOutFile) # Check whether the fMRI files have a time component/axis
            iterator += 1
        # Delete Temporary Folder
        self.deleteFolder(tempFolder)

        # Check how many mnc files were generated
        mncList = []
        for root, dirnames, filenames in os.walk(convertionObj.converted_folder):
            for filename in fnmatch.filter(filenames, '*.mnc'):
                mncList.append(os.path.join(root, filename))
        if len(mncList) == 0:
            PipelineLogger.log('converter', 'error',
                               'MINC Conversion unsuccessful : Check log for : {0} - {1} - {2} - {3}'.format(
                                   convertionObj.study, convertionObj.rid, convertionObj.scan_date,
                                   convertionObj.scan_type))
            return 0
        else:
            return 1

    def convertMinc(self, convertionObj):
        rawFile = '{0}/*.mnc'.format(convertionObj.raw_folder)
        outFile = '{0}/{1}_{2}{3}{4}{5}_{6}.mnc'.format(convertionObj.converted_folder, convertionObj.study,
                                                        convertionObj.rid, convertionObj.scan_date.replace('-', ''),
                                                        convertionObj.s_identifier, convertionObj.i_identifier,
                                                        convertionObj.scan_type)
        # Move files
        cmd = '{0} {1} {2}/../'.format('mv ' + rawFile + ' ' + outFile)
        PipelineLogger.log('converter', 'info',
                           'MINC transfer starting for : {0} - {1} - {2} - {3}'.format(convertionObj.study,
                                                                                         convertionObj.rid,
                                                                                         convertionObj.scan_date,
                                                                                         convertionObj.scan_type))
        PipelineLogger.log('converter', 'debug', 'Command : {0}'.format(cmd))
        self.runShellCommand(cmd)

    def createNewFolder(self, folder):
        self.deleteFolder(folder)
        try:
            distutils.dir_util.mkpath(folder)
        except:
            pass

    def deleteFolder(self, folder):
        try:
            shutil.rmtree(folder)
        except:
            pass

    def checkMncFile(self, mncFile):
        cmd = Config.ConverterConfig.mincSource_exec + '; mincinfo ' + mncFile + ' | grep \"time\" '
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if not out: # If no output, string empty
            PipelineLogger.log('converter', 'debug', mncFile + 'does not have a time axis!')
            os.remove(mncFile)

    def runShellCommand(self, cmd):
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        PipelineLogger.log('converter', 'debug', 'Conversion Log Output : \n{0}'.format(out))
        PipelineLogger.log('converter', 'debug', 'Conversion Log Err : \n{0}'.format(err))

    def removeOtherFilesInFolder(self, original_folder, extToKeep, temp_file_folder):
        otherFiles = []
        for file in os.listdir(original_folder):
            if not file.endswith(extToKeep):
                shutil.move(original_folder + "/" + file, temp_file_folder)
                otherFiles.append(file)
        return otherFiles

    def addBackOtherFiles(self, folderPath, otherFiles, temp_file_folder):
        for file in otherFiles:
            shutil.move(temp_file_folder + '/' + file, folderPath + "/")
