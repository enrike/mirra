#!/usr/bin/env python

from __future__ import print_function
from mirra import main
from mirra.graphics import *
from mirra import utilities

""" Mirra : 2D graphic engine in OpenGL by www.ixi-software.net
    Check out documentation files
"""


class MirraApp(main.App):
    """ it just reads the prefs.txt file which is in JSON format . Those are the values that can be set

    {"setup": {"fullscreen": false, "framerate": 8, "pos": [0, 0], "size": [1024, 768],
    "bgColor": [0.7, 0.7, 0.7], "mouseVisible": true}}

    you can setup your own prefs easily
    """
        
    def start(self):
        self.Circle = Circle(200, 200, 1, 200, color=(1,0,0))
        


    def readOwnPrefs(self, filename) :
        ''' read only the ones related to windows setup. others wont work yet
        '''
        try :
            p = utilities.getabspath(filename)

            raw = open(p, 'rU').read()
            self.jsondata = json.loads(raw)

            self.whatever = self.jsondata['whateverprop']

        except :
            print('warning : could not find a valid preference file  .........')





MirraApp() # init always here your main app class that extends main.App




