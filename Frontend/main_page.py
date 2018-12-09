from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, QPushButton, QTableWidget, QLabel, QLineEdit, QTableWidgetItem, QFileDialog, QProgressDialog
from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal, QWaitCondition, QMutex
from Backend.output_utils import save_project
from Backend.input_reading import thread_read_file
from Frontend.main_page_field_of_studies_display import *
from Frontend.main_page_add_company import *
from Frontend.main_page_specify_file_columns import *
from Frontend.string_matcher_page import *
from Frontend.main_page_selection_process_settings import *
from Backend.output_utils import PDF_thread
import Backend.backend_interface as backend_interface
import Backend.statistics as statistics
import PyQt5.QtGui as QtGui
from Frontend.main_page_unknown_company import *
import threading
from Data.data_structures import Degree

class mainPage(QWidget):
    # Signals
    input_table_specified = pyqtSignal()
    process_run = pyqtSignal()
    correct_student_name_signal = pyqtSignal('PyQt_PyObject')
    update_progress_dialog_signal = pyqtSignal('int')
    pdf_generation_done_signal = pyqtSignal()
    create_unknown_company_window_signal = pyqtSignal(str)
    unknown_field_of_study_specified = pyqtSignal('PyQt_PyObject')
    create_string_matcher_signal = pyqtSignal('PyQt_PyObject','PyQt_PyObject','PyQt_PyObject','PyQt_PyObject')

    def __init__(self, parent):
        super().__init__()
        self.initialize()
        self.update_companies()
        self.update_students()
        self.update_pdf_dir_display(globals.current_session.pdf_dir)
        self.parent = parent
        self.fields_of_study_window = []
        self.add_company_window = []
        self.file_specifier_page = []
        self.input_table_specified.connect(self.read_table)
        self.process_run.connect(self.update_statistics_display)
        self.file_path = []
        self.pdf_thread = []
        self.correct_student_name_signal.connect(self.correct_student_name)
        self.wait_condition = QWaitCondition()
        self.mutex = QMutex()
        self.progress_dialog = []
        self.update_progress_dialog_signal.connect(self.set_progress_dialog)
        self.pdf_generation_done_signal.connect(self.pdf_generation_done)
        self.messagebox = []
        self.unknown_company_window = []
        self.reading_thread = []
        self.create_unknown_company_window_signal.connect(self.create_unknown_company_window)
        self.unknown_field_of_study_specified.connect(self.on_field_of_study_specified)
        self.create_string_matcher_signal.connect(self.slot_create_string_matcher)
        # Copy the current session to the buffer
        globals.current_session_buffer = copy.deepcopy(globals.current_session)
        # Save reference to this window globally
        globals.main_page = self
    # GUI construction
    def initialize(self):
        self.setWindowTitle("Career Night App")
        self.showMaximized()

        # Define layouts
        main_layout = QVBoxLayout()
        upper_grid = QGridLayout()
        settings = QVBoxLayout()
        bottom_grid = QGridLayout()

        #------- Upper grid -------#
        button_save = QPushButton()
        button_save.setText("Projekt speichern")
        button_save.clicked.connect(self.save_project_clicked)

        label_students = QLabel()
        label_students.setText("Studenten")

        button_fields = QPushButton()
        button_fields.setText("Studienrichtungen eingeben")
        button_fields.clicked.connect(self.settings_clicked)

        button_import_students = QPushButton()
        button_import_students.setText("Studentendaten aus einer Tabelle auslesen")
        button_import_students.clicked.connect(self.choose_file_clicked)

        label_firmen = QLabel()
        label_firmen.setText("Firmen")

        button_import_companies = QPushButton()
        button_import_companies.setText("Firma hinzufügen")
        button_import_companies.clicked.connect(self.add_company_clicked)

        button_delete_company = QPushButton("Firma entfernen")
        button_delete_company.clicked.connect(self.delete_company_clicked)

        # Student and company QTableWidgets
        self.table_students = QTableWidget()
        header_student_name = QTableWidgetItem("Name")
        header_student_name.setFlags(Qt.ItemIsEnabled)
        header_field = QTableWidgetItem("Studiengang")
        header_field.setFlags(Qt.ItemIsEnabled)
        header_companies = QTableWidgetItem("Gewünschte Firmen")
        header_companies.setFlags(Qt.ItemIsEnabled)
        header_degree = QTableWidgetItem('Studienabschnitt')
        header_degree.setFlags(Qt.ItemIsEnabled)
        header_match = QTableWidgetItem("Matching mit den Firmen")
        header_match.setFlags(Qt.ItemIsEnabled)
        self.table_students.setColumnCount(4)
        #self.table_students.
        self.table_students.setColumnWidth(0,self.table_students.width()/5)
        self.table_students.setColumnWidth(1, self.table_students.width() / 5)
        self.table_students.setColumnWidth(2, self.table_students.width() / 5)
        self.table_students.setColumnWidth(3, self.table_students.width() / 5)
        self.table_students.setColumnWidth(4, self.table_students.width() / 5)
        self.table_students.setHorizontalHeaderItem(0,header_student_name)
        self.table_students.setHorizontalHeaderItem(1,header_field)
        self.table_students.setHorizontalHeaderItem(2,header_companies)
        self.table_students.setHorizontalHeaderItem(3,header_degree)
        self.table_students.setHorizontalHeaderItem(4,header_match)

        self.table_companies = QTableWidget()
        header_horizontal_name = QTableWidgetItem("Firma")
        header_horizontal_name.setFlags(Qt.ItemIsEnabled)
        header_horizontal_fields = QTableWidgetItem("Gesuchte Studienrichtungen")
        header_horizontal_fields.setFlags(Qt.ItemIsEnabled)
        header_horizontal_degrees = QTableWidgetItem("Gesuchte Studienabschnitte")
        header_horizontal_degrees.setFlags(Qt.ItemIsEnabled)
        self.table_companies.setColumnCount(3)
        self.table_companies.setRowCount(0)
        self.table_companies.setHorizontalHeaderItem(0,header_horizontal_name)
        self.table_companies.setHorizontalHeaderItem(1,header_horizontal_fields)
        self.table_companies.setHorizontalHeaderItem(2, header_horizontal_degrees)
        self.table_companies.setColumnWidth(0,self.table_companies.width()/3)
        self.table_companies.setColumnWidth(1, self.table_companies.width() / 3)
        self.table_companies.setColumnWidth(2, self.table_companies.width() / 3)


        upper_grid.addWidget(label_students,0,0)
        upper_grid.addWidget(button_fields,0,1)
        upper_grid.addWidget(button_import_students,0,2)
        upper_grid.addWidget(label_firmen,0,3)
        upper_grid.addWidget(button_import_companies,0,4)
        upper_grid.addWidget(button_delete_company,0,5)
        upper_grid.addWidget(self.table_students,1,0,5,3)
        upper_grid.addWidget(self.table_companies,1,3,5,3)

        #---------- Settings -----------#
        button_settings = QPushButton()
        button_settings.setText("Prozess Einstellungen")
        button_settings.clicked.connect(self.process_settings_clicked)


        button_start_process = QPushButton()
        button_start_process.setText("Prozess neu ausführen")
        button_start_process.clicked.connect(self.new_start_clicked)

        button_start_process_limited = QPushButton()
        button_start_process_limited.setText("Prozess nur an neuen Studenten ausführen")


        settings.addWidget(button_settings)
        settings.addWidget(button_start_process)
        #settings.addWidget(button_start_process_limited)

        #------- Bottom grid --------#
        label_statistik = QLabel()
        label_statistik.setText("Ergebnisse")

        button_statistics = QPushButton()
        button_statistics.setText("Detailierte Statistik")

        self.text_output = QTextEdit()
        self.text_output.setText("Anzahl von Studenten: 40 \nAnzahl von Firmen: 8")
        self.text_output.setReadOnly(True)

        button_pdf_dir = QPushButton()
        button_pdf_dir.setText("Zielpfad eingeben")
        button_pdf_dir.clicked.connect(self.set_pdf_dir_clicked)

        self.label_pdf_dir = QLabel()
        self.label_pdf_dir.setText('Kein Zielpfad für die pdfs wurde ausgewählt!')

        button_pdf_gen = QPushButton()
        button_pdf_gen.setText("Generate pdfs")
        button_pdf_gen.clicked.connect(self.generate_pdfs_clicked)

        button_home = QPushButton()
        button_home.setText("HOME")
        button_home.clicked.connect(self.callback_home)

        button_help = QPushButton()
        button_help.setText("HILFE")

        bottom_grid.addWidget(label_statistik,0,0,1,5)
        #bottom_grid.addWidget(button_statistics,0,5,1,1)
        bottom_grid.addWidget(self.text_output,1,0,6,6)
        bottom_grid.addWidget(button_pdf_dir,7,0)
        bottom_grid.addWidget(self.label_pdf_dir,7,1,1,2)
        bottom_grid.addWidget(button_pdf_gen,8,0,1,3)
        bottom_grid.addWidget(button_home,8,3)
        #bottom_grid.addWidget(button_help,8,5)

        # ----- Main Groupboxes ----- #
        groupbox_data = QGroupBox()
        groupbox_data.setTitle("Studenten und Firmen")
        groupbox_data.setLayout(upper_grid)

        groupbox_settings = QGroupBox()
        groupbox_settings.setTitle("Steuerung des Auswahlprozesses")
        groupbox_settings.setLayout(settings)

        groupbox_output = QGroupBox()
        groupbox_output.setTitle("Ausgaben")
        groupbox_output.setLayout(bottom_grid)

        # Set main layout
        #main_layout.addWidget(button_save)
        main_layout.addWidget(groupbox_data)
        main_layout.addWidget(groupbox_settings)
        main_layout.addWidget(groupbox_output)
        self.setLayout(main_layout)
        self.show()


    # Update company display
    def update_companies(self):
        # Clear table
        self.table_companies.setRowCount(0)
        # Reserve table rows
        self.table_companies.setRowCount(len(globals.current_session.companies))

        index = 0
        for company in globals.current_session.companies:
            company_name = QTableWidgetItem(company.name)
            company_name.setFlags(Qt.ItemIsEnabled)

            list_of_fields = []
            for field in company.field_of_study:
                list_of_fields.append(field.name)
            string = ",".join(list_of_fields)

            list_of_degrees = []
            for degree in company.degrees:
                list_of_degrees.append(degree.name)
            string_ = ",".join(list_of_degrees)

            company_fields = QTableWidgetItem(string)
            company_fields.setFlags(Qt.ItemIsEnabled)
            company_degrees = QTableWidgetItem(string_)
            company_degrees.setFlags(Qt.ItemIsEnabled)
            self.table_companies.setItem(index,0,company_name)
            self.table_companies.setItem(index, 1, company_fields)
            self.table_companies.setItem(index, 2, company_degrees)
            index+=1
        self.table_companies.resizeRowsToContents()
    # Update students display
    def update_students(self):
        # First delete all remaining table items
        self.table_students.setRowCount(0)
        # Reserve table rows
        self.table_students.setRowCount(len(globals.current_session.students))
        index = 0
        for student in globals.current_session.students:
            student_name = QTableWidgetItem(student.name)
            student_name.setFlags(Qt.ItemIsEnabled)
            student_field_of_study = QTableWidgetItem(student.field_of_study.name)
            student_field_of_study.setFlags(Qt.ItemIsEnabled)
            if isinstance(student.degree, Degree):
                student_degree = QTableWidgetItem(student.degree.name)
            else:
                student_degree = QTableWidgetItem('')
            student_degree.setFlags(Qt.ItemIsEnabled)
            list_companies = []
            for company in student.companies:
                if company != []:
                    list_companies.append(company.name)
            student_companies = QTableWidgetItem(",".join(list_companies))
            student_companies.setFlags(Qt.ItemIsEnabled)
            self.table_students.setItem(index,0,student_name)
            self.table_students.setItem(index,1,student_field_of_study)
            self.table_students.setItem(index,2,student_companies)
            self.table_students.setItem(index,3,student_degree)
            index = index + 1

    # Callback when the main window is closed
    def closeEvent(self, QCloseEvent):
        save_project()
        super().closeEvent(QCloseEvent)

    # Slot: for creating a QInputDialog to remove nonlatin letters from a students name
    @pyqtSlot('PyQt_PyObject')
    def correct_student_name(self,student_object):
        print('Slot called!')
        [get_str, okPressed] = QInputDialog.getText(None, "Unbekannter Buchstabe!",
                                                    "Bitte gebe die deutsche Version diesen Namens an: " + student_object.name,
                                                    QLineEdit.Normal, "")
        if okPressed and get_str != "":
            student_object.name = get_str
        else:
            #TODO: How to react to this?
            pass
        # Wake all waiting threads (waiting on the wait_condition)
        self.wait_condition.wakeAll()

    # Slot: Home button clicked (emits a signal to the start_page)
    @pyqtSlot()
    def callback_home(self):
        self.parent.home_button_clicked_signal.emit()

    # Slot: Settings clicked (creates the settings window)
    @pyqtSlot()
    def settings_clicked(self):
        self.fields_of_study_window = field_of_study(self)

    # Slot: Add a company to the list
    @pyqtSlot()
    def add_company_clicked(self):
        self.add_company_window = add_company_page(self)

    # Slot: Delete a company from the list
    @pyqtSlot()
    def delete_company_clicked(self):
        current_row = self.table_companies.currentRow()
        if current_row == -1: return
        company_item = self.table_companies.item(current_row,0)
        for company in globals.current_session.companies:
            if company_item.text() == company.name:
                globals.current_session.companies.remove(company)
        self.update_companies()

    # Slot: Display a QFileDialog to choose the file and run the file_specifier afterwards
    @pyqtSlot()
    def choose_file_clicked(self):
        matcher = string_matcher_page(self)
        if len(globals.current_session.fields_of_study) == 0 and len(globals.current_session.companies) == 0:
            matcher.display_error(window=self, window_title="Fehlende Daten",
                                  text="Zuerst müssen Studiengänge und Firmen definiert werden!")
            return
        elif len(globals.current_session.fields_of_study) == 0:
            matcher.display_error(window=self, window_title="Fehlende Daten",
                                  text="Studiengänge müssen noch definiert!")
            return
        elif len(globals.current_session.companies) == 0:
            matcher.display_error(window=self, window_title="Fehlende Daten",
                                  text="Firmen müssen noch definiert werden!")
            return
        self.file_path =  QFileDialog.getOpenFileName(self, 'Open file',
         globals.home_dir+"\\Input","CSV File (*.csv)")
        if self.file_path[0] != "":
            self.file_specifier_page = file_specifier_page(self)

    # Slot: Read the specified file (run when the signal file_specified is emitted)
    @pyqtSlot()
    def read_table(self):
        self.reading_thread = thread_read_file(file=self.file_path[0],widget = self, parent=self,
                                               mutex=self.mutex,wait_condition=self.wait_condition)
        self.reading_thread.start()

    # Slot: Display the process settings page to alter the display settings
    @pyqtSlot()
    def process_settings_clicked(self):
        self.process_settings_page = process_settings_page()

    # Slot: The selection process should be rerun
    @pyqtSlot()
    def new_start_clicked(self):
        backend_interface.start()

    # Slot: Update the statistics text display (run when the signal process_run is emitted)
    @pyqtSlot()
    def update_statistics_display(self):
        string = " ERGEBNISSE: \n"
        string+= "Angenommene Studenten: " + str(statistics.get_student_pass_rate()[0])+" von "+str(statistics.get_student_pass_rate()[1])+"\n"
        string += "Durchschnittliche Erfüllung der Wünsche von Studenten: " + str(
            int(statistics.get_students_average_wish_rate()*100)) + "%\n"
        string += "Durchschnittliche Erfüllung der Wünsche von Firmen: " + str(
            int(statistics.get_company_average_wish_rate()*100)) + "%\n"
        string += "--------------------------------------------\n"
        string += "Besetzung der Gänge je Firma je Gang: \n"
        for company in globals.current_session.companies:
            string+= company.name + " "
            string+=str(statistics.get_row_covering(company)) + "\n"
        self.text_output.setText(string)

    # Slot: QFileDialog is displayed to specify the savepath of pdf files
    @pyqtSlot()
    def set_pdf_dir_clicked(self):
        dir = QFileDialog.getExistingDirectory(parent=self,caption="Wähle den Zielpfad aus",directory="C://")
        self.update_pdf_dir_display(dir=dir)

    def update_pdf_dir_display(self,dir):
        if dir != None and dir!='':
            self.label_pdf_dir.setText(dir)
            globals.current_session.pdf_dir = dir
            #print("Saved pdf dir to session: " + globals.current_session.pdf_dir)
            save_project()
        else:
            self.label_pdf_dir.setText('Kein Zielpfad für die pdfs wurde ausgewählt!')
            globals.current_session.pdf_dir = None
            save_project()

    # Slot: Start the PDF generation thread
    @pyqtSlot()
    def generate_pdfs_clicked(self):
        path = globals.current_session.pdf_dir
        # pdf path not yet specified
        if path == None or path == "":
            QMessageBox.warning(None,"Warning","Specify the pdf output directory first!",QMessageBox.Ok)
            return 0
        # Create a new thread for pdf generation
        self.pdf_thread = PDF_thread(wait_condition=self.wait_condition,mutex=self.mutex)
        # Progressbar initialization
        self.progress_dialog = QProgressDialog()
        self.progress_dialog.setMaximum(len(globals.passed_students))
        self.progress_dialog.setLabelText("Bitte warte ein Moment ...")
        self.progress_dialog.setWindowTitle("PDF Generierung")
        self.progress_dialog.open()

        print("Progress bar opened!")
        self.pdf_thread.start()
        print("PDF Thread started!")

    @pyqtSlot(int)
    def set_progress_dialog(self, value):
        self.progress_dialog.setValue(value)
        print("Progressbar updated")

    @pyqtSlot()
    def pdf_generation_done(self):
        if not (self.progress_dialog.wasCanceled()):
            self.progress_dialog.cancel()
        QMessageBox.information(None,"PDF Generierung","Fertig!")
        self.pdf_thread = []

    @pyqtSlot()
    def save_project_clicked(self):
        save_project()
        #self.unknown_company_window = unknown_company_window("blabla",self.wait_condition)

    @pyqtSlot(str)
    def create_unknown_company_window(self,company_text):
        self.unknown_company_window = unknown_company_window(company_text,self.wait_condition)

    @pyqtSlot('PyQt_PyObject')
    def on_field_of_study_specified(self, results):
        self.results = results
        self.wait_condition.wakeAll()

    def return_result_field_of_study(self):
        return self.results


    def create_string_matcher(self,window = [],window_title="Unbekannter Studiengang",
                                        text= [],
                                        items=[]):
        self.create_string_matcher_signal.emit(window,window_title,text,items)


    @pyqtSlot('PyQt_PyObject','PyQt_PyObject','PyQt_PyObject','PyQt_PyObject')
    def slot_create_string_matcher(self,window,window_title,text,items):
        self.field_of_study_window = string_matcher_page(self)
        self.field_of_study_window.get_item(window = self, window_title=window_title,
                                                       text = text, items = items)













