__author__ = 'wang'

import Manager.CsvImport as CsvImport
from Utils.DbUtils import DBUtils

class AdniCsvImport:
    def __init__(self, inputFolder):
        # Initiate Database Client
        self.DBClient = DBUtils()

        # For each csv file, import it into the SQL database
        for csvFile in inputFolder:
            sqlLocation = 'Study_Data.ADNI/' + csvFile.replace('.csv', '')
            CsvImport(self.DBClient, csvFile, sqlLocation)

        #  Close the connection to the database
        self.DBClient.close()