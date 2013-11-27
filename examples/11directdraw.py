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
        self.caption = "direct drawing using graphics engine instance" # window name
        self.size = 640, 480 #window size
        self.pos = 100,100 # window top left location
        self.fullScreen = 0 # if fullScreen is on it will overwrite your pos and size to match the display's resolution
        self.frameRate = 15 # set refresh framerate


    def start(self):
        """ First thing to happen after the instance has been initalisiated
            good place to instanciate classes and init stuff
        """
        self.bgColor = 0.9,0.9,0.9


    def render(self) : #, e):
        """ this method receives an instance of the graphics engine 'e' that allows to call drawing functions
        direclty from main application. Drawing calls from here are excuted after all objects on stack
        are drawn, this means that Z argument has no value they go on top of everything and get drawn
        in order of execution
        """
        # Z location has no effect in this case. They will be drawn on top of everything else
        # and in the order or execution
        engine.drawPolygon([(100,200), (250, 300), (490, 330), (100, 410), (50, 30)], 0,
                      color=(0.4,0.5,0.4,0.5), stroke=1, style=0x08FF)
        engine.drawText('hellooooooo!!', 290, 100, 0, color=(0,0,0,1))
        engine.drawLine((10, 10),(300,100), 0, color=(0,0,1,0.6), style=0xF00F)
        engine.drawRect(100,100, 0 ,100,100, color=(1,0,0,0.7))
        engine.drawRect(400,100, 0 ,100,200, color=(1,0,1,0.2),rotation=30)
        engine.drawCircle(150,150, 0 ,100, color=(0,1,0,1), stroke=5, style = GLU_SILHOUETTE)
        engine.drawCircle(450,350, 0 ,100, color=(1,1,0,0.6), stroke=50)
        engine.drawArc(480, 250, 0 , 150, 0, 125, (1,0,0,0.6), 100, style = GLU_LINE)
        engine.drawArc(380, 350, 0, 100, 45, 125, (1,0.5,0,1), 100, style = GLU_POINT)
 

MirraApp() # init always your main app class that extends main.App







