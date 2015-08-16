__author__ = 'Sulantha'
import logging.config
from Utils.PipelineLogger import PipelineLogger
from Test.logTestSubModule import testSubModuleLogging


logging.config.fileConfig('../Config/LoggingConfig.conf')

PipelineLogger.log('root', 'info', 'Main module log')

lg = testSubModuleLogging()

lg.log()

