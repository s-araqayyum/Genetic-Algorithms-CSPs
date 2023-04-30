import time

from GeneticAlgorithm import GeneticAlgorithm
from prettytable import PrettyTable


class GeneralMenu:
    # Define a representation for a solution to the scheduling problem
    courses = 0
    halls = 0
    timeslots = 0
    conflicts = []

    def general_menu(self):

        user_input = -1
        while user_input != "3":
            print()
            print("Welcome to the scheduler! ♡ Would you like to: ")
            print("1. Enter schedule details")
            print("2. Enter details about a conflict")
            print("3. Create an optimal schedule\n")
            user_input = input("\n")
            if user_input == "1":
                while True:
                    try:
                        self.courses = int(input("Enter number of courses:"))
                        self.halls = int(input("Enter number of halls:"))
                        self.timeslots = int(input("Enter number of time-slots:"))
                        break
                    except ValueError:
                        print("Invalid input! Please enter an integer.")
            elif user_input == "2":
                if self.courses > 0:
                    print("Choose the first course:")
                    for course in range(self.courses):
                        print(course + 1, ". Course ", course + 1)
                    course_one = int(input())
                    print("Choose the second course:")
                    for course in range(self.courses):
                        print(course + 1, ". Course ", course + 1)
                    course_two = int(input())
                    conflict = int(input("Enter number of conflicting/common students:"))
                    if (self.courses >= course_one > 0) and (self.courses >= course_two > 0):
                        self.conflicts.append(str(course_one) + str(course_two))
                        self.print_conflicts()
                    else:
                        print("Chosen course does not exist - try again")
                else:
                    print("Please enter schedule details first")
            elif user_input == "3":
                if self.courses != 0:
                    algorithm = GeneticAlgorithm()
                    user_choice = input(
                        "Press any key to use default values [Exam : 2hrs, Hall : 6hrs, Population: 100, Loop: 100], or 0 to customize")
                    if user_choice == "0":
                        exam_hours = int(input("Enter the number of hours one exam can take:"))
                        hall_hours = int(input("Enter the number of hours that a hall can be booked for:"))
                        initial_population = int(input("Choose the size of the population:"))
                        evolutionary_loop_size = int(
                            input("Choose the evolutionary loop size of the genetic algorithm:"))
                        starting = time.time()
                        algorithm.genetic_algorithm_driver(self.courses, self.halls, self.timeslots, self.conflicts,
                                                           exam_hours, hall_hours, initial_population,
                                                           evolutionary_loop_size)
                        ending = time.time()
                        total_time = ending - starting
                        print("Thank you for using the algorithm! It took", total_time, "seconds to run.")
                    else:
                        starting = time.time()
                        algorithm.genetic_algorithm_driver(self.courses, self.halls, self.timeslots, self.conflicts, 2,
                                                           6, 100, 100)
                        ending = time.time()
                        total_time = ending - starting
                        print("Thank you for using the algorithm! It took", total_time, "seconds to run.")
                    break
                else:
                    print("Sorry - valid details were amiss - try running the algorithm again")
            else:
                print("Not a valid option - Please select from the menu")

    def print_conflicts(self):
        table = PrettyTable()
        table.field_names = ["First Conflicting Course", "Second Conflicting Course"]
        for conflict in self.conflicts:
            course_one, course_two = int(conflict[0]), int(conflict[1])
            table.add_row([f"Course {course_one}", f"Course {course_two}"])
        print(table)
