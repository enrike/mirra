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
        self.caption = "mirra extending other classes" # window name
        self.size = 640, 480 #window size
        self.pos = 100,100 # window top left location
        self.fullScreen = 0 # if fullScreen is on it will overwrite your pos and size to match the display's resolution
        self.frameRate = 15 # set refresh framerate


    def start(self):
        """ First thing to happen after the instance has been initalisiated
            good place to instanciate classes and init stuff
        """
        for z in range(20):
            y = utilities.randint(0, self.size[0])
            h = utilities.randint(1, 200)
            c = utilities.randRGBA()
            Strippe(y, z, h, c, self.size)




class Strippe(Polygon):
    def __init__(self, y=10, z=0, h=10, color=(0, 0, 0), size=(0,0)):
        tl= (0,   y - (h/2))
        tr= (size[0], y - (h/2))
        br= (size[0], y + (h/2))
        bl= (0,   y + (h/2))
        v = [tl,tr,br,bl] # poligon vertex

        #Polygon.__init__(self, v, z, color)
        super(Strippe, self).__init__(v, z, color)

        self.size = size
        self.y = y
        self.h = h

        self.deltaY = 0
        while self.deltaY == 0 :
            self.deltaY = utilities.randint(-200, 200) / 100

    def step(self):
        y = self.y + self.deltaY

        if y < 0 :
            y = 0 # force to top
            self.deltaY *= -1
        if y > self.size[1] :
            y = self.size[1] # force to bottom
            self.deltaY *= -1

        self.setY()
        self.y = y # update center


    def setY(self):
        v = self.v[:] # duplicate! always when manipulating arrays this way

        tl = (v[0][0], v[0][1]+self.deltaY)
        tr = (v[1][0], v[1][1]+self.deltaY)
        br = (v[2][0], v[2][1]+self.deltaY)
        bl = (v[3][0], v[3][1]+self.deltaY)

        v = [tl,tr,br,bl] # new vertexes
        self.v = v # update vertex array




MirraApp() # init always your main app class that extends main.App


