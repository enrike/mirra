#!/usr/bin/env python

from __future__ import print_function
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
        self.caption = "mirra example testing mouse events" # window name
        self.size = 640, 480 #window size
        self.pos = 100,100 # window top left location
        self.fullScreen = 0 # if fullScreen is on it will overwrite your pos and size to match the display's resolution
        self.frameRate = 15 # set refresh framerate


    def start(self):
        """ First thing to happen after the instance has been initalisiated
            good place to instanciate classes and init stuff
        """
        self.bgColor=1, 0, 1, 0.03
        self.trails = 1 # trails ON in this example!!

        a = Rect(100, 400, 5, 75, 150, (1,0,0.3,0.3), 3, rotation=45)
        b = Circle(200, 300,6, 100, (1,0,0.5,0.2))
        c = Polygon([(100,100),(210, 230), (190, 240),(10,200)], 7, (1,0.1,0,0.2), 1, rotation=25)
        d = Rect(100, 400, 0, 25, 25, (1,1,0.3,0.3), 3)
        for x in a,b,c,d:
            x.interactiveState = 2 # draggable
      
    # other general app methods defined below
    # If no object trap this events then this methods are called
    def mouseDown(self, x,y):       print("mouseDown", x,y)
    def mouseUp(self, x,y):         print("mouseUp", x,y)
    def mouseDragged(self, x,y):    print("mouseDragged", x,y)
    def rightMouseDown(self, x,y):  print("rightMouseDown", x,y)
    def rightMouseUp(self, x,y):    print("rightMouseUp", x,y)
    def keyDown(self, key):         print("keyDown", key)
    def keyUp(self, key):           print("keyUp", key)

    def joyAxisMotion(self, joystick, index, value): 
       print("Moved axis %d on joystick %d by: %s" % (index, joystick, value))

    def joyBallMotion(self, joystick, index, value):
        print("Moved ball %d on joystick %d by: %s" % (index, joystick, value))

    def joyHatMotion(self, joystick, index, value):
        print("Moved hat %d on joystick %d by: %s" % (index, joystick, value))

    def joyButtonDown(self, joystick, button):
        print("down button %d on joystick %d" % (button, joystick))

    def joyButtonUp(self, joystick, button):
        print("up button %d on joystick %d" % (button, joystick))





MirraApp() # init always your main app class that extends main.App































































