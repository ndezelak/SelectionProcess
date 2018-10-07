import Data.globals as globals
import pickle
from PyQt5.QtCore import QThread
from fpdf import FPDF
from PyQt5.QtWidgets import QMessageBox

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

    # Callback for thread start by the system
    def run(self):
        #print("Thread started")
        globals.main_page.update_progress_dialog_signal.emit(1)
        self.generate_student_pdfs()
        self.generate_company_pdfs()
        globals.main_page.pdf_generation_done_signal.emit()
        print("Done generating the pdf file")
        self.quit()

    # Callback for thread termination by the system
    def finished(self):
        super().finished()
        print("Thread finished")

    # Create a single page for a student
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

    # Create a single page for a company
    def create_company_page(self, company):
        globals.pdf_companies.add_page()

        globals.pdf_companies.image("logo.png", x=(globals.pdf_companies.w) / 4, y=10, w=(globals.pdf_companies.w) / 2,
                                   h=60)
        globals.pdf_companies.ln(80)
        globals.pdf_companies.set_font("Arial", "B", size=32)
        globals.pdf_companies.multi_cell(globals.pdf_companies.w,10,txt=company.name,ln=1,align="C")
        globals.pdf_companies.ln(5)
        counter = 1
        for seat in company.seats:
            globals.pdf_companies.set_font("Arial", size=16)
            globals.pdf_companies.multi_cell(globals.pdf_companies.w,10,txt="Gang "+str(counter)+":",ln=1,align="C")
            globals.pdf_companies.set_font("Arial", size=12)
            counter+=1
            for student in seat:
                globals.pdf_companies.multi_cell(globals.pdf_companies.w,10,txt=student.name,ln=1,align="C")


    # Create the pdf for companies
    def generate_company_pdfs(self):
        path = globals.current_session.pdf_dir
        if path == None or path == "":
            #QMessageBox.warning(None, "Warning", "Specify the pdf output directory first!", QMessageBox.Ok)
            return 0
        for company in globals.current_session.companies:
            self.create_company_page(company = company)
        while(True):
            try:
                with open(path+"\Companies.pdf","wb") as file:
                    break
            except PermissionError:
                QMessageBox.warning(None, "Warning", "Close the open PDF document with the name " +
                                    "Company.pdf" + "!",
                                            QMessageBox.Ok)
        globals.pdf_companies.output(path + '\Companies.pdf')
        globals.pdf_companies = FPDF()
        globals.pdf_companies.set_margins(left=0, right=0, top=0)
    # Create the PDF for students
    def generate_student_pdfs(self):
        path = globals.current_session.pdf_dir
        if path == None or path == "":
            #QMessageBox.warning(None, "Warning", "Specify the pdf output directory first!", QMessageBox.Ok)
            return 0
        for student in globals.current_session.passed_students:
            self.counter +=1
            #print("Update progress dialog called")
            globals.main_page.update_progress_dialog_signal.emit(self.counter)
            self.create_student_page(student)
        print("Done creating pages")
        try:
            with open(path+'\Studenten.pdf','wb') as file:
                pass
        except PermissionError:
            print("Please close the PDF document with the name "+"Studenten.pdf"+"!")
            value = 0
            while(value == 0):
                value = QMessageBox.warning(None,"Warning","Please close the PDF document with the name "+"Studenten.pdf"+"!"
                                            ,QMessageBox.Ok)
        # Create the pdf document in the specified folder
        globals.pdf_students.output(path+'\Studenten.pdf')
        # Reinitialize the document object
        globals.pdf_students = FPDF()
        globals.pdf_students.set_margins(left=0,right=0,top=0)
