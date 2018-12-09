from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QSpinBox, QFrame, QVBoxLayout, QHBoxLayout, QGroupBox
from PyQt5.QtCore import pyqtSlot, Qt
import Data.globals as globals
from Data.data_structures import Table_Specs
class file_specifier_page(QWidget):
    def __init__(self,parent):
        super().__init__()
        self.initialize()
        self.parent = parent

    def initialize(self):
        self.setWindowTitle("Spezifizierung der Input-Tabelle")
        # User prompt text
        label_user_prompt = QLabel("Bitte gebe die Spalten- bzw. Zeilennummern ein. \nDie erste Spalte bzw. Zeile hat die Nummer 1")
        # Name, surname, field of study, degree, companies spinboxes
        label_name = QLabel("Vorname")
        label_name.setAlignment(Qt.AlignCenter)
        label_surname = QLabel("Name")
        label_surname.setAlignment(Qt.AlignCenter)
        label_field_of_study = QLabel("Studienrichtung")
        label_field_of_study.setAlignment(Qt.AlignCenter)
        label_degree = QLabel('Studienabschluss')
        label_degree.setAlignment(Qt.AlignCenter)
        label_companies = QLabel("Gewünschte Firmen von")
        label_companies.setAlignment(Qt.AlignCenter)
        label_to_1 = QLabel("bis")
        label_to_1.setAlignment(Qt.AlignCenter)
        label_to_2 = QLabel("bis")
        label_to_2.setAlignment(Qt.AlignCenter)
        self.spinbox_name = QSpinBox()
        self.spinbox_name.setAlignment(Qt.AlignCenter)
        self.spinbox_surname = QSpinBox()
        self.spinbox_surname.setAlignment(Qt.AlignCenter)
        self.spinbox_field_of_study = QSpinBox()
        self.spinbox_field_of_study.setAlignment(Qt.AlignCenter)
        self.spinbox_degree = QSpinBox()
        self.spinbox_degree.setAlignment(Qt.AlignCenter)
        self.spinbox_companies_from = QSpinBox()
        self.spinbox_companies_from.setAlignment(Qt.AlignCenter)
        self.spinbox_companies_to = QSpinBox()
        self.spinbox_companies_to.setAlignment(Qt.AlignCenter)
        # Layouts of the labels and spinboxes
        layout_name = QHBoxLayout()
        layout_name.addWidget(label_name)
        layout_name.addWidget(self.spinbox_name)
        layout_surname = QHBoxLayout()
        layout_surname.addWidget(label_surname)
        layout_surname.addWidget(self.spinbox_surname)
        layout_field_of_study = QHBoxLayout()
        layout_field_of_study.addWidget(label_field_of_study)
        layout_field_of_study.addWidget(self.spinbox_field_of_study)
        layout_degree = QHBoxLayout()
        layout_degree.addWidget(label_degree)
        layout_degree.addWidget(self.spinbox_degree)
        layout_companies = QHBoxLayout()
        layout_companies.addWidget(label_companies)
        layout_companies.addWidget(self.spinbox_companies_from)
        layout_companies.addWidget(label_to_1)
        layout_companies.addWidget(self.spinbox_companies_to)

        # Rows labels & spinboxes
        label_rows = QLabel("Studenten von")
        label_rows.setAlignment(Qt.AlignCenter)
        self.spinbox_rows_from = QSpinBox()
        self.spinbox_rows_from.setAlignment(Qt.AlignCenter)
        self.spinbox_rows_to = QSpinBox()
        self.spinbox_companies_to.setAlignment(Qt.AlignCenter)
        # Layout for the row labels and spinboxes
        layout_rows = QHBoxLayout()
        layout_rows.addWidget(label_rows)
        layout_rows.addWidget(self.spinbox_rows_from)
        layout_rows.addWidget(label_to_2)
        layout_rows.addWidget(self.spinbox_rows_to)
        #QFrames
        frame_name = QFrame()
        frame_name.setLayout(layout_name)
        frame_surname = QFrame()
        frame_surname.setLayout(layout_surname)
        frame_field_of_study = QFrame()
        frame_field_of_study.setLayout(layout_field_of_study)
        frame_degree = QFrame()
        frame_degree.setLayout(layout_degree)
        frame_companies = QFrame()
        frame_companies.setLayout(layout_companies)
        frame_rows = QFrame()
        frame_rows.setLayout(layout_rows)
        # OK and cancel pushbuttons
        pushbutton_ok = QPushButton("OK")
        pushbutton_ok.clicked.connect(self.ok_clicked)
        pushbutton_cancel = QPushButton("Abbrechen")
        pushbutton_cancel.clicked.connect(self.cancel_clicked)
        # Layout and frame for the pushbuttons
        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(pushbutton_ok)
        layout_buttons.addWidget(pushbutton_cancel)
        frame_buttons = QFrame(frame_name)
        frame_buttons.setLayout(layout_buttons)
        # Groupboxes
        groupbox_columns = QGroupBox("Spaltennummern")
        layout_columns = QVBoxLayout()
        layout_columns.addWidget(frame_name)
        layout_columns.addWidget(frame_surname)
        layout_columns.addWidget(frame_field_of_study)
        layout_columns.addWidget(frame_degree)
        layout_columns.addWidget(frame_companies)
        groupbox_columns.setLayout(layout_columns)
        groupbox_rows = QGroupBox("Zeilennummern")
        layout_rows = QVBoxLayout()
        layout_rows.addWidget(frame_rows)
        groupbox_rows.setLayout(layout_rows)

        # Main layout
        layout_main = QVBoxLayout()
        layout_main.addWidget(label_user_prompt)
        layout_main.addWidget(groupbox_columns)
        layout_main.addWidget(groupbox_rows)
        layout_main.addWidget(frame_buttons)

        self.setLayout(layout_main)
        self.setWindowModality(Qt.ApplicationModal)
        self.show()
    @pyqtSlot()
    def ok_clicked(self):
        globals.table_specs = Table_Specs(ID_name=self.spinbox_name.value(),
                                          ID_surname=self.spinbox_surname.value(),
                                          ID_field_of_study=self.spinbox_field_of_study.value(),
                                          ID_degree=self.spinbox_degree.value(),
                                          IDs_companies=[self.spinbox_companies_from.value(),self.spinbox_companies_to.value(),],
                                          IDs_students=[self.spinbox_rows_from.value(),self.spinbox_rows_to.value()])
        self.hide()
        self.parent.input_table_specified.emit()
    @pyqtSlot()
    def cancel_clicked(self):
        self.hide()
