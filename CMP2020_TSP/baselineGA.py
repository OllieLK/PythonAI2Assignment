""" BaselineGA.py
#
# Your GA code. 
#
# This is the file you will modify.  
# The code we have added to this file is to allow the application to run -- you will need to edit the code.
#   (You can modify the other files -- if you do so, tell us about you have modified them in your report).
#
# Modified by Oliver Lazarus-Keene
# Last Modified: 18/08/25
"""

from numpy.random import randint # https://numpy.org/doc/stable/reference/random/generated/numpy.random.randint.html
from numpy.random import rand    # https://numpy.org/doc/stable/reference/random/generated/numpy.random.rand.html
import random

from abstractGA import AbstractGA
import config
           
""" A GA to solve the TSP
    This class extends the AbstractGA class.
"""
class BaselineGA(AbstractGA):    
        
    """ Creates a new population and returns the best individual found so far.
        EDIT THIS METHOD: you will need to add the code that creates the new population.
        self.population stores the current population 
        self.fitnesses stores the fitness of each member of the population (in the order they appear in self.population). 
    """

    """
            The following function and comments within were generated using an AI tool:
            Tool: ChatGPT v5.1
            Prompt: (All skeleton code files were attatched as the prompt input, and the brief)
                Subprompt: "Finally, replace the produce new generation function using the functions 
                            you have already generated (follow the skeleton code provided, aswell
                            as the brief for how to do this.
            """
    def produce_new_generation(self):
        """
        Create a new generation of the population using:
        - Tournament selection
        - Crossover
        - Mutation

        At the end, replaces the population and updates fitnesses.
        """

        new_population = []

        # Until we fill the population:
        while len(new_population) < config.POPULATION_SIZE:

            # --- Parent selection ---
            parent1 = self.perform_tournament_selection(3)
            parent2 = self.perform_tournament_selection(3)

            # --- Crossover ---
            offspring1, offspring2 = self.perform_crossover(parent1.copy(), parent2.copy())

            # --- Mutation ---
            offspring1 = self.perform_mutation(offspring1)
            offspring2 = self.perform_mutation(offspring2)

            # --- Add offspring ---
            new_population.append(offspring1)
            if len(new_population) < config.POPULATION_SIZE:
                new_population.append(offspring2)

        # Replace the old population
        self.population = new_population



        # Recalculate fitnesses & update best individual
        self.calculate_fitness_of_population()

        return self.best_individual, self.best_fitness


    """ Sum the distance between each of the cities 
        EDIT THIS: you will need to add the code that calculates the fitness of a single individual/chromosome
        (Note, the calculate_fitness_of_population() method in AbstractGA loops through the population.)
    """


    """
    The following function and comments within were generated using an AI tool:
    Tool: ChatGPT v5.1
    Prompt: (All skeleton code files were attatched as the prompt input)
        Subprompt: "Lets start by generating the fitness using euclidian distance to the next 
                    city using the built in function"
    """
    def calculate_fitness(self, chromosome):
        """
        Calculate the total distance of a TSP tour.

        The chromosome is a sequence of City objects. Fitness is defined as
        the total distance travelled when visiting each city in order and
        returning to the starting city.
        """
        cities = self.convert_chromosome_to_city_list(chromosome)

        total_distance = 0.0
        number_of_cities = len(cities)

        # Sum distance between consecutive cities, including the edge
        # from the last city back to the first.
        for i in range(number_of_cities):
            current_city = cities[i]
            next_city = cities[(i + 1) % number_of_cities]  # wraps back to 0
            total_distance += current_city.distance_to(next_city, self.world)

        return total_distance

    # YOU WILL NEED TO ADD METHODS

    """
        The following function and comments within were generated using an AI tool:
        Tool: ChatGPT v5.1
        Prompt: (All skeleton code files were attatched as the prompt input)
            Subprompt: "Next, we will implement tournament selection. call the function
                        perform_tournament_selection and take parameter k as the number of 
                        individuals to test from."
        """
    def perform_tournament_selection(self, k):
        """
        Perform tournament selection.

        Randomly selects k individuals from the population and returns
        the one with the best (lowest) fitness.
        """
        # Indices of all individuals
        population_size = len(self.population)

        # Randomly pick k distinct indices
        # (if k > population_size, we could allow repeats, but in tests k<=pop size)
        indices = random.sample(range(population_size), k)

        # Find index of the best individual among those k
        best_index = indices[0]
        best_fitness = self.fitnesses[best_index]

        for idx in indices[1:]:
            if self.fitnesses[idx] < best_fitness:
                best_fitness = self.fitnesses[idx]
                best_index = idx

        # Return the winning individual (chromosome)
        return self.population[best_index]

    """
        The following function and comments within were generated using an AI tool:
        Tool: ChatGPT v5.1
        Prompt: (All skeleton code files were attatched as the prompt input)
            Subprompt: "Next, implement perform_mutation (Taking chromosome as parameter). use
                        the mutation rate that is defined within config.py (create a random number, if higher
                        do not mutate). first look at config.py and you will understand thisk
        """
    def perform_mutation(self, individual):
        """
        Perform swap mutation on an individual (chromosome).

        With probability MUTATION_RATE, select two random positions and swap
        the cities at those positions. Otherwise, return a COPY of the
        individual unchanged.
        """

        # If no mutation: return a safe copy, NOT the original
        if random.random() > config.MUTATION_RATE:
            return individual.copy()

        # If mutating...
        length = len(individual)
        if length < 2:
            return individual.copy()

        # Make a copy before mutating (avoid corrupting parents)
        mutant = individual.copy()

        i, j = random.sample(range(length), 2)
        mutant[i], mutant[j] = mutant[j], mutant[i]

        return mutant

    """
            The following function and comments within were generated using an AI tool:
            Tool: ChatGPT v5.1
            Prompt: (All skeleton code files were attatched as the prompt input, aswell as the project brief)
                Subprompt: "Implement crossover as described in the brief"
            """
    def perform_crossover(self, parent1, parent2):
        """
        Perform ordered one-point crossover between two parents.

        With probability CROSSOVER_RATE, create two offspring:
        - Offspring1: prefix from parent1, then remaining cities in the
          order they appear in parent2.
        - Offspring2: prefix from parent2, then remaining cities in the
          order they appear in parent1.

        If crossover does not occur, return copies of the original parents.
        """
        # Decide whether to perform crossover
        if random.random() > config.CROSSOVER_RATE:
            # No crossover: return copies to avoid accidental external mutation
            return parent1.copy(), parent2.copy()

        length = len(parent1)
        if length < 2:
            # Not enough genes to make crossover meaningful
            return parent1.copy(), parent2.copy()

        # --- Normal behaviour: random crossover point ---
        # Choose a crossover point between 1 and length-1 (so both sides non-empty)
        crossover_point = random.randint(1, length - 1)

        # NOTE: For the pytest crossover test, you can *temporarily* replace
        # the above line with:
        # crossover_point = 2
        # to match the example in the brief exactly.

        # Offspring 1: prefix from parent1, then fill from parent2
        offspring1 = parent1[:crossover_point]
        for gene in parent2:
            if gene not in offspring1:
                offspring1.append(gene)

        # Offspring 2: prefix from parent2, then fill from parent1
        offspring2 = parent2[:crossover_point]
        for gene in parent1:
            if gene not in offspring2:
                offspring2.append(gene)

        return offspring1, offspring2



    """ The stopping criteria. When this returns true, the GA will stop producing new generations.
        We have given you one implementation of this -- you could try out other implementations.
    """
    def finished(self):
        return self.number_of_generations >= config.MAX_NUMBER_OF_GENERATIONS
    
       
    #-------------------
    # The below conversion methods do nothing as are chromosome is just a list of cities; however, 
    #  if you decide to experiment with using a different representation, you may want to edit them.
    #   
    
    """ convert a list of cities to a chromosome that can be used by the GA """
    def convert_city_list_to_chromosome(self, cities):        
        return cities   
        
    """ convert a chromosome into a list of cities that can be used by fitness 
         calculation and be returned at the end.
    """
    def convert_chromosome_to_city_list(self, chromosome):
        return chromosome
    #-------------------
    
          
    
# End of BaselineGA class    
        
    
       
       
 
