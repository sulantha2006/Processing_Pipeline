__author__ = 'sulantha'
import threading
import socket
from Utils.PipelineLogger import PipelineLogger
import datetime
from Manager.QSubJob import QSubJob
from Manager.QSubJobStatusReporter import QSubJobStatusReporter

class QSubJobHandler(threading.Thread):
    submittedJobs = {'xxxx':QSubJob('xxxx', '23:59:59', None, 'beast')}
    QUIT = 0

    def checkJobs(self):
        if not self.submittedJobs:
            return False
        else:
            timeNow = datetime.datetime.now()
            for jobID in list(self.submittedJobs):
                job = self.submittedJobs[jobID]
                submitTime = job.submitTime
                wallTime = job.wallTime
                if (job.Start and timeNow - submitTime > wallTime) or job.Fin:
                    self.submittedJobs.pop(jobID)
            return True

    def __init__(self):
        threading.Thread.__init__(self)
        self.sock = None
        self.thread_list = []
        self.jobReporter = QSubJobStatusReporter()

    def doWork(self, conn):
        data = conn.recv(1024)
        jobID = data.strip().decode('utf-8').split('_')[0]
        status = data.strip().decode('utf-8').split('_')[1]
        PipelineLogger.log('manager', 'info',' ++++++++ QSub Job Handler received JobID - {0}.'.format(jobID))
        if jobID not in self.submittedJobs:
            PipelineLogger.log('manager', 'error',' ++++++++ QSub Job Handler unidentified JobID - {0}.'.format(jobID))
        else:
            if  status == 'Start':
                PipelineLogger.log('manager', 'info',' ++++++++ JobID - {0} -> Status - {1}.'.format(jobID, status))
                self.submittedJobs[jobID].Start = True
            elif status == 'Success':
                PipelineLogger.log('manager', 'info',' ++++++++ JobID - {0} -> Status - {1}.'.format(jobID, status))
                self.submittedJobs[jobID].Fin = True
                self.jobReporter.setStatus(self.submittedJobs[jobID], status)
            elif status == 'Fail':
                PipelineLogger.log('manager', 'info',' ++++++++ JobID - {0} -> Status - {1}.'.format(jobID, status))
                self.submittedJobs[jobID].Fin = True
                self.jobReporter.setStatus(self.submittedJobs[jobID], status)
            else:
                PipelineLogger.log('manager', 'info',' ++++++++ JobID - {0} -> Status (Unhandled)- {1}.'.format(jobID, status))


    def run(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((socket.gethostname(), 50500))
            self.sock.settimeout(300)
            self.sock.listen(10)
        except:
            PipelineLogger.log('manager', 'error','Cannot create QSubJobHandler... Will not listen to on jobs. ')
            del self.sock

        PipelineLogger.log('manager', 'info',' ++++++++ QSub Job Handler started.')
        PipelineLogger.log('manager', 'info',' ++++++++ QSub Job Handler listening in Host : {0} at Port : {1}.'.format(socket.gethostname(), 50500))
        while not self.QUIT and self.checkJobs():
            try:
                conn = self.sock.accept()[0]
                thread = threading.Thread(target=self.doWork, args=(conn, ))
                thread.start()
            except socket.timeout:
                continue
