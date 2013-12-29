
from math import * # local binding should be faster
import random
import sys
import os

#global random seed
seed = random.Random()


def getabspath(f=''):
    p = ''
    if run_as_app() :
        if sys.platform == 'darwin' :
            p = os.path.join(os.getcwd(), '../../../', f)
        elif sys.platform == "win32":
            # get the exe directory and append the prefs file name
            p = os.path.join(sys.executable[:-len(os.path.basename(sys.executable))], f)
        else :
            p = os.path.join(os.getcwd(), f)
    else :
        p = os.path.join(os.getcwd(), f)

    if not os.path.isfile( p ) :
        print "prefs file does not exist", p

    return p


def path(res = '') :
    """ DEPRECATED. use getabspath()
        returns the absolute path to a file or folder -> string
    """
    p = os.path.join(os.path.dirname(sys.argv[0]), res)
    if os.path.isfile(p) or os.path.isfile(p) :
        return p
    else :
        print '%s not a valid resource'%res
        return ''

def get_cwd() :
    """ returns the right app cwd when running as mac app
    """
    if sys.platform == 'darwin' and run_as_app() :
        return os.path.join(os.getcwd(), '../../../')
    else :
        return os.getcwd()
    

def get_main_dir() :
    """ returns the directory name of the script or the directory name of the exe -> string
    """
##    import inspect
##    return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    directory = ''
    if run_as_app() :
        directory = os.path.dirname(sys.executable)

    directory = os.getcwd() # os.path.dirname(sys.argv[0])

    return directory


def run_as_app() :
    """ returns True when running the exe, and False when running from a script. -> boolean
    """
    return getattr(sys, 'frozen', False)

##    import imp, sys
##    return (hasattr(sys, "frozen") or # new py2exe
##        hasattr(sys, "importers") # old py2exe
##            or imp.is_frozen("__main__") ) # tools/freeze
##

##if getattr(sys, 'frozen', False):
##    application_path = os.path.dirname(sys.executable)
##elif __file__:
##    application_path = os.path.dirname(__file__)
##
##config_path = os.path.join(application_path, config_name)



# pygame stuff #


try:
    import pygame
except ImportError:
    print 'Mirra > utilities.py : ImportError, could not import pygame. Pygame must be installed in your system to run Mirra'
    sys.exit() # quit


class Audio:
    """ provides basic audio functionality.
    receives an integer with the sampling frequency to init the pygame mixer, defaults to 44100
    To be extended further.
    """
    def __init__(self, freq=44100) :
        self.sounds = {}
        try :
            pygame.mixer.init(freq)
            self.init = 1
        except pygame.error:
            print "no sound device available"

    def loadSound(self, path) :#name) :
        """ returns the path to a sound file
        """
        if self.sounds.has_key(path) : # loaded already there dont load it again
            return self.sounds[path]
        else :
            try :
                sound = pygame.mixer.Sound(path) # load it
##                sound = wx.Sound(path)
                self.sounds[path] = sound # remember
                return sound
            except pygame.error:
                print "no sound device available"

    def playSound(self, path, volume=1.0, pan=0.5, channel=0, loop=0, maxtime=-1) :
        """ playSound(self, name, volume=1.0, pan=0.5, channel=0, loop=0, maxtime=-1)
        """
        if not channel : channel = self.findFreeChannel()

        sound = self.loadSound(path)

        channel.stop() # just in case

        if volume > 1 : volume = 1 # limit
        if volume < 0 : volume = 0
        if pan > 1 : pan = 1
        if pan < 0 : pan = 0

        self.setVolume(channel, volume, pan)
        channel.play(sound, loop, maxtime)
##        sound.Play(wx.SOUND_SYNC)


    def findFreeChannel(self) :
        """ returns a free channel in the mixer
        """
        try :
            return pygame.mixer.find_channel()
        except pygame.error:
            print "no sound device available"
            return 0
        
    def setVolume(self, channel, volume=1, pan=0.5) : # vol 0 to 1, pan 0 to 1
        """ setVolume(self, channel, volume=1, pan=0.5)
        sets volume and pan of given chanel
        """
        pan = 1 - pan # to get 0 left and 1 right
        lvol = (volume * pan)/1. # need to calculte the volume for each channel from vol and pan
        rvol = volume - lvol
        channel.set_volume(lvol, rvol)

    def getVolume(self, channel) : channel.get_volume()
    def stopSound(self, channel) : channel.stop()
    def pauseAll(self) :     pygame.mixer.pause()
    def unpauseAll(self) :   pygame.mixer.unpause()
    def stopAll(self) :      pygame.mixer.stop()





