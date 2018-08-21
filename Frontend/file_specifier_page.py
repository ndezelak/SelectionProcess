from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QSpinBox, QFrame, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import pyqtSlot
import Data.globals as globals
from Data.data_structures import Table_Specs
class file_specifier_page(QWidget):
    def __init__(self,parent):
        super().__init__()
        self.initialize()
        self.parent = parent

    def initialize(self):
        self.setWindowTitle("Spezifizierung der Tabelle")
        # User prompt
        label_user_prompt = QLabel("Bitte gebe die Spaltennummer ein (von links nach rechts, die erste Spalte hat die Nummer 1)")
        # Name, surname, field of study, companies
        label_name = QLabel("Vorname")
        label_surname = QLabel("Name")
        label_field_of_study = QLabel("Studienrichtung")
        label_companies = QLabel("Gewünschte Firmen von _ bis _ (Bei nur einer Spalte die Spaltennummer zweimal eingeben)")
        self.spinbox_name = QSpinBox()
        self.spinbox_surname = QSpinBox()
        self.spinbox_field_of_study = QSpinBox()
        self.spinbox_companies_from = QSpinBox()
        self.spinbox_companies_to = QSpinBox()
        layout_name = QHBoxLayout()
        layout_name.addWidget(label_name)
        layout_name.addWidget(self.spinbox_name)
        layout_surname = QHBoxLayout()
        layout_surname.addWidget(label_surname)
        layout_surname.addWidget(self.spinbox_surname)
        layout_field_of_study = QHBoxLayout()
        layout_field_of_study.addWidget(label_field_of_study)
        layout_field_of_study.addWidget(self.spinbox_field_of_study)
        layout_companies = QHBoxLayout()
        layout_companies.addWidget(label_companies)
        layout_companies.addWidget(self.spinbox_companies_from)
        layout_companies.addWidget(self.spinbox_companies_to)
        # Rows
        label_rows = QLabel("Zeilen mit Studenten von _ bis _")
        self.spinbox_rows_from = QSpinBox()
        self.spinbox_rows_to = QSpinBox()
        layout_rows = QHBoxLayout()
        layout_rows.addWidget(label_rows)
        layout_rows.addWidget(self.spinbox_rows_from)
        layout_rows.addWidget(self.spinbox_rows_to)
        frame_rows = QFrame()
        frame_rows.setLayout(layout_rows)
        #Frames
        frame_name = QFrame()
        frame_name.setLayout(layout_name)
        frame_surname = QFrame()
        frame_surname.setLayout(layout_surname)
        frame_field_of_study = QFrame()
        frame_field_of_study.setLayout(layout_field_of_study)
        frame_companies = QFrame()
        frame_companies.setLayout(layout_companies)
        # Pushbuttons
        pushbutton_ok = QPushButton("OK")
        pushbutton_ok.clicked.connect(self.ok_clicked)
        pushbutton_cancel = QPushButton("Abbrechen")
        pushbutton_cancel.clicked.connect(self.cancel_clicked)
        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(pushbutton_ok)
        layout_buttons.addWidget(pushbutton_cancel)
        frame_buttons = QFrame()
        frame_buttons.setLayout(layout_buttons)
        # Main layout
        layout_main = QVBoxLayout()
        layout_main.addWidget(label_user_prompt)
        layout_main.addWidget(frame_name)
        layout_main.addWidget(frame_surname)
        layout_main.addWidget(frame_field_of_study)
        layout_main.addWidget(frame_companies)
        layout_main.addWidget(frame_rows)
        layout_main.addWidget(frame_buttons)

        self.setLayout(layout_main)
        self.show()
    @pyqtSlot()
    def ok_clicked(self):
        globals.table_specs = Table_Specs(ID_name=self.spinbox_name.value(),
                                          ID_surname=self.spinbox_surname.value(),
                                          ID_field_of_study=self.spinbox_field_of_study.value(),
                                          IDs_companies=[self.spinbox_companies_from.value(),self.spinbox_companies_to.value(),],
                                          IDs_students=[self.spinbox_rows_from.value(),self.spinbox_rows_to.value()])
        self.hide()
        self.parent.input_table_specified.emit()
    @pyqtSlot()
    def cancel_clicked(self):
        self.hide()
