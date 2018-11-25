from PyQt5.QtWidgets import QWidget, QLabel, QTextEdit, QPushButton, QRadioButton, QFrame, QVBoxLayout, QHBoxLayout, QGridLayout
import Data.globals as globals
from PyQt5.QtCore import pyqtSlot
import Data.globals as globals
from Data.data_structures import Company
import copy
class add_company_page(QWidget):
    def __init__(self,parent):
        super().__init__()
        self.initialize()
        self.parent = parent

    def initialize(self):
        self.setWindowTitle("Firma hinzufügen")
        # Basic widgets
        label_name = QLabel("Firmenname")
        self.text_name = QTextEdit()
        label_fields = QLabel("Gesuchte Studienrichtungen")
        button_ok = QPushButton("Firma hinzufügen")
        button_ok.clicked.connect(self.ok_clicked)
        button_cancel = QPushButton("Abbrechen")


        # OK and Cancel buttons
        buttons = QHBoxLayout()
        buttons.addWidget(button_ok)
        buttons.addWidget(button_cancel)
        frame_buttons = QFrame()
        frame_buttons.setLayout(buttons)

        # Radio buttons for fields of study
        self.radio_buttons = []
        label_radio_buttons = QLabel("Keine Studienrichtungen wurden eingegeben!")
        grid_radio_buttons = QGridLayout()
        for field in globals.current_session.fields_of_study:
            button = QPushButton(field.name)
            button.setCheckable(True)
            self.radio_buttons.append(button)

        if len(self.radio_buttons) == 0:
            grid_radio_buttons.addWidget(label_radio_buttons)
        else:
            for button in self.radio_buttons:
                grid_radio_buttons.addWidget(button)
        frame_radio_buttons = QFrame()
        frame_radio_buttons.setLayout(grid_radio_buttons)

        # GUI construction
        main_layout = QVBoxLayout()
        main_layout.addWidget(label_name)
        main_layout.addWidget(self.text_name)
        main_layout.addWidget(label_fields)
        main_layout.addWidget(frame_radio_buttons)
        main_layout.addWidget(frame_buttons)

        self.setLayout(main_layout)
        self.show()

    # Callbacks pushbuttons
    @pyqtSlot()
    def ok_clicked(self):
        fields = []
        for button in self.radio_buttons:
            if button.isChecked():
                button_text = button.text()
                for field in globals.current_session.fields_of_study:
                    if field.name == button_text:
                        fields.append(field)
                        break
        globals.current_session.companies.append(Company(name=self.text_name.toPlainText(),field_of_study=fields))
        self.hide()
        self.parent.update_companies()



