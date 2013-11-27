""" graphics module of Mirra. www.ixi-software.net
"""
import sys, os

try :
##    from OpenGL.GLUT import *
    from OpenGL.GLU import *
##    from OpenGL.GL import *
except ImportError:
    import_error = 'pyOpenGL'
    print '*'*10
    print 'Mirra > graphics.py : ImportError, could not import %s . It must be installed in your system to run Mirra' % (import_error)
    print '*'*10
    import sys
    sys.exit() # quit


from utilities import * # collision detection, etc...

import engine 






# basic drawing classes below

class Base(object):
    """ Implements the basic funtions for objects to be rendered. ALL renderable objects should inherit from it.
        Adds its instances to graphicsStack on __init__ automagically for rendering.
    """
    def __init__(self, x, y, z=0, color=(0,0,0,1), stroke=0, rotation=0):
        """ receives the z loc needed to add itself in the right position on the graphicsStack
        """
        try :
            self.rect
        except AttributeError:
            self.rect = RectUtils(x,y,1,1) # this inits x,y and loc as well

        self.z = z # setting it. >>> THIS AUTOMATICALLY ADDS THE INSTACNCE TO THE RENDERING STACK <<<
        self.rotation = rotation
        self.stroke = stroke
        self.color = color
        self.blend = self.color[3] #alpha
        self.interactiveState = 0 # 0: no interactive, 1: clickable, 2: draggable
        self.texID = None
        self.texCoord = [(0, 1), (1, 1), (1, 0), (0, 0)] #[(0, 1), (1, 1), (1, 0), (0, 0)]
        self.clicked = 0
        self.mouseoffset = 0,0 # it is a tuple representing a point
        self.constrainRect = 0,0,0,0 # None
        
        self.start() #  before subclasses __init__!

    def start(self):
        """ just after self.__init__, but before subclasses __init__
        """
        pass

    def getMouseLoc(self):
        """ returns mouse location via top's window. --> x,y tuple
        """
        return Base.app.mouseLoc
    mouseloc = property(getMouseLoc)

    def getZ(self): return self.__z
    def setZ(self, z):
        """ sets instance's z depth buffer position
        >>> AND THE INSTANCE TO THE STACK ON THE RIGHT POSITION, if NOT there already <<<
        """
        self.__z = z # and now update prop
        engine.newZ(z, self) # oldz, newz, and reference to instance
    z = property(getZ, setZ)

    def getColor(self): return self.__color
    def setColor(self, c):
        """ sets the color of shape (alpha is default to 1) --> 3 or 4 floats between 0 and 1. 4th is alpha and it is optional
        """
        if len(c) == 3 : c = c[0],c[1],c[2], 1 # alpha was not set, so default to 1
        self.__color = c
    color = property(getColor, setColor)

    def getBlend(self): return self.color[3] #self.__blend
    def setBlend(self, f):
        """ sets alpha component of self.color --> float between 0 to 1 value
        """
        self.color = self.color[0], self.color[1], self.color[2], f # << update alpha factor
    blend = property(getBlend, setBlend)
    
## rect and pos related properties, they all interface to rect property (instance of utilities.Rect)
    def setLoc(self, p) : self.rect.loc = p 
    def getLoc(self) : return self.rect.loc 
    def setX(self, x) : self.rect.x = x 
    def getX(self) : return self.rect.x 
    def setY(self, y) : self.rect.y = y 
    def getY(self) : return self.rect.y 
    x = property(getX, setX)
    y = property(getY, setY)
    loc = property(getLoc, setLoc)

    def setWidth(self,w) : self.rect.width = w
    def getWidth(self) : return self.rect.width
    def setHeight(self, h) : self.rect.height = h
    def getHeight(self) : return self.rect.height
    width = property(getWidth, setWidth)
    height = property(getHeight, setHeight)
    
    def getWidth2(self) : return self.rect.width*0.5
    def getHeight2(self) : return self.rect.height *0.5
    width2 = property(getWidth2)
    height2 = property(getHeight2)

