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
        self.caption = "mirra example constraining a shape to a rect" # window name
        self.size = 640, 480 #window size
        self.pos = 100,100 # window top left location
        self.fullScreen = 0 # if fullScreen is on it will overwrite your pos and size to match the display's resolution
        self.frameRate = 15 # set refresh framerate


    def start(self):
        """ First thing to happen after the instance has been initalisiated
            good place to instanciate classes and init stuff
        """
        Text('constraining a shape : try to drag the circle few times', 20, 50, 1)
        self.c = ConstrainCircle(100,100,2,50,(1,0,0))
        self.c.interactiveState = 2
        Rect(150, 150, 1, 100, 100, stroke=1)

        #self.c2 = Circle(100,100,2,50,(0.5,0.5,0.5))
        #self.c2.setInteractiveState(2)
        #w,h = self.getSize() # windows size
        #self.c2.setConstrainRect(0,0,w,h) # this one always constrain to window boundaries


class ConstrainCircle(Circle):

    def mouseDown(self,x,y):
        Circle.mouseDown(self, x,y)
        if self.constrainRect == (0,0,0,0):
            self.constrainRect = 100,100,200,200
            self.color = 1,0,0
        else:
            self.constrainRect = 0,0,0,0
            self.color = 0,1,0






MirraApp() # init always your main app class that extends main.App






