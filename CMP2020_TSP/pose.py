""" pose.py
#
# Contains the pose class
#
# Written by: Simon Parsons
# Modified by: Helen Harman
# Last Modified: 01/02/24
"""

import math

    
""" Class to represent the position of elements within the world """
class Pose():
    x = 0
    y = 0
    
    def __init__(self, *args): 
        if len(args) > 1:
            self.x = args[0]
            self.y = args[1]        
        
    """ returns the Euclidean distance between this pose 
        and the provided pose. 
    """
    def distance_to(self, p): 
        return math.dist([self.x, self.y], [p.x, p.y])
        
    def print(self):
        print('[', self.x, ',', self.y, ']')
        
    
    def __repr__(self):
        return f"<Pose x:{self.x} y:{self.y}>"
            
    def __str__(self):
        return f"[{self.x},{self.y}]"
        
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Pose):
            return (self.x == other.x and self.y == other.y)
        return False

# End of Pose class
