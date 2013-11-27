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
        self.caption = "mirra example complex" # window name
        self.size = 640, 480 #window size
        self.pos = 100,100 # window top left location
        self.fullScreen = 0 # if fullScreen is on it will overwrite your pos and size to match the display's resolution
        self.frameRate = 15 # set refresh framerate

    def start(self):
        """ First thing to happen after the instance has been initalisiated
            good place to instanciate classes and init stuff
        """
        self.text = Text('dummy text', 20, 20, 99, 'timesroman', 10)

        self.circle = Circle(350, 350, 3, 200, (0.5, 0.1, 0))
        self.circle.blend = 0.3  # another way to set blend
        self.circle.interactiveState = 2 # now it can be dragged

    def step(self):
        w = self.size[0] # stage width
        f = (1.0/w)*self.circle.loc[0] # how many steps within 0 to 1 range of blend is each width pixel so that window left is 0 blend and window right is blend 1
        self.circle.blend = f

        blend= self.circle.blend
        loc = self.circle.loc
        r,g,b,a = self.circle.color
        z = self.circle.z
        i = self.circle.interactiveState
        string = 'blend:'+str(blend)+' | loc:' + str(loc) +' | color: '+str(r)+", "+str(g)+", "+str(b)+", "+str(a)+' | z loc:' + str(z)+' | interactivestate:' + str(i)
        self.text.text = string





MirraApp() # init always your main app class that extends main.App













































