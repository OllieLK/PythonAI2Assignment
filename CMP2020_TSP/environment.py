""" environment.py

 The Environment class.

  You shouldn't need modify anything in this file -- unless part of your creative additions.
  If you modify this file, tell us in your report.

  Written by: Simon Parsons. 
  Modified by: Helen Harman
  Last Modified: 23/08/25
"""

from graphics import *

""" Code for displaying the world. """
class Environment():

    def __init__(self, world, window_name = "World"):
        # Make a copy of the world an attribute, so that the graphics
        # have access.
        self.world = world

        # How many pixels the grid if offset in the window
        self.offset = 10
        
        # How many pixels correspond to each coordinate.
        #
        # This works with the current images. any smaller and the
        # images will not fit in the grid.
        self.magnify = 30

        # How big to make "characters" when not using images
        self.cSize = 0.4

        # How big to make objects when not using images.
        self.oSize = 0.6

        # Setup window and draw objects
        self.pane = GraphWin(window_name, ((2*self.offset)+((self.world.max_x+1)*self.magnify)), ((2*self.offset)+((self.world.max_y+1)*self.magnify)))
        self.pane.setBackground("white")
        self.drawBoundary()
        self.drawGrid()
        
        self.drawWalls()
        
        self.pathLines = []
        self.drawCities()       
        

    #
    # Draw the world
    #
    
    """ Put a box around the world """
    def drawBoundary(self):
        rect = Rectangle(self.convert(0, 0), self.convert(self.world.max_x+1, self.world.max_y+1))
        rect.draw(self.pane)

    #------

    """ Draw gridlines, to visualise the coordinates. """
    def drawGrid(self):
        lineColor = "gray77"
        # Vertical lines
        vLines = []
        for i in range(self.world.max_x+1):
            vLines.append(Line(self.convert(i, 0), self.convert(i, self.world.max_y+1)))
            vLines[i].setOutline(lineColor)
        for line in vLines:
            line.draw(self.pane)
        # Horizontal lines
        hLines = []
        for i in range(self.world.max_y + 1):
            hLines.append(Line(self.convert(0, i), self.convert(self.world.max_x+1, i)))
            hLines[i].setOutline(lineColor)
        for line in hLines:
            line.draw(self.pane)
    
    #------
    
    """ Draw walls as black rectangles """
    def drawWalls(self):
        for wall in self.world.get_walls():
            w = Rectangle(self.convert(wall.x, wall.y), self.convert(wall.x + 1, wall.y + 1)) 
            w.setFill("black")
            w.draw(self.pane)

    #-------------------------------

    #
    # Draw the cities
    #

    """ Uses a Text object to display the locations of the cities. 
         Draws lines between the cities to show the path taken to visit them
    """
    def drawCities(self):
        self.pathLines = []
        counter = 0
        for city in self.world.get_cities():
            city.set_text_object( Text(self.convert2(city.pose.x, city.pose.y), str(city.name) + str(counter)) )
            city.get_text_object().setSize(18)
            city.get_text_object().draw(self.pane)
            
            # draw lines between the cities
            if (counter < len(self.world.get_cities())):
                if (counter < len(self.world.get_cities())-1): # if the agent has not yet reached the last city in the list,
                    city2 = self.world.cities[counter+1]      # the city the agent is travelling to is the next one in the list
                else:                                # when the agent has reached the last city in the list, 
                    city2 = self.world.cities[0] # the agent returns to the first city
                    
                self.pathLines.append( Line(self.convertPathPoint(city.pose.x, city.pose.y), self.convertPathPoint(city2.pose.x, city2.pose.y)) )
                self.pathLines[counter].draw(self.pane)
            
            counter = counter + 1
    #------

    """ removes the cities and lines between them, and re-draws them. """
    def update(self):
        for city in self.world.getCities(): 
            city.get_text_object().undraw()
        for pathLine in self.pathLines: 
            pathLine.undraw()
        self.drawCities()

    #---------------------------
    
    #
    # Pose convertion methods
    #
    
    """ Take x and y coordinates and transform them for using offset and magnify.   
     This conversion works for the grid lines. 
    """
    def convert(self, x, y):
        newX = self.offset + (x * self.magnify)
        newY = self.offset + (y * self.magnify)
        return Point(newX, newY)

    """ Take x and y coordinates and transform them for using offset and magnify.    
     This conversion works for objects, returning the centre of the
     relevant grid square.
    """
    def convert2(self, x ,y):
        newX = (self.offset + 0.5*self.magnify) + (x * self.magnify)
        newY = (self.offset + 0.5*self.magnify) + (y * self.magnify)
        return Point(newX, newY)
        
    """ Take x and y coordinates and transform them for using offset and magnify.
        This conversion works for the path lines, returning just above the 
        centre of the relevant grid square.
    """
    def convertPathPoint(self, x, y):
        newX = self.offset + ((x+0.5) * self.magnify)
        newY = self.offset + ((y+0.1) * self.magnify)
        return Point(newX, newY)
        
        
## End of class
