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
        self.caption = "mirra text" # window name
        self.size = 640, 480 #window size
        self.pos = 100,100 # window top left location
        self.fullScreen = 0 # if fullScreen is on it will overwrite your pos and size to match the display's resolution
        self.frameRate = 15 # set refresh framerate
        

    def start(self):
        """ First thing to happen after the instance has been initalisiated
            good place to instanciate classes and init stuff
        """
        Text('this are the available fonts and size combinations :', 20, 15)
        Text('typewriter 13', 20,40,1,'typewriter', 13)
        Text('typewriter 15', 20,60,1,'typewriter', 15)
        Text('timesroman 10', 20,80,1,'timesroman', 10)
        Text('timesroman 24', 20,100,1,'timesroman', 24)
        Text('helvetica 10', 20,120,1,'helvetica', 10)
        Text('helvetica 12', 20,140,1,'helvetica', 12)
        Text('helvetica 18', 20,160,1,'helvetica', 18)

        self.count = 0
        self.counterlabel = Text('dummystring', 300, 100, color=(0.5,0.3,0))

    def step(self):
        """ called from timer very x times per sec
            depends on the fps passed to App
        """
        #self.counterlabel.loc = self.getMouseLoc()
        #x,y = self.getMouseLoc()
        #self.counterlabel.setLoc(x,y)
        self.counterlabel.loc = self.mouseLoc
        self.counterlabel.text = 'counter is : '+str(self.count)
        self.count += 1






MirraApp() # init always your main app class that extends main.App


















































