#!/usr/bin/env python

from mirra import main
from mirra.graphics import *
from mirra import utilities

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
        self.caption = "colors" # window name
        self.size = 640, 480 #window size
        self.pos = 100,100 # window top left location
        self.fullScreen = 0 # if fullScreen is on it will overwrite your pos and size to match the display's resolution
        self.frameRate = 70 # set refresh framerate

    def start(self):
        """ First thing to happen after the instance has been initalisiated
            good place to instanciate classes and init stuff
        """
        print 'MirraTemplate is starting'
        self.rotation = 0
##        glBlendFunc(GL_SRC_COLOR, GL_ONE)
        


    def render(self) :
        rad =  100
        dist = rad-40
        resolution = 60
        self.rotation += self.mouseLoc[0]/2
        
        glPushMatrix() # push main
        
        glTranslatef(self.width*0.5, self.height*0.5, -1) # where we draw this shape?
        glRotate(self.rotation, 0, 0, 0.1) # shapes rotation

        glPushMatrix() # RED
        glColor4f (1, 0, 0, 0.5) 
        glTranslatef(-dist, 0, 0)
        gluDisk(engine.q, 0, rad, resolution, 1)
        glPopMatrix() # pop from circles
        
        glRotate(365/3, 0, 0, 0.1)

        glPushMatrix() # green
        glColor4f (0, 1, 0, 0.5) 
        glTranslatef(-dist, 0, 0)
        gluDisk(engine.q, 0, rad, resolution, 1)
        glPopMatrix() # pop from circles

        glRotate(365/3, 0, 0, 0.1)

        glPushMatrix() # blue
        glColor4f (0, 0, 1, 0.5)
        glTranslatef(-dist, 0, 0)
        gluDisk(engine.q, 0, rad, resolution, 1)
        glPopMatrix() # pop from circles
            
        glPopMatrix() # pop from main circle



MirraApp() # init always here your main app class that extends main.App


