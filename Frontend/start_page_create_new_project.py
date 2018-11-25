from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QLineEdit, QLabel, QSpinBox
from PyQt5.QtCore import *
import Data.globals as globals
from Data.data_structures import Session, Settings
from Backend.output_utils import save_project
import pickle

class newProjectWindow(QWidget):
    def __init__(self,parent):
        super().__init__()
        self.initialize()
        self.parent = parent
    def initialize(self):
        self.setWindowTitle("Einstellungen des neuen Projektes")

        # OK button
        self.button_ok = QPushButton()
        self.button_ok.setText("OK")
        self.button_ok.clicked.connect(self.finished)

        # Cancel button
        self.button_cancel = QPushButton()
        self.button_cancel.setText("Abbrechen")
        self.button_cancel.clicked.connect(self.cancel)

        # Projectname
        text_projectname = QLabel()
        text_projectname.setText("Projekt Name:")
        self.text_user = QLineEdit()
        #self.text_user.setFixedHeight(20)

        # Number of menus
        self.num_menus = QSpinBox()
        self.num_menus.setMinimum(1)
        self.num_menus.setMaximum(5)
        text_num_menus = QLabel()
        text_num_menus.setText("Anzahl der Gänge:")

        # Min and max number of people at each table
        self.min_people = QSpinBox()
        self.min_people.setMinimum(1)
        self.min_people.setMaximum(20)
        text_min_people = QLabel()
        text_min_people.setText("Minimale Anzahl von Teilnehmern pro Tisch:")
        self.max_people = QSpinBox()
        self.max_people.setMinimum(1)
        self.max_people.setMaximum(20)
        text_max_people = QLabel()
        text_max_people.setText("Maximale Anzahl von Teilnehmern pro Tisch:")
        # GUI construction
        grid = QGridLayout()
        grid.addWidget(text_projectname,0,0)
        grid.addWidget(self.text_user,0,1)
        grid.addWidget(text_num_menus,1,0)
        grid.addWidget(self.num_menus,1,1)
        grid.addWidget(text_min_people,2,0)
        grid.addWidget(self.min_people,2,1)
        grid.addWidget(text_max_people,3,0)
        grid.addWidget(self.max_people,3,1)
        grid.addWidget(self.button_ok, 4, 0)
        grid.addWidget(self.button_cancel,4,1)

        self.setLayout(grid)
        self.show()

    # Callbacks
    @pyqtSlot()
    def finished(self):
        self.close()
        globals.current_session = Session(name=self.text_user.text(),settings=Settings(num_rows = int(self.num_menus.text()),\
                                                                           min_num=int(self.min_people.text()), \
                                                                           max_num=int(self.max_people.text()),\
                                                                           points_student=0, points_company=0))

        save_project()
        self.parent.create_project_ok.emit()


    @pyqtSlot()
    def cancel(self):
        self.parent.create_project_canceled.emit()
        self.hide()
