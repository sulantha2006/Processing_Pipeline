__author__ = 'Sulantha'
from Utils.PipelineLogger import PipelineLogger

class testSubModuleLogging:
    def __init__(self):
        pass

    def log(self):
        PipelineLogger.log('manager', 'warning', 'Hope this works.')