# some utilities below : intersections, colors, random nums etc...

def randint(min, max) :
    """ returns random integer between min and max -> int
    """
    try :
        max <= min
    except:
        max = min+1
        print 'utilities.randint() error : min was bigger than max' # avoid error
    return seed.randint(min, max)

def random() :
    """ returns random float between 0 and 1 -> float between 0 and 1
    """
    return seed.random()

def randRGB() :
    """ returns random RGB tuple color -> tuple r,g,b
    """
    return seed.random(), seed.random(), seed.random()#, 1

def randRGBA() :
    """ returns random RGBA tuple color -> tuple r,g,b,a
    """
    return seed.random(), seed.random(), seed.random(), seed.random()

def randPoint(l=0,t=0,r=0,b=0,rect=(0,0,0,0)) :
    """ returns a random point within a given rect -> tuple x, y
        randPoint(l=0,t=0,r=0,b=0,rect=(0,0,0,0))
    """
    if rect != (0,0,0,0) : l,t,r,b = rect
    return seed.randint(l, r), seed.randint(t, b)

def choice(seq=()) :
    """ choose one in a list with few items -> one item in the sequence passed
    """
    return seed.choice(seq)



""" some quads and rect utilities
"""

def calcPolygonRect(pointArray) :
    """ receives a point list and returns the rect that contains them as a tupple -> tuple left, top, right, bottom
    calcPolygonRect( [ (a,b), (c,d), (a,b), (c,d)  ] ) 
    """
    # init to ridiculously big values. not very elegant or eficient
    l, t, r, b = 10000000, 10000000, -10000000, -10000000
##    l = pointArray[0]
##    t = pointArray[1]
##    r = l
##    b = t

    for n in pointArray: # calc bounding rectangle rect
        if n[0] < l : l = n[0] 
        if n[0] > r : r = n[0] 
        if n[1] < t : t = n[1] 
        if n[1] > b : b = n[1] 

    return l, t, r, b


def calcPolygonRectB(plainArray) :
    """ receives a point list and returns the rect that contains them as a tupple -> tuple left, top, right, bottom
    calcPolygonRect( [ (a,b), (c,d), (a,b), (c,d)  ] ) 
    """
    # init to ridiculously big values. not very elegant or eficient
    l, t, r, b = 10000000, 10000000, -10000000, -10000000
    
    for n in plainArray: # calc bounding rectangle rect
        if n < l : l = n 
        if n > r : r = n 
        if n < t : t = n 
        if n > b : b = n 

    return l, t, r, b




def calcRectCenter( l,t,r,b ) :
    """ returns rect center point -> x,y
        calcRectCenter(l,t,r,b)
    """
    return l+((r-l)*0.5), t+((b-t)*0.5)

def calcPlainRectCenter( r ) :
    """ returns rect center point -> x,y
        calcRectCenter( (l,t,r,b) )
    """
    return r[0] + ( ( r[2]-r[0] )*0.5 ),  r[1] + ( (r[3]-r[1]) *0.5 )


def calcRectRect(x, y, width, height) :
    """ calcs surrounding rect of a rectangular shape -> tuple left, top, right, bottom
        calcRectRect(x, y, width, height)
    """
    return x - width*0.5, y - height*0.5, x + width*0.5, y + height*0.5


def calcRectQuad(x, y, width, height) :
    """ returns a list containing the vertex points of a rect providing its
        x,y, width and height -> list [lefttop, righttop, rightbottom, leftbottom]
        calcRectQuad(x, y, width, height)
    """
    l,t,r,b = calcRectRect(x, y, width, height)
    return [ (l, t), (r, t), (r, b), (l, b) ]

def calcRectPlainQuad(x, y, width, height) :
    """ returns a list containing the vertex points of a rect providing its
        x,y, width and height -> list [ lef, ttop, righ, ttop, right, bottom, left, bottom ]
        calcRectQuad(x, y, width, height)
    """
    l,t,r,b = calcRectRect(x, y, width, height)
    return [ l, t, r, t, r, b, l, b ]

def moveQuad( quad=(), offset=(0,0) ) :
    """ giving a plain quad  [ lef, ttop, righ, ttop, right, bottom, left, bottom ] and an offset (x,y)
    returns the new quad
    """
    return quad[0] + offset[0] , \
            quad[1] + offset[1] , \
            quad[2] + offset[0] , \
            quad[3] + offset[1] , \
            quad[4] + offset[0] , \
            quad[5] + offset[1] , \
            quad[6] + offset[0] , \
            quad[7] + offset[1] , \

