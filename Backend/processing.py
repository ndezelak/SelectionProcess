# Module external functions:
#                           - fill_tables(students_sorted,sorted_companies,matrix,algorithm_step)
#                           - fill_left_places(passed_students, finished_students,sorted_companies, system)
#                           - post_process(students,sorted_companies,system)
# Created: 29/11/2016
# Last Change: 26/08/2018

from config import *
import Data.globals as globals

# Find seats for students with the matching point number in the system matrix
def fill_tables(passed_students, finished_students, sorted_companies, system, matching_points):
    print('Fill tables called with points: ' + str(matching_points))
    to_delete_students = []
    # Call fill_student for each student
    for student in passed_students:
        fill_student(matching_points, student, system, sorted_companies)
        # Check if a student has already filled all his seats and add him to the finished_students list
        if None not in student.seats:
            finished_students.append(student)
            to_delete_students.append(student)
    # Delete finished students from the student list
    for student in to_delete_students:
        passed_students.remove(student)

# Find seats for the student with the matching point in the system matrix
def fill_student(matching_points, student, system, sorted_companies):
    num_companies = len(sorted_companies)
    for i in range(0, num_companies):
        # Start with the last company (so that their seats would be more easily filled up)
        index =  i #num_companies - 1 - i
        # Only consider the student (and companies) with the matching point in the system matrix
        if system[student.list_id][sorted_companies[index].list_id] == matching_points:
            # Start with the first row and repeat until you come to the last one
            row = 0
            while row < globals.current_session.settings.num_rows:
                # Skip already filled student rows
                if student.seats[row] != None:
                    row = row + 1
                    continue
                # If there is enough space at the companies table then add student to the round
                if len(sorted_companies[index].seats[row]) < globals.current_session.settings.max_num:
                    sorted_companies[index].seats[row].append(student)
                    student.seats[row] = sorted_companies[index]
                    break
                row = row + 1
            # If you could not find a seat at the company
            if row >= globals.current_session.settings.num_rows:
                print("Could not find seat for student " + str(student.name) + " at company " + sorted_companies[index].name)
                # Search for solution using reordering
                print("Trying with reordering ...")
                reorder_seats(student, sorted_companies[index])
            # If all student seats are full, skip the further process
            if None not in student.seats:
                break


# Change the seat order and solve the "no free seat" problem
def reorder_seats(student, conflicting_company):
    student_free_seats = []
    student_filled_seats = []
    # Determine students free and filled rows
    for row in range(0, globals.current_session.settings.num_rows):
        if student.seats[row] == None:
            student_free_seats.append(row)
        else:
            student_filled_seats.append(row)
    # Determine conflicting company free rows
    conflict_company_free_rounds = []
    for round in range(0, globals.current_session.settings.num_rows):
        if len(conflicting_company.seats[round]) < globals.current_session.settings.max_num:
            conflict_company_free_rounds.append(round)

    # Which filled students seats match with free conflicting company seats?
    matching_free_rounds = []
    for round in conflict_company_free_rounds:
        for seat in student_filled_seats:
            if seat == round:
                matching_free_rounds.append(round)

    # Go through each potential row and see if the students company at that row might also have space in a free row
    for seat_filled in matching_free_rounds:
        for seat_free in student_free_seats:
            # There is a solution! Another company also has space in the round where the student could not find a seat
            if len(student.seats[seat_filled].seats[seat_free]) < globals.current_session.settings.max_num:
                print("Solution FOUND using reordering!")
                # Move student from one round to another
                student.seats[seat_filled].seats[seat_filled].remove(student)
                student.seats[seat_filled].seats[seat_free].append(student)
                # Add student to the conflicting companies round
                conflicting_company.seats[seat_filled].append(student)
                # Change students seat plan
                buffer = student.seats[seat_filled]
                student.seats[seat_filled] = conflicting_company
                student.seats[seat_free] = buffer
                return

    # Student failed to find a place at the particular company
    print("Solution not found. The company will be ignored.")

