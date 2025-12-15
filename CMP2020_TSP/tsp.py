
"""  tsp.py
#
# Displays the initial environment, runs the GA then displays the GA's result.
#
# run this using:
# python3 tsp.py  OR  python tsp.py  
#
# Written by: Helen Harman based on code by Simon Parsons
# Last Modified: 18/08/25
"""

from world import World
from baselineGA  import *
from advancedGA import *
from environment import Environment

import time

def main():
    random.seed(42) # for reproducibility during testing
    world = World()
    # show cities in the random order they were created in
    display = Environment(world, "world -- cities in random order")  
    random.seed() # reset the random seed for GA randomness

    GAChoice = input("Enter B for Baseline GA, A for Advanced GA: ").strip().upper()
    if GAChoice == 'A': ## Important to note: the fitness calculation in AdvancedGA does consider the walls it has to navigate around,
                        ## However the graphical output does not change, only showing the straight line routes between cities.
        ga = AdvancedGA(world)
    elif GAChoice == 'B':
        ga = BaselineGA(world) # <-- if you write multiple different GAs to compare, you can modify this line to test them out
    solution, fitness = ga.run_GA()
    
    # show cities in the order provided by the GA
    world.update_world(solution)
    print("Locations to visit: ", solution, " Fitness:", fitness)
    display_solution = Environment(world, "Best individual")
        

if __name__ == "__main__":
    main()    
    input("Press the Enter key to end program.")
        