##def moveQuadTo( quad=(), quadcenter=(0,0), dest=(0,0) ) :
####    rect = calcPolygonRectB( quad )
####    oldp = calcPlainRectCenter( rect )
##    offset = quadcenter[0]-dest[0], quadcenter[1]-dest[1] 
##    return quad[0] + offset[0] , \
##            quad[1] + offset[1] , \
##            quad[2] + offset[0] , \
##            quad[3] + offset[1] , \
##            quad[4] + offset[0] , \
##            quad[5] + offset[1] , \
##            quad[6] + offset[0] , \
##            quad[7] + offset[1] , \


def constrainToRect(x,y, r) :
    """ constrains a given x,y location to a given rect -> tupple x,y
        constrainToRect(x,y, (l,t,r,b))
    """
    if  x < r[0] : x = r[0] # left
    elif    x > r[2] : x = r[2] # right

    if  y < r[1] : y = r[1] # top
    elif    y > r[3] : y = r[3] # bottom

    return x,y


def calcRelativeVertex(x,y, v=()) :
    """ returns an list with relative x,y distances to a given point x,y from each point in the quad list
        calcRelativeVertex( x,y, [ (a,b), (c,d), (a,b), (c,d)  ] ) 
    """
    return [ (i[0] - x, i[1] - y) for i in v ] 


""" Intersections
glReadPixelsf(x,y,1,1,GL_RGBA)
glReadPixelsf(x,y,1,1,GL_RGBA)[0][0][0] > R
"""
def pointInLine(p, linePoints) :
    """ TO DO: point contained in line
    """
    return False

def pointInRect(p, r) :
    """ returns true if a point is inside a rect. rect is (left, top, right, bottom) -> Boolean
        pointInRect( (x,y), (l,t,r,b) )
    """
    if p[0] >= r[0] and p[0] <= r[2] and p[1] >= r[1] and p[1] <= r[3]: return True


def pointInCircle(p, p2, r)  :
    """ if distance from point to circle center is smaller than radius then it must be inside -> Boolean
    """
    if int(distance(p, p2)) <= r : return True


# point in elipse ?
##def pointInElipse(p, p2, r1, r2)  : pass

# -------------------------------------------

def pointInPoly(point, pointsList) :
    ##__author__ = "Jacob Schwartz"
    ##__copyright__ = "Copyright (c) 2004"
    ##__license__ = "Public Domain"
    ##__version__ = "1.0"

    """Return True if point is contained in polygon (defined by given list of points.) -> Boolean
        pointInPoly( (x,y), [ (a,b), (c,d), (a,b), (c,d)  ] )

        Is given point in polygon?
        Original (and UGLY) C code for this taken from:
        http://www.ecse.rpi.edu/Homepages/wrf/misc_notes/pnpoly.html
        copy-paste-modified into (equally ugly) python.
        Feel free to use, rewrite, (and beautify?) without restriction.
    """
    assert len(pointsList) >= 3, 'Not enough points to define a polygon (I require 3 or more.)'
    assert len(point) >= 2, 'Not enough dimensions to define a point(I require 2 or more.)'

    # If given values are ints, code will fail subtly. Force them to floats.
    x, y = float(point[0]), float(point[1])
    xp = [float(p[0]) for p in pointsList]
    yp = [float(p[1]) for p in pointsList]

    # Initialize loop
    c = False
    i = 0
    npol = len(pointsList)
    j = npol - 1

    while i < npol:
        if ((((yp[i] <= y) and (y < yp[j])) or
            ((yp[j] <= y) and (y <  yp[i]))) and
            (x < (xp[j] - xp[i]) * (y - yp[i]) / (yp[j] - yp[i]) + xp[i])) :
            c = not c
        j = i
        i += 1

    return c



def pointInCoordinates( point, coo) :
    """Return True if point is contained in polygon (defined by given list of coordinates.) -> Boolean
    pointInCoordinates( (x,y), [ a,b,c,d,e,f,g,h ] )
    """
    assert len(coo) >= 6, 'Not enough coordinates to define a polygon (I require 6or more.)'
    assert len(point) >= 2, 'Not enough dimensions to define a point(I require 2 or more.)'

    # If given values are ints, code will fail subtly. Force them to floats.
    x, y = float(point[0]), float(point[1])

    xp = [ float(coo[p]) for p in xrange( 0, len(coo), 2 ) ] # evens X
    yp = [ float(coo[p]) for p in xrange( 1, len(coo), 2 ) ] # odds Y

    # Initialize loop
    c = False
    i = 0
    npol = len(coo) / 2 # HALF
    j = npol - 1
    
    while i < npol:
        if ((((yp[ i ] <= y) and (y < yp[ j ])) or
            ((yp[ j ] <= y) and (y <  yp[ i ]))) and
            (x < (xp[ j ] - xp[ i ]) * (y - yp[ i ]) / (yp[ j ] - yp[ i ]) + xp[ i ])) :
            c = not c
        j = i
        i += 1

    return c


