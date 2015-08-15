__author__ = 'Sulantha'
import sys, argparse
from Config import StudyConfig
from Manager.PipelineManager import PipelineManager

def main(argv):
    studyList = None

    ##Added ability to run from command line.
    parser = argparse.ArgumentParser()
    parser.add_argument('--studyList', required=True, nargs='+', choices=StudyConfig.AllowedStudyList, help='Space seperated study list.')
    parser.add_argument('--steps', required=False, nargs='+', choices=StudyConfig.AllowedStepsList, help='Space seperated steps list.')
    args = parser.parse_args()
    studyList = args.studyList
    steps = args.steps

    if not validateStepSequence(steps):
        sys.exit(2)

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

