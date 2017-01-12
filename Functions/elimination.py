# Module external functions:
#                           - divide_students(sorted_students)
#                           - process_boundary(boundary_list, sorted_students, sorted_companies,matrix, algorithm_step)
#                           - user_prompt (boundary_students, num_allowed_seats)
# Created: 29/11/2016
# Last Change: 12/01/2017
from config import *

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

     # Look at the last student in the passed list
    if len(passed_students) > MAX_STUDENT_NUMBER:
        last_points = sorted_students[index].points
        last_index = index
    else:
        return [passed_students,boundary_region]


    # Identify a conflicting boundary region
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
        # Add students to the boundary region from the remaining list
        try:
            while sorted_students[index].points == last_points:
                    boundary_region.append(sorted_students[index])
                    index = index + 1
        except IndexError:
            # You reached the end of the sorted list. No problem, go further
            pass


    return [passed_students, boundary_region]

# TODO: Finish this function
def process_boundary(boundary_region, algorithm_step, system, left_places):
    # Depending on the algorithm step consider a given number of points that a student might have and look which one
    # fits the best into the left available seats. The "fill_table" function also has to be used here.
    for student in boundary_region:
        for company in student.companies:
            if system[student.list_id][company.list_id] == algorithm_step:
                student.other_points = student.other_points + algorithm_step



def user_prompt(boundary_list):
    pass