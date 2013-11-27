#!/usr/bin/env python

from mirra import main
from mirra.graphics import *
from mirra import utilities

import math

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
        self.caption = "mirra extending classes" # window name
        self.size = 640, 480 #window size
        self.pos = 100,100 # window top left location
        self.fullScreen = 0 # if fullScreen is on it will overwrite your pos and size to match the display's resolution
        self.frameRate = 15 # set refresh framerate

    def start(self):
        """ First thing to happen after the instance has been initalisiated
            good place to instanciate classes and init stuff
        """
        for z in range(100):
            x = utilities.randint(0, self.size[0])
            y = utilities.randint(0, self.size[1])
            h = utilities.randint(2, 20)
            w = utilities.randint(2, 20) 
            c = utilities.randRGBA()
            Orbit(x, y, z, h, w, c)



class Orbit(Rect):
    """ orbits around an point
    """
    def start(self):
        self.r = utilities.randint(1,10)
        self.inc = utilities.choice([1,-1])
        self.rotation = utilities.randint(1,360)

    def step(self):
        rads = math.radians(self.rotation) #float((self.rotation * math.pi)/180) # angs to rads
        h = self.x + (self.r * math.sin(rads))
        v = self.y + (self.r * math.cos(rads))
        self.loc = h,v
        self.rotation += self.inc
    





MirraApp() # init always your main app class that extends main.App





