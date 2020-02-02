#!/usr/bin/env python

# MUST put this is you are using pyopengl 3 and manually copy the eggs to the dist/lib folder
from __future__ import print_function
import sys, os
print('inserting eggs path for py2exe')
# need to manually do this for now. used when running as exe. crap, i know ...
sys.path.insert(0, os.path.join(sys.prefix, "PyOpenGL-3.0.0a6-py2.5.egg"))
sys.path.insert(0, os.path.join(sys.prefix, "setuptools-0.6c6-py2.5.egg"))
    
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
        self.size = 640, 480 # window size
        self.pos = 100,100 # window top left location
        self.fullScreen = 0 # if fullScreen is on it will overwrite your pos and size to match the display's resolution
        self.frameRate = 20 # set refresh framerate

        ## THIS BELOW IS ALL YOU NEED TO GET YOUR SCRIPT
        ## PACKED AS A WINDOWS EXE OR MAC APP.  Check the console output for possible errors.
        # you must have py2exe (windows users) or py2app (mac users) python library
        # installed to be able to pack apps. Check the mirra documentation for more details on packing
        from mirra import export
        export.pack('15exporting_app.py', winconsole=1) # name of the main script
        ##########################################################################

    def start(self):
        """ do some dragggable circles
        """
        for z in range(100):
            x, y = utilities.randPoint(0, 0, self.size[0], self.size[1])
            w = utilities.randint(0, 100)
            c = Circle(x,y,z,w, color = utilities.randRGBA())
            c.interactiveState = 2 # draggable
        




MirraApp() # init always here your main app class that extends main.App




