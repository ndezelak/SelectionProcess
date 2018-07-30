from PyQt5.QtGui import QPixmap
from Frontend.create_new_project_page import *
from Frontend.main_page import *
from PyQt5.QtCore import pyqtSignal
import Data.globals as globals

class startPage(QWidget):
    # Events
    create_project_ok = pyqtSignal()
    create_project_canceled = pyqtSignal()
    def __init__(self,parent):
        super().__init__()
        self.initialize()
        self.new_project_window = []
        self.main_window = []
        self.parent = parent
        self.create_project_canceled.connect(self.new_project_canceled)
        self.create_project_ok.connect(self.new_project_ok)
    # Create the GUI
    def initialize(self):
        self.setWindowTitle("bonding Career Night App")
        self.setGeometry(200,200,500,200)
        #startPage.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.setFixedSize(500,200)

        # Gridlayout
        grid = QGridLayout()

        # bonding LOGO
        backPicture = QLabel()
        picture = QPixmap("Data/startpage_background.png")
        backPicture.setPixmap(picture)
        backPicture.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)

        # Pushbutton "neues Projekt"
        button_neuprojekt = QPushButton()
        button_neuprojekt.setText("Neues Projekt ...")

        # Pushbutton "Projekt laden"
        button_altesprojekt = QPushButton()
        button_altesprojekt.setText("Projekt laden ...")

        # Callbacks
        button_neuprojekt.clicked.connect(self.new_project_selected)
        button_altesprojekt.clicked.connect(self.old_project_selected)

        # GUI construction
        grid.addWidget(button_neuprojekt,0,0)
        grid.addWidget(button_altesprojekt,0,1)
        grid.addWidget(backPicture,1,0,1,2)
        self.setLayout(grid)
        self.setStyleSheet("background-color:white;")
        self.show()

    # Callbacks for the buttons
    @pyqtSlot()
    def new_project_selected(self):
        self.new_project_window = newProjectWindow(self)
    @pyqtSlot()
    def old_project_selected(self):
        if self.new_project_window is not []:
            self.new_project_window.hide()
        #print(app.session.name)

    @pyqtSlot()
    def new_project_canceled(self):
        print("Project has been canceled!")


    @pyqtSlot()
    def new_project_ok(self):
        print("New project has been created!")
        self.main_window = mainPage(self)
        print("Main page has been created")
        self.hide()

