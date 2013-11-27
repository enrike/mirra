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
        self.caption = "mirra example BouncingBall class extends Circle" # window name
        self.size = 640, 480 #window size
        self.pos = 100,100 # window top left location
        self.fullScreen = 0 # if fullScreen is on it will overwrite your pos and size to match the display's resolution
        self.frameRate = 15 # set refresh framerate

    def start(self):
        """ First thing to happen after the instance has been initalisiated
            good place to instanciate classes and init stuff
        """
        self.trails = 1
        self.bgColor = 1, 1, 0, 0.06 # an alpha value causes fade out (better with values between 0.02 - 0.1)
        self.mouseVisible = 0 # hide mouse
        
        for z in range(100):
            w,h = self.size
            x,y = utilities.randPoint(0,0,w,h)
            d = utilities.randint(20, 50)
            rot = utilities.randint(1, 360)
            c = utilities.randRGBA()
            stroke = utilities.randint(0, (d/2)-5)
            deltax = deltay = 0
            while deltax==0 : deltax = utilities.randint(-20, 20)/10.0
            while deltay==0 : deltay = utilities.randint(-20, 20)/10.0
            b = BouncingBall(x, y, z, d, c, stroke, rot)#, style=GLU_POINT)
            b.delta = [deltax, deltay]


class BouncingBall(Circle):
    """ especialized circle that bounces against a given rect and moves
        following a given vector
    """
    def step(self):
        self.x += self.delta[0]
        self.y += self.delta[1]

        if self.x >= self.app.width or self.x <= 0 : self.delta[0] *= -1
        if self.y >= self.app.height or self.y <= 0 : self.delta[1] *= -1




MirraApp() # init always your main app class that extends main.App

