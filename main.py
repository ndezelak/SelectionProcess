# Main file
from Functions.rating_procedure import *
from Functions.elimination import *
from Functions.processing import *
from Functions.construct_data import *
from config import *
from dominate.tags import *
from dominate import *

#TODO: Construct an HTML that gives a global overview of all rounds
#TODO: Output matching success for each student and company
print('Starting the program ...')
print('Small change')
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

for student in finished_students:
    points = 0
    for company in student.seats:
        if company in student.companies:
            points = points +1
    print(" Student " + student.name +" "+ str(points)+"/4. Chosen together: "+ str(len(student.companies)))

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
    doc+=style("h3{text-align:center}")
    doc += style("h2{text-align:center; color:darkblue}")
    doc += style("h4{text-align:center}")
    doc+=style("div{text-align:center}")
    doc.head.add_raw_string("<header><center><img src=""logo.png"" alt=""Something"" align=""middle""></center></header>")
    doc+=br()
    doc+=br()

    doc+=h1(student.name)
    doc+=br()

    #doc.body.add_raw_string("<body background=""logo.jpg"">")

    for round in range(0,4):
        doc+=h3("Gang "+str(round+1))
        doc+=h2(str(student.seats[round].name))
        doc+=h4("Tischnummer:"+str(student.seats[round].list_id+1))
        doc+=br()
   # doc.body.add_raw_string("<footer><center><img src=""logo.png"" alt=""Something"" align=""middle""></center></footer>")

    # Output result ot a specific file
    file=open("Output/Students/"+str(student.name)+'.html','w')
    file.write(str(doc))
    file.close()
    i = i+1




#print(html(body(h1('This is the document title!')))  )