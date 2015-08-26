__author__ = 'wang'

import csv

class CSVImport:
    def __init__(self, sqlDatabase, csvFile, sqlLocation):
        # Insert csv file content per row
        header = 1
        for row in csv.reader(csvFile):
            if header:  # For first row of headers
                if not self.checkIfTableExists(sqlLocation):
                    sqlDatabase.executeNoResult('CREATE TABLE %s (%s)' % (sqlLocation, row))
                header = 0
                continue
            sqlDatabase.executeNoResult('INSERT IGNORE INTO %s %s' % (sqlLocation, row))

    def checkIfTableExists(self, tableName):
        # If table or csvfile does not exist in SQL database
        if not self.sqlDatabase.executeSomeResults("SHOW TABLES LIKE '%s'" % self.sqlLocation, 5):
            return False
        else:
            return True