__author__ = 'wang'
from Recursor.ADNI.MonicaDownloadAdni import MonicaDownloadAdni

class Recursor:
    def __init__(self, studyID, root_download):
        self.study = studyID
        self.root_download = root_download
        self.subRecursor = None
        if studyID == 'ADNI':
            self.subRecursor = MonicaDownloadAdni(studyID, root_download)

    def recurse(self):
        return self.subRecursor.recurse()
