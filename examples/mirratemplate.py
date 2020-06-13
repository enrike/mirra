#!/usr/bin/env python

from __future__ import print_function
from mirra import main
from mirra.graphics import *
from mirra import utilities

""" Mirra : 2D graphic engine in OpenGL by www.ixi-software.net
    Check out documentation files
"""


class MirraApp(main.App) :
    """ main appplication class, handles window contains events and graphics manager.
        Subclasses main.App and extends its public methods
    """
    def setUp(self) :
        """ set here the main window properties and characteristics
        """
        self.caption = "mirra template" # window name
        self.size = 640, 480 #window size
        self.pos = 100,100 # window top left location
        self.fullScreen = 0 # if fullScreen is on it will overwrite your pos and size to match the display's resolution
        self.frameRate =12 # set refresh framerate

    def start(self) :
        """ First thing to happen after the instance has been initalisiated
            good place to instanciate classes and init stuff
        """
        print('MirraTemplate is starting')
        Line((0,0), (300,300), 1) # just creating a line


        
    def step(self) :
        """ called from timer very x times per sec, depends on the fps passed to App
        """
        pass # do nothing in this case

    def render(self) :
        """ drawing functions from engine instance, or pure OpenGL can be used here
        """
        pass

    # other general app methods defined below
    # If no object trap this events then they get called
    def mouseDown(self, x,y) : pass
    def mouseUp(self, x,y) : pass
    def mouseDragged(self, x,y) : pass
    def rightMouseDown(self, x,y) : pass
    def rightMouseUp(self, x,y):  pass
    def keyDown(self, key) : pass
    def keyUp(self, key) : pass

    def end(self) :
        """ just before the app is killed
        """
        print('MirraTemplate is quiting')



MirraApp() # init always here your main app class that extends main.App




