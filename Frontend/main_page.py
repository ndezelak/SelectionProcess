from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, QPushButton, QTableWidget, QLabel, QTextEdit, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot, Qt
from Backend.output_utils import save_project
from Frontend.field_of_study_page import *
from Frontend.add_company_page import *
class mainPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.initialize()
        self.parent = parent
        self.fields_of_study_window = []
        self.add_company_window = []

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

        label_firmen = QLabel()
        label_firmen.setText("Firmen")

        button_import_companies = QPushButton()
        button_import_companies.setText("Firma hinzufügen")
        button_import_companies.clicked.connect(self.add_company_clicked)

        button_delete_company = QPushButton("Firma entfernen")
        button_delete_company.clicked.connect(self.delete_company_clicked)

        # Student and company QTableWidgets
        self.table_students = QTableWidget()
        self.table_companies = QTableWidget()
        header_horizontal_name = QTableWidgetItem("Firma")
        header_horizontal_name.setFlags(Qt.ItemIsEnabled)
        header_horizontal_fields = QTableWidgetItem("Gesuchte Studienrichtungen")
        header_horizontal_fields.setFlags(Qt.ItemIsEnabled)
        self.table_companies.setColumnCount(2)
        self.table_companies.setRowCount(0)
        self.table_companies.setHorizontalHeaderItem(0,header_horizontal_name)
        self.table_companies.setHorizontalHeaderItem(1,header_horizontal_fields)
        self.table_companies.resizeColumnsToContents()
        self.table_companies.resizeRowsToContents()


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

    def update_companies(self):
        # Clear table
        self.table_companies.setRowCount(0)
        # Reserve table rows
        self.table_companies.setRowCount(len(globals.current_session.companies))
        self.table_companies.setColumnCount(2)
        index = 0
        for company in globals.current_session.companies:
            company_name = QTableWidgetItem(company.name)
            company_name.setFlags(Qt.ItemIsEnabled)
            string = ""
            for field in company.field_of_study:
                string+=field.name
                string+=", "
            company_fields = QTableWidgetItem(string)
            company_fields.setFlags(Qt.ItemIsEnabled)
            self.table_companies.setItem(index,0,company_name)
            self.table_companies.setItem(index, 1, company_fields)
            index+=1
        self.table_companies.resizeColumnsToContents()
        self.table_companies.resizeRowsToContents()

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




