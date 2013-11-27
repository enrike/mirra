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
        self.caption = "mirra example complex" # window name
        self.size = 640, 480 #window position
        self.pos = 0,0 # window top left location
        self.fullScreen = 0 # if fullScreen is on it will overwrite your pos and size to match the display's resolution

        self.frameRate = 20 # set refresh framerate

    def start(self):
        """ First thing to happen after the instance has been initalisiated
            good place to instanciate classes and init stuff
        """
        self.bgColor = 0.9, 1, 0.8

        Text('more complex stuff', 100, 100, 99, 'timesroman', 24, (1,0.6,0))

        Pixel(10, 10, 0, (1, 0, 0))
        Line((0, 0), (640, 460), 1, (0, 1, 0, 0.5), 3, 45)
        Rect(330, 300, 0, 100, 160, (0, 0, 1), 2, 33, style=0xF0F0)
        Polygon([(40, 10), (150, 20), (300, 80), (10, 250)], 2, (0, 0.2, 0.5), 0, -42)

        Arc(480, 150, 1, 150, 0, 125, (1,0,0,0.2), 100, style = GLU_LINE)

        Circle(50, 350, 3, 100, (1, 0, 0))

        c = Circle(500, 350, 3, 200, (1, 0, 0), stroke=10, style=GLU_SILHOUETTE)
        c.blend = 0.3    # another way to set blend
        c.interactiveState = 2 # now it can be dragged

# GLU_LINE, GLU_FILL, GLU_, GLU_POINT


MirraApp() # init always your main app class that extends main.App












