# -------------------------------------------

def distance(p1, p2) :
    """ Return the distance between two points, which may be given as
        (x,y) tuples or as complex numbers. -> float
    """
    return  sqrt( ( (p1[0] - p2[0]) * (p1[0] - p2[0]) ) + ( (p1[1] - p2[1]) * (p1[1] - p2[1]) ) )

##    if p1.__class__ is  complex:
##        p1 = p1.real, p1.imag
##    if p2.__class__ is  complex:
##        p2 = p2.real, p2.imag
    
##    x = p1[0] - p2[0]
##    y = p1[1] - p2[1]
##
##    return sqrt(x*x + y*y)

def pseudoDist(p1, p2) :
    """ it does not use square root so it is cheaper but it is not real but pseudo
    """
    return ( (p1[0] - p2[0]) * (p1[0] - p2[0]) ) + ( (p1[1] - p2[1]) * (p1[1] - p2[1]) )
    


##def dot(c1, c2) :
##    """ ???
##    """
##    return c1.real*c2.real + c1.imag*c2.imag

## ---------------------------------------------------------------------------



def rotPoint(point, axis, ang) :
    """ Orbit. calcs the new loc for a point that rotates a given num of degrees around an axis point,
        +clockwise, -anticlockwise -> tuple x,y
    """
    r = distance(point, axis) # calc radius
    RAng = radians(ang-90)       # convert ang to radians. -90 to convert to normal ang system from opengl.
##    lH = axis[0] + ( r * cos(RAng) )
##    lV = axis[1] + ( r * sin(RAng) )
    return axis[0] + ( r * cos(RAng) ),  axis[1] + ( r * sin(RAng) )


def reverseAng(ang) :
    """ converts angles from OpenGL anticlockwise to clockwise and the other way around -> int ang in degrees
    """
    if ang > 360 or ang < -360: # quite unlikely
        ang = 360 - (ang%360) # 360 - (modulo of ang/360)
    else: # the most usual
        ang = 360 - ang

    return ang


def getAng(p1, p2) :
    """ returns the ang in degrees between two points *clockwise!* -> int ang in degrees
    """
    rAng = atan2(p1[0] - p2[0], p1[1] - p2[1]) # This gives a RadAngle between 2 points
    ang = degrees(rAng)             # convert to degrees
    # returns values between -180 to 180 anticlockwise, so south is 0
    ang = ang + 180                         # now north is 0
    ang = reverseAng(ang)                   # and now convert to clockwise

    return ang


##def x_extent(radius, angle_degrees) :
##        """ Return the x-component of the specified vector.
##        """
##        return cos(radians(angle_degrees)) * radius

##def y_extent(radius, angle_degrees) :
##        """ Return the y-component of the specified vector.
##        """
##        return sin(radians(angle_degrees)) * -radius



############################################################################




        
        
            
        
