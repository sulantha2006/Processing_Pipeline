__author__ = 'wang'

import glob
import os
import csv
import Config.CsvImportConfig as config
import openpyxl
from openpyxl.styles import Font

inputFolder = '/data/data01/wang/adni_csv'
outputFile = '/home/wang/Downloads/header.xlsx'


def extractHeader(csvFile, sqlTable, bookSheet, i):
    # Export the headers from the CSV file and output it to an outputfile

    # Read the header row
    for row in csvFile:
        headerRow = [i.replace('/', '').replace(' ', '').replace('\0', '') for i in row]
        break
    headerRow = [sqlTable] + headerRow + ['\n']

    j = 0
    for content in headerRow:
        cell = bookSheet.cell(row = i, column = j)
        cell.value = content
        if content.lower() in config.uniqueHeaders:
            cell.style.font.bold = True
        j += 1


if __name__ == "__main__":
    book = openpyxl.Workbook()
    bookSheet = book.active

    i = 0
    for inputFile in glob.glob(inputFolder + '/*.csv'):
        sqlLocation = os.path.basename(inputFile).replace('.csv', '')

        with open(inputFile, 'r') as inputFile:
            csvFile = csv.reader(inputFile)
            extractHeader(csvFile, sqlLocation, bookSheet, i)

        i += 1

    book.save(outputFile)