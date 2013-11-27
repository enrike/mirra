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
        self.caption = "mirra fullescreen example" # window name
        self.size = 140, 180 #window size
        self.pos = 100,100 # window top left location
        self.fullScreen = 1 # if fullScreen is on it will overwrite your pos and size to match the display's resolution
        self.frameRate = 15 # set refresh framerate


    def start(self):
        """ First thing to happen after the instance has been initalisiated
            good place to instanciate classes and init stuff
        """
        s = 'Size must fit your screen resolution under fullscreen mode, otherwise weird stuff happens'
        Text(s, 10, 100, 900, 'timesroman', 12)

        s = 'press scape to exit'
        Text(s, 10, 150, 900, 'timesroman', 12)

        for z in range(150):
            w,h = self.size
            x,y = utilities.randPoint(1,1,w,h)
            c = utilities.randRGBA()
            o = Rect(x,y,z, 40,40, c)
            o.interactiveState = 2 # this doesnt seem to affect the performance





MirraApp() # init always your main app class that extends main.App




