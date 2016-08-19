# -*- coding: utf-8 -*-
import xlrd
import csv
from os import sys


def csv_from_excel(workbook):

    wb = xlrd.open_workbook(workbook)
    sh = wb.sheet_by_name('Roster_Northeastern')
    your_csv_file = open('your_csv_file.csv', 'w')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        print(sh.row_values(rownum))
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()

if __name__ == "__main__":
    csv_from_excel(sys.argv[1])
