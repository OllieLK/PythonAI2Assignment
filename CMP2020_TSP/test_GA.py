"""
Tests for the baselineGA methods that are described within the brief.
All tests passing provides an indication that you have implemented the suggested GA correctly -- this is just an indication.

To test crossover, set your crossover point to 2 -- make sure you change this back to random once you have finished testing.

See: https://docs.pytest.org/en/stable/
"""

import pytest

import config
from baselineGA import BaselineGA
from world import World
from city import City
from pose import Pose

    
def test_selection():
    config.NUMBER_OF_CITIES = 2 
    world = World()
    ga = BaselineGA(world)
    
    # create a population
    ga.population = [ [City(Pose(1,1), 'a'), City(Pose(2,2), 'b')],  
                      [City(Pose(1,1), 'a'), City(Pose(3,3), 'b')],  
                      [City(Pose(1,1), 'a'), City(Pose(4,4), 'b')]   
                       ]
    # calculate its fitness
    ga.calculate_fitness_of_population()
    
    # perform selction
    winner = ga.perform_tournament_selection(3) # k = 3    
     
    # check the winner is correct
    assert winner == [City(Pose(1,1), 'a'), City(Pose(2,2), 'b')] 
    

def test_mutation():
    # force mutation to happen by editing the config
    config.MUTATION_RATE = 1
    config.NUMBER_OF_CITIES = 6
    
    world = World()
    ga = BaselineGA(world)
    
    # get an individual
    individual_before = world.get_cities()
    # perform mutation
    individual_after = ga.perform_mutation(individual_before.copy())
    
    # check that two cities have been swapped
    changes = []
    for i in range(len(individual_before)):
        if individual_after[i] != individual_before[i]:
            changes.append(i)
                       
    assert len(changes) == 2
    assert individual_after[changes[0]] == individual_before[changes[1]]
    assert individual_after[changes[1]] == individual_before[changes[0]]
    
   
    
def test_crossover(): 
    print("To use this test, temporarily change you crossover point to 2 instead of a random value!")

    # force crossover to happen by editing the config   
    config.CROSSOVER_RATE = 1
    config.NUMBER_OF_CITIES = 5
    
    # create two parents
    individual1 = [City(Pose(0,0), 'a'), City(Pose(0,0), 'b'), City(Pose(0,0), 'c'), City(Pose(0,0), 'd'), City(Pose(0,0), 'e')]
    individual2 = [City(Pose(0,0), 'b'), City(Pose(0,0), 'e'), City(Pose(0,0), 'd'), City(Pose(0,0), 'a'), City(Pose(0,0), 'c')]
    
    # perform crossover
    world = World()
    ga = BaselineGA(world)
    offspring1, offspring2 = ga.perform_crossover(individual1.copy(), individual2.copy())
    
    # check offspring1
    assert offspring1[0] == City(Pose(0,0), 'a')
    assert offspring1[1] == City(Pose(0,0), 'b')
    assert offspring1[2] == City(Pose(0,0), 'e')
    assert offspring1[3] == City(Pose(0,0), 'd')
    assert offspring1[4] == City(Pose(0,0), 'c')
    
    # check offspring2
    assert offspring2[0] == City(Pose(0,0), 'b')
    assert offspring2[1] == City(Pose(0,0), 'e')
    assert offspring2[2] == City(Pose(0,0), 'a')
    assert offspring2[3] == City(Pose(0,0), 'c')
    assert offspring2[4] == City(Pose(0,0), 'd')
    
    print("Don't forget to change your crossover point back to a random value!")
    
    
def test_fitness():
    config.NUMBER_OF_CITIES = 2  
    world = World()
    ga = BaselineGA(world)
    
    # create a individual and test its fitness. 
    individual = [City(Pose(1,1), 'a'), City(Pose(2,2), 'b')]     
    assert ga.calculate_fitness(individual) == pytest.approx(2.82, 0.05) # as fitness is a float, we use approx
    
    # create a individual and test its fitness.    
    config.NUMBER_OF_CITIES = 5 
    individual = [City(Pose(2,1), 'a'), City(Pose(3,0), 'b'), City(Pose(4,2), 'c'), City(Pose(5,6), 'd'), City(Pose(3,2), 'e')]   
    assert ga.calculate_fitness(individual) == pytest.approx(13.66, 0.05)      

  