##    left,top,right,bottom, quad 
    def setLeft(self, x): self.rect.left = x
    def getLeft(self) : return self.rect.left
    def setTop(self, y): self.rect.top= y
    def getTop(self) : return self.rect.top
    def setRight(self, x): self.rect.right = x
    def getRight(self) : return self.rect.right
    def setBottom(self, y): self.rect.bottom = y
    def getBottom(self) : return self.rect.bottom
    def setQuad(self, q): self.rect.quad = q
    def getQuad(self) : return self.rect.quad
    left = property(getLeft, setLeft)
    top = property(getTop, setTop)
    right = property(getRight, setRight)
    bottom = property(getBottom, setBottom)
    quad = property(getQuad, setQuad)
    ##############################

    def setImage(self, name): #, texCoord=[(0, 0), (1, 0), (1, 1), (0, 1)]):
        """ sets shape's texture
        """
        self.texID = engine.loadTexture(name) # class method

    def tile(self, n):
        """ sets the bitmap to be tiled an N number of times in the shape's surface
        """
        if self.texID : # is not None: # only textured shapes
            if n < 1 :  n = 1
            for i, v in enumerate(self.texCoord):
                a,b = 0,0
                if v[0] !=  0 : a = n
                if v[1] !=  0 : b = n
                self.texCoord[i] = a,b

    def render(self) : #, engine):
        """ render's the instance using engines's drawing functions. Defined for each different shape.
            This function is automaticly called by the Engine instance. 
            NOTE: render() can be extended by adding extra drawing functions (for example to define a Rect that has
            a diagonal stripe). But when you call draw functions directly from render() you must pass
            a color with an alpha chanel ON, even if it is just 1. This is due to the way OpenGL renders alphas
        """
        pass
    
    def step(self):
        """ called every frame (fps) by the Engine's instance
        """
        pass

    def intersects(self, x,y) :
        """ returns if instance is intersecting the point. Used to check if mouse is clicking it by Engine. --> x,y pixels
            Implemented by each subclass of Base
        """
##        print self,s elf.color, glReadPixelsf(x,y,1,1,GL_RGBA)[0][0]
##        if self.color == glReadPixelsf(x,y,1,1,GL_RGBA)[0][0] : return False
        return False # the classes that dont overwrite this will never be intersected by the mouse

    def end(self): # end !!
        """ kills object and removes it from rendering stack
        """
        engine.remove(self)
##        self.__del__() : self = 0

    # mouse events
    def rightMouseDown(self, x,y) : self.clicked = 1
    def rightMouseUp(self, x,y) :   self.clicked = 0

    def mouseDown(self, x,y) :
        self.clicked = 1
        if self.interactiveState > 1 :
            self.mouseoffset = self.x - x, self.y - y # h, v, to drag

    def mouseUp(self, x,y) :
        self.clicked = 0
        if self.interactiveState > 1 :
            self.mouseoffset = 0,0

    #def mouseUpOutside(self, x,y):
    #       self.clicked = 0
    #       if self.interactiveState > 1 :
    #               self.mouseoffset = []

    def mouseDragged(self, x,y) :
        if self.clicked and self.interactiveState == 2 :
            self.drag(x,y)

    def drag(self, x,y) :
        if self.constrainRect == (0,0,0,0) : # is free
            self.loc = x + self.mouseoffset[0], y + self.mouseoffset[1]
        else: #contrains the dragged object within the given rect
            self.loc = constrainToRect(x + self.mouseoffset[0], y + self.mouseoffset[1], self.constrainRect)






# non intersect/texture basic Primitives (non draggable)

class Text(Base) :
    def __init__(self, text, x=0, y=0, z=0, font='typewriter', size=13, color=(0,0,0,1)):
        """ draws a text at a given x,y,z position and color.
            Text("hello world", 10, 100, 1, 'helvetica', 10, (0.1, 1, 0.3, 0.8))
            available font and sizes are:
            typewriter 13 and 15
            timesroman 10 and 24
            helvetica 10,12 and 18
        """
        Base.__init__(self, x,y,z,color)
        self.text = text
        self.font = font
        self.size = size

    def render(self): #, engine):
        engine.drawText(self.text, self.x, self.y, self.z, self.font, self.size, self.color)


