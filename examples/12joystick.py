#!/usr/bin/env python

from mirra import main
from mirra.graphics import *
from mirra import utilities


""" Mirra : 2D graphic framework in OpenGL by www.ixi-software.net
    Check out documentation files
"""

import pygame
from pygame import locals



class MirraApp(main.App):
    """ main appplication class, handles window contains events and graphics manager.
        Subclasses main.App and extends its public methods
    """
    def setUp(self):
        """ set here the main window properties and characteristics
        """
        self.caption = "joystick events" # window name
        self.size = 640, 480 #window size
        self.pos = 0,0 # window top left location
        self.fullScreen = 0 # if fullScreen is on it will overwrite your pos and size to match the display's resolution

        self.frameRate = 30 # set refresh framerate

    def start(self):
        #print 'joystick support only available under pygame so far'
        self.c = MyCircle(300,300,1,200,(1,0,0))

    def joyAxisMotion(self, joystick, index, value): 
       print "Moved axis %d on joystick %d by: %s" % (index, joystick, value)

    def joyBallMotion(self, joystick, index, value):
        print "Moved ball %d on joystick %d by: %s" % (index, joystick, value)

    def joyHatMotion(self, joystick, index, value):
        print "Moved hat %d on joystick %d by: %s" % (index, joystick, value)
        self.c.delta = value[0], -value[1] # reverse the y

    def joyButtonDown(self, joystick, button):
        print "down button %d on joystick %d" % (button, joystick)
        self.c.color = 0,1,0

    def joyButtonUp(self, joystick, button):
        print "up button %d on joystick %d" % (button, joystick)
        r,g,b = utilities.randRGB()
        self.c.color = r,g,b


class MyCircle(Circle):
    def start(self):
        self.delta = 0,0

    def step(self):
        self.loc = self.loc[0] + self.delta[0], self.loc[1] + self.delta[1]




MirraApp() # init always your main app class that extends main.App










