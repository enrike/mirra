    #!/usr/bin/env python
"""  Mirra : 2D pyOpenGL graphic engine by www.ixi-software.net
    for detailed info check the documentation in the main folder
"""

try: # optimise with psyco if possible
    import psyco
    print "psyco found. optimising ..."
##    psyco.log()
    psyco.profile()
except ImportError:
    print "no psyco found in your system. Psyco can improve Python's performance"


import sys, os, json

# this is to bypass PyOpenGL problem with eggs
if sys.platform == 'win32' :
    for r, d, f in os.walk(sys.prefix) : # filenames
        if r == sys.prefix and '.egg' in f : # only eggs in top level
            if 'PyOpenGL' in f or 'setuptools' in f : #both 
                sys.path.insert( 0, os.path.join(sys.prefix, f) )

from mirra import graphics
from mirra import events

import utilities # for the Audio class
import engine



PREFSFILE = 'prefs.txt'


# Abstract window ########################

class Window(object):
    """ main abstract window class
    """
    def __init__(self, app, caption, pos, size, fullScreen, frameRate, smooth) : 
        """ properties are passed from App
        """
        self.smooth = smooth
        self.caption = caption
        self.pos = pos
        self.size = size
        self.fullScreen = fullScreen
        self.frameRate = frameRate

        self.app = app # remember app for step()
        self.events = 0
        self.audio = 0

        self.guiapp = 0 #self.app.frameClass() #gui.App()
                
        graphics.Base.app = app # pass top App reference to Base class

    def initAudio(self): self.audio = utilities.Audio()
    def mainWindowLoop(self) : pass
##    def render(self, e) : pass # 
    
    def getMouseLoc(self): return self.events.mouseLoc
    mouseLoc = property(getMouseLoc) #, setMouseLoc)



## QtWindow #####################################      
try:
    from PyQt4 import QtCore, QtGui, QtOpenGL
    from OpenGL.GL import *
##from PyQt5 import QtCore, QtGui#, QtOpenGL
##from PyQt5.QtWidgets import QOpenGLWidget, QMainWindow, QApplication

    ##class MirraGLWidget(QOpenGLWidget):
    class MirraGLWidget(QtOpenGL.QGLWidget):
        def __init__(self, parent=None, main=None, size=(800,600)):
            super(MirraGLWidget, self).__init__(parent)
            self.main = main
            self.setFixedSize( size[0], size[1] ) ## crucial. the opengl area rules

        def initializeGL(self):
