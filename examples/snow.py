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
        """ First thing to happen after the instance has been initalisiated
            good place to instanciate classes and init stuff
        """
       
        self.wind = utilities.randint(-2,2)
        
        for z in range(100):
            x = utilities.randint(0, self.width)
            y = utilities.randint(-150, 0) 
            d = utilities.randint(5,10)
            Flake(x,y,z,d,d,color=(0,1,0,float(d)/10))



class Flake(Rect):
    
    def start(self):
        self.setState()

    def setState(self):
##        self.deltaY = 0
        self.rotDelta = 0
        self.deltaY = utilities.random()*2 # to get float
        while self.rotDelta == 0 : # just the first time
            self.rotDelta = utilities.choice([-1,1])

    def step(self):
        self.y += self.deltaY
        self.x += self.app.wind
        if self.y >= self.app.height or self.x <= 0  or self.x >= self.app.width :
            self.y = 0
            self.x = utilities.randint(0, self.app.width)
            self.setState()
        self.rotation += self.rotDelta



MirraApp() # init always here your main app class that extends main.App




