# Main fle
from Classes.Person import *
from test_data import *
from Functions.rating_procedure import *
from Functions.elimination import *
from Functions.processing import *
from config import *

print('Starting the program ...')
#students = Student(0,name="Nejc Dezelak",field_of_study=Field_of_Study.EE)
#companies = Company(0,name="Infenion",field_of_study=[Field_of_Study.EE,Field_of_Study.MB],seats=[students])

students=[]
companies=[]
finished_students = []

# Read data and create data structures
print('Generating test data ...')
generate_test_data(students,companies)

# Create system matrix, rate students and companies and sort them
print('Constructing the system matrix ...')
system = generate_system_matrix(students,companies)
print('Rating and sorting process ...')
[sorted_companies,sorted_students]=rate_and_sort(students,companies,system)

# Eliminate students with not enough points
print('Elimination process started ...')
[passed_students,boundary_region]=divide_students(sorted_students,MAX_STUDENT_NUMBER)

# Occupy seats starting with perfect matches
print('--------------  OCCUPYING SEATS ---------------')
print("First pass, 3 points")
fill_tables(passed_students,finished_students,sorted_companies,system,3)
print("First pass, 2 points")
fill_tables(passed_students,finished_students,sorted_companies,system,2)
print("First pass, 1 point")
fill_tables(passed_students,finished_students,sorted_companies,system,1)
print ("First pass, 0 points")
fill_left_places(passed_students,finished_students,sorted_companies,system)

# Post processing of the occupied seats in order to assure minimal number of students at each table and at each round
print(" Post processing ...")
post_process(finished_students,sorted_companies,system)


print("---------------- RESULTS -------------------------")
for company in sorted_companies:
    print(company.name + ":")
    for row in range(0,4):
        print(len(company.seats[row]))
print ("Number of passed students:" + str(len(finished_students) + len(passed_students)))
print ("Number of finished students:" + str(len(finished_students)) )
