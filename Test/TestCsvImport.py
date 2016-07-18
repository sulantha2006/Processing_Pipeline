__author__ = 'wang'

from Manager.CsvImport.AdniCsvImport import AdniCsvImport

inputFolder = '/data/data03/ADNI_CSV_Folder'

newObject = AdniCsvImport(inputFolder, 'Study_Data.ADNI')