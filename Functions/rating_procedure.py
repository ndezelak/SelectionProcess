# Module external functions:
#                           - generate_system_matrix(students,companies)
#                           - rate_and_sort(students,companies,matrix) (is additionally able to resolve conflicts when too many students want to be with a particular company)
#
# Created: 27/11/2016
# Last Change: 09/01/2016


def generate_system_matrix (students, companies): # ****** TESTED ****** #
    pass
    col_count = len(companies)
    row_count = len(students)

    # Python list comprehension generating a M X N matrix
    system = [ [0 for x in range(col_count)] for y in range(row_count) ]

    count = 0
    # Add index number to each company
    for company in companies:
        company.list_id = count
        count = count +1

    count = 0
    # Add index number to each student and fill the rows of the matrix
    for student in students:
        student.list_id = count
        for company in student.companies:
            # One point means the student prefers the company
            system[count][company.list_id] = 1
        count = count + 1


    # Fill additionally the coloumns
    for company in companies:
       for student in students:
                for student_field in student.field_of_study:
                    # Field of study match gives 2 points
                    if student_field in company.field_of_study:
                        system[student.list_id][company.list_id]=system[student.list_id][company.list_id] + 2
                        if student.degree in company.degrees:
                            system[student.list_id][company.list_id] = system[student.list_id][company.list_id] + 1
                        break
                    # Additional degree match gives one more point
                    else:
                        if student.degree in company.degrees:
                            system[student.list_id][company.list_id] = system[student.list_id][company.list_id] + 1
                            break



    return system

#---------------------------------------------------#
#
def rate_and_sort(students,companies,system): # ****** TESTED ****** #
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


