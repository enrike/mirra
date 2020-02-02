#!/usr/bin/env python

from __future__ import print_function
from mirra import main
from mirra.graphics import *
from mirra.utilities import *

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
        self.smooth = 1
        self.caption = "mirra template" # window name
        self.size = 640, 480 #window size
        self.pos = 100,100 # window top left location
        self.fullScreen = 0 # if fullScreen is on it will overwrite your pos and size to match the display's resolution
        self.frameRate = 15 # set refresh framerate

    def start(self):
        """ First thing to happen after the instance has been initalisiated
            good place to instanciate classes and init stuff
        """
        print('MirraTemplate is starting')
        self.r = Rect(100,100, 1 ,50, 50, color=(0.5,0,0,0.6))
        self.c = Circle(300,100,1,50, stroke=3, color=(0.8,0,0.8,1))
        
    def step(self):
        """ called from timer very x times per sec, depends on the fps passed to App
        """
        self.r.x += (self.mouseLoc[0] - self.r.x)*0.03
        self.r.y += (self.mouseLoc[1] - self.r.y)*0.03
        self.r.height = self.r.width = distance(self.r.loc, self.mouseLoc) + 15
##        
        self.c.x += (self.mouseLoc[0] - self.c.x)*0.1
        self.c.y += (self.mouseLoc[1] - self.c.y)*0.1
        self.c.width = distance(self.c.loc, self.mouseLoc) + 18



##

MirraApp() # init always here your main app class that extends main.App