class Pixel(Base):
    """ draws a pixel at a given x,y,z position and color.
        Pixel(x=12, y=100, z=900, color=(1,0,0,0.5))
    """
    def render(self) : #, engine):
        engine.drawPixel(self.x, self.y, self.z, self.color)

    def intersects(self, x,y):
        if x==self.x and y==self.y : return True


##
class LineRel(Base):
    def __init__(self, x,y, a=(0,0), b=(0,0), z=0, color=(0,0,0,1), stroke=0, rotation=0.0, style=0):
        """ Draws a basic line given the begining and end point (tuples), color (tuple) and stroke
            (thickness of line)
            Line( x,y, a=(1,1), b=(100,100), z=0, color=(0.2,0,0,1), stroke=10, rotation=45)
        """
        w = (b[0] - a[0]) 
        h = (b[1] - a[1]) 
        x = abs(a[0] + w*0.5)
        y = abs(a[1] + h*0.5)
        self.a2 = abs(a[0]) - x, abs(a[1]) - y
        self.b2 = abs(b[0]) - x, abs(b[1]) - y
        self.a = x - w*0.5, y - w*0.5
        self.b = x + w*0.5, y + w*0.5
        self.rect = RectUtils(x, y, w, h)
        self.style = style
        Base.__init__(self, x, y, z,color,stroke,rotation)

    def render(self) : #, engine):
        engine.drawLineRel(self.rect.x,self.rect.y, self.a2, self.b2, self.z, self.color, self.stroke,
                           self.rotation, self.style)

    def updateAB(self):
        self.a = self.x + self.a[0], self.y + self.a[0]
        self.b = self.x + self.b[0], self.y + self.b[0]

    def setLoc(self, p):
        self.rect.loc = p ; self.updateAB()
    def setX(self, x):
        self.rect.x = x ; self.updateAB()
    def setY(self, y):
        self.rect.y = y; self.updateAB()
    x = property(Base.getX, setX)
    y = property(Base.getY, setY)
    loc = property(Base.getLoc, setLoc)


class Line(LineRel):
    def __init__(self, a=(0,0), b=(0,0), z=0, color=(0,0,0,1), stroke=0, rotation=0.0, style=0):
        """ Draws a basic line given the begining and end point (tuples), color (tuple) and stroke
            (thickness of line)
            Line( a=(1,1), b=(100,100), z=20, color=(0.2,0,0,1), stroke=10, rotation=45)
        """
        w = (b[0] - a[0]) 
        h = (b[1] - a[1]) 
        x = abs(a[0] + w*0.5) # abs x,y
        y = abs(a[1] + h*0.5)
        a = x-w*0.5, y-h*0.5 # relative a,b
        b = x+w*0.5, y+h*0.5
        LineRel.__init__(self, x, y, a, b, z, color, stroke, rotation, style)

        

# intersectable shapes (draggable)

class Polygon(Base):
    def __init__(self, v, z=0, color=(0,0,0,1), stroke=0, rotation=0.0, style=0):
##    def __init__(self, x, y, z=0, v=[], color=(0,0,0,1), stroke=0, rotation=0.0, style=0):
        """ polygon class
            Polygon(vertexarray=[(0, 0), (29, 100), (30, 200)], z=100, color=(0,0.3,0.1,1), stroke=0, rotation=23)
            overwrites few methods from superclass as polygons are more complex, needs to update everyvertex.
            Defines polygon intersection. This is tricky as when the object is rotated the position is actually
            different from the points in self.v they are actually self.v + rotation so i have to take this
            into account when checking for intersection
        """
        self.v = v
        l, t, r, b = calcPolygonRect(v) # get the bounding rect
        self.rect = RectUtils(l+(r-l)*0.5, t+(b-t)*0.5, r-l, b-t)
        self.v2 = [(i[0] - self.rect.x, i[1] - self.rect.y) for i in v] #relative polygon

        self.style = style
        
        Base.__init__(self, self.rect.x, self.rect.y, z,color,stroke,rotation)


    def updateV(self):
        self.v = [(self.rect.x + n[0], self.rect.y + n[1]) for n in self.v2]

    def setLoc(self, p) :
        self.rect.loc = p
        self.updateV()
    def setX(self, x) :
        self.rect.x = x
        self.updateV()
    def setY(self, y) :
        self.rect.y = y
        self.updateV()
    x = property(Base.getX, setX)
    y = property(Base.getY, setY)
    loc = property(Base.getLoc, setLoc)
    
    def render(self) : #, engine):
        engine.drawVertex(self.rect.x, self.rect.y, self.z, self.v2, self.color,  self.stroke, self.rotation,
                           self.style)

    def intersects(self, x, y) :
        """ calcs actual vertex if polygon is rotated and checks for intersection.
        Rotations are performaed by opengl so if you create a polygon and rotate it the vertex list is not
        updated to the place they are after the rotation. This is why we need to calc temporarily the real
        position were they are drawn to check for intersection. It doesnt sound very good but updating the
        vertex position after rotation is performed causes some funny problems.
        """
        if self.rotation != 0 :
            self.updateV()
            return pointInPoly( (x,y), [ rotPoint(n, self.rect.loc, getAng(n, self.rect.loc) + self.rotation)
                                        for n in self.v[:] ]
                                ) # calc intersect with rotated vertexes
        else:
            return pointInPoly((x,y), self.v) # it was not rotated. easy





