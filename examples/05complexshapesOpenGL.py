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
        self.caption = "mirra example drawing complex shapes 1" # window name
        self.size = 640, 480 #window size
        self.pos = 100,100 # window top left location
        self.fullScreen = 0 # if fullScreen is on it will overwrite your pos and size to match the display's resolution
        self.frameRate = 15 # set refresh framerate

    def start(self):
        """ First thing to happen after the instance has been initalisiated
            good place to instanciate classes and init stuff
        """
        for z in range(20):
            w,h = self.size
            x,y = utilities.randPoint(1,1,w,h)
            s = Shape(x, y, z, 50, (0.5, 0,8, 0.2, 0.7))
            s.interactiveState = 2
            s.rotation = utilities.randint(1,360)



class Shape(Circle):
    """ totally overwrites the Circle render function
        but yet it uses its other methods and props such as intersection, it is
        dragable, it has rotation prop (though this does not rotate the shape itself)
    """
    def step(self):
        """ in this case this does not rotate the shape because the render method
        is totally overwriten. But I use this prop in the new render to rotate it
        """
        self.rotation += 1
        

    def render(self) : #,engine):
        rad = 8
        inner = rad-2
        
        glPushMatrix() # puch main
        
        glTranslatef(self.x, self.y, -self.z) # where we draw this shape?
        glRotate(self.rotation, 0, 0, 0.1) # here is the rotation happening, # shapes rotation
        glColor4f (self.color[0], self.color[1],self.color[2], self.color[3]) # shapes color
        gluDisk(engine.q, 0, self.width/2, 50, 1)

        glPushMatrix() # push circles
       
        glColor4f (0.2, 0.5, 0.2, 0.7) # orbital circles color
        
        glTranslatef(-self.radius, 0, 0)
        gluDisk(engine.q, inner, rad, 20, 1)

        glTranslatef(self.radius, -self.radius, 0)
        gluDisk(engine.q, inner, rad, 20, 1)

        glTranslatef(self.radius, self.radius, 0)
        gluDisk(engine.q, inner, rad, 20, 1)

        glTranslatef(-self.radius, self.radius, 0)
        gluDisk(engine.q, inner, rad, 20, 1)

        glPopMatrix() # pop from circles
            
        glPopMatrix() # pop from main circle





MirraApp() # init always your main app class that extends main.App



