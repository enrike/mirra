#!/usr/bin/env python

from mirra import main
from mirra.graphics import *
from mirra import utilities



""" Mirra : 2D graphic engine in OpenGL by www.ixi-software.net
    Check out documentation file
"""


class MirraApp(main.App):
    """ main appplication class, handles window contains events and graphics manager.
        Subclasses main.App and extends its public methods
    """
    def setUp(self) :
        """ set here the main window properties and characteristics
        """
        self.env = 'qt'
        self.caption = "mirra QT example" # window name
        self.size = 800, 600 #window size
        self.pos = 100,100 # window top left location
        self.fullScreen = 0 # if fullScreen is on it will overwrite your pos and size to match the display's resolution
        self.frameRate = 15 # set refresh framerate

    def start(self) :
        """ First thing to happen after the instance has been initalisiated
            good place to instanciate classes and init stuff
        """
        import qtgui
        qtgui.do(self.window)
        
        self.bgColor = 1,0.5,0.7,0.5
        
        s = 'this is Mirra window opened using QT'
        Text(s, 10, 100)
        s = 'check QT website'
        Text(s, 10, 120)
        s = 'You just need to set self.env to qt on setUp() to activate QT '
        Text(s, 10, 140)
        s = 'If no QT is found it defaults to pygame'
        Text(s, 10, 200)

        d = Rect(100, 400, 0, 25, 25)
        d.interactiveState = 2 # draggable
        
        self.r = Rect(100, 100, 1, 20, 20, color=(1,0,0,1), stroke=1)
        Rect(self.size[0]/2, self.size[1]/2, 1, self.size[0], self.size[1], color=(1,1,0,1), stroke=1)

        Line((0,0), self.size)
        
        Line((0,self.size[1]),(self.size[0],0))

##        self.window.frame.doMenu()

    def step(self):
        """ called from timer very x times per sec
            depends on the fps passed to App
        """
        self.r.loc = self.mouseLoc


    # other general app methods defined below
    # If no object trap this events then this methods are called
    def mouseDown(self, x,y): pass
    def mouseUp(self, x,y): pass
    def mouseDragged(self, x,y): pass
    def rightMouseDown(self, x,y): pass
    def rightMouseUp(self, x,y): pass
    def keyPressed(self, key,x,y): pass



MirraApp() # init always your main app class that extends main.App






