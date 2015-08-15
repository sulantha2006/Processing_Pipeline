__author__ = 'Seqian Wang'

from Recursor.ADNI.ADNIRecursor import ADNIRecursor

newFolder = ADNIRecursor('/data/data02/ADNI/downloads/New2')
instancesList = newFolder.execute()

for i in instancesList:
    i.printObject()