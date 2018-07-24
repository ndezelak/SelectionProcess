from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QHBoxLayout, QVBoxLayout, QPushButton, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
# Here the start page is created
startPage = []
def initialize_startpage():
    # Main page
    startPage = QWidget()
    startPage.setWindowTitle("bonding Career Night App")
    startPage.setGeometry(200,200,500,200)
    #startPage.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
    startPage.setFixedSize(500,200)
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

    # GUI construction
    grid.addWidget(button_neuprojekt,0,0)
    grid.addWidget(button_altesprojekt,0,1)
    grid.addWidget(backPicture,1,0,1,2)


    startPage.setLayout(grid)
    startPage.setStyleSheet("background-color:white;")
    return startPage
