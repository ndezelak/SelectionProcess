import Data.globals as globals

def get_row_covering(company):
    return_list = []
    for row in company.seats:
        return_list.append(len(row))
    return return_list

def get_student_pass_rate():
    return [len(globals.passed_students),len(globals.current_session.students)]

def get_students_average_wish_rate():
    list_rates = []
    for student in globals.passed_students:
        if not all(company == [] for company in student.companies):
            list_rates.append(get_student_wish_rate(student))
    return float(sum(list_rates))/float(len(list_rates))

def get_company_average_wish_rate():
    list_rates = []
    for company in globals.current_session.companies:
        list_rates.append(get_company_wish_rate(company))
    return float(sum(list_rates))/float(len(list_rates))

def get_student_wish_rate(student):
    students_rate = float(0)
    for company in student.seats:
        if company in student.companies:
            students_rate += float(1)
    return students_rate / float(len(student.companies))

def get_company_wish_rate(company):
    company_rate = 0
    sum_students = 0
    for row in company.seats:
        for student in row:
            sum_students += 1
            if student.field_of_study in company.field_of_study:
                company_rate += float(globals.current_session.settings.points_field_of_study)/(float(globals.current_session.settings.points_field_of_study)+float(globals.current_session.settings.points_degree))
            if student.degree in company.degrees:
                company_rate+=float(globals.current_session.settings.points_degree)/(float(globals.current_session.settings.points_field_of_study)+float(globals.current_session.settings.points_degree))
    if float(sum_students) == 0:
        return 0
    else:
        return float(company_rate)/float(sum_students)
