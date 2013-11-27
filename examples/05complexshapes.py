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
        self.caption = "mirra example drawing complex shapes 1" # window name
        self.size = 640, 480 #window size
        self.pos = 100,100 # window top left location
        self.fullScreen = 0 # if fullScreen is on it will overwrite your pos and size to match the display's resolution
        self.frameRate = 15 # set refresh framerate

    def start(self):
        """ First thing to happen after the instance has been initalisiated
            good place to instanciate classes and init stuff
        """
        for i in range(6):
            w,h = self.size
            x,y = utilities.randPoint(1,1,w,h)
            r,g,b = utilities.randRGB()
            c = r,g,b,0.3
            s = utilities.choice((GLU_LINE, GLU_FILL, GLU_SILHOUETTE, GLU_POINT))
            Shape(x, y, i, 80, c, s)



class Shape(Circle):
    def __init__(self, x,y,z,d,c,s):
        super(Shape, self).__init__(x,y,z,d,c,style=s)
        self.interactiveState = 2

    def render(self) : #,engine):
        """ extends built in render method to make it more complex
        """
        super(Shape,self).render()

        for i in range(1,20):
            engine.drawCircle(self.x, self.y, self.z, self.width/i, self.color, style=self.style)
            # NOTE: when you call draw functions directly from render() you must pass
            # a color with an alpha chanel ON, if self.color contains alpha
            # this is due to the way OpenGL renders alphas.
            # so if you want to mix a non alpha with an alpha use an object instead of a
            # drawing function like is shown in example8extendingrender2.py
            left = self.x - self.width/2, self.y
            right = self.x + self.width/2, self.y
            engine.drawLine(left, right, 0)




MirraApp() # init always your main app class that extends main.App



