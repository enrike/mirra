#!/usr/bin/env python

from mirra import main
from mirra.graphics import *
from mirra.utilities import *
from mirra import engine



""" Mirra : 2D graphic engine in OpenGL by www.ixi-software.net
    Check out documentation files
"""


class MirraApp(main.App) :
    """ main appplication class, handles window contains events and graphics manager.
        Subclasses main.App and extends its public methods
    """
    def setUp(self):
        """ set here the main window properties and characteristics
        """
        self.caption = "mirra example BouncingRect class extends Rect" # window name
        self.size = 640, 480 #window size
        self.pos = 100,100 # window top left location
        self.fullScreen = 0 # if fullScreen is on it will overwrite your pos and size to match the display's resolution
        self.frameRate = 15 # set refresh framerate

    def start(self):
        """ First thing to happen after the instance has been initalisiated
            good place to instanciate classes and init stuff
        """
        for i in range(100):
            x,y = randPoint(0, 0, self.width, self.height)
            d = randint(10, 30)
            bl = Blob(x, y, i, d, d, randRGBA())
            bl.interactiveState = 2 #draggable




import time #! Blob uses it


class Blob(Rect):
    """ especialized circle that bounces against a given rect and moves
        following a given vector
    """
    def __init__(self, x=1, y=0, z=0, width=10, height=10, color=(0, 0, 0)) :
        super(Blob, self).__init__(x,y, z, width, height, color) #init superclass
        self.delta = self.calcDelta()
        self.timeOut = self.doTimeOut()
        self.rotation = getAng(self.delta,(0,0))
        self.sq= 1

    def step(self):
        self.checkTimeOut()
        
        self.x += self.delta[0]
        self.y += self.delta[1]
        if self.x >= self.app.width or self.x <= 0 :
            self.delta[0] *= -1
            self.rotation = getAng(self.delta,(0,0))
        if self.y >= self.app.height or self.y <= 0 :
            self.delta[1] *= -1
            self.rotation = getAng(self.delta,(0,0))

    def doTimeOut(self):
        return time.time()+ randint(5, 10)

    def checkTimeOut(self):
        if time.time() >= self.timeOut :
            self.delta = self.calcDelta()
            self.timeOut = self.doTimeOut() # again
            self.rotation = getAng(self.delta,(0,0))
            
    def calcDelta(self):
        deltax = deltay = 0
        deltax = randint(-20, 20)/10.0 # while deltax==0 : 
        deltay = randint(-20, 20)/10.0 # while deltay==0 : 
        return [deltax,deltay] # needs to be an array because it changes

    def render(self) : # , e):
        super(Blob, self).render()
        self.sq += 1
        if self.sq > self.width+20 : self.sq = 1
        c = self.color[0], self.color[1], self.color[2], 1-self.sq/50.
        for i in xrange(1,4):
##            e.drawCircle(self.x,self.y,self.z, self.width+self.sq+i*10, c, 1)
            d = self.width+self.sq+i*10
            engine.drawRect(self.x,self.y,self.z, d, d, c, 1, self.rotation)
        




MirraApp() # init always your main app class that extends main.App



























