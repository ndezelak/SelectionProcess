# Here the actual algorithm is written
from Classes.Person import *
from test_data import *

print('Hello world!')
#students = Student(0,name="Nejc Dezelak",field_of_study=Field_of_Study.EE)
#companies = Company(0,name="Infenion",field_of_study=[Field_of_Study.EE,Field_of_Study.MB],seats=[students])

students=[]
companies=[]

generate_test_data(students,companies)



print ('Done!')