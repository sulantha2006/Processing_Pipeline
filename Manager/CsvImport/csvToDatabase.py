__author__ = 'wang'

import csv
import Config.CsvImportConfig as config
import sys

class csvToDatabase:
    def __init__(self, sqlDatabase, csvFile, sqlTable):
        # Insert csv file content per row
        header = 1
        for row in csv.reader(line.replace('\0', '') for line in csvFile):
            if header:  # For first row of headers
                if not self.checkIfTableExists(sqlDatabase, sqlTable):
                    # Create Table if it doesn't exist already
                    row=[self.simplifyString(i) for i in row]
                    sqlCommand = 'CREATE TABLE %s (%s varchar(64))' % (sqlTable, ' varchar(64), '.join(row))
                    sqlDatabase.executeNoResult(sqlCommand)

                    # Setting unique indexes
                    uniqueList = self.uniqueColumns(row)
                    sqlCommand = 'ALTER TABLE %s ADD UNIQUE (%s)' % (sqlTable, ', '.join(uniqueList))
                    sqlDatabase.executeNoResult(sqlCommand)

                header = 0
                continue

            # Insert if dataset does not exit already
            row = [i.replace('"','') for i in row]
            sqlDatabase.executeNoResult('INSERT IGNORE INTO %s VALUES ("%s")' % (sqlTable, '", "'.join(row)))

    def checkIfTableExists(self, sqlDatabase, tableName):
        # If table or csvfile does not exist in SQL database
        if not sqlDatabase.executeSomeResults("SHOW TABLES LIKE '%s'" % tableName, 5):
            return False
        else:
            return True

    def simplifyString(self, string):
        return string.lower().replace(' ', '').replace('/', '').replace('.', '')

    def uniqueColumns(self, headerRow):
        uniqueColumns = []
        for header in headerRow:
            if header in config.uniqueHeaders:
                uniqueColumns.append(header)
        return uniqueColumns