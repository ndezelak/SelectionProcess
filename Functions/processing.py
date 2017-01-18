# Module external functions:
#                           - fill_tables(students_sorted,sorted_companies,matrix,algorithm_step)
#                           - fill_left_places(passed_students, finished_students,sorted_companies, system)
#                           - post_process(students,sorted_companies,system)
# Created: 29/11/2016
# Last Change: 17/01/2017

from config import *

def fill_tables(passed_students, finished_students,sorted_companies, system, algorithm_step):
    #finished_students = []
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

    for i in range(0,len(sorted_companies)):
        index = num_companies - 1 - i
        # If the system value equals the algorithm step then you fill the seats
        if system[student.list_id][sorted_companies[index].list_id] == algorithm_step:
        #if system[student.list_id][sorted_companies[i].list_id] == algorithm_step:
                row = 0
                while row <=3:
                        # Check if students round is not yet filled
                        if student_seats[row]!=0:
                            row = row +1
                            continue
                        # If there is enough space at the companies table then add student to the round
                        if len(sorted_companies[index].seats[row]) < AVAILABLE_SEATS:
                            sorted_companies[index].seats[row].append(student)
                            student_seats[row]=sorted_companies[index]
                            break
                        row = row +1
               # If you could not find a seat at the company
                if row >= 4:
                        print("Student" + str(student.list_id) + " could not find seat at company " + sorted_companies[index].name)
                        # Search for solution
                        print("Finding solution ...!")
                        #reorder_seats(student, sorted_companies[num_companies -1 -i])
                        reorder_seats(student, sorted_companies[index])
                # If all student seats are full, skip the further process
                if 0 not in student_seats:
                    break
    #student.companies = student_companies
    student.seats = student_seats

# Change the seat order and solve the "no free seat" problem
def reorder_seats(student, conflicted_company):

        free_seats = []
        filled_seats = []
        # Determine students free seats
        for row in range(0,4):
            if student.seats[row] == 0:
                free_seats.append(row)
            else:
                filled_seats.append(row)
        # Determine conflicting company free rounds
        free_rounds = []
        for round in range(0,4):
            if len(conflicted_company.seats[round]) < AVAILABLE_SEATS:
                free_rounds.append(round)

        # Which filled students seats match with free conflicting company seats?
        matching_seats = []
        for round in free_rounds:
            for seat_filled in filled_seats:
                if seat_filled == round:
                    matching_seats.append(round)

        # Go through each filled student seat and check if the company listed also has space at other free rounds
        for seat_filled in matching_seats:
            for seat_free in free_seats:
                # there is a solution!
                if len(student.seats[seat_filled].seats[seat_free]) < AVAILABLE_SEATS:
                        print("Solution FOUND!")
                        # Delete student from the companies round
                        student.seats[seat_filled].seats[seat_filled].remove(student)
                        # Add student to the other companies round
                        student.seats[seat_filled].seats[seat_free].append(student)
                        # Add student to the conflicting companies round
                        conflicted_company.seats[seat_filled].append(student)
                        # Change students seat plan
                        buffer = student.seats[seat_filled]
                        student.seats[seat_filled] = conflicted_company
                        student.seats[seat_free] = buffer
                        return

        # Student failed to find a place at the particular company
        print("Solution not found :(")


def fill_left_places(passed_students, finished_students,sorted_companies, system):
    students_to_delete = []
    for student in passed_students:
        for row in range(0,4):
            # If students seat is still empty
            if student.seats[row] == 0:
                min_company_index = -1
                min_seats = AVAILABLE_SEATS
                index = 0
                # Find the company with the least occupied seats at that round
                for company in sorted_companies:
                    # As companies are sorted companies with the list number of points are prioritized
                    # Making sure a student is not added to a company twice
                    if len(company.seats[row]) <= min_seats and system[student.list_id][company.list_id] == 0 and \
                        (company != student.seats[0] and company != student.seats[1] and company != student.seats[2]
                        and company != student.seats[3]):
                        min_seats = len(company.seats[row])
                        min_company_index = index
                    index = index +1

                # TODO: How to handle this case??
                if min_company_index == -1:
                    print("student" + str(student.list_id) + " could not found any left seat in the row " + str(row)+"!")
                    print("Problematic student: " + student.name)
                else:
                    print("student"+str(student.list_id)+" has found a left seat in the round " + str(row) +"!")
                    sorted_companies[min_company_index].seats[row].append(student)
                    student.seats[row] = sorted_companies[min_company_index]
                    print(" The company " + sorted_companies[min_company_index].name + " has now in total " + str( \
                        len(sorted_companies[min_company_index].seats[row])) + " seats in that round")
        if 0 not in student.seats:
            finished_students.append(student)
            students_to_delete.append(student)

    for student in students_to_delete:
        passed_students.remove(student)



def post_process(students,sorted_companies,system):
    problematic_companies = []
    index = 0

    # Identify companies with lack of seats at a particular round
    for company in sorted_companies:
        for round in range(0,4):
            if len(company.seats[round]) < MIN_NUM_SEATS:
                problematic_companies.append([index,round])
        index = index +1
    print("Problematic places : ")
    print(problematic_companies)
    SOLUTION_FOUND = True

    # Try to solve each problematic round of a company
    for target in problematic_companies:
        sorted_rounds = []
        if SOLUTION_FOUND == False:
            print(" Could NOT find a complete solution!")
        SOLUTION_FOUND = False

        # Sort filled companies round by length
        for round in range(0,4):
            length = len(sorted_companies[target[0]].seats[round])
            if  length >= (MIN_NUM_SEATS+1):
                    sorted_rounds.append( [len(sorted_companies[target[0]].seats[round]),round]  )
        sorted_rounds.sort(reverse=True)

        # Go through each enough full round of the company
        for [length,round] in sorted_rounds:
            # Pick a random student from that round
            for student in sorted_companies[target[0]].seats[round]:
                # Check if the students company at the empty round has enough space at the current round and that it wont go below
                # the minimum number of seats if it makes an exchange
                if len(student.seats[target[1]].seats[round]) <= AVAILABLE_SEATS and len(student.seats[target[1]].seats[target[1]]) > MIN_NUM_SEATS:
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
                    if len(company_A.seats[target[1]]) >=MIN_NUM_SEATS:
                        SOLUTION_FOUND = True
                        break
                    else:
                        print(" But still need to do some more work")

            # You have found the solution so you can exit the outer for loop
            if SOLUTION_FOUND:
                print("A complete solution for " + str(target) + " has been found!")
                break
            else:
                print("Trying with the next round ...")






