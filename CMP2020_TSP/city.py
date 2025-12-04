""" city.py

 The city class.

  Written by: Helen Harman
  Last Modified: 18/08/25
"""

import math

""" Contains the cities that the agent needs to visit. """
class City():
    #distances = None # if you are using a search algorithm, you could calculate all the distances 
                      # between cities upfront and then look-up the distance. (This will speed-up the run time.)

    """ pose: Pose object
        name: a single character (each city has a unique name)
    """
    def __init__(self, pose, name):
         self.pose = pose
         self.name = name        
         
    #--
    """ set the object used to display the city """
    def set_text_object(self, text):
        self.text = text
    
    """ access the object used to display the city """    
    def get_text_object(self):
        return self.text
    #---  
    
    """ calculates the distance between this city and the provided city """
    def distance_to(self, city, world): 
        # Euclidean distance
        return math.dist([self.pose.x, self.pose.y], [city.pose.x, city.pose.y]) 
        
        
    #---------    
    
    def __repr__(self):
        return f"<City name:{self.name}, pose:{self.pose}>"
            
    def __str__(self):
        return f"[{self.x},{self.y}]"
        
    def __eq__(self, other):
        return self.name == other.name
        
    #---    

# End of City class    
