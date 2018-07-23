from dominate import *
from dominate import *
from dominate.tags import *
from config import *
def create_global_plan(finished_students,sorted_companies):
    #doc += style("h3{text-align:center}")
    #doc += style("h4{text-align:center}")
    for round in range(0,NUM_ROWS):
        doc = document()
        doc += style("h1{text-align:center; font size=""40""}")
       # doc += style("h2{text-align:center}")
        doc+=h1("Gang "+str(round+1))
        for company in sorted_companies:
            doc+=h2(company.name)
            for student in company.seats[round]:
               doc+=h3(pre("    "+student.name))
        file = open("Output\Global\Gang"+str(round)+" global" + '.html', 'w')
        file.write(str(doc))
        file.close()

def create_student_plans(finished_students):
    # Seat plan for each student
    i = 0
    for student in finished_students:
        doc = document()
        doc += style("h1{text-align:center}")
        doc += style("h3{text-align:center}")
        doc += style("h2{text-align:center}")
        doc += style("h4{text-align:center}")
        doc += style("div{text-align:center}")
        doc +=style(".container{ \
        height:250px; \
        background:#f8f8f8; \
        display: -ms-flexbox; \
        display: -webkit-flex; \
        display: flex; \
        -ms-flex-align: center; \
        align-items: center; \
        -webkit-box-align: center; \
        justify-content: center;\
        } \
        h1{ \
        font-size:48px;} \
        h2{font-size:30px;}\
        h3{font-size:20px;} h4{font-size:14px;}         ") \

        doc.head.add_raw_string(
        "<header><center><img src=""logo.png"" alt=""Something"" align=""middle"" width=""500""></center></header>")
        doc += br()
        doc += br()

        doc += h1(student.name)
        doc += br()
        doc += style("h1{text-align:center; color:darkblue}")

        for round in range(0, NUM_ROWS):
            doc+=h3("Gang " + str(round + 1))
            doc+=h2(unicode(str(student.seats[round].name)))
           # doc+=h4("Tischnummer:" + str(student.seats[round].list_id + 1))
            doc+=br()
        # doc.body.add_raw_string("<footer><center><img src=""logo.png"" alt=""Something"" align=""middle""></center></footer>")

    # Output result ot a specific file
        file = open("Output/Students/" + str(student.name) + '.html', 'w')
        file.write(str(doc))
        file.close()
        i = i + 1

def create_company_plan(sorted_companies,system):

    for company in sorted_companies:
        doc = document()
        doc += style("h1{text-align:left}")
        doc += style("h3{text-align:left}")
        doc += style("h2{text-align:left}")
        doc += style("h4{text-align:left}")
        doc += style("div{text-align:left}")
        doc+=h2(company.name)
        for round in range(0, NUM_ROWS):
            doc += h3("Gang " + str(round + 1))
            for student in company.seats[round]:
                doc += h5(" " + unicode(str(student.name))+" ("+str(system[student.list_id][company.list_id])+")")
            doc += br()
        file = open("Output/Global/" + str(company.name) + '.html', 'w')
        file.write(str(doc))
        file.close()


