# Module external functions:
#                           - generate_system_matrix(students,companies)
#                           - rate_and_sort(students,companies,matrix) (is additionally able to resolve conflicts when too many students want to be with a particular company)
#

def generate_system_matrix (students, companies):
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
            system[count][company.list_id] = 1
        count = count + 1


    # Fill additionally the coloumns
    for company in companies:
       for student in students:
            for field in company.field_of_study:
                if student.field_of_study ==field:
                    if system[student.list_id][company.list_id] == 1:
                        system[student.list_id][company.list_id] = 3
                    else:
                        system[student.list_id][company.list_id] = 2

    return system

#---------------------------------------------------#
# rate and sort function
def rate_and_sort(students,companies,system):
    sorted_students=students
    sorted_companies=companies

    # Calculate points for each company and student
    for company in companies:
        for student in students:
                match_value = system[student.list_id][company.list_id]
                student.points = student.points + match_value
                company.points = company.points + match_value

    sort_by_points(sorted_students)
    sort_by_points(sorted_companies)
    return [sorted_companies,sorted_students]

#---------------------------------------------------#
# Helper function
def sort_by_points(person_list):
    # Insertion algorithm
    for master_pointer in range(0,len(person_list)):
        pointer = master_pointer -1
        while ( pointer > 0):
            if person_list[pointer].points < person_list[pointer+1].points:
                # Swap the list elements
                buffer = person_list[pointer]
                person_list[pointer] = person_list[pointer+1]
                person_list[pointer + 1] = buffer
                pointer = pointer -1
            else:
                break


