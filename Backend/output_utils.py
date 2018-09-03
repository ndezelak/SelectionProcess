import Data.globals as globals
import pickle
from PyQt5.QtCore import QThread
from fpdf import FPDF

def save_project():
    with open(globals.current_session.name+".bonding","wb") as file:
        pickle.dump(globals.current_session,file,pickle.HIGHEST_PROTOCOL)
    print("Project saved!")

# Thread for generating PDF files
class PDF_thread(QThread):
    def __init__(self, wait_condition = [], mutex = []):
        super().__init__()
        self.wait_condition = wait_condition
        self.mutex = mutex
        self.counter = 0
    def run(self):
        print("Thread started")
        globals.main_page.update_progress_dialog_signal.emit(1)
        self.generate_student_pdfs()

    def finished(self):
        super().finished()
        print("Thread finished")

    def initialize_document(self):
        globals.pdf_students.add_font(family='DejaVu',style='',fname='DejaVuSansCondensed.ttf', uni=True)

    def create_student_page(self,student):
        globals.pdf_students.add_page()
        globals.pdf_students.image("logo.png", x=(globals.pdf_students.w) / 4, y=10, w=(globals.pdf_students.w) / 2,
                                   h=30)
        globals.pdf_students.ln(80)

        #Check if student's names are all latin-1 encodable
        try:
            self.mutex.lock()
            student.name.encode('latin-1')
        except UnicodeEncodeError:
            print("Signal is about to be emitted!")
            globals.main_page.correct_student_name_signal.emit(student)
            print("Thread is about to wait ...")
            self.wait_condition.wait(self.mutex)
        except Exception as e:
            print("Unexpected exception:")
        # Student name display
        globals.pdf_students.set_font("Arial", "B", size=32)
        globals.pdf_students.multi_cell(globals.pdf_students.w, 10, txt=student.name, ln=1, align="C")
        # Student companies
        globals.pdf_students.ln(20)

        pointer = 1
        for seat in student.seats:
            globals.pdf_students.set_font("Arial", size=16)
            globals.pdf_students.multi_cell(200, 10, txt="Gang "+str(pointer)+":", ln=1, align="C")
            globals.pdf_students.set_font("Arial", "B", size=24)
            globals.pdf_students.multi_cell(200,10, txt = seat.name, ln=1, align="C")
            globals.pdf_students.ln(5)
            pointer += 1

        self.mutex.unlock()
    def generate_student_pdfs(self):
        for student in globals.passed_students:
            self.counter +=1
            print("Update progress dialog called")
            globals.main_page.update_progress_dialog_signal.emit(self.counter)
            self.create_student_page(student)
        print("Done creating pages")
        globals.pdf_students.output('Studenten.pdf')
        globals.pdf_students = FPDF()
        globals.pdf_students.set_margins(left=0,right=0,top=0)
        globals.main_page.pdf_generation_done_signal.emit()
        self.quit()
        print("Done generating the pdf file")


'''
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


def create_company_plan(sorted_companies, system):
    for company in sorted_companies:
        doc = document()
        doc += style("h1{text-align:left}")
        doc += style("h3{text-align:left}")
        doc += style("h2{text-align:left}")
        doc += style("h4{text-align:left}")
        doc += style("div{text-align:left}")
        doc += h2(company.name)
        for round in range(0, NUM_ROWS):
            doc += h3("Gang " + str(round + 1))
            for student in company.seats[round]:
                doc += h5(
                    " " + unicode(str(student.name)) + " (" + str(system[student.list_id][company.list_id]) + ")")
            doc += br()
        file = open("Output/Global/" + str(company.name) + '.html', 'w')
        file.write(str(doc))
        file.close()
'''