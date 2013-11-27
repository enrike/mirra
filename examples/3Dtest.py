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
        self.mode = '3D'
        self.caption = "direct drawing with OpenGL using graphics engine instance" # window name
        self.size = 800, 600 # window size
        self.pos = 0,0 # window top left location
        self.fullScreen = 1 # if fullScreen is on it will overwrite your pos and size to match the display's resolution
        self.frameRate = 20 # set refresh framerate

    def start(self):
        self.rx = 0


    def render(self, e):
        """ this is receives an instance of the graphics engine 'e' that allows to call drawing functions direclty
        from main application.
        this method receives an instance of the graphics engine 'e' that allows to call drawing functions
        direclty from main application. Drawing calls from here are excuted after all objects on stack
        are drawn, this means that Z position has no value, they go on top of everything and get drawn
        in order of execution
        """
##        # draw a line
##        glPushMatrix()
##
##        glTranslatef(self.size[0]/2, self.size[1]/2, -1) # translate to window center p0int
####        glRotatef(rotation, 0, 0, 0.1)
##        glColor4f (1.0, 0, 0, 1)
##        glLineWidth(10)
##
##        glBegin(GL_LINES)
##        glVertex2i(10, -100) # draw pixel points
##        glVertex2i(200, -200)
##        glEnd()
##        glPopMatrix()
##
##        # draw a circle
##        glPushMatrix()
##        
##        glTranslatef(200, 200, -1) # translate to window center point
##        glColor4f (0.3, 0.5, 0.2, 0.3)
##        gluDisk(gluNewQuadric(), 90, 100, 30, 1) # there is a gluNewQuadric() in engine, we could access it with e.q
##        
##        glPopMatrix()

        ##################################################################################
        
        glPushMatrix()
        
	glTranslatef(300, 200, -5000.0);		# Move Right And Into The Screen
	glRotatef(self.rx, 1.0, 1.0, 1.0);		# Rotate The Cube On X, Y & Z

	s = 120.0
	
	glBegin(GL_QUADS);			# Start Drawing The Cube

	glColor3f(0.0,1,0.0);			# Set The Color To Blue
	glVertex3f( s, s,-s);		# Top Right Of The Quad (Top)
	glVertex3f(-s, s,-s);		# Top Left Of The Quad (Top)
	glVertex3f(-s, s, s);		# Bottom Left Of The Quad (Top)
	glVertex3f( s, s, s);		# Bottom Right Of The Quad (Top)

	glColor3f(1.0,0.5,0.0);			# Set The Color To Orange
	glVertex3f( s,-s, s);		# Top Right Of The Quad (Bottom)
	glVertex3f(-s,-s, s);		# Top Left Of The Quad (Bottom)
	glVertex3f(-s,-s,-s);		# Bottom Left Of The Quad (Bottom)
	glVertex3f( s,-s,-s);		# Bottom Right Of The Quad (Bottom)

	glColor3f(1.0,0.0,0.0);			# Set The Color To Red
	glVertex3f( s, s, s);		# Top Right Of The Quad (Front)
	glVertex3f(-s, s, s);		# Top Left Of The Quad (Front)
	glVertex3f(-s,-s, s);		# Bottom Left Of The Quad (Front)
	glVertex3f( s,-s, s);		# Bottom Right Of The Quad (Front)

	glColor3f(1.0,1.0,0.0);			# Set The Color To Yellow
	glVertex3f( s,-s,-s);		# Bottom Left Of The Quad (Back)
	glVertex3f(-s,-s,-s);		# Bottom Right Of The Quad (Back)
	glVertex3f(-s, s,-s);		# Top Right Of The Quad (Back)
	glVertex3f( s, s,-s);		# Top Left Of The Quad (Back)

	glColor3f(0.0,0.0,1.0);			# Set The Color To Blue
	glVertex3f(-s, s, s);		# Top Right Of The Quad (Left)
	glVertex3f(-s, s,-s);		# Top Left Of The Quad (Left)
	glVertex3f(-s,-s,-s);		# Bottom Left Of The Quad (Left)
	glVertex3f(-s,-s, s);		# Bottom Right Of The Quad (Left)

	glColor3f(1.0,0.0,1.0);			# Set The Color To Violet
	glVertex3f( s, s,-s);		# Top Right Of The Quad (Right)
	glVertex3f( s, s, s);		# Top Left Of The Quad (Right)
	glVertex3f( s,-s, s);		# Bottom Left Of The Quad (Right)
	glVertex3f( s,-s,-s);		# Bottom Right Of The Quad (Right)
	
	glEnd();				# Done Drawing The Quad

	glPopMatrix()

	self.rx += 0.5                 # Decrease The Rotation Variable For The Quad




MirraApp() # init always your main app class that extends main.App
















































