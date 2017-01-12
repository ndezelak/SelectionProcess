# Here all used classes in the algortihm are defined
# Created: 23/11/2016
# Last Change: 29/11/2016
from enum import Enum

class Field_of_Study(Enum):
    EE = 0
    MB = 1
    INF = 2
    WIW = 3

class Student:
    def __init__(self, list_id, seats,name="Empty", field_of_study = Field_of_Study.EE, text = "Empty", companies = [], points = 0, other_points=0):
        self.name=name
        self.field_of_study=field_of_study
        self.text = text
        self.list_id=list_id
        self.companies=companies
        self.points=points
        self.seats=seats
        self.other_points = other_points

class Company:
    def __init__(self, list_id, seats, name="Empty", field_of_study = [Field_of_Study.EE], points = 0, ):
        self.name=name
        self.field_of_study=field_of_study
        self.list_id=list_id
        self.points=points
        self.seats=seats