##            print "-------INITIALIZEGL-------"
##            engine.gl = self.context().versionFunctions()
##            engine.gl.initializeOpenGLFunctions()
##            print dir(engine.gl)
            engine.restart()
        def paintGL(self): self.main.render() ## called after updateGL
        def resizeGL(self, w,h):
            engine.size = w, h
            engine.restart()

        def mousePressEvent(self, event): self.main.mousePressEvent(event)
        def mouseReleaseEvent(self, event): self.main.mouseReleaseEvent(event)
        def mouseMoveEvent(self, event): self.main.mouseMoveEvent(event)
        def keyPressEvent(self,event): self.main.keyPressEvent(event)

        def dragMoveEvent(self, event): print "dragMoveEvent"
        def mouseGrabber(self, event): print "mouseGrabber"
        def dropEvent(self, event): print "dropEvent"


    ##class QTWindow(Window, QMainWindow):
    class QTWindow(Window, QtGui.QMainWindow):

        qapp = QtGui.QApplication(sys.argv)
    ##    qapp = QApplication(sys.argv)
        
        def __init__(self, app, frameclass, caption, pos, size, fullScreen, frameRate, smooth):
            Window.__init__(self, app, caption, pos, size, fullScreen, frameRate, smooth) #, mode) # env removed
            QtGui.QMainWindow.__init__(self, None)
    ##        QMainWindow.__init__(self, None)

            if fullScreen: self.showFullScreen()

            self.glWidget = MirraGLWidget(None, self, size)       
            self.setCentralWidget(self.glWidget)

            self.setWindowTitle(caption)
            self.resize(size[0], size[1]) # size of the whole window

            self.events = events.EventListener(self.app) #, engine) # instance of event handler
            engine.start( size ) # this is overwritten later by the resize

            timer = QtCore.QTimer(self)
            timer.timeout.connect(self.glWidget.updateGL) ## prepares for paintGL
    ##        timer.timeout.connect(self.glWidget.update)
            timer.start(frameRate)

        def render(self):
            self.app.step()
            engine.render()
            self.app.render()

        def mousePressEvent(self, e): self.events.mousePress(e.x(), e.y(), e.button())
        def mouseReleaseEvent(self, e): self.events.mouseRelease(e.x(), e.y(), e.button())
        def mouseMoveEvent(self, e): self.events.mouseDrag(e.x(), e.y())
        def keyPressEvent(self, e): self.events.keyDown(e.key())
        def keyReleaseEvent(self, e): self.events.keyUp(e.key())

        def dragMoveEvent(self, e): print "dragMoveEvent"
        def mouseGrabber(self, e): print "mouseGrabber"
        def dropEvent(self, e): print "dropEvent"
        
        def closeEvent(self, e):
            print "quiting..."
            self.app.end() # just before exiting
            print "app end..."
            engine.end()
            print "engine end..."
            
        def mainWindowLoop(self):
            self.app.start()
            print "after app start"
            self.show()
            print "after self.show()"
            sys.exit( QTWindow.qapp.exec_() )
            
except ImportError:
    print '*'*10
    print 'Mirra > main.py : ImportError, could not import QT'
    print '*'*10


  




# main mirra application #########################################
    
class App(object):
    """ contains window
        defines main events and interface to set general vars on setUp and during runtime
    """    
    def getBgColor(self): return engine.bgColor
    def setBgColor(self, c):
        if len(c) == 3 : c = c[0], c[1], c[2], 0
        engine.bgColor = c  
    bgColor = property(getBgColor, setBgColor)

    def getTrails(self): return engine.trails
    def setTrails(self, b): engine.trails = b      # boolean
    trails = property(getTrails, setTrails)

    def getMouseVisible(self): return self.window.mouseVisible 
    def setMouseVisible(self, b): self.window.mouseVisible = b  
    mouseVisible = property(getMouseVisible, setMouseVisible)
   
    def getMouseLoc(self): return self.window.events.mouseLoc
    #def setMouseLoc(self, b): pass
    mouseLoc = property(getMouseLoc) # , setMouseLoc)

    def getWidth(self): return self.size[0]
    width = property(getWidth)
    def getHeight(self): return self.size[1]
    height = property(getHeight)
    def getWidth2(self): return self.size[0]*0.5 # half
    width2 = property(getWidth2)
    def getHeight2(self): return self.size[1]*0.5 # half
    height2 = property(getHeight2)

    def setWindowProps(self) :
        ''' those props could not be set earlier because windows wasnt setup yet
        '''
        try :
            self.mouseVisible = self.jsondata['setup']['mouseVisible']
            self.bgColor = self.jsondata['setup']['bgColor']
        except :
            print 'error, something wrong with jsondata please check : %s' % self.jsondata

    def readSetUpPrefs(self) :
        ''' read only the ones related to windows setup. others wont work yet
        '''
##        try :
##        if sys.platform == 'darwin' and utilities.run_as_app() :
##            p = os.path.join(os.getcwd(), '../../../', f)
##        else :
##            p = os.path.join(os.getcwd(), f)

