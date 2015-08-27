__author__ = 'sulantha'
import threading
import socket
from Utils.PipelineLogger import PipelineLogger
import datetime
from Manager.QSubJob import QSubJob

class QSubJobHandler(threading.Thread):
    submittedJobs = {'100':QSubJob('100', '00:00:40')}
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
                if timeNow - submitTime > wallTime or job.Fin:
                    self.submittedJobs.pop(jobID)
            return True

    def __init__(self):
        threading.Thread.__init__(self)
        self.sock = None
        self.thread_list = []

    def doWork(self, conn):
        data = conn.recv(1024)
        jobID = data.strip().decode('utf-8')
        PipelineLogger.log('manager', 'info',' ++++++++ QSub Job Handler received JobID - {0}.'.format(jobID))
        if jobID not in self.submittedJobs:
            PipelineLogger.log('manager', 'error',' ++++++++ QSub Job Handler unidentified JobID - {0}.'.format(jobID))
        else:
            self.submittedJobs[jobID].Fin = True

    def run(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((socket.gethostname(), 50500))
            self.sock.settimeout(5)
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
