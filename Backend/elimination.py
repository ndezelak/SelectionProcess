# Module external functions:
#                           - divide_students(sorted_students)
#                           - process_boundary(boundary_list, sorted_students, sorted_companies,matrix, algorithm_step)
#                           - user_prompt (boundary_students, num_allowed_seats)
# Created: 29/11/2016
# Last Change: 12/01/2017
import Data.globals as globals
import Backend.rating_procedures as sorting

def divide_students(sorted_students, max_number): # ****** TESTED ****** #
    passed_students=[]
    boundary_region = []
    index = 0

    # Fill the passed students group until the maximum number is reached
    while (index < max_number):
        try:
            passed_students.append(sorted_students[index])
            index = index+1
        except IndexError:
            break

     # Look at the last student in the passed list (it is assumed that if there are too many students the list size is greater than the maximum allowed size by +1
    if len(sorted_students) > max_number:
        last_points = sorted_students[index].points
        last_index = index
    # The passed_students list is already smaller than the maximum, therefor nothing is to be done
    else:
        return [passed_students,boundary_region]

    # Identify a conflicting boundary region
    if sorted_students[last_index].points == sorted_students[last_index-1].points:
        delete_students =[]
        # For all students with the same amount of points
        for student in sorted_students:
            if student.points == last_points:
                # Add them to the boundary region and delete them from the passed region
                boundary_region.append(student)
                if student in passed_students:
                    delete_students.append(student)
        # Delete every student that belongs to the boundary region from the passed group
        for student in delete_students:
                passed_students.remove(student)
    return [passed_students, boundary_region]

#
def process_boundary(boundary_region,passed_students):
    # First come, first serve principle
    sorting.sort_by_id(boundary_region)
    left_places = globals.current_session.settings.max_num * len(globals.current_session.companies) - len(passed_students)
    to_be_deleted = []
    for j in range(0,left_places):
        passed_students.append(boundary_region[j])
        to_be_deleted.append(boundary_region[j])
    for student in to_be_deleted:
        boundary_region.remove(student)