class Rect(Base) :
    """ defines base for rect object. render(), intersection and properties
        Rect(x=10, y=100, z=1, width=40, height=60, color=(0.5,0.5,0.5,1), stroke=0, rotation=90)
    """
    def __init__(self, x=0, y=0, z=0, width=10, height=10, color=(0,0,0,1), stroke=0, rotation=0.0, style =0): 
        self.rect = RectUtils(x, y, width, height)
        Base.__init__(self, x,y,z,color,stroke,rotation)
        self.updateV()
        self.style = style

    def updateV(self):
        v = [self.rect.quad[0], self.rect.quad[1], self.rect.quad[2], self.rect.quad[3]] #calcRectQuad(x, y, width, height)
        self.v2 = [(i[0] - self.x, i[1] - self.y) for i in v] # vertex list relative to x,y

    def setWidth(self, w):
        self.rect.width = w
        self.updateV()  
    width = property(Base.getWidth, setWidth)

    def setHeight(self, h):
        self.rect.height = h
        self.updateV()
    height = property(Base.getHeight, setHeight)

    def render(self) : #, engine):
        self.updateV()
        engine.drawVertex(self.rect.x, self.rect.y, self.z, self.v2, self.color, self.stroke, self.rotation,
                           self.style)

    def intersects(self, x,y):
        if self.rotation != 0 : # calcs actual vertex if polygon is rotated
            self.updateV()
            return pointInPoly( (x,y), [ rotPoint(n, self.rect.loc, getAng(n, self.rect.loc) + self.rotation)
                                        for n in self.rect.quad[:] ]
                                 ) # calc intersect with rotated vertexes
        else:
            return pointInRect((x,y), self.rect.rect)


class Circle(Base) :
    """ Circle class
        Circle(x=20, y=100, z=1, width=300, color=(1,1,0,0.3), stroke=5, rotation=0, style=GLU_FILL)
        style choices are : GLU_LINE, GLU_FILL, GLU_SILHOUETTE, GLU_POINT
    """
    def __init__(self, x=10, y=10, z=0, width=2, color=(0,0,0,1), stroke=0, rotation=0.0, style=GLU_FILL):
        self.radius = width*0.5
        self.rect = RectUtils(x, y, width, width)
        self.style = style
        Base.__init__(self, x,y,z,color, stroke, rotation)
        
    def setWidth(self, w):
        self.radius = w*0.5
        self.rect.width = w
    width = property(Base.getWidth, setWidth)
        
    def render(self) :#, engine):
        engine.drawCircle(self.rect.x, self.rect.y, self.z, self.radius, self.color, self.stroke,
                          self.rotation, self.texID, self.texCoord, self.style)

    def intersects(self, x,y):
        return pointInCircle((x,y), self.rect.loc, self.radius)


    
class Arc(Base) :
    """ Arc class
        Arc(x=10, y=10, z=0, radius=1, start=0, sweep=1, color=(0,0,0,1), stroke=0, rotation=0.0, style=GLU_FILL)
        style choices are : GLU_LINE, GLU_FILL, GLU_SILHOUETTE, GLU_POINT
    """
    def __init__(self, x=10, y=10, z=0, radius=1, start=0, sweep=1, color=(0,0,0,1), stroke=0,
                 rotation=0.0, style=GLU_FILL):