class RectUtils(object) :
    def __init__(self, x=0,y=0,w=0,h=0) :
        """ rect(self, x=0,y=0,w=0,h=0)
            x,y,loc, width, height
            left,top,right,bottom
            quad ->
            --------------------
            topleft = quad[0]
            topright = quad[1]
            bottomright = quad[2]
            bottomleft = quad[3]
        """
        self.rect = x,y,w,h

    def setRect(self, r) :
        self.__x = r[0]
        self.__y = r[1]
        self.__width = r[2]
        self.__height = r[3]
        w = r[2]*0.5 ; h = r[3]*0.5
        self.__rect = r[0]-w, r[1]-h, r[0]+w, r[1]+h # l t r b
    def getRect(self) :
        return self.__rect
    rect = property(getRect, setRect)

    def setQuad(self, q) : # [ q[0][0], q[0][1], q[1][0], q[2][1] ] # l t r b
        self.rect = q[0][0]+(q[1][0]-q[0][0])*0.5, q[0][1]+(q[2][1]-q[0][1])*0.5, q[1][0]-q[0][0], q[2][1]-q[0][1] 
    def getQuad(self) :
        return [(self.rect[0], self.rect[1]),(self.rect[2], self.rect[1]),(self.rect[2], self.rect[3]),(self.rect[0], self.rect[3])] # tl tr br bl
    quad = property(getQuad, setQuad)

    def setX(self, x) :
        self.rect = x, self.y, self.width, self.height
    def getX(self) : return self.__x
    x = property(getX, setX)

    def setY(self, y) :
        self.rect = self.x, y, self.width, self.height
    def getY(self) : return self.__y
    y = property(getY, setY)

    def setLoc(self, p) :
        self.rect = p[0], p[1], self.width, self.height
    def getLoc(self) : return self.__x, self.__y # self.x, self.y
    loc = property(getLoc, setLoc)

    def setWidth(self, w) :
        self.rect = self.x, self.y, w, self.height
    def getWidth(self) : return self.__width
    width = property(getWidth, setWidth)
    
    def setHeight(self, h) :
        self.rect = self.x, self.y, self.width, h
    def getHeight(self) : return self.__height
    height = property(getHeight, setHeight)

    def setLeft(self,x) :
        self.rect = x+self.width*0.5, self.y, self.width, self.height
    def getLeft(self) : return self.rect[0]
    left = property(getLeft, setLeft)
    
    def setTop(self,y) :
        self.rect = self.x, y+self.width*0.5, self.width, self.height
    def getTop(self) : return self.rect[1]
    top = property(getTop, setTop)
    
    def setRight(self,x) :
        self.rect = x-self.width*0.5, self.y, self.width, self.height
    def getRight(self) : return self.rect[2]
    right = property(getRight, setRight)
    
    def setBottom(self,x) :
        self.rect = self.x, y-self.width*0.5, self.width, self.height
    def getBottom(self) : return self.rect[3]
    bottom = property(getBottom, setBottom)


       







class Fps:
    import time # as class variable

    def __init__(self) :
        self.t = Fps.time.time() # update

    def fps(self) :
        """ returns fps from last call
        """
        lapse = Fps.time.time() - self.t # how long did it take to do current frame?
        self.t = Fps.time.time() # update before returning
        if lapse == 0 : pass # avoid dividing by 0
        print 1/lapse
#





## WXpython utility classes ##

try:
    import wx
    import wx.glcanvas

    class WxMirraFrame(wx.Frame) :
        """ basic frame, just puts the gl canvas covering the whole window
        to be extended by users
        """
        def __init__(self, app, parent, ID, title, pos, size) :
            wx.Frame.__init__(self, parent, ID, title, pos, size)#, wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
            self.app = app # this is the top mirra app. keep a reference to comunicate back
            self.SetSize(size) # sets wx window size
            
##            self.app.window.canvas.Bind(wx.EVT_CLOSE, OnCloseWindow)

##        def OnCloseWindow(evt) :
####            print 'quit'
####            self.t.stop() # stop timer
##            self.Close(True)
##            self.Destroy()
            

        def doMenu(self) :
            menuBar = wx.MenuBar()
            menu1 = wx.Menu()
            menuBar.Append(menu1,"&Archive")
            menu1.Append(101, "&New", "new archive")
            menu1.AppendSeparator()
            menu1.Append(105, "&Quit", "quit")
            self.SetMenuBar(menuBar)
            
##        def doStatusBar(self) :
##            self.CreateStatusBar(1,0)
##            self.SetStatusText("status bar")
     	
        def doStructure(self, canvas) : 
            """ defines a basic layout structure
            to be overwriten by users needing complex structures
            """
            mallaV = wx.BoxSizer(wx.VERTICAL)
##            mallaH = wx.BoxSizer(wx.HORIZONTAL)
##
##            mallaV.Add(mallaH, 0, wx.EXPAND, 4)
##            mallaV.Add(canvas, proportion=0, flag=wx.GROW|wx.ALL, border=0)
            mallaV.Add(canvas, 0, wx.EXPAND | wx.ADJUST_MINSIZE, 0)

            self.SetAutoLayout(True)
            self.SetSizer(mallaV) 
            mallaV.Fit(self) #
            mallaV.SetSizeHints(self) #
            self.Layout()
            self.Centre()

        def doFrame(self, canvas) :
            """called from wxWindow in main. Construct here the menus, status bars ...
            """
##            self.doMenu()
            #self.doStatusBar()
            self.doStructure(canvas)



            

    class FpsTimer(wx.Timer) :
        """ instanciated in main.py 
        """
        def __init__(self, fps, f) :
            wx.Timer.__init__(self)
            self.Start(1000./fps)
            self.f = f # function to call on notify

        def Notify(self) : self.f()




except ImportError:
    class wxMirraFrame: pass # void class otherwise frame might not defined and there is an error



