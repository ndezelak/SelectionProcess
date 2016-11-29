# Module external functions:
#                           - divide_students(sorted_students)
#                           - process_boundary(boundary_list, sorted_students, sorted_companies,matrix, algorithm_step)
#                           - user_prompt (boundary_students, num_allowed_seats)
# Created: 29/11/2016
# Last Change: 29/11/2016

def divide_students(sorted_students, max_number):
    passed_students=[]
    boundary_region = []
    index = 0

    # Fill the passed students group until the maximum number is reached
    while (index < max_number):
        passed_students.append(sorted_students[index])
        index = index+1

    last_points = sorted_students[index].points
    last_index = index

    # Only do this if there exists a boundary region
    if sorted_students[last_index].points == sorted_students[last_index-1].points:
        delete_students =[]
        # For all students with the same amount of points
        for student in passed_students:
            if student.points == last_points:
                # Add them to the boundary region and delete them from the passed region
                boundary_region.append(student)
                delete_students.append(student)
        # Delete every student that belongs to the boundary region from the passed group
        for student in delete_students:
                passed_students.remove(student)
        # And now go into the other direction
        while sorted_students[index].points == last_points:
                boundary_region.append(sorted_students[index])
                index = index + 1

    return [passed_students, boundary_region]


