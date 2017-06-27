# Module external functions:
#                           - read_csv( csv_file, person_type)
from Classes.Person import *
from csv import *
from config import *

def construct_companies(companies):
   file = open('Input/firmen.txt')
   while(1):
        line = file.readline()
        if(line is ''):
            break
        data=line.split('.')
        list_id=int(data[0])-1
        data = data[1].split(':')
        name = data[0]
        branches = data[1].split(',')
        fields = []
        for branch in branches:
            if 'Informatik' in branch or 'informatik' in branch:
                if Field_of_Study.INF not in fields:
                    fields.append(Field_of_Study.INF)
            elif 'Elektrotechnik' in branch or 'Medizintechnik' in branch or 'Mechatronik' in branch or 'Luft' in branch:
                if Field_of_Study.EE not in fields:
                    fields.append(Field_of_Study.EE)
            elif 'Maschinenbau' in branch or 'Mechatronik' in branch or 'Fahrzeugtechnik' in branch or 'Feinwerktechnik' in branch or 'Luft' in branch:
                if Field_of_Study.MB not in fields:
                    fields.append(Field_of_Study.MB)
            elif 'Mathe' in branch or 'Chem' in branch or 'Physik' in branch or 'Optik' in branch or 'Bau' in branch:
                if Field_of_Study.NAT not in fields:
                    fields.append(Field_of_Study.NAT)
            elif 'Wirtschaft' in branch or 'Wirt'  in branch:
                if Field_of_Study.WIW not in fields:
                    fields.append(Field_of_Study.WIW)
            else:
                if Field_of_Study.SONSTIGES not in fields:
                    fields.append(Field_of_Study.SONSTIGES)
        #Hack
        if 'zurch' in name.lower():
            name = 'Zürcher'

        companies.append(Company(list_id=list_id,name=name,seats=[ [] for i in range(NUM_ROWS) ],field_of_study=fields,degrees=[]))


   '''


   :param companies:
   :return:
   ''''''
    CARMEQ_ID = 0
    FKA_ID=1
    ZIELPULS_ID=2
    BASF_ID=3
    ISERV_ID=4
    P3_ID=5
    BERTRANDT_ID=6
    MIELE_ID=7
    HD_ID=8
    BUNDESWEHR_ID=9

    # Carmeq
    companies.append(Company(list_id=CARMEQ_ID,seats=[ [] for i in range(4) ],name='Carmeq GmbH',
                    field_of_study=[Field_of_Study.INF,Field_of_Study.WIW,Field_of_Study.EE],
                     degrees=[Degree.MASTER, Degree.DOCTOR, Degree.ABSOLVENT]) )

    # Iserv
    companies.append(Company(list_id= ISERV_ID, seats=[[] for i in range(4)], name='Iserv GmbH',
                             field_of_study=[Field_of_Study.INF],
                     degrees=[Degree.MASTER, Degree.ABSOLVENT, Degree.BACHELOR]))

    # BASF
    companies.append(Company(list_id=BASF_ID,seats= [[] for i in range(4)], name='BASF AG',
                             field_of_study=[Field_of_Study.WIW, Field_of_Study.EE, Field_of_Study.NAT],
                            degrees=[Degree.MASTER, Degree.DOCTOR, Degree.ABSOLVENT]))
    #Bertrand AG
    companies.append(Company(BERTRANDT_ID,seats= [[] for i in range(4)], name='Bertrandt AG',
                             field_of_study=[Field_of_Study.WIW, Field_of_Study.EE],
                     degrees=[Degree.MASTER, Degree.ABSOLVENT]))

    # Bundeswehr
    companies.append(Company(BUNDESWEHR_ID,seats= [[] for i in range(4)], name='Bundeswehr Braunschweig',
                             field_of_study=[Field_of_Study.WIW, Field_of_Study.EE, Field_of_Study.MB,Field_of_Study.NAT,Field_of_Study.INF],
                            degrees =[Degree.MASTER,Degree.DOCTOR,Degree.ABSOLVENT,Degree.BACHELOR,Degree.PROMOTION]))

    # Aachen
    companies.append(Company(FKA_ID,seats= [[] for i in range(4)], name='Forschungsgesellschaft Kraftfahrwesen mbH Aachen',
                         field_of_study=[Field_of_Study.EE, Field_of_Study.MB,Field_of_Study.INF],
                     degrees=[Degree.DOCTOR, Degree.ABSOLVENT]))

    #H&D
    companies.append(Company(HD_ID,seats= [[] for i in range(4)], name='H&D International Group',
                             field_of_study=[Field_of_Study.MB,
                                             Field_of_Study.INF],
                     degrees=[Degree.MASTER, Degree.ABSOLVENT]))
    #Miele
    companies.append(Company(MIELE_ID,seats= [[] for i in range(4)], name='Miele & Cie. KG',
                             field_of_study=[Field_of_Study.MB, Field_of_Study.WIW,Field_of_Study.EE,Field_of_Study.INF],
                     degrees=[Degree.MASTER, Degree.DOCTOR, Degree.ABSOLVENT, Degree.BACHELOR, Degree.PROMOTION]))
    # P3
    companies.append(Company(P3_ID,seats= [[] for i in range(4)], name='P3 Automotive GmbH',
                             field_of_study=[Field_of_Study.MB, Field_of_Study.WIW, Field_of_Study.EE,
                                             Field_of_Study.INF],
                     degrees=[Degree.MASTER,  Degree.ABSOLVENT]))
    #Zielpuls
    companies.append(Company(ZIELPULS_ID,seats= [[] for i in range(4)], name='Zielpuls GmbH',
                             field_of_study=[Field_of_Study.MB, Field_of_Study.WIW, Field_of_Study.EE,
                                             Field_of_Study.INF],
                     degrees=[Degree.MASTER, Degree.ABSOLVENT]))
    '''

