__author__ = 'wang'

from Manager.CsvImport.csvToDatabase import csvToDatabase
from Utils.DbUtils import DbUtils
import glob, os
import Config.DBConfig as config

class AdniCsvImport:
    def __init__(self, inputFolder, database_location):
        # Initiate Database Client
        self.DbClient = DbUtils(database=database_location)

        # For each csv file, import it into the SQL database
        for inputFile in glob.glob(inputFolder + '/*.csv'):
            if inputFile in config.AdniIgnored:
                continue
            sqlLocation = os.path.basename(inputFile).replace('.csv', '')
            with open(inputFile, 'r') as csvFile:
                csvToDatabase(self.DbClient, csvFile, sqlLocation)

        #  Close the connection to the database
        self.DbClient.close()