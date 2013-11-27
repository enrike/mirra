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
        self.caption = "mirra template" # window name
        self.size = 640, 480 #window size
        self.pos = 100,100 # window top left location
        self.fullScreen = 0 # if fullScreen is on it will overwrite your pos and size to match the display's resolution
        self.frameRate = 15 # set refresh framerate

    def start(self):
        self.rect = 0,0, self.size[0], self.size[1]
        self.drunks = []
        for z in range(100):
            x,y = utilities.randPoint(rect=self.rect)#0,0, self.size[0], self.size[1])
            w = utilities.randint(20,40)
            c = utilities.randRGBA()
            s = utilities.choice((GLU_LINE, GLU_FILL, GLU_SILHOUETTE, GLU_POINT))
            self.drunks.append(Drunk(x,y,z,w, color=c, style=s))


class Drunk(Circle):

    def start(self):
        """ First thing to happen after the instance has been initalisiated
            good place to instanciate classes and init stuff
        """
        self.xi = 0
        self.yi = 0 
        self.Xpath=[]
        self.Ypath=[]
        
    def step(self):
        """ called from timer very x times per sec, depends on the fps passed to App
        """
        if self.xi >= len(self.Xpath):
            self.Xpath = self.doRandRange(self.x)
            self.xi = 0
       
        if self.yi >= len(self.Ypath):
            self.Ypath = self.doRandRange(self.y)
            self.yi = 0

        self.loc = utilities.constrainToRect(self.Xpath[self.xi], self.Ypath[self.yi], self.app.rect)
        
        self.xi += 1 # next
        self.yi += 1 # next

    def doRandRange(self, pos):
        sense = utilities.seed.choice([-1,1])
        d = utilities.randint(20,100)*sense
        r = utilities.randint(1,5)*sense
        return xrange(pos, pos+d, r)
        
        



##

MirraApp() # init always here your main app class that extends main.App




