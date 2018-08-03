from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, QPushButton, QTableWidget, QLabel, QTextEdit
from PyQt5.QtCore import pyqtSlot
from Backend.output_utils import save_project
class mainPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.initialize()
        self.parent = parent

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

        button_import_students = QPushButton()
        button_import_students.setText("Studenten aus einer Tabelle importieren")

        label_firmen = QLabel()
        label_firmen.setText("Firmen")

        button_import_companies = QPushButton()
        button_import_companies.setText("Firmen aus einer Tabelle importieren")

        table_students = QTableWidget()
        table_companies = QTableWidget()

        #upper_grid.addWidget(button_save, 0, 2)
        upper_grid.addWidget(label_students,0,0)
        upper_grid.addWidget(button_fields,0,1)
        upper_grid.addWidget(button_import_students,0,2)
        upper_grid.addWidget(label_firmen,0,3)
        upper_grid.addWidget(button_import_companies,0,4)
        upper_grid.addWidget(table_students,1,0,2,3)
        upper_grid.addWidget(table_companies,1,3,2,2)


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

    def closeEvent(self, QCloseEvent):
        save_project()
        super().closeEvent(QCloseEvent)

    @pyqtSlot()
    def callback_home(self):
        self.parent.home_button_clicked_signal.emit()



