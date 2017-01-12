# Until no .csv file is available you will construct your data with this file
from random import randint,sample
from Classes.Person import *


def generate_test_data(students_list,companies_list):

    available_names = ["Nejc Dezelak", "Person 1", "Person 2", "Person X"]
    available_company_names =  ["BASF","Betrand AG","Bundeswehr","CARMEQ","Kraftfahrwesen Aachen",
                            "HORBACH","H&D","MIELE","P3 Stuttgart","Zielplus GmbH"]


# Generate random data for students
    for i in range (0,39):

        students_list.append(Student(list_id=i,seats=[0,0,0,0],
                                   name=available_names[randint(0,3)],
                                   field_of_study=Field_of_Study(value=randint(0,3)) ) )


# Generate random data for companies
    for i in range (0,10):
        companies_list.append(Company(i,[ [] for i in range(4)   ] , name=available_company_names[i],
                                  field_of_study=[ Field_of_Study(value=randint(0,3)) ] ))

# Pick random companies for each students

    for k in students_list:
        k.companies=[]
        for j in sample(range(0,9),5):
            k.companies.append(companies_list[j])
