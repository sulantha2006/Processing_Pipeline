__author__ = 'wang'

import subprocess, os, glob, socket, shutil
from Utils.DbUtils import DbUtils
import Config.PipelineConfig as config
import distutils.dir_util
from Manager.QSubJob import QSubJob
from Manager.QSubJobHanlder import QSubJobHandler
from Utils.PipelineLogger import PipelineLogger
import socket
from Pipelines.ADNI_T1.ADNI_T1_Fmri_Helper import ADNI_T1_Fmri_Helper # Different for Fmri and PET
import glob

class Niak:
    def __init__(self):
        self.DBClient = DbUtils()

    def getScanType(self, processingItemObj):
        r = self.DBClient.executeAllResults("SELECT SCAN_TYPE FROM Conversion WHERE STUDY = '{0}' AND RID = '{1}' "
                                        "AND SCAN_DATE = '{2}' AND S_IDENTIFIER = '{3}' "
                                        "AND I_IDENTIFIER = '{4}'".format(processingItemObj.study,
                                                                          processingItemObj.subject_rid,
                                                                          processingItemObj.scan_date,
                                                                          processingItemObj.s_identifier,
                                                                          processingItemObj.i_identifier))
        return r[0][0]

    def process(self, processingItemObj):
        try:
            matlabScript, nativeFileName, niakFolder = self.readTemplateFile(processingItemObj)
            PipelineLogger.log('manager', 'info', 'NIAK starting for {0}'.format(nativeFileName))
        except:
            return 0

        # Delete PIPE.lock file, if is exists
        if os.path.isfile("%s/preprocessing/logs/PIPE.lock" % niakFolder):
            os.remove("%s/preprocessing/logs/PIPE.lock" % niakFolder)

        success = self.executeScript(processingItemObj, matlabScript, niakFolder)

        #### After, if Niak succeeded, concatenate all runs together using combiningRuns
        if False:
            if success:
                self.combiningRuns(processingItemObj)
            else:
                PipelineLogger.log()
                #### Report error

    def readTemplateFile(self, processingItemObj):
        niakTemplateFile = os.path.dirname(__file__) + '/MatlabScripts/niakPreprocessingTemplate.m'

        niakFolder = '{0}/niak'.format(processingItemObj.root_folder)
        logDir = '{0}/logs'.format(processingItemObj.root_folder)

        # Get the corresponding subject-space MRI path
        correspondingMRI = self.findCorrespondingMRI(processingItemObj)
        if not correspondingMRI: # If there is no corresponding MRI file
            return 0
        else:
            anat = correspondingMRI + '/civet/native/*t1.mnc'  # correspondingMRI[9] returns the root folder of the T1 MRI file
            anat = glob.glob(anat)[0]

        # Get all subjects
        patientInfo = "files_in.subject1.anat = '%s';" % (anat)
        for fmri in glob.glob(processingItemObj.converted_folder + '/*.mnc*'):
            iteration = fmri[fmri.rindex('_run') + 4 : fmri.rindex('.mnc')]
            patientInfo = patientInfo + "\nfiles_in.subject1.fmri.session1{%s} = '%s'" % (iteration, fmri)

        # Read templateFileWithInformation
        with open(niakTemplateFile, 'r') as templateFile:
            templateFileWithInformation = templateFile.read()
            templateFile.close()

        # Replacing template placeholders with information
        replacing_dict = {'%{patient_information}': patientInfo,
                          '%{opt.folder_out}': niakFolder,
                          '%{niak_location}': config.niak_location,
                          '%{nu_correct}': processingItemObj.parameters['nu_correct']
                          }
        templateFileWithInformation = self.replaceString(templateFileWithInformation, replacing_dict)

        return templateFileWithInformation, fmri, niakFolder

    def findCorrespondingMRI(self, processingItemObj):
		# Find Matching T1
        matching_t1 = ADNI_T1_Fmri_Helper().getMatchingT1(processingItemObj)
        if not matching_t1:
            return 0
			
		# Find out whether T1 has been processed
        processed = ADNI_T1_Fmri_Helper().checkProcessed(matching_t1)
        if not processed:
            PipelineLogger.log('root', 'error', 'FMRI cannot be processed due to matching T1 not being processed.')
            return 0
        else:
            return processed

    def replaceString(self, templateText, replacing_dict):
        for query, replacedInto in replacing_dict.items():
            templateText = templateText.replace(query, replacedInto)
        return templateText


    def createMatlabFile(self, matlabScript, niakFolder):
        matlab_file_path = niakFolder + '/preprocessing_script.m'
        if not os.path.exists(niakFolder):
            os.makedirs(niakFolder)
        with open(matlab_file_path, 'w') as matlab_file:  # Overwrite previous matlab script file if it already existed
            matlab_file.write(matlabScript)
        return matlab_file_path


    def executeScript(self, processingItemObj, matlabScript, niakFolder):

        # Create a matlab file to be called later on
        matlabFile = self.createMatlabFile(matlabScript, niakFolder)

        # Prepare matlab command
        matlabCommand = '%s run %s;exit"' % (config.matlab_call, matlabFile)

        # Creating log folder
        logDir = '{0}/logs'.format(processingItemObj.root_folder)
        try:
            distutils.dir_util.mkpath(logDir)
        except Exception as e:
            PipelineLogger.log('manager', 'error', 'Error in creating log folder \n {0}'.format(e))
            return 0

        # Create list of files that should be present
        fmri_file = niakFolder + '/fmri/fmri_subject1_session1_run1.mnc'
        anat_ln_file = niakFolder + '/anat/anat_subject1_nuc_stereolin.mnc'
        anat_nl_file = niakFolder + '/anat/anat_subject1_nuc_stereonl.mnc'
        fmri_mean_file = niakFolder + '/anat/func_subject1_mean_stereonl.mnc'
        func_coregister = niakFolder + '/quality_control/group_coregistration/func_tab_qc_coregister_stereonl.csv'
        anat_ln_coregister = niakFolder + '/quality_control/group_coregistration/anat_tab_qc_coregister_stereolin.csv'
        anat_nl_coregister = niakFolder + '/quality_control/group_coregistration/anat_tab_qc_coregister_stereonl.csv'
        func_motion = niakFolder + '/quality_control/group_motion/qc_scrubbing_group.csv'
        outputFiles = ' '.join([fmri_file, anat_ln_file, anat_nl_file, fmri_mean_file, func_coregister,
                                anat_ln_coregister, anat_nl_coregister, func_motion])

        # Prepare bash command
        id = '{0}{1}{2}{3}'.format(processingItemObj.subject_rid, processingItemObj.scan_date.replace('-', ''),
                                   processingItemObj.s_identifier, processingItemObj.i_identifier)
        command = '%s; Pipelines/ADNI_Fmri/MatlabScripts/startMatlabScript.sh %s %s %s %s %s %s %s' % \
                  (config.sourcing, id, matlabCommand, niakFolder, logDir, socket.gethostname(), '50500', outputFiles)

        # Create NIAK folder
        if not os.path.exists(niakFolder):
            os.makedirs(niakFolder)

        # Run converter command
        PipelineLogger.log('converter', 'debug', 'Command : {0}'.format(command))
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable='/bin/bash')
        out, err = p.communicate()
        PipelineLogger.log('converter', 'debug', 'Conversion Log Output : \n{0}'.format(out))
        PipelineLogger.log('converter', 'debug', 'Conversion Log Err : \n{0}'.format(err))

        QSubJobHandler.submittedJobs[id] = QSubJob(id, '01:00:00', processingItemObj, 'niak')
        return 1

    def combiningRuns(self, processingItemObj):
        #### Needs to improve it a lot more
        command = "%s combiningRuns('%s', '%s', %s, %s, %s)" %\
                  (config.matlab_call, config.fmristat_location, config.emma_tools_location,
                   processingItemObj.root_folder, processingItemObj.subject_rid, '1')

        # Run matlab command
        PipelineLogger.log('processing', 'debug', 'Command : {0}'.format(command))
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable='/bin/bash')
        out, err = p.communicate()
        PipelineLogger.log('processing', 'debug', 'combiningRuns Log Output : \n{0}'.format(out))
        PipelineLogger.log('processing', 'debug', 'combiningRuns Log Err : \n{0}'.format(err))

        return out