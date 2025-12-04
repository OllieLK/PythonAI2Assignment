""" world.py

  Contains the class that represents the World.
 
  Written by: Simon Parsons
  Modified by: Helen Harman
  Last Modified: 01/02/24
"""

import random
import config
from pose import Pose
from city import City

""" Keeps track of the position of all the objects. """
class World():

    def __init__(self):

        # Import boundaries of the world. because we index from 0,
        # these are one less than the number of rows and columns.
        self.max_x = config.WORLD_WIDTH - 1
        self.max_y = config.WORLD_HEIGHT - 1

        self.occupied_locations = [] # so that two cities/walls don't get placed in the same location
     
        # if you use path planning, you may want to add some walls to the world
        #  Walls are added to random locations. 
        self.walls = []  #list of Pose objects
        for i in range(config.NUMBER_OF_WALLS):
            self.walls.append(self.make_new_unoccupied_pose())
                 
        # Create cities in random locations      
        self.cities = []
        for i in range(config.NUMBER_OF_CITIES):            
            self.cities.append(City(self.make_new_unoccupied_pose(), chr(97+i)))

    #--------------------------------------------------            
         
    """ returns a Pose within the environment that is not within occupied_locations
         adds that location to occupied_locations
    """
    def make_new_unoccupied_pose(self):
        newLoc = Pose(random.randint(0, self.max_x), random.randint(0, self.max_y))
        while newLoc in self.occupied_locations:
            newLoc = Pose(random.randint(0, self.max_x), random.randint(0, self.max_y))
        
        self.occupied_locations.append(newLoc)
        return newLoc
        
    #--------------------------------------------------  
   
    """ access the list of cities """
    def get_cities(self):
        return self.cities  
            
    #------------        
            
    """ set the Cities in a new order """
    def update_world(self, cities):
        self.cities = cities
        
    #------------    
    
    """ access the list of walls """
    def get_walls(self):
        return self.walls
        
    #-------------------------------------------
    
    #
    # These methods help with path planning:
    #
    
    """ returns the locations that can be reached from the provided location (Pose object) """
    def get_actions(self, pose):
        possible_moves = []
        
        if self.is_xy_traversable(pose.x + 1, pose.y):
            possible_moves.append(  Pose(pose.x + 1, pose.y) )
             
        if self.is_xy_traversable(pose.x - 1, pose.y):
            possible_moves.append( Pose(pose.x - 1, pose.y) )
        
        if self.is_xy_traversable(pose.x, pose.y + 1):
            possible_moves.append( Pose(pose.x, pose.y + 1) )
        
        if self.is_xy_traversable(pose.x, pose.y - 1):
            possible_moves.append( Pose(pose.x, pose.y - 1) )
            
        return possible_moves  

    #------------ 

    """ can the agent enter the provided x,y position? """
    def is_traversable(self, pose):
        return ( (pose not in self.walls) 
                   and (pose.x >= 0) and (pose.y >= 0) 
                    and (pose.x <= self.max_x) and (pose.y <= self.max_y) )
     
    #------------ 
    
    """ can the agent enter the provided x,y position? """
    def is_xy_traversable(self, x, y):
        return self.is_traversable(Pose(x, y))    
    
    #--------------------------------------------------   
         
# End of World class        
            
            
        

        
            