##        p = f
##        if utilities.run_as_app() :
##            if sys.platform == 'darwin' :
##                p = os.path.join(os.getcwd(), '../../../', f)
##            elif sys.platform == "win32":
##                # get the exe directory and append the prefs file name
##                p = os.path.join(sys.executable[:-len(os.path.basename(sys.executable))], f)
##            else :
##                print os.getcwd()
##                p = os.path.join(os.getcwd(), f)

        abspath = utilities.getabspath(PREFSFILE)

        print "reading preferences from%s" % PREFSFILE

        if not abspath == '' :
            raw = open(abspath, 'rU').read()
            self.jsondata = json.loads(raw)
            
            self.frameRate = self.jsondata['setup']['framerate'] 
            self.size = self.jsondata['setup']['size']  
            self.pos = self.jsondata['setup']['pos']  
            self.fullScreen = self.jsondata['setup']['fullscreen'] # if True you must pass your display resolution

##        except :
##            print 'warning : could not find a valid preference file  .........'


    def __init__(self, smooth = 0, env = 'qt', caption = 'mirra', pos = (0,0), size = (640, 480),
                 fullScreen = 0, frameRate = 15):
        """ declare and init to some default values for general vars to void errors if
        user doesnt define them on setUp. they are properties so that i can set them from
        setUp() without needed to return them. It just looks more 'clean' 
        despite of maybe not being very elegant
        """
        self.smooth = smooth
        self.env = env
        self.caption = caption
        self.pos = pos
        self.size = size
        self.fullScreen = fullScreen
        self.frameRate = frameRate
        self.window = None
        self.frameClass = None # for wx python
        self.jsondata = None
    
        self.setUp() # get general window parameters from subclass
        #self.readSetUpPrefs(PREFSFILE)

        self.window = QTWindow(self, self.frameClass, self.caption, self.pos, self.size, self.fullScreen,
                                       self.frameRate, self.smooth)
            
        self.setWindowProps() ## set now the props from prefs.txt that could not be set earlier
        self.window.mainWindowLoop() # all done!, enter main loop
            
        self.end() # main loop exited, this is the last thing that happens in our application

    def exit(self) :  self.window.exit()

    # methods to extend later in subclass
    def setUp(self) : pass
    
    def start(self) : pass
    def end(self) : pass
    def step(self) : pass
    def render(self) : pass
    
    def mouseDown(self, x,y) : pass
    def mouseUp(self, x,y) : pass
    def mouseDragged(self, x,y) : pass
    def rightMouseDown(self, x,y) : pass
    def rightMouseUp(self, x,y) : pass
    def keyDown(self, k) : pass
    def keyUp(self, k) : pass

##    def joyAxisMotion(self, joystick, index, value) : pass
##    def joyBallMotion(self, joystick, index, value) : pass
##    def joyHatMotion(self, joystick, index, value) : pass
##    def joyButtonDown(self, joystick, button) : pass
##    def joyButtonUp(self, joystick, button) : pass

    # audio stuff
    def initAudio(self) : 
        self.window.initAudio()
    
    def preLoadSound(self, path) :
        """ def loadSound(self, path)
        """
        self.window.audio.loadSound(path)
        
    def playSound(self, name, volume=1.0, pan=0.5, channel=0, loop=0, maxtime=-1) :
        """ playSound(self, name, volume=1.0, pan=0.5, channel=0, loop=0, maxtime=-1)
        """
        self.window.audio.playSound(name, volume, pan, channel, loop, maxtime)
        
    def setVolume(self, channel, volume=1, pan=0.5):
        """ setVolume(self, channel, volume=1, pan=0.5)
        """
        self.window.audio.setVolume(channel, volume, pan)
        
    def findFreeChannel(self) :
        """ findFreeChannel(self)
        """
        return self.window.audio.findFreeChannel()
    
    def getVolume(self, channel):
        """getVolume(self, channel)
        """
        self.window.audio.getVolume(channel) 
        
    def stopSound(self, channel):
        """stopSound(self, channel)
        """
        self.window.audio.stopSound(channel) 
        
    def pauseAll(self):
        """pauseAll(self)
        """
        self.window.audio.pauseAll() 
        
    def unpauseAll(self):
        """unpauseAll(self)
        """
        self.window.audio.unpauseAll() 
        
    def stopAll(self):
        """stopAll(self)
        """
        self.window.audio.stopAll() 

