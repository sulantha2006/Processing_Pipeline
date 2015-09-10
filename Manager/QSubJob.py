__author__ = 'sulantha'
from datetime import datetime, timedelta

class QSubJob:
    def __init__(self, id, wallTime, job, jobType):
        self.id = id
        wt = datetime.strptime(wallTime, '%H:%M:%S')
        self.wallTime = timedelta(hours=wt.hour, minutes=wt.minute, seconds=wt.second)
        self.submitTime = datetime.now()
        self.job = job
        self.jobType = jobType
        self.Start = False
        self.Fin = False

