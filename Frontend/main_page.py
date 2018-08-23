from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, QPushButton, QTableWidget, QLabel, QTextEdit, QTableWidgetItem, QFileDialog
from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal
from Backend.output_utils import save_project
from Backend.input_reading import read_file
from Frontend.field_of_study_page import *
from Frontend.add_company_page import *
from Frontend.file_specifier_page import *
from Frontend.string_matcher_page import *
class mainPage(QWidget):
    # signals
    input_table_specified = pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.initialize()
        self.parent = parent
        self.fields_of_study_window = []
        self.add_company_window = []
        self.file_specifier_page = []
        self.input_table_specified.connect(self.read_table)
        self.file_path = []
        self.update_companies()

    def initialize(self):
        self.setWindowTitle("Career Night App")
        self.showMaximized()

        # Define layouts
        main_layout = QVBoxLayout()
        upper_grid = QGridLayout()
        settings = QVBoxLayout()
        bottom_grid = QGridLayout()

        # Upper grid
        button_save = QPushButton()
        button_save.setText("Projekt speichern")

        label_students = QLabel()
        label_students.setText("Studenten")

        button_fields = QPushButton()
        button_fields.setText("Studienrichtungen eingeben")
        button_fields.clicked.connect(self.settings_clicked)

        button_import_students = QPushButton()
        button_import_students.setText("Studenten aus einer Tabelle importieren")
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
        header_match = QTableWidgetItem("Matching mit den Firmen")
        header_match.setFlags(Qt.ItemIsEnabled)
        self.table_students.setColumnCount(4)
        #self.table_students.
        self.table_students.setColumnWidth(0,self.table_students.width()/4)
        self.table_students.setColumnWidth(1, self.table_students.width() / 4)
        self.table_students.setColumnWidth(2, self.table_students.width() / 4)
        self.table_students.setColumnWidth(3, self.table_students.width() / 4)
        self.table_students.setHorizontalHeaderItem(0,header_student_name)
        self.table_students.setHorizontalHeaderItem(1,header_field)
        self.table_students.setHorizontalHeaderItem(2,header_companies)
        self.table_students.setHorizontalHeaderItem(3,header_match)

        self.table_companies = QTableWidget()
        header_horizontal_name = QTableWidgetItem("Firma")
        header_horizontal_name.setFlags(Qt.ItemIsEnabled)
        header_horizontal_fields = QTableWidgetItem("Gesuchte Studienrichtungen")
        header_horizontal_fields.setFlags(Qt.ItemIsEnabled)
        self.table_companies.setColumnCount(2)
        self.table_companies.setRowCount(0)
        self.table_companies.setHorizontalHeaderItem(0,header_horizontal_name)
        self.table_companies.setHorizontalHeaderItem(1,header_horizontal_fields)
        self.table_companies.setColumnWidth(0,self.table_companies.width()/2)
        self.table_companies.setColumnWidth(1, self.table_companies.width() / 2)


        upper_grid.addWidget(label_students,0,0)
        upper_grid.addWidget(button_fields,0,1)
        upper_grid.addWidget(button_import_students,0,2)
        upper_grid.addWidget(label_firmen,0,3)
        upper_grid.addWidget(button_import_companies,0,4)
        upper_grid.addWidget(button_delete_company,0,5)
        upper_grid.addWidget(self.table_students,1,0,5,3)
        upper_grid.addWidget(self.table_companies,1,3,5,3)

        # Settings
        button_settings = QPushButton()
        button_settings.setText("Prozess Einstellungen")


        button_start_process = QPushButton()
        button_start_process.setText("Prozess neu ausführen")

        button_start_process_limited = QPushButton()
        button_start_process_limited.setText("Prozess nur an neuen Studenten ausführen")


        settings.addWidget(button_settings)
        settings.addWidget(button_start_process)
        settings.addWidget(button_start_process_limited)

        # Bottom grid
        label_statistik = QLabel()
        label_statistik.setText("Ergebnisse")

        button_statistics = QPushButton()
        button_statistics.setText("Detailierte Statistik")

        text_output = QTextEdit()
        text_output.setText("Anzahl von Studenten: 40 \nAnzahl von Firmen: 8")
        text_output.setReadOnly(True)

        button_pdf_dir = QPushButton()
        button_pdf_dir.setText("Zielpfad eingeben")

        label_pdf_dir = QLabel()
        label_pdf_dir.setText("C:/Users")

        button_pdf_gen = QPushButton()
        button_pdf_gen.setText("Generate pdfs")

        button_home = QPushButton()
        button_home.setText("HOME")
        button_home.clicked.connect(self.callback_home)

        button_help = QPushButton()
        button_help.setText("HILFE")

        bottom_grid.addWidget(label_statistik,0,0,1,5)
        bottom_grid.addWidget(button_statistics,0,5,1,1)
        bottom_grid.addWidget(text_output,1,0,6,6)
        bottom_grid.addWidget(button_pdf_dir,7,0)
        bottom_grid.addWidget(label_pdf_dir,7,1,1,2)
        bottom_grid.addWidget(button_pdf_gen,8,0,1,3)
        bottom_grid.addWidget(button_home,8,3)
        bottom_grid.addWidget(button_help,8,5)

        # Groupboxes
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
        main_layout.addWidget(button_save)
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
            company_fields = QTableWidgetItem(string)
            company_fields.setFlags(Qt.ItemIsEnabled)
            self.table_companies.setItem(index,0,company_name)
            self.table_companies.setItem(index, 1, company_fields)
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
            list_companies = []
            for company in student.companies:
                if company != "":
                    list_companies.append(company.name)
            student_companies = QTableWidgetItem(",".join(list_companies))
            student_companies.setFlags(Qt.ItemIsEnabled)
            self.table_students.setItem(index,0,student_name)
            self.table_students.setItem(index,1,student_field_of_study)
            self.table_students.setItem(index,2,student_companies)
            index = index + 1

    # Callback when the main window is closed
    def closeEvent(self, QCloseEvent):
        save_project()
        super().closeEvent(QCloseEvent)

    @pyqtSlot()
    def callback_home(self):
        self.parent.home_button_clicked_signal.emit()

    @pyqtSlot()
    def settings_clicked(self):
        self.fields_of_study_window = field_of_study(self)

    @pyqtSlot()
    def add_company_clicked(self):
        self.add_company_window = add_company_page(self)

    @pyqtSlot()
    def delete_company_clicked(self):
        current_row = self.table_companies.currentRow()
        company_item = self.table_companies.item(current_row,0)
        for company in globals.current_session.companies:
            if company_item.text() == company.name:
                globals.current_session.companies.remove(company)
        self.update_companies()

    @pyqtSlot()
    def choose_file_clicked(self):
        matcher = string_matcher_page()
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
        self.file_specifier_page = file_specifier_page(self)

    @pyqtSlot()
    def read_table(self):
        read_file(file_path=self.file_path[0],widget=self) #file_path is a tuple of file_path and file type filter
        self.update_students()
        save_project()






