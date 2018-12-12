from PyQt5.QtWidgets import QWidget, QLabel, QSpinBox, QHBoxLayout, QVBoxLayout, QFrame, QPushButton, QErrorMessage, QMessageBox
from PyQt5.QtCore import Qt,pyqtSlot
import Data.globals as globals
from Data.data_structures import Settings
from Backend.output_utils import save_project
class process_settings_page(QWidget):
    def __init__(self):
        super().__init__()
        self.initialize()
    def initialize(self):
        self.setWindowTitle("Einstellungen Sitzplanerstellung")
        # Labels
        label_rows = QLabel("Anzahl der Gänge")
        label_rows.setAlignment(Qt.AlignCenter)

        label_min_seats = QLabel("Minimale Anzahl von Studenten pro Tisch")
        label_min_seats.setAlignment(Qt.AlignCenter)

        label_max_seats = QLabel("Maximale Anzahl von Studenten pro Tisch")
        label_max_seats.setAlignment(Qt.AlignCenter)

        label_points_students = QLabel("Punkte für Studentenwunsch")
        label_points_students.setAlignment(Qt.AlignCenter)

        label_points_company = QLabel("Punkte für Firmenwunsch Studiengang")
        label_points_company.setAlignment(Qt.AlignCenter)

        label_points_degree = QLabel("Punkte für Firmenwunsch Studienabschnitt")
        label_points_degree.setAlignment(Qt.AlignCenter)
        # Spinboxes
        self.spinbox_rows = QSpinBox()
        self.spinbox_rows.setAlignment(Qt.AlignCenter)
        self.spinbox_rows.setMinimum(1)

        self.spinbox_min_seats = QSpinBox()
        self.spinbox_min_seats.setAlignment(Qt.AlignCenter)
        self.spinbox_min_seats.setMinimum(1)

        self.spinbox_max_seats = QSpinBox()
        self.spinbox_max_seats.setAlignment(Qt.AlignCenter)
        self.spinbox_max_seats.setMinimum(1)

        self.spinbox_points_students = QSpinBox()
        self.spinbox_points_students.setAlignment(Qt.AlignCenter)
        self.spinbox_points_students.setMinimum(0)

        self.spinbox_points_company = QSpinBox()
        self.spinbox_points_company.setAlignment(Qt.AlignCenter)
        self.spinbox_points_company.setMinimum(0)

        self.spinbox_points_degree = QSpinBox()
        self.spinbox_points_degree.setAlignment(Qt.AlignCenter)
        self.spinbox_points_degree.setMinimum(0)
        # Horizontal layouts and frames
        layout_rows = QHBoxLayout()
        layout_rows.addWidget(label_rows)
        layout_rows.addWidget(self.spinbox_rows)
        frame_rows = QFrame()
        frame_rows.setLayout(layout_rows)

        layout_min_seats = QHBoxLayout()
        layout_min_seats.addWidget(label_min_seats)
        layout_min_seats.addWidget(self.spinbox_min_seats)
        frame_min_seats = QFrame()
        frame_min_seats.setLayout(layout_min_seats)

        layout_max_seats = QHBoxLayout()
        layout_max_seats.addWidget(label_max_seats)
        layout_max_seats.addWidget(self.spinbox_max_seats)
        frame_max_seats = QFrame()
        frame_max_seats.setLayout(layout_max_seats)

        layout_points_students = QHBoxLayout()
        layout_points_students.addWidget(label_points_students)
        layout_points_students.addWidget(self.spinbox_points_students)
        frame_points_students = QFrame()
        frame_points_students.setLayout(layout_points_students)

        layout_points_company = QHBoxLayout()
        layout_points_company.addWidget(label_points_company)
        layout_points_company.addWidget(self.spinbox_points_company)
        frame_points_company = QFrame()
        frame_points_company.setLayout(layout_points_company)

        layout_points_degree= QHBoxLayout()
        layout_points_degree.addWidget(label_points_degree)
        layout_points_degree.addWidget(self.spinbox_points_degree)
        frame_points_degree = QFrame()
        frame_points_degree.setLayout(layout_points_degree)
        # OK and CANCEL buttons
        self.pushbutton_ok = QPushButton("OK")
        self.pushbutton_ok.clicked.connect(self.ok_clicked)
        self.pushbutton_cancel = QPushButton("CANCEL")
        self.pushbutton_cancel.clicked.connect(self.cancel_clicked)
        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(self.pushbutton_ok)
        layout_buttons.addWidget(self.pushbutton_cancel)
        frame_buttons = QFrame()
        frame_buttons.setLayout(layout_buttons)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(frame_rows)
        main_layout.addWidget(frame_min_seats)
        main_layout.addWidget(frame_max_seats)
        main_layout.addWidget(frame_points_students)
        main_layout.addWidget(frame_points_company)
        main_layout.addWidget(frame_points_degree)
        main_layout.addWidget(frame_buttons)

        # Read current settings and set the spinboxes
        if globals.current_session.settings is not None:
            self.spinbox_rows.setValue(globals.current_session.settings.num_rows)
            self.spinbox_min_seats.setValue(globals.current_session.settings.min_num)
            self.spinbox_max_seats.setValue(globals.current_session.settings.max_num)
            self.spinbox_points_students.setValue(globals.current_session.settings.points_student)
            self.spinbox_points_company.setValue(globals.current_session.settings.points_field_of_study)
            self.spinbox_points_degree.setValue(globals.current_session.settings.points_degree)

        # Final window creation
        self.setLayout(main_layout)
        self.setWindowModality(Qt.ApplicationModal)
        self.show()
    @pyqtSlot()
    def ok_clicked(self):
        # Read settings
        settings = Settings(num_rows=self.spinbox_rows.value(),min_num=self.spinbox_min_seats.value(),max_num=self.spinbox_max_seats.value(),
                            points_student=self.spinbox_points_students.value(),points_company=self.spinbox_points_company.value(),
                            points_degree=self.spinbox_points_degree.value())
        # Value check and error display
        if settings.min_num > settings.max_num:
            error_message = QMessageBox()
            error_message.setWindowModality(Qt.ApplicationModal)
            error_message.critical(self,"Fehler","Die minimale Anzahl von Personen pro Tisch ist größer als die maximale!")
            return
        # Save settings if value check passed
        globals.current_session.settings = settings
        save_project()
        self.close()
    @pyqtSlot()
    def cancel_clicked(self):
        self.close()

    def closeEvent(self, QCloseEvent):
        super().closeEvent(QCloseEvent)

