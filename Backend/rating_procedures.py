# Module external functions:
#                           - generate_system_matrix(students,companies)
#                           - rate_and_sort(students,companies,matrix) (is additionally able to resolve conflicts when too many students want to be with a particular company)
#
# Created: 27/11/2016
# Last Change: 09/01/2017
import Data.globals as globals

def generate_system_matrix (students, companies): # ****** TESTED ****** #
    col_count = len(companies)
    row_count = len(students)

    # Python list comprehension generating a M X N matrix
    system = [ [0 for x in range(col_count)] for y in range(row_count) ]

    # Define list IDs
    count = 0
    for student in students:
        student.points = 0
        student.list_id = count
        count += 1
    count = 0
    for company in companies:
        company.points = 0
        company.list_id = count
        count += 1
    # Determine points of the system matrix
    for company in companies:
        for student in students:
            try:
                # Field of study match
                check = any(student.field_of_study.name == field.name for field in company.field_of_study)
                # check = any(student.field_of_study.name == field.name for field in company.field_of_study)
                if check:
                    system[student.list_id][company.list_id] += globals.current_session.settings.points_field_of_study
                    student.points+= globals.current_session.settings.points_field_of_study
                    check = any(student.degree.name == degree.name for degree in company.degrees)
                    if check:
                        system[student.list_id][company.list_id] += globals.current_session.settings.points_degree
                        student.points += globals.current_session.settings.points_degree
                check = any(company.name == comp.name for comp in student.companies)
                if check:
                    system[student.list_id][company.list_id]+=globals.current_session.settings.points_student
                    company.points += globals.current_session.settings.points_student
            except Exception as e:
                pass#print(str(e))
    # Add index number to each student and fill the rows of the matrix
    '''
    for student in students:
        for company in student.companies:
            if company == []: continue
            # One point means the student prefers the company
            system[student.list_id][company.list_id] = globals.current_session.settings.points_student
            student.points += globals.current_session.settings.points_student
            company.points += globals.current_session.settings.points_student
        count = count + 1
    '''
    return system

#---------------------------------------------------#
#
def rate_and_sort(students,companies,system): # ****** TESTED ****** #
    #Internal lists of students and companies
    sorted_students=students
    sorted_companies=companies

    # Calculate points for each company and student so that they can be ranked
    for company in companies:
        for student in students:
                match_value = system[student.list_id][company.list_id]
                student.points = student.points + match_value
                company.points = company.points + match_value

    # Sort both lists. Note that order of the original list already determines the priority of each individual (if 2 students have the same number
    # of points
    sort_by_points(sorted_students)
    sort_by_points(sorted_companies)
    return [sorted_companies,sorted_students]

#---------------------------------------------------#
# Helper function - Insertion sort
def sort_by_points(person_list):# ****** TESTED ****** #
    for master_pointer in range(0,len(person_list)):
        # Go one place back
        pointer = master_pointer -1

        while (pointer >= 0):
            if person_list[pointer].points < person_list[pointer+1].points:
                # Swap the list elements
                buffer = person_list[pointer]
                person_list[pointer] = person_list[pointer+1]
                person_list[pointer + 1] = buffer
                # Reduce the pointer so that you compare the next pair of values
                pointer = pointer -1
            # Exit the loop if the pair of elements is already ordered
            else:
                break
def sort_by_id(person_list):
    for master_pointer in range(0,len(person_list)):
        # Go one place back
        pointer = master_pointer -1

        while (pointer >= 0):
            if person_list[pointer].list_id > person_list[pointer+1].list_id:
                # Swap the list elements
                buffer = person_list[pointer]
                person_list[pointer] = person_list[pointer+1]
                person_list[pointer + 1] = buffer
                # Reduce the pointer so that you compare the next pair of values
                pointer = pointer -1
            # Exit the loop if the pair of elements is already ordered
            else:
                break