##        self.rect = RectUtils(x, y, width, width)
        Base.__init__(self, x,y,z,color, stroke, rotation)
        self.radius = radius
        self.start = start
        self.sweep = sweep
        self.style = style
        
    def render(self) : #, engine):
        engine.drawArc(self.rect.x, self.rect.y, self.z, self.radius, self.start, self.sweep, self.color,
                       self.stroke, self.rotation, self.texID, self.texCoord, self.style)

    def intersects(self, x,y):
        return pointInCircle((x,y), self.rect.loc, self.radius)



##class Ellipse(Base) :
##    """ Circle class
##        Circle(x=20, y=100, z=1, width=300, color=(1,1,0,0.3), stroke=5, rotation=0, style=GLU_FILL)
##        style choices are : GLU_LINE, GLU_FILL, GLU_SILHOUETTE, GLU_POINT
##    """
##    def __init__(self, x=10, y=10, z=0, width=2, height=2, color=(0,0,0,1), stroke=0, rotation=0.0, style=GLU_FILL):
##        self.rect = RectUtils(x, y, width, width)
##        self.style = style
##        Base.__init__(self, x,y,z,color, stroke, rotation)
##        print 'ellipse'
##        
####    def setWidth(self, w):
####        self.radius = w*0.5
####        self.rect.width = w
####    width = property(Base.getWidth, setWidth)
##        
##    def render(self, engine):
##        engine.drawEllipse(self.rect.x, self.rect.y, self.z, self.width, self.height, self.color, self.stroke,
##                          self.rotation, self.texID, self.texCoord, self.style)
##
##    def intersects(self, x,y):
##        return pointInCircle((x,y), self.rect.loc, self.radius)



# textured classes

class Bitmap(Rect):
    """ Bitmap with Rect shape
    It doesnt use Color nor Fill properties
    example: Bitmap('ixi.bmp', 100, 100, 1, 50, 50, 45)
    """
    def __init__(self, file, x=0, y=0, z=0, width=10, height=10, rotation=0.0) : 
        Rect.__init__(self, x, y, z, width, height, (0,0,0,1), 0, rotation)
        self.setImage(file)

    def flipV(self):
        """ flips vertically the image (not the shape)
        """
        # --> self.texCoord=[(0, 0), (1, 0), (1, 1), (0, 1)]
        #self.texCoord.reverse() # there was an error
        a = self.texCoord[0]
        b = self.texCoord[1]
        c = self.texCoord[2]
        d = self.texCoord[3]
        self.texCoord = [d, c, b, a]

    def flipH(self):
        """ flips horizonallly the image (not the shape)
        """
        # --> texCoord=[(1, 1), (0, 1), (0, 0), (1, 0)]
        a = self.texCoord[0]
        b = self.texCoord[1]
        c = self.texCoord[2]
        d = self.texCoord[3]
        self.texCoord = [b, a, d, c]

    def end(self):
        #Engine.deleteTexture(self.texID)
        engine.deleteTexture(self.texID)

    def render(self) : #, e):
        self.updateV()
        engine.drawTexturedVertex(self.rect.x, self.rect.y, self.z, self.v2, self.rotation,
                          self.texID, self.texCoord)
        



class BitmapPolygon(Polygon):
    """ Bitmap with Polygon shape
    It doesnt use Color nor Fill properties
    example : BitmapPolygon('ixi.bmp', [(0,0), (100,10), (150, 200), (0, 300)], 1, 45)
    """
    def __init__(self, file, vertexarray=[], z=0, rotation=0.0 ) : 
        Polygon.__init__(self, vertexarray, z, (0,0,0,1), 0, rotation)
        self.setImage(file)

    def end(self):
        #Engine.deleteTexture(self.texID)
        engine.deleteTexture(self.texID)

    def render(self) : #, e):
        self.updateV()
        engine.drawTexturedVertex(self.rect.x, self.rect.y, self.z, self.v2, self.rotation,
                          self.texID, self.texCoord)

