__author__ = 'alexrdz'

import unicodecsv, csv
import xlrd
import datetime

from models import MonederoUser
from models import PreAccountStatement

from StatementProcessor import StatementProcessor



def parse(xlsfile, name_of_sheet):
    """

    :param xlsfile: Excel file to be read
    :param name_of_sheet: Name of the sheet of excel book
    """
    book = xlrd.open_workbook(xlsfile)
    sheet = book.sheet_by_name(name_of_sheet)
    output = open('data.csv', 'wb')
    write = unicodecsv.writer(output, quoting=unicodecsv.QUOTE_ALL)
    for row in xrange(1, sheet.nrows):
        write.writerow((sheet.row_values(row)))
    print "Data written on " + output.name
    output.close()


class UserList:
    def __init__(self):
        self.csv_list = []
        self.students = []
        self.user = None
        self.statement_list = []
        self.statement = None

    def to_list(self, csvfile, delimiter=','):
        """

        :param csvfile: CSV file to be read
        :param delimiter:
        :return: Returns a list obtained of the csv file
        """
        with open(csvfile) as csv_file:
            users = unicodecsv.reader(csv_file, dialect='excel', delimiter=delimiter)
            for row in users:
                self.user = MonederoUser(row)
                #if self.user.student_id[2] == '0':
                #    self.user.student_id = self.user.student_id[3:]
                #else:
                #    self.user.student_id = self.user.student_id[2:]
                self.csv_list.append(self.user)
            return self.csv_list

    def sort_by_column(self, csv_list):
        """
        Sorts the list by the ID column
        :param csv_list: list to be read
        :return:
        """
        data = sorted(csv_list, key=lambda user: self.user.student_id)
        return data

    def get_students_id(self, csv_list):
        """
        Extracts the IDs of all of the students on file
        :param csv_list:
        :return:
        """
        for self.user in csv_list:
            self.students.append(self.user.student_id)
        return self.students

    def get_statements(self, csvfile, delimiter=','):
        with open(csvfile, 'rU') as csv_file:
            csv_statements = csv.reader(csv_file, dialect=csv.excel_tab, delimiter=delimiter)
            for row in csv_statements:
                self.statement = PreAccountStatement(row)
                self.statement_list.append(self.statement)
        return self.statement_list


    def get_users(self, statement_list):
        user_list = []
        for statement in statement_list:
            user_list.append(statement.statement_student)
        return user_list

    def upload_users_to_server(self, students_list, statements_list):
        for student in students_list:

            if student.student_id in list(statements_list):
                student.upload()

    def upload_statements_to_server(self, students_list, statements_list, statement):
        for student in statements_list:

            if student in students_list:
                matches = StatementProcessor.search_for_statements_by_student(statement, student)
                StatementProcessor.process_transactions(matches, student)

start = datetime.datetime.now()
# 1a. Parse the xls file to csv
parse('alumnos CITA.xlsx', 'prof')

# 1b. Creates an instance of UserList
app = UserList()

# 2a.  Creates a list from the Users file
students = app.to_list('data.csv')

# 2b. Creates a list from the Statements file
statements = app.get_statements('test.csv')

# 3. Sorts the User list by the id column
sorted_students = app.sort_by_column(students)

# 4. Get the IDs of the students
students_id = app.get_students_id(sorted_students)
print students_id


# 5. Get users of statements
user_of_statements = app.get_users(statements)
print user_of_statements

# 5. Delete duplicates
student_set = set(user_of_statements)

# 6. Search for statements and check what students have statements in file
print "In file..."
app.upload_users_to_server(sorted_students,student_set)
app.upload_statements_to_server(students_id,student_set, statements)
finish = datetime.datetime.now()

print ("Time spent uploading files: %s" % (finish - start))







