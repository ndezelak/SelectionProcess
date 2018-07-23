# Module external functions:
#                           - fill_tables(students_sorted,sorted_companies,matrix,algorithm_step)
#                           - fill_left_places(passed_students, finished_students,sorted_companies, system)
#                           - post_process(students,sorted_companies,system)
# Created: 29/11/2016
# Last Change: 17/01/2017

from config import *


def fill_tables(passed_students, finished_students, sorted_companies, system, algorithm_step):
    # finished_students = []
    to_delete_students = []
    for student in passed_students:

        fill_student(algorithm_step, student, system, sorted_companies)

        # Check if a student has already filled all his seats
        if 0 not in student.seats:
            finished_students.append(student)
            to_delete_students.append(student)

    # Very important to delete the finished student afterwards as deleting them in the for loop
    # causes the loop to skip students
    for student in to_delete_students:
        passed_students.remove(student)


def fill_student(algorithm_step, student, system, sorted_companies):
    student_seats = student.seats
    num_companies = len(sorted_companies)

    for i in range(0, len(sorted_companies)):
        # Start with the last company
        index = num_companies - 1 - i
        # If the system value equals the algorithm step then you fill the seats
        if system[student.list_id][sorted_companies[index].list_id] == algorithm_step:
            # if system[student.list_id][sorted_companies[i].list_id] == algorithm_step:
            row = 0
            while row <= (NUM_ROWS - 1):
                # Check if students round is not yet filled
                if student_seats[row] != 0:
                    row = row + 1
                    continue
                # If there is enough space at the companies table then add student to the round
                if len(sorted_companies[index].seats[row]) < AVAILABLE_SEATS:
                    sorted_companies[index].seats[row].append(student)
                    student_seats[row] = sorted_companies[index]
                    break
                row = row + 1
                # If you could not find a seat at the company
            if row >= NUM_ROWS:
                print("Student" + str(student.name) + " could not find seat at company " + sorted_companies[index].name)
                # Search for solution
                print("Finding solution ...!")
                # reorder_seats(student, sorted_companies[num_companies -1 -i])
                reorder_seats(student, sorted_companies[index])
            # If all student seats are full, skip the further process
            if 0 not in student_seats:
                break
    # student.companies = student_companies
    student.seats = student_seats


# Change the seat order and solve the "no free seat" problem
def reorder_seats(student, conflicted_company):
    student_free_seats = []
    student_filled_seats = []
    # Determine students free seats
    for row in range(0, NUM_ROWS):
        if student.seats[row] == 0:
            student_free_seats.append(row)
        else:
            student_filled_seats.append(row)
    # Determine conflicting company free rounds
    conflict_company_free_rounds = []
    for round in range(0, NUM_ROWS):
        if len(conflicted_company.seats[round]) < AVAILABLE_SEATS:
            conflict_company_free_rounds.append(round)

    # Which filled students seats match with free conflicting company seats?
    matching_free_rounds = []
    for round in conflict_company_free_rounds:
        for seat in student_filled_seats:
            if seat == round:
                matching_free_rounds.append(round)

    # Go through each filled student seat and check if the company listed also has space at other free rounds
    for seat_filled in matching_free_rounds:
        for seat_free in student_free_seats:
            # There is a solution! Another company also has space in the round where the student could not find a seat
            if len(student.seats[seat_filled].seats[seat_free]) < AVAILABLE_SEATS:
                print("Solution FOUND!")
                # Move student from one round to another
                student.seats[seat_filled].seats[seat_filled].remove(student)
                student.seats[seat_filled].seats[seat_free].append(student)
                # Add student to the conflicting companies round
                conflicted_company.seats[seat_filled].append(student)
                # Change students seat plan
                buffer = student.seats[seat_filled]
                student.seats[seat_filled] = conflicted_company
                student.seats[seat_free] = buffer
                return

    # Student failed to find a place at the particular company
    print("Solution not found :(. Another company might be considered.")


