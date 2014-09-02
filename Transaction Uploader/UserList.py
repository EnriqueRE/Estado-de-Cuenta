__author__ = 'alexrdz'

import unicodecsv
import xlrd
import datetime

from models import MonederoUser


def parse(xlsfile, name_of_sheet):
    """

    :param xlsfile: Excel file to be read
    :param name_of_sheet: Name of the sheet of excel book
    """
    book = xlrd.open_workbook(xlsfile)
    sheet = book.sheet_by_name(name_of_sheet)
    output = open('data.csv', 'wb')
    write = unicodecsv.writer(output, quoting=unicodecsv.QUOTE_ALL)

    for row in xrange(sheet.nrows):
        write.writerow((sheet.row_values(row)))
    print "Data written on " + output.name
    output.close()

class UserList:
    def __init__(self):
        self.users_list = []
        self.students = []
        self.user = None


    def to_list(self, csvfile, delimiter=','):
        """

        :param csvfile: CSV file to be read
        :param delimiter:
        :return: Returns a list obtained of the csv file
        """
        with open(csvfile) as csv_file:
            users = unicodecsv.reader(csv_file,dialect='excel', delimiter=delimiter)
            for row in users:
                self.user = MonederoUser(row)
                self.users_list.append(self.user)
        return self.users_list


    def sort_by_column(self, csv_list):
        """
        Sorts the list by the ID column
        :param csv_list: list to be read
        :return:
        """
        data = sorted(csv_list, key=lambda user: self.user.student_id)
        return data

    def get_students(self, csv_list):
        """
        Extracts the IDs of all of the students on file
        :param csv_list:
        :return:
        """
        for self.user in csv_list:
            self.students.append(self.user.student_id)
        return self.students



# Creates an instance of UserList
app = UserList()
# Creates a list from the sent file
list1 = app.to_list('data.csv')

## for student in list1:
##      student.upload_to_server()



