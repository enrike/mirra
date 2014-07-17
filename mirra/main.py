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


global wxisthere
wxisthere = 1 # global flag to remember if wx was found or not

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




##
## PygameWindow ################################

try :
    import pygame
    from pygame.locals import *

    class PygameWindow(Window) :
        """ pygame based window
        """
        def setMouseVisible(self, b) : pygame.mouse.set_visible(b) # boolean
        def getMouseVisible(self) : pass #return pygame.mouse.get_visible()
        mouseVisible = property(getMouseVisible, setMouseVisible)

        def close(self) :  self.running = 0

        def __init__(self, app, caption, pos, size, fullScreen, frameRate, smooth, mode) :
            """ init window acording to setup variables
            """
            Window.__init__(self, app, caption, pos, size, fullScreen, frameRate, smooth) # , mode)
            
##            if sys.platform == 'win32' : # it is win
##                os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % self.pos
##            elif sys.platform == 'darwin':
            os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (self.pos[0], self.pos[1])
            
            pygame.init()
            pygame.display.init()
##            FULLSCREEN    create a fullscreen display
##            DOUBLEBUF     recommended for HWSURFACE or OPENGL
##            HWSURFACE     hardware accelereated, only in FULLSCREEN
##            OPENGL        create an opengl renderable display
##            RESIZABLE     display window should be sizeable
##            NOFRAME       display window will have no border or controls
            
            if self.fullScreen :
                for d in pygame.display.list_modes() : # match the size to the display's resolution
                    if pygame.display.mode_ok(d) :
                        self.size = self.app.size = d
                        break
                self.screen = pygame.display.set_mode(self.size, HWSURFACE | FULLSCREEN | OPENGL | DOUBLEBUF) 
            else:
                self.screen = pygame.display.set_mode(self.size, OPENGL | DOUBLEBUF) # HWSURFACE

            pygame.display.set_caption(self.caption)

            self.clock = pygame.time.Clock()

            engine.start( self.size, sm=self.smooth, m=mode )
            self.events = events.PygameEventsListener(self.app)#, self.engine)

        def mainWindowLoop(self) :
            self.running = 1
            self.app.start()
            while self.running :   # we are done with everything so enter the endless loop
                if self.events.deal() == -1 : break # break the loop to quit
                self.clock.tick(self.frameRate) # mantain framerate in fps                
##                engine.step()              # step all objects in stack
                self.app.step()                 # call subclass step method
                engine.render()
                self.app.render() #engine) # render in main application
                pygame.display.flip()
            self.app.end() # just before exiting
            engine.end()
            pygame.quit() # quiting
##
except ImportError:
    print 'Mirra > main.py : ImportError, no pygame found.'



## WxWindow #####################################      

try:
    import wx
    from wx import glcanvas
    import time
    
    class WxWindow(Window, wx.App) :
        """ wxpython window, it inherits from Window and from wx.App contains the Canvas and the wxtimer
        """
        def getMouseLoc(self) : return self.events.mouseLoc
        mouseLoc = property(getMouseLoc)

        def exit(self) : self.frame.Close(True) 
    
        def __init__(self, app, frameclass, caption, pos, size, fullScreen, frameRate, smooth, mode):

            if 'linux' in sys.platform : ## correct  menu weirdness
                size = size[0] - 4, size[1] - 23
                
            Window.__init__(self, app, caption, pos, size, fullScreen, frameRate, smooth) #, mode) # env removed
            wx.App.__init__(self, 0)
            self.app = app
            self.frameClass = frameclass
            self.init = 0
            self.mode = mode

        def initWindow(self): # 2
            if self.fullScreen :
                self.size = self.app.size = wx.GetDisplaySize() # set to screen resolution

            frame_size = 0,0#self.size#[0]-100, self.size[1] -100
            canvas_size = self.size#[0], self.size[1] #- 45
            glsize = self.size

            if sys.platform == 'win32':# to correct weirdness of wx menu
                glsize = self.size[0] - 8, self.size[1]
                self.app.size = self.size[0] - 8, self.size[1] - 45
            elif 'linux' in sys.platform :
                self.app.size = self.size[0], self.size[1] - 18
            
            self.frame = self.frameClass(self.app, None, -1, self.caption, self.pos, frame_size) # init
            
