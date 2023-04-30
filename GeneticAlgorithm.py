import math
import random
from prettytable import PrettyTable


class GeneticAlgorithm:
    """
    The general outline of the genetic algorithm being followed is:
        → Generating a population of n random solutions {Also called Individuals/Chromosomes}
        → Each individual is assigned a fitness score to evaluate it through a fitness function
        → We generate new population and loop through these to find a better fitness score by:
            → Select k individuals called parents
            → Crossing over to produce new generations
            → Mutation with low probability (Randomly changing a small part of the solution) - Set static at 0.8
            → Check if stopping criteria is reached

    We also need to encode our solution
        → (Course 1, Timeslot 1, Hall 1) would be represented a 111
    """

    def generate_one_solution(self, courses, hall, timeslots):  # Generating on potential solution in the population → Therein, referred to as a chromosome
        chromosome = []
        for course in range(courses):
            random_hall = random.randint(1, hall)
            random_slot = random.randint(1, timeslots)
            chromosome.append(str(course + 1) + str(random_slot) + str(random_hall))
        return chromosome

    def generate_population(self, courses, hall, timeslots, initial_population):  # Generating an entire population of solutions based on the parameter sze of initial_population
        entire_population = []
        for solution in range(initial_population):
            entire_population.append(self.generate_one_solution(courses, hall, timeslots))
        return entire_population

    def fitness_function(self, chromosome, conflicts, hall_hours, exam_hours, fitness):  # Creating a fitness function based on penalties of double booking, overbooking and conflicts
        penalty = 0

        # Penalty addition for double booking
        checked = []
        for i in range(len(chromosome)):
            for j in range(i + 1, len(chromosome)):
                if chromosome[i][1:3] == chromosome[j][1:3]:
                    if i != j:
                        if chromosome[i][1:3] not in checked:
                            penalty += 10
            checked.append(chromosome[i][1:3])

        # Penalty addition for overbooking
        overbooked = math.floor(hall_hours / exam_hours)
        for i in range(len(chromosome)):
            if int(chromosome[i][1]) > overbooked:
                penalty += 100

        # Penalty addition for conflicting students in the same timeslot
        checked = []
        for i in range(len(chromosome)):
            for j in range(i + 1, len(chromosome)):
                if chromosome[i][1] == chromosome[j][1]:
                    for k in range(len(conflicts)):
                        # print(int(conflicts[k][0]), int(chromosome[i][0]), int(conflicts[k][1]), int(chromosome[j][0]))
                        if int(conflicts[k][0]) == int(chromosome[i][0]):
                            if int(conflicts[k][1]) == int(chromosome[j][0]):
                                penalty += 1000
                        if int(conflicts[k][0]) == int(chromosome[j][0]):
                            if int(conflicts[k][1]) == int(chromosome[i][0]):
                                penalty += 1000

        fitness.append(penalty)

    def selection(self, population, fitness):  # Selection criterion based on a sequential tournament selection methodology
        # Using tournament selection -> Set static at 5
        tournament_size = 5
        selected = []
        for f in range(0, len(population), tournament_size):
            index_of_selected = fitness.index(min(fitness[f:f + 5]))
            selected.append(population[index_of_selected])
        return selected

    def crossover(self, chromosome_one, chromosome_two, courses):  # Single-point cross over method applied with a cross-over point of [1]
        offsprings = []
        offsprings_one = []
        offsprings_two = []
        for i in range(courses):
            offspring_one = chromosome_one[i][0] + chromosome_one[i][1] + chromosome_two[i][2]
            offspring_two = chromosome_two[i][0] + chromosome_two[i][1] + chromosome_one[i][2]
            offsprings_one.append(offspring_one)
            offsprings_two.append(offspring_two)
        offsprings.append(offsprings_one)
        offsprings.append(offsprings_two)
        return offsprings_one

    def mutate(self, mutation_rate, population):  # Mutating solution with a probability of 0.1
        for individual in population:
            for chromosome in individual:
                if random.random() < mutation_rate:
                    temp = str(chromosome[0]) + str(chromosome[2]) + str(chromosome[1])
                    chromosome = temp

    def genetic_algorithm_driver(self, courses, halls, timeslots, conflicts, exam_hours, hall_hours, initial_population,
                                 evolutionary_loop_size):
        population = self.generate_population(courses, halls, timeslots, initial_population)
        fitness = []
        for i in range(len(population)):
            self.fitness_function(population[i], conflicts, hall_hours, exam_hours, fitness)
        # print(fitness)
        for generation in range(evolutionary_loop_size):
            selected = self.selection(population, fitness)
            population.clear()
            population.extend(selected)
            offsprings = []
            for reproduced in range(1, len(population)):
                for solution in range(courses):
                    offspring = self.crossover(population[reproduced - 1], population[reproduced], courses)
                    offsprings.append(offspring)
            population.extend(offsprings)
            population = population[:initial_population]
            self.mutate(0.1, population)
            fitness.clear()
            for fit in range(len(population)):
                self.fitness_function(population[fit], conflicts, hall_hours, exam_hours, fitness)

        possible_solution_index = fitness.index(min(fitness))
        self.printSolution(population[possible_solution_index], min(fitness))

    def printSolution(self, chromosome, value):
        table = PrettyTable()
        table.field_names = ["Course", "Time Interval", "Hall"]
        table_title = "The schedule is as follows [Selected at a fitness score of {}]".format(value)
        table.title = table_title
        course = 0
        for i in chromosome:
            course += 1
            time_interval = "T{}".format(i[1])
            hall = i[2]
            table.add_row([course, time_interval, hall])
        print(table)
