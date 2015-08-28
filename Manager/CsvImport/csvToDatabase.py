__author__ = 'wang'

import csv

class csvToDatabase:
    def __init__(self, sqlDatabase, csvFile, sqlLocation):
        # Insert csv file content per row
        header = 1
        for row in csv.reader(csvFile):
            if header:  # For first row of headers
                if not self.checkIfTableExists(sqlDatabase, sqlLocation):
                    print('CREATE TABLE %s (%s)' % (sqlLocation, ' char(32),'.join(row)))
                    sqlDatabase.executeNoResult('CREATE TABLE %s (%s)' % (sqlLocation, ' char(32), '.join(row)))
                header = 0
                continue
            print('INSERT INTO %s VALUES ("%s") WHERE NOT EXISTS (SELECT * FROM %s)'
                  % (sqlLocation, '", "'.join(row), sqlLocation))
            sqlDatabase.executeNoResult('IF NOT EXISTS (SELECT * FROM %s) INSERT INTO %s (%s' % (sqlLocation, sqlLocation, ', '.join(row)))

    def checkIfTableExists(self, sqlDatabase, tableName):
        # If table or csvfile does not exist in SQL database
        if not sqlDatabase.executeSomeResults("SHOW TABLES LIKE '%s'" % tableName, 5):
            return False
        else:
            return True