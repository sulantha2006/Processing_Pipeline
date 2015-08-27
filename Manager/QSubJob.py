__author__ = 'sulantha'
from datetime import datetime, timedelta

class QSubJob:
    def __init__(self, id, wallTime):
        self.id = id
        wt = datetime.strptime(wallTime, '%H:%M:%S')
        self.wallTime = timedelta(hours=wt.hour, minutes=wt.minute, seconds=wt.second)
        self.submitTime = datetime.now()
        self.Fin = False

