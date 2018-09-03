from PyQt5.QtWidgets import QWidget, QListWidget, QVBoxLayout, QPushButton, QTextEdit, QHBoxLayout, QFrame, QGroupBox, QLabel
from PyQt5.QtCore import pyqtSlot
from Frontend.main_page_add_field_of_study import *
import Data.globals as globals
import copy
from Data.data_structures import Field_of_Study
class field_of_study(QWidget):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        self.initialize()
        globals.current_session_buffer = copy.deepcopy(globals.current_session)
        self.edit_window = []

    def initialize(self):
        self.setWindowTitle("Studiengänge")
        # Layout managers
        main_layout = QVBoxLayout()
        upper_layout = QVBoxLayout()
        buttons_listview = QHBoxLayout()
        buttons_main = QHBoxLayout()
        # Main listview
        self.main_display = QListWidget()
        self.main_display.itemClicked.connect(self.itemClick)
        # Pushbuttons
        button_new = QPushButton("Neu hinzufügen")
        button_new.clicked.connect(self.new_field_clicked)
        button_edit = QPushButton("Bearbeiten")
        button_edit.clicked.connect(self.edit_field_clicked)
        button_delete = QPushButton("Löschen")
        button_delete.clicked.connect(self.delete_field_clicked)
        # Creat row of pushbuttons
        buttons_listview.addWidget(button_new)
        buttons_listview.addWidget(button_edit)
        buttons_listview.addWidget(button_delete)
        # Tag display
        self.tag_display = QTextEdit()
        self.tag_display.setReadOnly(True)
        label_tag_display = QLabel("Schlagwörter")
        # Global pushbuttons
        button_ok = QPushButton("Änderungen speichern")
        button_ok.clicked.connect(self.save_settings_clicked)
        button_cancel = QPushButton("Abbrechen")
        button_cancel.clicked.connect(self.cancel_settings_clicked)
        # Create row of pushbuttons
        buttons_main.addWidget(button_ok)
        buttons_main.addWidget(button_cancel)
        # Frame for the GroupBox
        frame_buttons_listview = QFrame()
        frame_buttons_listview.setLayout(buttons_listview)
        frame_buttons_main = QFrame()
        frame_buttons_main.setLayout(buttons_main)
        # Layout for the GroupBox
        upper_layout.addWidget(self.main_display)
        upper_layout.addWidget(frame_buttons_listview)
        upper_layout.addWidget(label_tag_display)
        upper_layout.addWidget(self.tag_display)
        # GrouBox containing all the settings
        box_upper = QGroupBox("Einstellungen der möglichen Studiengänge")
        box_upper.setLayout(upper_layout)
        # Main layout manager
        main_layout.addWidget(box_upper)
        main_layout.addWidget(frame_buttons_main)
        # Read settings of the current session
        self.main_display.clear()
        for field in globals.current_session.fields_of_study:
            self.main_display.addItem(field.name)
        self.setLayout(main_layout)
        self.show()
    # Button callbacks
    @pyqtSlot()
    def new_field_clicked(self):
        self.edit_window = edit_field_of_study(self)
    @pyqtSlot()
    def edit_field_clicked(self):
        # Do nothing if no item is selected
        if not self.main_display.selectedItems():
            return
        selected_item = self.main_display.currentItem().text()
        index = []
        # Find item in the buffer
        for j in range(0,len(globals.current_session_buffer.fields_of_study)):
            if selected_item == globals.current_session_buffer.fields_of_study[j].name:
                index = j
                break
        pass
        self.edit_window = edit_field_of_study(self,item_index=index)
    @pyqtSlot()
    def delete_field_clicked(self):
        if not self.main_display.selectedItems():
            return
        item = self.main_display.currentItem()
        item_name = item.text()
        for field in globals.current_session_buffer.fields_of_study:
            if field.name == item_name:
                globals.current_session_buffer.fields_of_study.remove(field)
                self.main_display.takeItem(self.main_display.currentRow())
                self.tag_display.setText("")
        pass
    @pyqtSlot()
    def save_settings_clicked(self):
        globals.current_session = copy.deepcopy(globals.current_session_buffer)
        save_project()
        self.hide()
    @pyqtSlot()
    def cancel_settings_clicked(self):
        globals.current_session_buffer = copy.deepcopy(globals.current_session)
        self.hide()
    @pyqtSlot()
    def itemClick(self):
        item_name = self.main_display.currentItem().text()
        for field in globals.current_session_buffer.fields_of_study:
            if item_name == field.name:
                self.tag_display.setText("\n".join(field.tags))



