__author__ = 'Seqian Wang'

from Recursor.Recursor import Recursor
from Utils.DbUtils import DBUtils

newFolder = Recursor('ADNI', '/data/backup-data02/ADNI/downloads/New2')
instancesList = newFolder.recurse()

for i in instancesList:
    i.printObject()

#sqlDatabase = DBUtils(location="localhost", username="wang030", password="firefox", database="Processing_Pipeline")
#for record in instancesList:
    #sqlDatabase.insertIfNotExist(record.sqlInsert, record.sqlUnique)