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

    count = 0
    # Add index number to each student and fill the rows of the matrix
    for student in students:
        if student.list_id == []: continue
        student.list_id = count
        for company in student.companies:
            if company == []: continue
            # One point means the student prefers the company
            system[count][company.list_id] = globals.current_session.settings.points_student
            student.points += globals.current_session.settings.points_student
            company.points += globals.current_session.settings.points_student
        count = count + 1


    # Fill additionally the coloumns
    for company in companies:
       for student in students:
                # Field of study match
                for field in company.field_of_study:
                    if student.field_of_study.name == field.name:
                        system[student.list_id][company.list_id]=system[student.list_id][company.list_id] + globals.current_session.settings.points_company
                        student.points += globals.current_session.settings.points_company
                        company.points += globals.current_session.settings.points_company
                        break
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


