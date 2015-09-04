__author__ = 'wang'

import glob
import os
import csv
import Config.CsvImportConfig as config
import openpyxl

inputFolder = '/data/data01/wang/adni_csv'
outputFile = '/home/wang/Downloads/header.xlsx'


def extractHeader(csvFile, sqlTable, book, i):
    # Export the headers from the CSV file and output it to an outputfile
    for row in csvFile:
        headerRow = [i.replace('/', '').replace(' ', '').replace('\0', '') for i in row]
        break

    headerRow = [sqlTable] + headerRow + ['\n']

    font0 = openpyxl.Font()
    font0.bold = False
    style0 = openpyxl.XFStyle()
    style0.font = font0

    font1 = openpyxl.Font()
    font1.bold = True
    style1 = openpyxl.XFStyle()
    style1.font = font1

    j = 0
    for column in headerRow:
        if column.lower() in config.uniqueHeaders:
            style = style1
        else:
            style = style0
        book.write(i, j, column, style)
        j+= 1


if __name__ == "__main__":
    book = openpyxl.Workbook()
    bookSheet = book.active

    i = 0
    for inputFile in glob.glob(inputFolder + '/*.csv'):
        sqlLocation = os.path.basename(inputFile).replace('.csv', '')

        with open(inputFile, 'r') as inputFile:
            csvFile = csv.reader(inputFile)
            extractHeader(csvFile, sqlLocation, bookSheet, i)

        i+= 1

    book.save(outputFile)