# Without using the system matrix simply fill all the left places
def fill_left_places(passed_students, finished_students, sorted_companies):
    students_to_delete = []
    for student in passed_students:
        for row in range(0, globals.current_session.settings.num_rows):
            # Go through each students empty row and try to find a company that still has space
            if student.seats[row] == None:
                min_company_index = -1
                min_seats = globals.current_session.settings.max_num
                index = len(sorted_companies) - 1
                # Find the company with the least occupied seats at that row that the student can attend (and he doesn't attend in some other round)
                while (index >= 0):
                    if len(sorted_companies[index].seats[row]) < min_seats and \
                            sorted_companies[index] not in student.seats:
                        # Save companies index and number of seats with the minimal number of seats so far
                        min_seats = len(sorted_companies[index].seats[row])
                        min_company_index = index
                    index = index - 1
                # Free seats could not be found without reordering in that round
                if min_company_index == -1:
                    print("FILLING LEFT PLACES: "+student.name + " can NOT find place in round " + str(
                        row) + ". Looking for solution with reordering ...")
                    SOLUTION_FOUND = 0
                    # Try with reordering
                    student_round = 0
                    while (student_round < globals.current_session.settings.num_rows):
                        # If students round is empty
                        if student.seats[student_round] == None:
                            student_round = student_round + 1
                            continue
                        # Check if the company originally at row=student_round also has space in the problematic round
                        if len(student.seats[student_round].seats[row]) < globals.current_session.settings.max_num and \
                                        len(student.seats[student_round].seats[student_round]) > globals.current_session.settings.min_num: # Make sure taking away the student won't reduce the number of students at that round below minimum
                            considered_company = student.seats[student_round]
                            # Go through each company and check if it has space in the round from which the considered_company will be taken away
                            for comp in sorted_companies:
                                # Skip the same company
                                if comp.list_id == considered_company.list_id:
                                    continue
                                else:
                                    # A company has space in the round where the considered_company will be taken away
                                    # Reordering is possible!
                                    if (len(comp.seats[student_round]) < globals.current_session.settings.max_num) and (
                                                comp not in student.seats):
                                        considered_company.seats[student_round].remove(student)
                                        considered_company.seats[row].append(student)
                                        comp.seats[student_round].append(student)
                                        student.seats[student_round] = comp
                                        student.seats[row] = considered_company
                                        SOLUTION_FOUND = 1
                                        print(
                                            "FILLING LEFT PLACES: reordering solved the problem for the problematic row!")
                                        break
                        # Stop finding a solution using reordering for that particular round and look at the next students free row
                        if SOLUTION_FOUND == 1:
                            break
                        # If no solution found try with the next students filled round
                        student_round = student_round + 1

                    # Even reordering didn't help!
                    if SOLUTION_FOUND == 0:
                        print("WARNING!!!: " + student.name + " could not found any left seat in the row " + str(
                            row) + "! He won't be added to finished students at this round. All his entries will be deleted")
                        delete_all_student_entries(student)

                # It worked without reordering!
                else:
                    print("FILLING LEFT PLACES: " + student.name + " has found a left seat in the round " + str(
                        row) + " without reordering!")
                    sorted_companies[min_company_index].seats[row].append(student)
                    student.seats[row] = sorted_companies[min_company_index]
                    #print(" The company " + sorted_companies[min_company_index].name + " has now in total " + str( \
                     #   len(sorted_companies[min_company_index].seats[row])) + " seats at that round")
        # A last check that a student has all his rows filled.
        if None not in student.seats:
            finished_students.append(student)
            students_to_delete.append(student)
    # Remove student from passed list as he was moved to the finished_students list
    for student in students_to_delete:
        passed_students.remove(student)


def post_process(sorted_companies):
    print("Looking at the results ...")
    problematic_companies = []
    index = 0
    # Identify companies with lack of seats at a particular round
    for company in sorted_companies:
        for round in range(0, globals.current_session.settings.num_rows):
            if len(company.seats[round]) < globals.current_session.settings.min_num:
                problematic_companies.append([index, round])
                print("Problematic companies and rounds: " + sorted_companies[index].name + " at round " + str(round + 1))
        index = index + 1
    SOLUTION_FOUND = True

    # Try to solve each problematic round of a company
    for target in problematic_companies:
        sorted_rounds = []
        if SOLUTION_FOUND == False:
            print(" Could NOT find a complete solution!")
        SOLUTION_FOUND = False

        # Sort filled(nonproblematic) companies round by length
        for round in range(0, globals.current_session.settings.num_rows):
            length = len(sorted_companies[target[0]].seats[round])
            if length >= (globals.current_session.settings.min_num + 1):
                sorted_rounds.append([len(sorted_companies[target[0]].seats[round]), round])
        sorted_rounds.sort(reverse=True)

        # Go through each enough full round of the company
        for [length, round] in sorted_rounds:
            # Pick a random student from that round
            for student in sorted_companies[target[0]].seats[round]:
                # Check if the students company at the empty round has enough space at the current round and that it wont go below
                # the minimum number of seats if it makes an exchange
                try:
                    if len(student.seats[target[1]].seats[round]) < globals.current_session.settings.max_num and \
                       len(student.seats[target[1]].seats[target[1]]) > globals.current_session.settings.min_num:
                        print("A solution could be found!")
                        # company_A is the conflicting company, company_B is the "saver"
                        company_A = student.seats[round]
                        company_B = student.seats[target[1]]

                        # Process company_B
                        student.seats[round] = company_B
                        company_B.seats[round].append(student)
                        company_B.seats[target[1]].remove(student)

                        # Process company_A
                        student.seats[target[1]] = company_A
                        company_A.seats[round].remove(student)
                        company_A.seats[target[1]].append(student)

                        # Have you solved the problem?
                        if len(company_A.seats[target[1]]) >= globals.current_session.settings.min_num:
                            SOLUTION_FOUND = True
                            break
                        else:
                            print(" But still need to do some more work")
                except AttributeError:
                        pass
            # You have found the solution so you can exit the outer for loop
            if SOLUTION_FOUND:
                print("A complete solution for " + str(target) + " has been found!")
                break
            else:
                print("Trying with the next round ...")
    # Here you should simply pick students with least points from companies
    # that have the most students in the problematic round

def delete_all_student_entries(student):
    # Delete everything
    row = 0
    for company in student.seats:
        if company == None:
            break
        else:
            company.seats[row].remove(student)
            student.seats[row] = None
        row = row + 1
