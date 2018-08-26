# Main function to start a fresh selection process
import Backend.rating_procedures as rating
import Backend.elimination as elimination
import Data.globals as globals
import Backend.processing as process
from PyQt5.QtWidgets import QMessageBox
def start():
    print("New start of the selection process ...")
    print('Constructing the system matrix ...')
    students = globals.current_session.students
    companies = globals.current_session.companies
    system = rating.generate_system_matrix(students, companies)
    print('Starting the rating and sorting process ...')
    rating.sort_by_points(students)
    rating.sort_by_points(companies)
    print('Elimination started ...')
    [passed_students, boundary_region] = elimination.divide_students(students, globals.current_session.settings.max_num*len(companies))
    if len(boundary_region) !=0:
        warning_message = QMessageBox()
        warning_message.warning(None, "Warning", "Eine Gruppe von "+ str(len(boundary_region)) +
                              " Studenten hat nach den Bewertungskriterien eine gleiche Punktzahl erhalten. "
                              "Beim Fortfahren wird das Prinzip \" First come, first serve \" verwendet - die Studenten,"
                              " die höher in der Tabelle standen werden Vorteil haben."
                              "\n\n Durch Änderung der Prozesseinstellungen könnte dieses Problem gegebenfalls vermieden werden.")
    #   First come, first serve principle
    elimination.process_boundary(boundary_region,passed_students)
    finished_students = []
    # Initialize company and student seats
    for company in companies:
        company.seats = [[] for i in range(globals.current_session.settings.num_rows)]
    for student in passed_students:
        student.seats = [None for i in range(globals.current_session.settings.num_rows)]
    process.fill_tables(passed_students = passed_students,
                        finished_students = finished_students,
                        sorted_companies = companies,
                        system = system,
                        matching_points=globals.current_session.settings.points_company+globals.current_session.settings.points_student)
    process.fill_tables(passed_students=passed_students,
                        finished_students=finished_students,
                        sorted_companies=companies,
                        system=system,
                        matching_points=max(globals.current_session.settings.points_company ,globals.current_session.settings.points_student) )
    if globals.current_session.settings.points_company  != globals.current_session.settings.points_student:
        process.fill_tables(passed_students=passed_students,
                        finished_students=finished_students,
                        sorted_companies=companies,
                        system=system,
                        matching_points=min(globals.current_session.settings.points_company,
                                            globals.current_session.settings.points_student))

    # Try to fill left places five times or until you are done.
    watchdog = 0
    while (len(passed_students) > 0):
        print("Filling left places attempt n." + str(watchdog+1) )
        process.fill_left_places(passed_students=passed_students,
                                 finished_students=finished_students,
                                 sorted_companies=companies)
        watchdog = watchdog + 1
        if watchdog > 5:
            print("NO SOLUTIONS FOUND\nPROBLEMATIC STUDENTS:\n")
            for student in passed_students:
                print(student.name + "\n")
            break
    # Post process the results (so that companies won't have not enough filled seats at a round
    process.post_process(companies)
    # Try to find left places for not yet finished students on the postprocessed state

    watchdog = 0
    while (len(passed_students) > 0):
        print("Filling left places after postprocessing. Attempt n." + str(watchdog + 1))
        process.fill_left_places(passed_students=passed_students,
                                 finished_students=finished_students,
                                 sorted_companies=companies)
        watchdog = watchdog + 1
        if watchdog > 5:
            print("NO SOLUTIONS FOUND\nPROBLEMATIC STUDENTS:\n")
            for student in passed_students:
                print(student.name + "\n")
            break
    print("DONE!")
    print("--------------------------------------------------------------------------")
    pass
def restart():
    pass
