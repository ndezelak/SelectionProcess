# Here the actual algorithm is written
from Classes.Person import *
from test_data import *
from Functions.rating_procedure import *
from Functions.elimination import *
print('Hello world!')
#students = Student(0,name="Nejc Dezelak",field_of_study=Field_of_Study.EE)
#companies = Company(0,name="Infenion",field_of_study=[Field_of_Study.EE,Field_of_Study.MB],seats=[students])

students=[]
companies=[]

generate_test_data(students,companies)
system = generate_system_matrix(students,companies)
[sorted_companies,sorted_students]=rate_and_sort(students,companies,system)
[passed_students,boundary_region]=divide_students(sorted_students,80)
print ('Done!')