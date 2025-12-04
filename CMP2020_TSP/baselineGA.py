""" BaselineGA.py
#
# Your GA code. 
#
# This is the file you will modify.  
# The code we have added to this file is to allow the application to run -- you will need to edit the code.
#   (You can modify the other files -- if you do so, tell us about you have modified them in your report).
#
# Modified by XXX
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
    def produce_new_generation(self):
    
        # ENTER YOUR CODE
        
        # calculate the new fitness and return the best individual
        self.calculate_fitness_of_population() # <-- this method is in abstractGA.py
        return (self.best_individual, self.best_fitness)   
    
    
    """ Sum the distance between each of the cities 
        EDIT THIS: you will need to add the code that calculates the fitness of a single individual/chromosome
        (Note, the calculate_fitness_of_population() method in AbstractGA loops through the population.)
    """
    def calculate_fitness(self, chromosome):    
        cities = self.convert_chromosome_to_city_list(chromosome)   
         
        total = 0
        
        # ENTER YOUR CODE
                   
        return total 
    
    # YOU WILL NEED TO ADD METHODS
           
           
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
        
    
       
       
 
