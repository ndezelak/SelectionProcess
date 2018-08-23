# Module external functions:
#                           - read_csv( csv_file, person_type)
from Data.data_structures import *
from csv import *
from config import *
import Data.globals as globals
from Frontend.string_matcher_page import *

def construct_companies(companies):
   file = open('Input/firmen.txt')
   while(1):
        line = file.readline()
        if(line is ''):
            break
        data=line.split('.')
        #Company name order
        list_id=int(data[0])-1
        data = data[1].split(':')
        #Company name
        name = data[0]
        #Student majors the company is looking for
        branches = data[1].split(',')
        fields = []
        # Fill student majors into the company data structure
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
            elif 'Natur' in branch or 'Chem' in branch or 'Physik' in branch or 'Optik' in branch:
                if Field_of_Study.NAT not in fields:
                    fields.append(Field_of_Study.NAT)
            elif 'Wirtschaft' in branch or 'Wirt'  in branch:
                if Field_of_Study.WIW not in fields:
                    fields.append(Field_of_Study.WIW)
            elif 'Bau' in branch:
                if Field_of_Study.BAU not in fields:
                    fields.append(Field_of_Study.BAU)
            else:
                if Field_of_Study.SONSTIGES not in fields:
                    fields.append(Field_of_Study.SONSTIGES)
        #Hack
  #      if 'zurch' in name.lower():
   #         name = 'Zürcher'
        #Construct an instance of the company and add it to the list of companies
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
    file = open('Input/studenten_ka2018.csv','r')
    rows = reader(file, delimiter = ';')
    k = 0
    i = 0
    name_index = -1
    surname_index = -1
    field_of_study_index = -1
    degree_index = -1
    firmen_pointer = []
    hack_pointer = 0
    # Go through each student in the .csv file
    for row in rows:
        # Skip first row as it has no data
        if k == 0:
            k=1
            try:
                name_index=row.index('Vorname')
            except ValueError:
                print('Could not find column with "Name" in the .csv file!')
                raise ValueError
            try:
                surname_index = row.index('Nachname*')
            except ValueError:
                try:
                    surname_index = row.index('Nachname')
                except ValueError:
                    print('Could not find column with "Surname" in the .csv file!')
                    raise ValueError

            try:
                field_of_study_index = row.index('Studiengang')
            except ValueError:
                print('Could not find field of study column in the .csv file!')
                raise ValueError
            '''
            try:
                degree_index = row.index('Studienabschnitt')
            except ValueError:
                print('Could not find degree column in the .csv file!')
                raise ValueError

            try:
                firmen_pointer = row.index('Firmen')
            except ValueError:
                print('Could not find column "wanted companies" in the .csv file!')
                raise ValueError
            '''
            try:
                firmen_pointer.append(row.index('Wunsch 1'))
                firmen_pointer.append(row.index('Wunsch 2'))
                firmen_pointer.append(row.index('Wunsch 3'))
            except ValueError:
                print('Could not find column "wanted companies" in the .csv file!')
                raise ValueError
            continue


        data = row[field_of_study_index].split(',')
        major=[]

        # Field of study
        for _major in data:
            _major = _major.lower()
            if 'ele' in _major or 'mecha' in _major or 'sensor' in _major or 'nano' in _major or 'entech' in _major:
                major.append(Field_of_Study.EE)
            elif  'manag' in _major or 'wirtschaft' in _major or 'tvwl' in _major or 'bus' in _major or 'wing' in _major or 'ciw' in _major or 'wi' in _major or 'mark'in _major:
                major.append(Field_of_Study.WIW)
            elif 'masch' in _major or 'produk' in _major or 'mater' in _major:
                major.append(Field_of_Study.MB)
            elif 'inf' in _major or 'math' in _major or 'bildver' in _major:
                major.append(Field_of_Study.INF)
            elif 'phys' in _major or 'chem' in _major or 'bio' in _major or 'verfah' in _major:
                major.append(Field_of_Study.NAT)
            elif 'bau' in _major:
                major.append(Field_of_Study.BAU)
            elif 'sonstiges' in _major:
                major.append(Field_of_Study.SONSTIGES)
            else:
                print('Unknown major ' + _major + " for student " + row[0] + " " + row[1])
                major.append(Field_of_Study.SONSTIGES)


        # Prefered Companies -kA version
        pref_companies =[]
        data = []
        for pointer in firmen_pointer:
            comp_string = row[pointer]
            data.append(comp_string)
        for company in companies:
            for comp in data:
                if comp is '':
                    break
                elif comp.lower() in company.name.lower() or company.name.lower() in comp.lower():
                    pref_companies.append(company)
                    break

        # Construct the student data object and add it to the list of students
        seats =[ 0 for i in range(NUM_ROWS) ]
        students.append(Student(i,seats=seats,name=row[name_index]+" "+row[surname_index],field_of_study=major,companies = pref_companies, degree=Degree.MASTER))

        i = i +1

