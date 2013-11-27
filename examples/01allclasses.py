#!/usr/bin/env python

from mirra import  main
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
        self.smooth = 1
        self.caption = "mirra example basic" # window name
        self.size = 640,480 # window size.         self.pos = 50,50 # window top left location
        self.fullScreen = 0 # if fullScreen is on it will overwrite your pos and size to match the display's resolution
        self.frameRate = 15 # set refresh framerate

    def start(self) :
        """ First thing to happen after the instance has been initalisiated
            good place to instanciate classes and init stuff
        """
        self.bgColor = 1,0.5,0.7,0.5

        Text('the simplest stuff!', 350, 100, 7)
        Pixel(320, 230, 6)
        Line((10, 10), (630, 470), 5)
        Rect(220, 40, 4, 50, 50, (1,0.1,0)) 
        Polygon([(40, 10), (150, 20), (300, 80), (10, 250)], 1)
        Circle(400, 350, 2, width=100, color=(1,0.1,0.2,0.5))
        Arc(250, 300, 1, 100, 0, 200, (1,0,1,0.9), stroke=35)
##        Ellipse(250, 30, 1, 100, 50, (0,0,1,0.9), stroke=10)


MirraApp() # init always your main app class that extends main.App



