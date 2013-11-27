#!/usr/bin/env python

from mirra import main
from mirra.graphics import *
from mirra import utilities


""" Mirra : 2D graphic engine in OpenGL by www.ixi-software.net
    Check out documentation files
"""

import os

class MirraApp(main.App):
    """ main appplication class, handles window contains events and graphics manager.
        Subclasses main.App and extends its public methods
    """
    def setUp(self):
        """ set here the main window properties and characteristics
        """
        self.caption = "mirra example textures, flip and tile" # window name
        self.size = 640, 480 #window size
        self.pos = 100,100 # window top left location
        self.fullScreen = 0 # if fullScreen is on it will overwrite your pos and size to match the display's resolution
        self.frameRate = 15 # set refresh framerate

    def start(self):
        """ First thing to happen after the instance has been initalisiated
            good place to instanciate classes and init stuff
        """
        f = utilities.path("data/im.bmp")

        self.a = Bitmap(f, 150, 250, 0, 200,200)
        self.a.tile(4)
        self.a.flipV()

        self.aa = Bitmap(f, 350, 150, 1, 200, 250)
        self.aa.tile(2)

        f = utilities.path("data/ixi2.png")

        self.b = Bitmap(f, 450, 250, 3, 200, 150, rotation=25)
        self.b.flipH()
##        self.b.tile(0)
        
        self.c = BitmapPolygon(f, [(10, 10), (100,5), (120, 200), (30, 100)], 2)

        

    def mouseDown(self,x,y):
        # swap images on the fly
        f = utilities.path("data/ixi2.png")
        self.a.setImage(f)
        self.aa.setImage(f)

        f = utilities.path("data/im.bmp")
        self.b.setImage(f)
        self.c.setImage(f)
        self.b.flipH()



MirraApp() # init always your main app class that extends main.App