def hacks(students,companies):
    # Hack for Vanessa
    meumann_companies = ['Miele & Cie. KG', 'BASF AG', 'Zielpuls GmbH', 'Bertrandt AG']
    von_geldern_companies = ['BASF AG', 'Bundeswehr Braunschweig']
    pan_companies = ['Zielpuls GmbH']
    zielpuls_students = ['Liu','Bobe','Saul','Anwari','Michaelsen','Grunenberg','Sandede','Schlegel','Joswig','Bunse']
    j = 0
    seats = [ [] for i in range(NUM_ROWS) ]
    for student in students:
        if 'Meumann' in student.name:
            j=0
            for company in companies:
                if company.name in meumann_companies:
                    student.seats[j] = company
                    company.seats[j].append(student)
                    j = j + 1
        elif 'von Geldern' in student.name:
            j = 0
            for company in companies:
                if company.name in von_geldern_companies:
                    student.seats[j] = company
                    company.seats[j].append(student)
                    j = j + 1
        elif 'Pan' in student.name:
            j = 0
            for company in companies:
                if company.name in pan_companies:
                    student.seats[j] = company
                    company.seats[j].append(student)
                    j = j + 1
        for student in students:
            for name in zielpuls_students:
                if name in student.name:
                    for company in companies:
                        if company.name == 'Iserv GmbH':
                            round = 0
                            while (len(company.seats[round]) >= 3):
                                round = round + 1
                                if round > 3:
                                    return
                            company.seats[round].append(student)
                            student.seats[round] = company




def read_csv(students, companies):
    # Read .csv file rows and construct data structures
    file = open('Input/studenten.csv','r')
    rows = reader(file, delimiter = ';')
    k = 0
    i = 0
    name_index = -1
    surname_index = -1
    field_of_study_index = -1
    degree_index = -1
    firmen_pointer = -1
    hack_pointer = 0
    for row in rows:
        # Skip first row as it has no data
        if k == 0:
            k=1
            try:
                name_index=row.index('Vorname')
            except ValueError:
                print('Could not find name column in the .csv file!')
                raise ValueError
            try:
                surname_index = row.index('Nachname*')
            except ValueError:
                print('Could not find surnamename column in the .csv file!')
                raise ValueError
            try:
                field_of_study_index = row.index('Studiengang')
            except ValueError:
                print('Could not find field of study column in the .csv file!')
                raise ValueError
            try:
                degree_index = row.index('Studienabschnitt')
            except ValueError:
                print('Could not find degree f column in the .csv file!')
                raise ValueError
            try:
                firmen_pointer = row.index('Firmen')
            except ValueError:
                print('Could not find degree companies column in the .csv file!')
                raise ValueError
            continue

        # TODO: Make csv column finding more generic
        data = row[field_of_study_index].split(',')
        major=[]

        # Field of study
        for _major in data:
            _major = _major.lower()
            if 'ele' in _major or 'mecha' in _major or 'sensor' in _major or 'nano' in _major:
                major.append(Field_of_Study.EE)
            elif  'manag' in _major or 'wi' in _major or 'tvwl' in _major or 'bus' in _major :
                major.append(Field_of_Study.WIW)
            elif 'masch' in _major or 'produk' in _major or 'mater' in _major:
                major.append(Field_of_Study.MB)
            elif 'inf' in _major:
                major.append(Field_of_Study.INF)
            elif 'physik' in _major or 'chem' in _major or 'bio' in _major or 'mathe' in _major:
                major.append(Field_of_Study.NAT)
            else:
                print('Unknown major ' + _major + " for student " + row[0] + " " + row[1])
                major.append(Field_of_Study.SONSTIGES)

        # Degree of study
        data = row[degree_index]
        degree = []
        data = data.lower()
        if 'bach' in data:
            degree = Degree.BACHELOR
        elif 'mast' in data:
            degree = Degree.MASTER
        elif 'prom' in data:
            degree = Degree.PROMOTION
        elif 'abso' in data:
            degree = Degree.ABSOLVENT
        elif 'doc' in data or 'dok' in data:
            degree = Degree.DOCTOR
        else:
            print("Unknown degree "+ data + " for student " + row[0] + " " + row[1])


        # Prefered Companies
        pref_companies =[]
        data = row[firmen_pointer].split(',')
        for company in companies:
            for comp in data:
                if comp is '':
                    break
                elif comp.lower() in company.name.lower() or company.name.lower() in comp.lower():
                    pref_companies.append(company)
                    break

        seats =[ 0 for i in range(NUM_ROWS) ]
        students.append(Student(i,seats=seats,name=row[name_index]+" "+row[surname_index],field_of_study=major,companies = pref_companies, degree=degree))

        i = i +1