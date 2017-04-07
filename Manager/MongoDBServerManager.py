__author__ = 'sulantha'
from subprocess import check_output, Popen
import os
from Utils.PipelineLogger import PipelineLogger

class MongoDBManager:
    def __init__(self):
        self.old_pid = self.get_pid('mongod')
        print(self.old_pid)
        self.restart_mongo()

    def get_pid(self, name):
        try:
            return int(check_output(["pidof", "-s", name]))
        except:
            return 0

    def restart_mongo(self):
        try:
            if self.old_pid > 0:
                os.kill(self.old_pid, 9)
            mongo_Cmd = '/data/data03/MongoDB/mongodb/bin/mongod --logpath Logs/MongoLog.log --dbpath /data/data03/MongoDB/data/db/'
            Popen(mongo_Cmd, shell=True)
        except OSError as e:
            PipelineLogger.log('root', 'exception', 'MongoDB cannot be stopped or started.\n {0}\n'.format(e))

