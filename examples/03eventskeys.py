#!/usr/bin/env python

from mirra import main
from mirra.graphics import *
from mirra import utilities


""" Mirra : 2D graphic engine in OpenGL by www.ixi-software.net
    Check out documentation files
"""

import pygame.locals as p # importing key constants !!!!!!

""" NOTE :
importing pygame locals this way
from pygame.locals import *
causes conflicts with the mirra namespace, so better do it the way is done in this example.
"""


class MirraApp(main.App) :
    """ main appplication class, handles window contains events and graphics manager.
        Subclasses main.App and extends its public methods
    """
    def setUp(self) :
        """ set here the main window properties and characteristics
        """
        self.caption = "mirra example testing key events" # window name
        self.size = 640, 480 #window size
        self.pos = 100,100 # window top left location
        self.fullScreen = 0 # if fullScreen is on it will overwrite your pos and size to match the display's resolution
        self.frameRate = 15 # set refresh framerate
    def step(self):pass

    def start(self) :
        """ First thing to happen after the instance has been initalisiated
            good place to instanciate classes and init stuff
        """
        self.readme = Text('press any of these keys: m, n, b, v, c, SHIFT', 100, 50, 1)
        self.txtdisplay = Text('some text', 300, 300, 1)


    # notice that we have imported all pygame.local key constants above #
    def keyDown(self, key) :
##        print "keyDown", key
        if key == p.K_m :
            self.txtdisplay.text = 'key pressed is m'
        elif key == p.K_n :
            self.txtdisplay.text = 'key pressed is n'
        elif key == p.K_v :
            self.txtdisplay.text = 'key pressed is v'
        elif key == p.K_b :
            self.txtdisplay.text = 'key pressed is b'
        elif key == p.K_LSHIFT :
            self.txtdisplay.text = 'key pressed is LEFT SHIFT'
        
    def keyUp(self, key) :
##        print "keyUp", key
        if key == p.K_m :
            self.txtdisplay.text = 'key up is m'
        elif key == p.K_n :
            self.txtdisplay.text = 'key up is n'
        elif key == p.K_v :
            self.txtdisplay.text = 'key up is v'
        elif key == p.K_b :
            self.txtdisplay.text = 'key up is b'
        elif key == p.K_LSHIFT :
            self.txtdisplay.text = 'key up is LEFT SHIFT'







MirraApp() # init always your main app class that extends main.App































