def read_file(file_path,widget=[]):
    # Read .csv file
    with open(file_path,'r') as file:
        # Check for uninitialized file specifier
        if (globals.table_specs.ID_name == -1 or
            globals.table_specs.ID_surname == -1 or
            globals.table_specs.ID_field_of_study == -1 or
            globals.table_specs.IDs_students[0] == -1 or
            globals.table_specs.IDs_students[1] == -1 or
            globals.table_specs.IDs_companies[0] == -1 or
            globals.table_specs.IDs_companies[1] == -1):
            return
        # Open the file
        rows = reader(file, delimiter = ';')
        # Go through each line and create a list of students
        index = 0
        list_id = 0
        for row in rows:
            # Go only through specified rows
            if index >= globals.table_specs.IDs_students[0]-1 and index <= globals.table_specs.IDs_students[1]-1:
                name =row[globals.table_specs.ID_name-1]
                surname = row[globals.table_specs.ID_surname-1]
                string_field_of_study = row[globals.table_specs.ID_field_of_study-1]
                # Find matching field of study
                field_of_study=find_field_of_study(string_field_of_study,widget)
                # Something went wrong
                if field_of_study == -1:
                    print("ERROR: No matching field of study found! Table reading not completed!")
                    globals.current_session.students = []
                    return
                read_companies = []
                matched_companies = []
                # Single column case
                if globals.table_specs.IDs_companies[0] == globals.table_specs.IDs_companies[1]:
                    read_companies = row[globals.table_specs.IDs_companies[0]-1].split(",")
                # Multi column case
                else:
                    for j in range(globals.table_specs.IDs_companies[0],globals.table_specs.IDs_companies[1]):
                        read_companies.append(row[j-1])
                # Find matching company from DB
                for company in read_companies:
                    for company_ in globals.current_session.companies:
                        if company.lower() == company_.name.lower():
                            matched_companies.append(company_)
                globals.current_session.students.append(Student(list_id=list_id, seats = [], name = name + " " + surname, field_of_study=field_of_study, companies=matched_companies))
                list_id += 1
            index += 1
        pass


def find_field_of_study(string_field="",widget=[]):
    # Search for the matching field of study
    for field in globals.current_session.fields_of_study:
        for tag in field.tags:
            if tag in string_field:
                return field
        if string_field in field.name or field.name in string_field:
            return field
    # No match, therefor a user prompt is launched
    matcher = string_matcher_page()
    fields = []
    # Save all field names into a list of strings
    for field in globals.current_session.fields_of_study:
        fields.append(field.name)
    # Launch the user prompt
    field_chosen =  matcher.get_item(window=widget,window_title="Unbekannter Studiengang",text="Wähle den zugehörigen Studiengang für "+string_field,
                               items=fields)
    # Find the complete field object and return it
    for field in globals.current_session.fields_of_study:
        if field_chosen == field.name:
            return field
    # An error occurred?
    return -1

