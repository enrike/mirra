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
        self.caption = "mirra audio" # window name
        self.size = 640, 480 #window size
        self.pos = 100,100 # window top left location
        self.fullScreen = 0 # if fullScreen is on it will overwrite your pos and size to match the display's resolution
        self.frameRate = 15 # set refresh framerate


    def start(self):
        """ First thing to happen after the instance has been initalisiated
            good place to instanciate classes and init stuff
        """
	self.initAudio()
        
	self.c = SoundBlob()
        self.ch = self.findFreeChannel() # we need to remember the channel to be able to change the vol and pan

        f = utilities.path("data/tone.aiff")
        self.playSound(f, loop=-1)

    def step(self):
        x, y = self.mouseLoc
        v = 1 - (y/460.) # max vol is at top
        p = x/640. # 0 is left and 1 is right
        self.setVolume(self.ch, v, p)



class SoundBlob(Circle):

    def __init__(self):
        Circle.__init__(self, 100, 100, 1, 100, color=(1,0,0)) # hard wired props
        self.interactiveState = 2
        self.s = utilities.path("data/beep1.aiff")
        self.app.preLoadSound(self.s) # it can be preloaded if you want

    def mouseDown(self, x,y):
        Circle.mouseDown(self, x,y) # super

        #ch = self.app.findFreeChannel()
        v = 1 - (self.y/460.) # max vol is at top
        p =  self.x/640.
        self.app.playSound(self.s, volume=v, pan=p, loop=2)







MirraApp() # init always your main app class that extends main.App








