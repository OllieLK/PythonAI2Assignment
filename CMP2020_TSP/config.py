""" config.py
#
# Configuration information for the World. These are elements
# to play with as you develop your solution.
#
# Written by: Simon Parsons
# Modified by: Helen Harman
# Last Modified: 25/08/25
"""

import random


# Dimensions in terms of the numbers of rows and columns
WORLD_WIDTH = 40
WORLD_HEIGHT = 20

# number of cites 
NUMBER_OF_CITIES = 8

# when performing path planning to calculate fitness,
#  you may want to add some random walls to the environment by increasing this value:
NUMBER_OF_WALLS = 0

# GA parameters
POPULATION_SIZE = 30
CROSSOVER_RATE = 0.2
MUTATION_RATE = 0.05

MAX_NUMBER_OF_GENERATIONS = 20





