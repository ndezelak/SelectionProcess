from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QGridLayout, QButtonGroup, QFrame
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
import Data.globals as globals
import copy

class unknown_company_window(QWidget):
    user_return_signal = pyqtSignal(str)
    wait_condition = []
    company = []
    matched_company = []
    def __init__(self, company_text, wait_condition):
        super().__init__()
        self.button_group =  QButtonGroup()
        self.setWindowModality(Qt.ApplicationModal)
        self.initialize(unknown_company=company_text)
        self.wait_condition = wait_condition


    def initialize(self,  unknown_company):
        # Text creation
        self.text = QLabel(" Von einem Studenten wurde die gewünschte Firma als " +
                            "<span style= font-size:13pt><b>" + unknown_company + "</b></span> angegeben.<br><br>" +
                           "Bitte ordne die Angabe zu einer der folgenden Firmen zu:")
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.ok_button_clicked)
        self.ok_button.setFixedSize(40,20)
        grid_layout = QGridLayout()
        count = 0
        for company in globals.current_session.companies:
            count +=1
            button = QPushButton(company.name)
            button.setCheckable(True)
            grid_layout.addWidget(button)
            self.button_group.addButton(button)
            self.button_group.setId(button,count)
        button = QPushButton("Keine Zuordnung möglich")
        button.setCheckable(True)
        self.button_group.addButton(button)
        grid_layout.addWidget(button)
        self.button_group.buttonClicked.connect(self.push_button_clicked)
        # Main page layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.text)
        button_frame = QFrame()
        button_frame.setLayout(grid_layout)
        main_layout.addWidget(button_frame)
        main_layout.addWidget(self.ok_button)
        main_layout.setAlignment(self.ok_button,Qt.AlignCenter)

        self.setLayout(main_layout)
        self.show()

    @pyqtSlot()
    def push_button_clicked(self):
        button = self.button_group.checkedButton()
        for company in globals.current_session.companies:
            if company.name == button.text():
                self.matched_company = company
                break

    @pyqtSlot()
    def ok_button_clicked(self):
        print("ok clicked")
        globals.matched_company = self.matched_company
        self.wait_condition.wakeAll()
        self.hide()

    def closeEvent(self, QCloseEvent):
        QCloseEvent.ignore()











