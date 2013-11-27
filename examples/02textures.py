#!/usr/bin/env python

from mirra import main
from mirra.graphics import *
from mirra import utilities


""" Mirra : 2D graphic engine in OpenGL by www.ixi-software.net
    Check out documentation file
"""


class MirraApp(main.App):
    """ main appplication class, handles window contains events and graphics manager.
        Subclasses main.App and extends its public methods
    """
    def setUp(self):
        """ set here the main window properties and characteristics
        """
        self.caption = "mirra example basic texture" # window name
        self.size = 640, 480 #window size
        self.pos = 100,100 # window top left location
        self.fullScreen = 0 # if fullScreen is on it will overwrite your pos and size to match the display's resolution
        self.frameRate = 15 # set refresh framerate

    def start(self):
        """ First thing to happen after the instance has been initalisiated
            good place to instanciate classes and init stuff
        """
        self.bgColor = 0.3, 1, 1

        f = utilities.path("data/ixi2.png")
        self.a = Bitmap(f, 300, 200, 0, 100, 100, 45)
        b = Bitmap(f, 300, 200, 0, 200, 100)
        b.interactiveState = 2
        b.blend = 0.5
        BitmapPolygon(f, [(10, 10), (100,5), (120, 200), (30, 100)], 1, -3)

##    def step(self):
##        """ called from timer very x times per sec depends on the fps passed to App
##        """
##        w,h = self.size
##        self.a.loc = utilities.randPoint(0,0,w,h)








MirraApp() # init always your main app class that extends main.App





















































