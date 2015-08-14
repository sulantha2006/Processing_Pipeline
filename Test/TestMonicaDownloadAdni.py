__author__ = 'Seqian Wang'

from Recursor.ADNI.MonicaDownloadAdni import MonicaDownloadAdni

newFolder = MonicaDownloadAdni('/data/data02/ADNI/downloads/New2')
instancesList = newFolder.execute()

for i in instancesList:
    i.printObject()