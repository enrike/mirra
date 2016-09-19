#!/usr/bin/env python

from mirra import main
from mirra.graphics import *
from mirra import utilities
""" Mirra : 2D graphic engine in OpenGL by www.ixi-software.net
    Check out documentation files
"""
from OpenGL.GL import *


class MirraApp(main.App):
    """ main appplication class, handles window contains events and graphics manager.
        Subclasses main.App and extends its public methods
    """
    def setUp(self):
        """ set here the main window properties and characteristics
        """
        self.caption = "direct drawing with OpenGL using graphics engine instance" # window name
        self.size = 640, 480 #window size
        self.pos = 0,0 # window top left location
##        self.fullScreen = 1 # if fullScreen is on it will overwrite your pos and size to match the display's resolution
        self.frameRate = 20 # set refresh framerate


    def render(self) : #, e):
        """ this is receives an instance of the graphics engine 'e' that allows to call drawing functions direclty
        from main application.
        this method receives an instance of the graphics engine 'e' that allows to call drawing functions
        direclty from main application. Drawing calls from here are excuted after all objects on stack
        are drawn, this means that Z position has no value, they go on top of everything and get drawn
        in order of execution
        """
        # draw a line
        glPushMatrix()

        glTranslatef(self.size[0]/2, self.size[1]/2, 0) # translate to window center p0int
##        glRotatef(rotation, 0, 0, 0.1)
        glColor3f (1.0, 0, 0)
        glLineWidth(10)

        glBegin(GL_LINES)
        glVertex2i(0, -100) # draw pixel points
        glVertex2i(200, -200)
        glEnd()
        glPopMatrix()

        # draw a circle
        glPushMatrix()
        
        glTranslatef(200, 200, 0) # translate to window center point
        glColor4f (0.3, 0.5, 0.2, 0.3)
        gluDisk(gluNewQuadric(), 90, 100, 30, 1) # there is a gluNewQuadric() in engine, we could access it with e.q
        
        glPopMatrix()
        

MirraApp() # init always your main app class that extends main.App







