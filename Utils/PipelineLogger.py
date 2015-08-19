__author__ = 'Sulantha'
import logging

class PipelineLogger:
    logFunctions={'info':logging.info,
                'debug':logging.debug,
                'warning':logging.warning,
                'error':logging.error,
                'critical':logging.critical,
                  'exception':logging.exception}

    @staticmethod
    def log(moduleName, level, message):
        logging.getLogger(moduleName)
        PipelineLogger.logFunctions[level](message)


