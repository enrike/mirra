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
        self.pos = 0,0 # window top left location
        self.fullScreen = 1 # if fullScreen is on it will overwrite your pos and size to match the display's resolution
        self.frameRate = 20 # set refresh framerate

    def start(self):
        """ First thing to happen after the instance has been initalisiated
            good place to instanciate classes and init stuff
        """
        self.trails = 1
        for z in range(50):
            x,y = utilities.randPoint(0,0,self.height, self.width)
            s = utilities.choice((GLU_LINE, GLU_FILL, GLU_SILHOUETTE, GLU_POINT))
            Expands(x,y,z, utilities.randint(1,300), utilities.randRGBA(),
                    utilities.randint(1,140), style = s).interactiveState = 2

    


class Expands(Circle):

    def start(self):
        """ instead of using __init__() they implement start() which happens right after init
        this can made code cleaner in some cases
        """
        self.delta = utilities.seed.choice([-1,1]) # accessing the random seed in utilities module directly
        self.interactiveState = 2 # dragabble
        self.destColor = utilities.randRGBA()

    def step(self):
        """ increase size until 300 and then decrease down to 0
        change towards destination color, if reached choose new destination
        """
        self.width += self.delta
        if self.width > 300 or self.width < 1 : self.delta = -self.delta

        if self.color != self.destColor :
            r = self.color[0] + (self.destColor[0]-self.color[0])*0.005
            if self.destColor[0] - r < 0.005 : r = self.destColor[0] # snap
            g = self.color[1] + (self.destColor[1]-self.color[1])*0.005
            if self.destColor[1] - g < 0.005 : g = self.destColor[1] # snap
            b = self.color[2] + (self.destColor[2]-self.color[2])*0.005
            if self.destColor[2] - b < 0.005 : b = self.destColor[2] # snap
            a = self.color[3] + (self.destColor[3]-self.color[3])*0.005
            if self.destColor[3] - a < 0.005 : a = self.destColor[3] # snap
            self.color = r,g,b,a
            #print self.color, self.destColor
        else :
            self.destColor = utilities.randRGBA()

            #self.color[0] = self.color[0] + (self.destColor[1]-self.color[1])/100
            #self.color[0] = self.color[0] + (self.destColor[2]-self.color[2])/100
            #self.color[0] = self.color[0] + (self.destColor[3]-self.color[3])/100




##

MirraApp() # init always here your main app class that extends main.App






