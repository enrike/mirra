#!/usr/bin/env python

from mirra import main
from mirra.graphics import *
from mirra import utilities

from OpenGL.GL import *


""" Mirra : 2D graphic engine in OpenGL by www.ixi-software.net
    Check out documentation files
"""


class MirraApp(main.App):
    """ main appplication class, handles window contains events and graphics manager.
        Subclasses main.App and extends its public methods
    """
    def setUp(self):
        """ set here the main window properties and characteristics
        """
        self.caption = "mirra example drawing complex shapes 1" # window name
        self.size = 640, 480 #window size
        self.pos = 100,100 # window top left location
        self.fullScreen = 0 # if fullScreen is on it will overwrite your pos and size to match the display's resolution
        self.frameRate = 15 # set refresh framerate

    def start(self):
        """ First thing to happen after the instance has been initalisiated
            good place to instanciate classes and init stuff
        """
        for z in range(20):
            w,h = self.size
            x,y = utilities.randPoint(1,1,w,h)
            Shape(x, y, z, 50, (0.5, 0,8, 0.2, 0.7))


class Shape(Circle):
    """ compiles a list and calls it from render. this should be far more eficient but shape remains static
    """
    def render2(self) : #,e):
        glCallList(self.z+1)

    def render(self) : # ,e):
        rad = 8
        inner = 6
        
        glNewList(self.z+1, GL_COMPILE) # unique int id for each list

        glPushMatrix() # push main

        glTranslatef(self.x, self.y, -self.z) # where 
        
        glColor4f (self.color[0], self.color[1],self.color[2], self.color[3]) # shapes color
        gluDisk(engine.q, 0, self.width/2, 50, 1)

        glPushMatrix() # push circles
       
        glColor4f (0.2, 0.5, 0.2, 0.7) # orbital circles color
        
        glTranslatef(-self.radius, 0, 0)
        gluDisk(engine.q, inner, rad, 20, 1)

        glTranslatef(self.radius, -self.radius, 0)
        gluDisk(engine.q, inner, rad, 20, 1)

        glTranslatef(self.radius, self.radius, 0)
        gluDisk(engine.q, inner, rad, 20, 1)

        glTranslatef(-self.radius, self.radius, 0)
        gluDisk(engine.q, inner, rad, 20, 1)

        glPopMatrix() # pop from circles
            
        glPopMatrix() # pop from main circle
    
        glEndList() ###

        self.render = self.render2 # replace render method




MirraApp() # init always your main app class that extends main.App



