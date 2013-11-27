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
        for i in range(100):
            x,y = utilities.randPoint(0, 0, self.width, self.height)
            d = utilities.randint(10, 30)
            bl = Blob(x, y, i+1, d, d, utilities.randRGBA())
            bl.interactiveState = 2 #draggable



import time #! Blob uses it


class Blob(Rect):
    """ especialized circle that bounces against a given rect and moves
        following a given vector
    """
    def __init__(self, x=1, y=0, z=0, width=10, height=10, color=(0, 0, 0)) :
        super(Blob, self).__init__(x,y, z, width, height, color) #init superclass
        self.delta = self.calcDelta()
        self.rotation = utilities.getAng((0,0), self.delta)
        self.timeOut = self.doTimeOut()

    def step(self):
        self.checkTimeOut()
        
        self.x += self.delta[0]
        self.y += self.delta[1]
        if self.x >= self.app.width or self.x <= 0 :
            self.delta[0] *= -1
            self.rotation = utilities.getAng((0,0), self.delta)
        if self.y >= self.app.height or self.y <= 0 :
            self.delta[1] *= -1
            self.rotation = utilities.getAng((0,0), self.delta)
        

    def doTimeOut(self):
        return time.time()+ utilities.randint(1, 5)

    def checkTimeOut(self):
        if time.time() >= self.timeOut :
            self.delta = self.calcDelta()
            self.timeOut = self.doTimeOut() # again
            self.rotation = utilities.getAng((0,0), self.delta)

    def calcDelta(self):
        deltax = utilities.randint(-20, 20)*0.1 # while deltax==0 : 
        deltay = utilities.randint(-20, 20)*0.1 # while deltay==0 :
        return [deltax,deltay] # needs to be an array because it changes




MirraApp() # init always your main app class that extends main.App



























