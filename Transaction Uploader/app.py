__author__ = 'enriqueramirez'
import csv
import sys
import datetime
from models import PreAccountStatement
from StatementProcessor import StatementProcessor



# 1. Open the file and pass the information to a list
with open('test2.csv', 'rU') as csvfile:
    reader = csv.reader(csvfile, dialect=csv.excel_tab, delimiter=',')
    list_of_statements = []
    for row in reader:
        statement = PreAccountStatement(row)
        list_of_statements.append(statement)


# 2.  Sorting list by student id for faster search
sorting_start = datetime.datetime.now()
sorted(list_of_statements, key=lambda statement: statement.statement_student)
sorting_end = datetime.datetime.now()

print("Time spent sorting statements: %s" % (sorting_end - sorting_start))

# 3.  Get list of students in file
list_of_students = []
student_list_start = datetime.datetime.now()
for statement in list_of_statements:
    list_of_students.append(statement.statement_student)
student_list_end = datetime.datetime.now()
print("Time spent adding students to list: %s" % (
    student_list_end - student_list_start))


# deleting duplicates
duplicates_start = datetime.datetime.now()
student_set = set(list_of_students)
duplicates_end = datetime.datetime.now()
print(
    "Time spent deleting duplicates: %s" % (duplicates_end - duplicates_start))
print student_set
print len(student_set)

# 4. Search for statements for each student
total_search_start = datetime.datetime.now()
for student in student_set:
    matches = StatementProcessor.search_for_statements_by_student(
        list_of_statements, student)
    # 5. Process information and prepare for uploading
    print('processing info')
    StatementProcessor.process_transactions(matches, student)
total_search_end = datetime.datetime.now()
print(
    "Total time spent searching: %s" % (total_search_end - total_search_start))
# 6. Upload Transaction