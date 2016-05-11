__author__ = 'Sulantha'
import sys, argparse
sys.path.extend(['/home/sulantha/PycharmProjects/Processing_Pipeline'])
from Config import StudyConfig
from Manager.PipelineManager import PipelineManager
import logging.config
from Utils.PipelineLogger import PipelineLogger
import Config.EmailConfig as ec
from Utils.EmailClient import EmailClient
import traceback
from Manager.QSubJobHanlder import QSubJobHandler

def main():

    # Start an email client and logging capacity
    emailClient = EmailClient()
    logging.config.fileConfig('Config/LoggingConfig.conf')
    studyList = None

    ## Added ability to run from command line.
    try:
        ## Open up for arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('--studyList', required=True, nargs='+', choices=StudyConfig.AllowedStudyList, help='Space seperated study list.')
        parser.add_argument('--steps', required=False, nargs='+', choices=StudyConfig.AllowedStepsList, help='Space seperated steps list.')
        parser.add_argument('--modalities', required=False, nargs='+', choices=StudyConfig.AllowedModalityList, help='Space seperated modality list.')
        parser.add_argument('--pipe_v', required=False, nargs='+', choices=StudyConfig.AllowedVersions, help='Version of pipeline need to run.')
        args = parser.parse_args()
        studyList = args.studyList
        steps = args.steps
        modalities = args.modalities
        version = args.pipe_v

        if not validateStepSequence(steps):
            sys.exit(2)

        steps = ['ALL'] if not steps else steps
        modalities = StudyConfig.AllowedModalityList if not modalities else modalities
        if version and len(version) > 1 and len(studyList) > 1:
            PipelineLogger.log('root', 'info', 'Versioning with multiple studies is not supported. ')
            sys.exit(2)
        version = StudyConfig.defaultVersioningForStudy[studyList[0]] if not version else dict(zip(modalities, version))

        PipelineLogger.log('root', 'info', '##################Pipeline Started.#################')
        PipelineLogger.log('root', 'info', 'StudyIds = %s' %', '.join(map(str, studyList)))
        PipelineLogger.log('root', 'info', 'Steps = %s' %', '.join(map(str, steps)))
        PipelineLogger.log('root', 'info', 'Version = %s' %version)

        pipeline = PipelineManager(studyList, version)

        ####ToDo: Process steps sequence.

        ## Recurse for new data
        PipelineLogger.log('root', 'info', 'Recursing for new data started ...')
        pipeline.recurseForNewData()
        PipelineLogger.log('root', 'info', 'Recursing for new data done ...############')
        ## Add data to Sorting table.
        pipeline.addNewDatatoDB()
        ##Get Unmoved Raw File List
        pipeline.getUnmovedRawDataList()
        PipelineLogger.log('root', 'info', 'Moving new data started ...')
        pipeline.moveRawData()
        PipelineLogger.log('root', 'info', 'Moving new data done ...############')
        pipeline.getConversionList()
        PipelineLogger.log('root', 'info', 'Converting to MINC started ...')
        pipeline.convertRawData()
        PipelineLogger.log('root', 'info', 'Converting to MINC done ...############')
        PipelineLogger.log('root', 'info', 'Modifying processing pipeline table. This may take a while. Please wait....############')
        pipeline.getConvertedList()  # Get all files that have been converted, from Conversion table
        pipeline.refreshModalityTables()  # Get the correct modality, insert or ignore information in Processing table, takes quite some time
        pipeline.getProcessList()  # Returning all rows from the Processing table that has not been processed or skipped, takes time too
        pipeline.fillPipelineTables()  # Creating jobs queue in {study}_{modality}_Pipeline table, takes time too
        for modality in modalities:
            if modality == 'BLUFF':
                break
            pipeline.checkExternalJobs(modality)  # Update list of external waiting jobs in externalWaitingJobs table
        for modality in modalities:
            if modality == 'BLUFF':
                break
            pipeline.checkOnQCJobs(modality)  # Update jobs with success QC in Processing table
        for modality in modalities:
            if modality == 'BLUFF':
                break
            pipeline.processModality(modality)  # Actually processing jobs

        QSubJobHandler.submittedJobs['xxxx'].Fin = True
        PipelineLogger.log('root', 'info', 'Pipeline reached end. Waiting on submitted jobs. ')
        #### End
        if not QSubJobHandler.submittedJobs:
            PipelineLogger.log('root', 'info', 'No QSUB Jobs in waiting ...############')
            PipelineLogger.log('root', 'info', 'Pipeline exiting ...############')
            PipelineLogger.log('root', 'info', '##################Pipeline Done.#################')
            pipeline.qsubJobHandler.QUIT = 1
    except:
        PipelineLogger.log('root', 'exception', 'Pipeline crashed with exception. ')
        emailClient.send_email(ec.EmailRecList_admin, 'Pipeline crashed with exception. ', ' {0} '.format(traceback.format_exc()))



##This method will validate the sequence of steps. If not returns False.
def validateStepSequence(stepsList):
    return True

if __name__ == '__main__':
    main()

