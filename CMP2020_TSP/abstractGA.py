"""
abstractGA.py

The abstract GA.
You may want to modify this file when gathering experimental data
to produce your results tables and plots.

Written by: Helen Harman
Last Modified: 18/08/25

Experimental logging extended by: Oliver Lazarus-Keene
"""

from abc import ABC, abstractmethod
import random
import csv
import os

import config


class AbstractGA(ABC):

    def __init__(self, world):
        # The world object contains the list of cities that the agent needs to visit
        self.world = world

        # GA state
        self.population = []
        self.fitnesses = []
        self.best_fitness = -1
        self.best_individual = None
        self.number_of_generations = 0

    """
    Returns the best individual found and the fitness of that individual.
    """
    def run_GA(self):
        # reset state
        self.fitnesses = []
        self.best_fitness = -1
        self.best_individual = None

        # initialise population and calculate fitness
        self.initialise_population()
        self.calculate_fitness_of_population()
        self.number_of_generations = 1

        # run GA
        while not self.finished():
            self.produce_new_generation()
            self.number_of_generations += 1
            print(
                "number of generations =",
                self.number_of_generations,
                " best fitness = ",
                self.best_fitness
            )

        # log one row for this run
        self._append_run_to_csv()

        return (
            self.convert_chromosome_to_city_list(self.best_individual),
            self.best_fitness
        )

    """ Creates the initial population by placing the cities in random orders. """
    def initialise_population(self):
        self.population = []
        for _ in range(config.POPULATION_SIZE):
            cities = self.world.get_cities().copy()
            random.shuffle(cities)
            chromosome = self.convert_city_list_to_chromosome(cities)
            self.population.append(chromosome)

    """ Calculates fitness for the entire population. """
    def calculate_fitness_of_population(self):
        self.fitnesses = [self.calculate_fitness(i) for i in self.population]

        for i in range(len(self.population)):
            if self.best_individual is None or self.fitnesses[i] < self.best_fitness:
                self.best_fitness = self.fitnesses[i]
                self.best_individual = self.population[i]

    # ------------------------------------------------------------------
    # CSV logging (ONE ROW PER RUN)
    # ------------------------------------------------------------------
    def _append_run_to_csv(self, filename="ga_results.csv"):
        """
        Append summary statistics for a single GA run.
        Designed for parameter-sweep experiments.
        """
        file_exists = os.path.isfile(filename)

        with open(filename, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)

            if not file_exists:
                writer.writerow([
                    "city_count",
                    "population_size",
                    "max_generations",
                    "stall_limit",
                    "mutation_rate",
                    "actual_generations",
                    "best_fitness"
                ])

            writer.writerow([
                len(self.world.get_cities()),
                config.POPULATION_SIZE,
                config.MAX_NUMBER_OF_GENERATIONS,
                getattr(config, "STALL_LIMIT", None),
                config.MUTATION_RATE,
                self.number_of_generations,
                self.best_fitness
            ])

    # ------------------------------------------------------------------
    # abstract methods
    # ------------------------------------------------------------------
    @abstractmethod
    def produce_new_generation(self):
        pass

    @abstractmethod
    def finished(self):
        pass

    @abstractmethod
    def convert_city_list_to_chromosome(self, cities):
        pass

    @abstractmethod
    def convert_chromosome_to_city_list(self, chromosome):
        pass

    @abstractmethod
    def calculate_fitness(self, chromosome):
        pass
