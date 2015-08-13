__author__ = 'Seqian Wang'

from Recurser.ADNI import MonicaDownloadAdni

newFolder = MonicaDownloadAdni('/data/data02/ADNI/downloads/New')
instancesList = newFolder.execute()

for i in instancesList:
    i.print_object()