##            if sys.platform == 'darwin' :
##                self.canvas = glcanvas.GLCanvas(self.frame, -1, self.pos, self.frame.GetClientSize())
##            else:
##                self.canvas = glcanvas.GLCanvas(self.frame, -1, self.pos, (self.size[0]+10,self.size[1]+45)) #, name=self.caption)

            attribList = (glcanvas.WX_GL_RGBA, # RGBA
                      glcanvas.WX_GL_DOUBLEBUFFER, # Double Buffered
                      glcanvas.WX_GL_DEPTH_SIZE, 24) # 24 bit

            self.canvas = glcanvas.GLCanvas(self.frame, -1, self.pos, canvas_size, attribList=attribList) #, name=self.caption)

            self.canvas.Bind(wx.EVT_PAINT, self.OnPaint, )
            self.canvas.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground) # dummy

            def OnCloseWindow(evt):
                self.t.Stop()
                self.frame.Destroy()
            self.frame.Bind(wx.EVT_CLOSE, OnCloseWindow)

            self.glsize = glsize # self.canvas.GetSize() # passed to glOrtho in engine initialisation
            self.frame.doFrame(self.canvas)
            if self.fullScreen : self.frame.ShowFullScreen(1)       
            self.SetTopWindow(self.frame)
            self.frame.Show()

            print "window", self.size, "app", self.app.size, "frame", frame_size, "canvas", canvas_size, "glsize", self.glsize


        def initFrameRate(self) : # THIS IS THE LAST THING TO HAPPEN, from the first loop
            """ in wx this initialises all, this is because there are problems with the order specially
            on linux
            """
            #self.engine = graphics.Engine(self.glsize, smooth=self.smooth, mode=self.mode) # init rendering engine with GLSIZE
            engine.start(self.glsize, sm=self.smooth, m=self.mode)
            self.initInputEvents() # init window, graphics engine, event system, bind events etc...
            self.t = utilities.FpsTimer(self.frameRate, self.canvas.Refresh) #  this triggers EVT_PAINT and therefore self.loop# self.refreshGL)
            self.init = True
            self.last = time.time()
            self.app.start() # call start subclass method just before entering the main loop, to initialise objects etc...

        def OnSize(self, evt) : pass         # to do : reset engine etc.. to match current window size
        def OnEraseBackground(self,evt) : pass         # to avoid flashing on windows
        #def onMouseDClick(self, evt):      self.events.wxmouseDClick(self, evt)
        def OnMouseDown(self, evt) :        self.events.wxmouseDown(self.canvas, evt)
        def OnMouseUp(self, evt) :            self.events.wxmouseUp(self.canvas, evt)
        def OnRightMouseDown(self, evt) : self.events.wxrightMouseDown(self.canvas, evt)
        def OnRightMouseUp(self, evt) :     self.events.wxrightMouseUp(self.canvas, evt)
        def OnMouseMotion(self, evt) :      self.events.wxmouseMoved(self.canvas, evt)
        def OnKeyDown(self, evt) :            self.events.wxkeyDown(self.canvas, evt)
        def OnKeyUp(self, evt) :                self.events.wxkeyUp(self.canvas, evt)
        # joystick
        def OnJoyButtonUp(self, evt) :             self.events.joyButtonUp(self.canvas, evt)
        def OnJoyButtonDown(self, evt) :    self.events.joyButtonDown(self.canvas, evt)
        def OnJoyMove(self, evt) :              self.events.joyMove(self.canvas, evt)
        def OnJoyZMove(self, evt) :             self.events.joyZMove(self.canvas, evt)
        def OnJoyEvents(self, evt) :             self.events.joyEvents(self.canvas, evt)

        def initInputEvents(self) : # 6
            self.events = events.WxEventsListener(self.app) #, engine) # instance of event handler
            # mouse events
            self.canvas.Bind(wx.EVT_LEFT_DOWN,    self.OnMouseDown)
            #self.app.Bind(wx.EVT_LEFT_DCLICK,self.onMouseDClick)
            self.canvas.Bind(wx.EVT_LEFT_UP,            self.OnMouseUp)
            self.canvas.Bind(wx.EVT_LEFT_DOWN,      self.OnMouseDown)
            self.canvas.Bind(wx.EVT_RIGHT_DOWN,     self.OnRightMouseDown)
            self.canvas.Bind(wx.EVT_RIGHT_UP,           self.OnRightMouseUp)
            self.canvas.Bind(wx.EVT_MOTION,             self.OnMouseMotion)
            self.canvas.Bind(wx.EVT_KEY_DOWN,       self.OnKeyDown)
            self.canvas.Bind(wx.EVT_KEY_UP,             self.OnKeyUp)
            if wx.Platform == '__WXMSW__' : # avoid some wx weirdness on windows
                self.Bind(wx.EVT_LEFT_DCLICK,  self.OnMouseDown)       
            # joystick / gamepads
            self.joy = wx.Joystick()
            self.joy.SetCapture(self.frame)
            self.canvas.Bind(wx.EVT_JOY_BUTTON_DOWN, self.OnJoyButtonUp)
            self.canvas.Bind(wx.EVT_JOY_BUTTON_UP,      self.OnJoyButtonDown)
            self.canvas.Bind(wx.EVT_JOY_MOVE,               self.OnJoyMove)
            self.canvas.Bind(wx.EVT_JOY_ZMOVE,              self.OnJoyZMove)
            self.canvas.Bind(wx.EVT_JOYSTICK_EVENTS,    self.OnJoyEvents)
        

        def OnPaint(self, evt) : # triggerd from EVT_PAINT after glcanvas.Refresh from abstractimer
            wx.PaintDC(self.canvas) # prepare glcanvas for opengl drawing
            self.canvas.SetCurrent()
            if not self.init: self.initFrameRate()
            self.app.step() # call subclass step method
