__author__ = 'Seqian Wang'

from Recursor import Recursor
from Utils.DbUtils import DBUtils

newFolder = Recursor('ADNI', '/data/data02/ADNI/downloads/New2')
instancesList = newFolder.recurse()

for i in instancesList:
    i.printObject()

sqlDatabase = DBUtils()
for record in instancesList:
    sqlDatabase.insert(record.sqlInsert, record.sqlUnique)