def fill_left_places(passed_students, finished_students, sorted_companies, system):
    students_to_delete = []
    for student in passed_students:
        for row in range(0, NUM_ROWS):
            # If students seat is still empty
            if student.seats[row] == 0:
                min_company_index = -1
                min_seats = AVAILABLE_SEATS
                index = len(sorted_companies) - 1
                # Find the company with the least occupied seats at that round that the student can attend
                while (index >= 0):
                    if len(sorted_companies[index].seats[row]) < min_seats and sorted_companies[
                        index] not in student.seats:
                        min_seats = len(sorted_companies[index].seats[row])
                        min_company_index = index
                    index = index - 1
                # Free seats could not be found without reordering in that round
                if min_company_index == -1:
                    print(student.name + " has trouble finding left places in round " + str(
                        row) + ". Looking for solution with reordering ...")
                    SOLUTION_FOUND = 0
                    # Try with reordering
                    student_round = 0
                    while (student_round < NUM_ROWS):
                        if student.seats[student_round] == 0:
                            student_round = student_round + 1
                            continue
                        # A company already selected also has space in the problematic round
                        if len(student.seats[student_round].seats[row]) < AVAILABLE_SEATS and len(
                                student.seats[student_round].seats[student_round]) > MIN_NUM_SEATS:
                            considered_company = student.seats[student_round]
                            # Go through each company and check if it has space in the "exchange" round
                            for comp in sorted_companies:
                                # Skip the same company
                                if comp.list_id == considered_company.list_id:
                                    continue
                                else:
                                    # A company has space in the round where the considered_company will be taken away
                                    # Reordering is possible!
                                    if (len(comp.seats[student_round]) < AVAILABLE_SEATS) and (
                                                comp not in student.seats):
                                        considered_company.seats[student_round].remove(student)
                                        considered_company.seats[row].append(student)
                                        comp.seats[student_round].append(student)
                                        student.seats[student_round] = comp
                                        student.seats[row] = considered_company
                                        SOLUTION_FOUND = 1
                                        print(
                                            'REORDERING solved the problem! I have exchanged companies ' + considered_company.name
                                            + " and " + comp.name + "!")
                                        break
                        if SOLUTION_FOUND == 1:
                            break
                        student_round = student_round + 1

                    # Even reordering didn't help!
                    if SOLUTION_FOUND == 0:
                        print("WARNING!!!: " + student.name + " could not found any left seat in the row " + str(
                            row) + "! He won't be added to finished students at this round. All his entries will be deleted")
                        print("Problematic student: " + student.name)
                        delete_all_student_entries(student)

                # It worked without reordering!
                else:
                    print("FILLING LEFT PLACES: " + student.name + " has found a left seat in the round " + str(
                        row) + "!")
                    sorted_companies[min_company_index].seats[row].append(student)
                    student.seats[row] = sorted_companies[min_company_index]
                    print(" The company " + sorted_companies[min_company_index].name + " has now in total " + str( \
                        len(sorted_companies[min_company_index].seats[row])) + " seats at that round")
        # A last check that a student has all his rows filled.
        if 0 not in student.seats:
            finished_students.append(student)
            students_to_delete.append(student)
    # Remove student from passed list as he was moved to the finished_students list
    for student in students_to_delete:
        passed_students.remove(student)


def post_process(students, sorted_companies, system):
    problematic_companies = []
    index = 0

    # Identify companies with lack of seats at a particular round
    for company in sorted_companies:
        for round in range(0, NUM_ROWS):
            if len(company.seats[round]) < MIN_NUM_SEATS:
                problematic_companies.append([index, round])
                print("Problematic companies and rounds : ")
                print(sorted_companies[index].name + ": Round " + str(round + 1))
        index = index + 1
    SOLUTION_FOUND = True

    # Try to solve each problematic round of a company
    for target in problematic_companies:
        sorted_rounds = []
        if SOLUTION_FOUND == False:
            print(" Could NOT find a complete solution!")
        SOLUTION_FOUND = False

        # Sort filled(nonproblematic) companies round by length
        for round in range(0, NUM_ROWS):
            length = len(sorted_companies[target[0]].seats[round])
            if length >= (MIN_NUM_SEATS + 1):
                sorted_rounds.append([len(sorted_companies[target[0]].seats[round]), round])
        sorted_rounds.sort(reverse=True)

        # Go through each enough full round of the company
        for [length, round] in sorted_rounds:
            # Pick a random student from that round
            for student in sorted_companies[target[0]].seats[round]:
                # Check if the students company at the empty round has enough space at the current round and that it wont go below
                # the minimum number of seats if it makes an exchange
                try:
                    if len(student.seats[target[1]].seats[round]) < AVAILABLE_SEATS and len(
                            student.seats[target[1]].seats[target[1]]) > MIN_NUM_SEATS:
                        print(" One solution could be found!")
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
                        if len(company_A.seats[target[1]]) >= MIN_NUM_SEATS:
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


def delete_all_student_entries(student):
    # Delete everything
    row = 0
    for company in student.seats:
        if company == 0:
            break
        else:
            company.seats[row].remove(student)
            student.seats[row] = 0
        row = row + 1
