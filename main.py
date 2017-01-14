# Here the actual algorithm is written
from Classes.Person import *
from test_data import *
from Functions.rating_procedure import *
from Functions.elimination import *
from Functions.processing import *
from config import *
print('Hello world!')
#students = Student(0,name="Nejc Dezelak",field_of_study=Field_of_Study.EE)
#companies = Company(0,name="Infenion",field_of_study=[Field_of_Study.EE,Field_of_Study.MB],seats=[students])

students=[]
companies=[]
finished_students = []

generate_test_data(students,companies)
system = generate_system_matrix(students,companies)
[sorted_companies,sorted_students]=rate_and_sort(students,companies,system)
[passed_students,boundary_region]=divide_students(sorted_students,MAX_STUDENT_NUMBER)


print("First pass, 3 points")
fill_tables(passed_students,finished_students,sorted_companies,system,3)
print("First pass, 2 points")
fill_tables(passed_students,finished_students,sorted_companies,system,2)
print("First pass, 1 point")
fill_tables(passed_students,finished_students,sorted_companies,system,1)

print (" Let us fill all the left seats")
fill_left_places(passed_students,finished_students,sorted_companies,system)

print(" Post processing ...")
post_process(finished_students,sorted_companies,system)


# TODO: Implement the boundary region elimination + what to do when students seats are still left after the complete first pass?
print("---- RESULTS ----")
for company in sorted_companies:
    print(company.name + ":")
    for row in range(0,4):
        print(len(company.seats[row]))
print ("Number of passed students:" + str(len(finished_students) + len(passed_students)))
print ("Number of finished students:" + str(len(finished_students)) )
print ('Done!')