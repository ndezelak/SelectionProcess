from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog
from Frontend.start_page_create_new_project import *
from Frontend.main_page import *
from Frontend.main_page_field_of_studies_display import *
from PyQt5.QtCore import pyqtSignal
from pickle import *


class startPage(QWidget):
    # Events
    create_project_ok = pyqtSignal()
    create_project_canceled = pyqtSignal()
    home_button_clicked_signal = pyqtSignal()

    def __init__(self,parent,dir=[]):
        super().__init__()
        self.initialize()
        self.new_project_window = []
        self.main_window = []
        self.current_project_name = ""
        self.parent = parent
        self.create_project_canceled.connect(self.new_project_canceled)
        self.create_project_ok.connect(self.new_project_ok)
        self.home_button_clicked_signal.connect(self.home_button_clicked)
        self.test = []
        self.dir = dir
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
        file_path = QFileDialog.getOpenFileName(directory=globals.home_dir,filter = "bonding Files(*.bonding)")
        print(file_path)
        try:
            with open(file_path[0],"rb") as file:
                globals.current_session = pickle.load(file)
        except FileNotFoundError:
            print("File not found!")
            return
        except Exception as e:
            print("Some other exception has happened!")
            return
        print("Done!")
        self.main_window = mainPage(self)

    @pyqtSlot()
    def new_project_canceled(self):
        print("Project has been canceled!")

    @pyqtSlot()
    def new_project_ok(self):
        print("New project has been created!")
        print("Creating default session data ...")
        field_etech = Field_of_Study(name="Elektrotechnik",tags = ["Etechnik","Robotik","Elektronik"])
        field_masch = Field_of_Study(name="Maschinenbau",tags = ["Masch","Fahrzeugtechnik"])
        field_inf = Field_of_Study(name="Informatik",tags= ["Wirtschaftsinformatik"])
        field_sonstiges = Field_of_Study(name="Sonstiges", tags=[])
        field_wirtschaft = Field_of_Study(name="Wirtschaft", tags=["Wirtschaftsingenieurwesen","Finanzen", "BWL"])
        field_natur = Field_of_Study(name="Naturwissenschaften", tags=["Chemie","Physik","Bio","Biotechnologie"])
        globals.current_session.fields_of_study.append(field_etech)
        globals.current_session.fields_of_study.append(field_inf)
        globals.current_session.fields_of_study.append(field_sonstiges)
        globals.current_session.fields_of_study.append(field_wirtschaft)
        globals.current_session.fields_of_study.append(field_masch)
        globals.current_session.fields_of_study.append(field_natur)
        globals.current_session.companies.append(Company(list_id=0,name="Carmeq",field_of_study=[field_etech,field_masch,field_inf]))
        globals.current_session.companies.append(Company(list_id=1,name="Bertrandt AG",field_of_study=[field_etech,field_masch,field_inf,field_wirtschaft]))
        globals.current_session.companies.append(Company(list_id=2,name="Bundeswehr",field_of_study=[field_masch,field_wirtschaft,field_etech]))
        globals.current_session.companies.append(Company(list_id=3,name="H&D International Group",field_of_study=[field_etech,field_inf,field_masch,field_wirtschaft]))
        globals.current_session.companies.append(Company(list_id=4, name="Miele", field_of_study=[field_etech, field_inf, field_masch]))
        globals.current_session.companies.append(Company(list_id=5, name="P3", field_of_study=[field_etech, field_inf]))
        globals.current_session.companies.append(Company(list_id=6, name="Zielpuls", field_of_study=[field_etech, field_inf]))
        globals.current_session.companies.append(Company(list_id=7, name="BASF", field_of_study=[field_natur,field_masch,field_etech]))
        globals.current_session.companies.append(Company(list_id=8, name="Kraftfahrwesen mbH", field_of_study=[field_etech, field_masch]))
        globals.current_session.companies.append(Company(list_id=9, name="IServ", field_of_study=[field_inf]))
        # Default settings
        globals.current_session.settings = Settings(num_rows=4,min_num=4,max_num=6,points_student=1,points_company=2)
        self.main_window = mainPage(self)
        print("Main page has been created")
        self.hide()

    @pyqtSlot()
    def home_button_clicked(self):
        save_project()
        self.main_window.hide()
        self.show()
