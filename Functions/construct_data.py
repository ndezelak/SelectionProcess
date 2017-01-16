# Module external functions:
#                           - read_csv( csv_file, person_type)
from Classes.Person import *
from csv import *

def construct_companies(companies):
    # Carmeq
    companies.append(Company(0,[ [] for i in range(4) ],name='Carmeq GmbH',
                    field_of_study=[Field_of_Study.INF,Field_of_Study.WIW,Field_of_Study.EE],
                     degrees=[Degree.MASTER, Degree.DOCTOR, Degree.ABSOLVENT]) )

    # Iserv
    companies.append(Company(0, [[] for i in range(4)], name='Iserv GmbH',
                             field_of_study=[Field_of_Study.INF],
                     degrees=[Degree.MASTER, Degree.ABSOLVENT, Degree.BACHELOR]))

    # BASF
    companies.append(Company(0, [[] for i in range(4)], name='BASF AG',
                             field_of_study=[Field_of_Study.WIW, Field_of_Study.EE, Field_of_Study.NAT],
                            degrees=[Degree.MASTER, Degree.DOCTOR, Degree.ABSOLVENT]))
    #Bertrand AG
    companies.append(Company(0, [[] for i in range(4)], name='Bertrandt AG',
                             field_of_study=[Field_of_Study.WIW, Field_of_Study.EE],
                     degrees=[Degree.MASTER, Degree.ABSOLVENT]))

    # Bundeswehr
    companies.append(Company(0, [[] for i in range(4)], name='Bundeswehr Braunschweig',
                             field_of_study=[Field_of_Study.WIW, Field_of_Study.EE, Field_of_Study.MB,Field_of_Study.NAT,Field_of_Study.INF],
                            degrees =[Degree.MASTER,Degree.DOCTOR,Degree.ABSOLVENT,Degree.BACHELOR,Degree.PROMOTION]))

    # Aachen
    companies.append(Company(0, [[] for i in range(4)], name='Forschungsgesellschaft Kraftfahrwesen mbH Aachen',
                         field_of_study=[Field_of_Study.EE, Field_of_Study.MB,Field_of_Study.INF],
                     degrees=[Degree.DOCTOR, Degree.ABSOLVENT]))

    #H&D
    companies.append(Company(0, [[] for i in range(4)], name='H&D International Group',
                             field_of_study=[Field_of_Study.MB,
                                             Field_of_Study.INF],
                     degrees=[Degree.MASTER, Degree.ABSOLVENT]))
    #Miele
    companies.append(Company(0, [[] for i in range(4)], name='Miele & Cie. KG',
                             field_of_study=[Field_of_Study.MB, Field_of_Study.WIW,Field_of_Study.EE,Field_of_Study.INF],
                     degrees=[Degree.MASTER, Degree.DOCTOR, Degree.ABSOLVENT, Degree.BACHELOR, Degree.PROMOTION]))
    # P3
    companies.append(Company(0, [[] for i in range(4)], name='P3 Automotive GmbH',
                             field_of_study=[Field_of_Study.MB, Field_of_Study.WIW, Field_of_Study.EE,
                                             Field_of_Study.INF],
                     degrees=[Degree.MASTER,  Degree.ABSOLVENT]))
    #Zielpuls
    companies.append(Company(0, [[] for i in range(4)], name='Zielpuls GmbH',
                             field_of_study=[Field_of_Study.MB, Field_of_Study.WIW, Field_of_Study.EE,
                                             Field_of_Study.INF],
                     degrees=[Degree.MASTER, Degree.ABSOLVENT]))


def read_csv(students, companies):
    # Read .csv file rows and construct data structures
    file = open('Input/studenten.csv','r')
    rows = reader(file, delimiter = ';')
    i = 0
    for row in rows:
        if i == 0:
            i = i+1
            continue
        #print(row)
        #print(row[6].split(','))
        data = row[7].split(',')
        major=[]

        # Field of study
        for _major in data:
            if _major in 'Elektrotechnik':
                major.append(Field_of_Study.EE)
            elif _major in 'Wirtschaftsingenieurswesen':
                major.append(Field_of_Study.WIW)
            elif _major in 'Maschinenbau':
                major.append(Field_of_Study.MB)
            elif _major in 'Informatik':
                major.append(Field_of_Study.INF)
            elif _major in 'Naturwissenschaften':
                major.append(Field_of_Study.NAT)
            else:
                print('Unknown major ' + _major + " for student " + row[0] + " " + row[1])

        # Degree of study
        data = row[4]
        degree = []
        if data in 'Bachelor':
            degree = Degree.BACHELOR
        elif data in 'Master':
            degree = Degree.MASTER
        elif data in 'Promotion':
            degree = Degree.PROMOTION
        elif data in 'Absolvent':
            degree = Degree.ABSOLVENT
        elif data in 'Doktorant':
            degree = Degree.DOCTOR
        else:
            print("Unknown degree "+ data + " for student " + row[0] + " " + row[1])


        # Prefered Companies
        pref_companies =[]
        data = row[6].split(',')
        for company in companies:
            for comp in data:
                if comp in company.name:
                    pref_companies.append(company)
                    break



        students.append(Student(i,[0,0,0,0],name=row[0]+" "+row[1],field_of_study=major,companies = pref_companies))
        i = i+1