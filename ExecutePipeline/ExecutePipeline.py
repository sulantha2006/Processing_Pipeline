__author__ = 'Sulantha'
import sys, argparse
from Config import StudyConfig
from Manager.PipelineManager import PipelineManager
import logging.config
from Utils.PipelineLogger import PipelineLogger

def main(argv):
    logging.config.fileConfig('../Config/LoggingConfig.conf')
    studyList = None

    ##Added ability to run from command line.
    parser = argparse.ArgumentParser()
    parser.add_argument('--studyList', required=True, nargs='+', choices=StudyConfig.AllowedStudyList, help='Space seperated study list.')
    parser.add_argument('--steps', required=False, nargs='+', choices=StudyConfig.AllowedStepsList, help='Space seperated steps list.')
    parser.add_argument('--pipe_v', required=False, nargs='+', choices=StudyConfig.AllowedVersions, help='Version of pipeline need to run.')
    args = parser.parse_args()
    studyList = args.studyList
    steps = args.steps
    version = args.pipe_v

    if not validateStepSequence(steps):
        sys.exit(2)

    PipelineLogger.log('root', 'info', '##################Pipeline Started.#################')
    PipelineLogger.log('root', 'info', 'StudyIds = %s' %', '.join(map(str, studyList)))
    PipelineLogger.log('root', 'info', 'Steps = %s' %', '.join(map(str, steps)))
    PipelineLogger.log('root', 'info', 'Version = %s' %', '.join(map(str, version)))

    pipeline = PipelineManager(studyList)

    ####ToDo: Process steps sequence.

    ## Recurse for new data
    pipeline.recurseForNewData()
    ## Add data to Sorting table.
    pipeline.addNewDatatoDB()



##This method will validate the sequence of steps. If not returns False.
def validateStepSequence(stepsList):
    return True

if __name__ == '__main__':
    main()

