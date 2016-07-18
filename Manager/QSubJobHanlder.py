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
                startTime = job.startTime
                wallTime = job.wallTime
                if (job.startTime and job.Start and timeNow - startTime > wallTime) or job.Fin:
                    self.submittedJobs.pop(jobID)
            return True

    def __init__(self):
        threading.Thread.__init__(self)
        self.sock = None
        self.thread_list = []


    def doWork(self, conn):
        data = conn.recv(1024)
        #PipelineLogger.log('manager', 'info', ' Data recieved - {0}.'.format(data))
        jobID = data.strip().decode('utf-8').split('_')[0]
        status = data.strip().decode('utf-8').split('_')[1]
        PipelineLogger.log('manager', 'info',' ++++++++ QSub Job Handler received JobID - {0}.'.format(jobID))
        if jobID not in self.submittedJobs:
            PipelineLogger.log('manager', 'error',' ++++++++ QSub Job Handler unidentified JobID - {0}.'.format(jobID))
        else:
            jobReporter = QSubJobStatusReporter()
            if  status == 'Start':
                PipelineLogger.log('manager', 'info',' ++++++++ JobID - {0} -> Status - {1}.'.format(jobID, status))
                self.submittedJobs[jobID].Start = True
                self.submittedJobs[jobID].startTime = datetime.datetime.now()
            elif status == 'Success':
                PipelineLogger.log('manager', 'info',' ++++++++ JobID - {0} -> Status - {1}.'.format(jobID, status))
                self.submittedJobs[jobID].Fin = True
                jobReporter.setStatus(self.submittedJobs[jobID], status)
            elif status == 'Fail':
                PipelineLogger.log('manager', 'info',' ++++++++ JobID - {0} -> Status - {1}.'.format(jobID, status))
                self.submittedJobs[jobID].Fin = True
                jobReporter.setStatus(self.submittedJobs[jobID], status)
            else:
                PipelineLogger.log('manager', 'info',' ++++++++ JobID - {0} -> Status (Unhandled)- {1}.'.format(jobID, status))


    def run(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((socket.gethostname(), 50500))
            self.sock.settimeout(300)
            self.sock.listen(1000)
            PipelineLogger.log('manager', 'info',' ++++++++ QSub Job Handler started.')
            PipelineLogger.log('manager', 'info',' ++++++++ QSub Job Handler listening in Host : {0} at Port : {1}.'.format(socket.gethostname(), 50500))
            while not self.QUIT and self.checkJobs():
                try:
                    conn = self.sock.accept()[0]
                    thread = threading.Thread(target=self.doWork, args=(conn, ))
                    thread.start()
                except socket.timeout:
                    continue
        except Exception as e:
            PipelineLogger.log('manager', 'exception',e)
            PipelineLogger.log('manager', 'error','Cannot create QSubJobHandler... Will not listen to on jobs. ')
            del self.sock



