# Main fle
from Classes.Person import *
from test_data import *
from Functions.rating_procedure import *
from Functions.elimination import *
from Functions.processing import *
from Functions.construct_data import *
from config import *
from dominate.tags import *
from dominate import *
import os

print('Starting the program ...')
#students = Student(0,name="Nejc Dezelak",field_of_study=Field_of_Study.EE)
#companies = Company(0,name="Infenion",field_of_study=[Field_of_Study.EE,Field_of_Study.MB],seats=[students])

students=[]
companies=[]
finished_students = []

construct_companies(companies)
read_csv(students,companies)

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

# HTML document construction

# List of all students
doc = document()
section=div(style("div{color:red;text-align:center}"))
section+=h1("Studenten Liste")
section2=div(style("div{color:black}"))
for student in finished_students:
    section2+=student.name
    section2+=br()
doc+=section
doc+=section2

# List of all companies
doc2 = document()
doc2+=style("h1{text-align:center}")
section_2=div(style("div{color:red;text-align:center}"))
doc2+=h1("Firmen Liste")
for company in sorted_companies:
    section_2+=company.name
    section_2+=br()
doc2+=section_2

# Writing everything into a HTML file
file = open('Output\HTML_students_list.html','w')
file.write(str(doc))
file.close()

file = open('Output\HTML_company_list.html','w')
file.write(str(doc2))
file.close()

# Seat plan for each student
i = 0
for student in finished_students:
    doc = document()
    doc+=style("h1{text-align:center}")
    doc+=style("h2{text-align:center}")
    doc+=style("div{text-align:center}")
    doc+=h1(student.name)
    for round in range(0,4):
        doc+=h2("Runde "+str(round+1)+":")
        doc+=div("Firma:"+str(student.seats[round].name))
        doc+=div("Tischnummer:"+str(student.seats[round].list_id+1))
        doc+=br()

    # Output result ot a specific file
    file=open('Output\Students\sitzplan_'+str(student.name)+str(i)+'.html','w')
    file.write(str(doc))
    file.close()
    i = i+1




#print(html(body(h1('This is the document title!')))  )