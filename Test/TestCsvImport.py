__author__ = 'wang'

from Manager.CsvImport.AdniCsvImport import AdniCsvImport

inputFolder = '/data/data01/wang/adni_csv'

newObject = AdniCsvImport(inputFolder, 'Study_Data.ADNI')