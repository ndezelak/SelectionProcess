# Main file
from Backend.rating_procedures import *
from Backend.elimination import *
from Backend.processing import *
from Backend.input_reading import *
from config import *
from Backend.output_utils import *

#TODO: Construct an HTML that gives a global overview of all rounds
#TODO: Output matching success for each student and company
print('Starting the program ...')
#print('Small change')
#students = Student(0,name="Nejc Dezelak",field_of_study=Field_of_Study.EE)
#companies = Company(0,name="Infenion",field_of_study=[Field_of_Study.EE,Field_of_Study.MB],seats=[students])

students=[]
companies=[]
finished_students = []
not_passed_students = []
construct_companies(companies)
read_csv(students,companies)
#hacks(students,companies)
# Read data and create data structures
#print('Generating test data ...')
#generate_test_data(students,companies)

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
print("First pass, 5 points")
fill_tables(passed_students,finished_students,sorted_companies,system,5)
print("First pass, 4 points")
fill_tables(passed_students,finished_students,sorted_companies,system,4)
print("First pass, 3 points")
fill_tables(passed_students,finished_students,sorted_companies,system,3)
print("First pass, 2 points")
fill_tables(passed_students,finished_students,sorted_companies,system,2)
print("First pass, 1 point")
fill_tables(passed_students,finished_students,sorted_companies,system,1)
print ("Filling left places, 0 points")
watchdog = 0
while(len(finished_students)<MAX_STUDENT_NUMBER):
    fill_left_places(passed_students,finished_students,sorted_companies,system)
    watchdog = watchdog +1
    if watchdog>5:
        print("NO SOLUTIONS FOUND\nPROBLEMATIC STUDENTS:\n")
        for student in passed_students:
            print(student.name+"\n")
        break

# Post processing of the occupied seats in order to assure minimal number of students at each table and at each round
print(" Post processing ...")
post_process(finished_students,sorted_companies,system)

watchdog = 0
while(len(finished_students)<MAX_STUDENT_NUMBER):
    fill_left_places(passed_students,finished_students,sorted_companies,system)
    watchdog = watchdog +1
    if watchdog>5:
        print("NO SOLUTIONS FOUND\nPROBLEMATIC STUDENTS:\n")
        for student in passed_students:
            print(student.name+"\n")
        break

print("---------------- RESULTS -------------------------")
for company in sorted_companies:
    print(company.name + ":")
    for row in range(0,NUM_ROWS):
        print(len(company.seats[row]))
print ("Number of passed students:" + str(len(finished_students) + len(passed_students)))
print ("Number of finished students:" + str(len(finished_students)) )

for student in finished_students:
    points = 0
    for company in student.seats:
        if company in student.companies:
            points = points +1
    print(" Student " + student.name +" "+ str(points)+"/"+str(NUM_ROWS)+".Wanted: "+ str(len(student.companies)))

# Not passed students
print("----------------------------------------")
print("Not passed students\n")
for student in students:
    if student not in finished_students:
        print(student.name + "\n")

# HTML document construction
print("-----------Creating student HTMLs -------------- ")
create_student_plans(finished_students)
print("-----------Creating global HTMLs -------------- ")
create_global_plan(finished_students,sorted_companies)
print("-----------Creating company plans-------------- ")
create_company_plan(sorted_companies,system)