##            engine.step() # step all objects in stack
            engine.render() #self.fcount)
            self.app.render() #engine) # main application
            self.canvas.SwapBuffers()

        def mainWindowLoop(self):
            self.MainLoop() # entering wx.App main loop
            engine.end() # main loop exited


except ImportError:
    print '*'*10
    print 'Mirra > main.py : ImportError, could not import wxPython. This is not a problem unless you want to use wxpython instead of pygame'
    print '*'*10
    global wxisthere
    wxisthere = 0 # flag checked when trying to instanciate wx based window class













# main mirra application #########################################
    
class App(object):
    """ contains (wxPython/Pygame) window
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

    def readSetUpPrefs(self, f) :
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

        abspath = utilities.getabspath(f)

        if not abspath == '' :
            raw = open(abspath, 'rU').read()
            self.jsondata = json.loads(raw)
            
            self.frameRate = self.jsondata['setup']['framerate'] 
            self.size = self.jsondata['setup']['size']  
            self.pos = self.jsondata['setup']['pos']  
            self.fullScreen = self.jsondata['setup']['fullscreen'] # if True you must pass your display resolution

##        except :
##            print 'warning : could not find a valid preference file  .........'


    def __init__(self, smooth = 0, env = 'pygame', caption = 'mirra', pos = (0,0), size = (640, 480),
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
        self.mode = '2D'
        self.jsondata = None
    
        self.setUp() # get general window parameters from subclass
        self.readSetUpPrefs(PREFSFILE)

        if self.env == 'wx' :  #wpython selected
            if not wxisthere : # wx is NOT installed in the system, 
                print 'wxPython was not found in your system, using pygame instead'
                self.env = 'pygame' # RESET TO PYGAME to enter next if statement !!
            else:
                if not self.frameClass : # a wxframe was not defined by user
                    self.frameClass = utilities.WxMirraFrame # set default from basic frame in utilities
                    
##                if sys.platform == 'darwin': # mac
##                    corrected_size = self.size[0], self.size[1] 
##                elif sys.platform == 'win32' : # windows
##                    corrected_size = self.size[0] -10, self.size[1] ## correct deformation
##                else : # linux an others
##                    corrected_size = self.size[0], self.size[1]

                wxwindow_size = self.size[0], self.size[1] # CHECK THIS
                    
                self.window = WxWindow(self, self.frameClass, self.caption, self.pos, wxwindow_size,
                                       self.fullScreen, self.frameRate, self.smooth, self.mode)
                self.window.initWindow()
             
        if self.env == 'pygame': # either pygame was selected or wxpython was selected but not found in the system 
            self.window = PygameWindow(self, self.caption, self.pos, self.size, self.fullScreen,
                                       self.frameRate, self.smooth, self.mode)
            
        self.setWindowProps() ## set now the props from prefs.txt that could not be set earlier
        self.window.mainWindowLoop() # all done!, enter main loop
            
        self.end() # main loop exited, this is the last thing that happens in our application

    def exit(self) :  self.window.exit()

    # methods to extend later in subclass
    def setUp(self) : pass
    
    def start(self) : pass
    def end(self) : pass
    def step(self) : pass
    def render(self) : pass #, e) : pass # allow opengl commands using e instance of engine
    
    def mouseDown(self, x,y) : pass
    def mouseUp(self, x,y) : pass
    def mouseDragged(self, x,y) : pass
    def rightMouseDown(self, x,y) : pass
    def rightMouseUp(self, x,y) : pass
    def keyDown(self, k) : pass
    def keyUp(self, k) : pass

    def joyAxisMotion(self, joystick, index, value) : pass
    def joyBallMotion(self, joystick, index, value) : pass
    def joyHatMotion(self, joystick, index, value) : pass
    def joyButtonDown(self, joystick, button) : pass
    def joyButtonUp(self, joystick, button) : pass

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

