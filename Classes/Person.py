# Here all used classes in the algortihm are defined
from enum import Enum

class Field_of_Study(Enum):
    EE = 0
    MB = 1
    INF = 2
    WIW = 3

class Student:
    def __init__(self, list_id, name="Empty", field_of_study = Field_of_Study.EE, text = "Empty", companies = [], points = 0,seats=[]):
        self.name=name
        self.field_of_study=field_of_study
        self.text = text
        self.list_id=list_id
        self.companies=companies
        self.points=points
        self.seats=seats

class Company:
    def __init__(self, list_id, name="Empty", field_of_study = [Field_of_Study.EE], points = 0,seats=[Student(0)]):
        self.name=name
        self.field_of_study=field_of_study
        self.list_id=list_id
        self.points=points
        self.seats=seats




