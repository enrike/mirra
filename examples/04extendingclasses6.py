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

        for z in range(50):
            v = []
            x,y = utilities.randPoint(0, 0, self.width, self.height)
            for j in xrange(4):
                v.append( utilities.randPoint(x-100, y-100, x+100, y+100) )
            d = utilities.randint(10, 30)
##            bl = Marquee(x, y, z, d, d, color=(1,0,0,1), stroke=1)
            bl = Marquee(v, z, color=utilities.randRGB(), stroke=1)
            bl.interactiveState = 2 #draggable



import time #! Blob uses it

class Marquee(Polygon):
    """ especialized circle that bounces against a given rect and moves
        following a given vector
    """
    def step(self):
        self.rotation+= 1
        
    def render(self) : #, e):
        super(Marquee, self).render()
        c = self.color[0], self.color[1], self.color[2], 0.4
        engine.drawVertex(self.x, self.y, self.z, self.v2, color=c, rotation=self.rotation)
        



MirraApp() # init always your main app class that extends main.App




























