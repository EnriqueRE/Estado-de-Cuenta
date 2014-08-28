__author__ = 'alexrdz'

import unicodecsv
import xlrd


# Excel file used to read
source = 'alumnos CITA.xlsx'

class XLSReader():
    """
    Converts excel file to output csv file
    :return:
    """
    def __init__(self):
        book = xlrd.open_workbook(source)
        sheet = book.sheet_by_index(0)
        output = open('data.csv', 'wb')
        write = unicodecsv.writer(output, quoting=unicodecsv.QUOTE_ALL)

        for row in xrange(sheet.nrows):
            write.writerow((sheet.row_values(row)))
        output.close()

reader = XLSReader()