from mirra.graphics import *
from mirra import utilities



class StatusBar(Rect) :
    
    def start(self) :
        self.text = 'status bar'

    def render(self) : 
        # compile this to a list some day
        #Rect.render(self) 
        #engine.drawLine((self.rect.left, self.rect.top), (self.rect.right, self.rect.top), self.z,
         #               color=(0.2,0.2,0.2, 1))
        
        engine.drawText(self.text, 10, self.y, self.z)

        
class Label(Text) :
    """ text box with background color and outline
    """
    def __init__(self,st, x, y, z, font='typewriter', size=13, textcolor=(0,0,0), bgtransparent=0,
                 bgcolor=(1,1,1), borderstroke=0, bordercolor=(0,0,0)) :
        Text.__init__(self,st,x,y,z,font,size,textcolor)
        self.bgtransparent = bgtransparent
        self.bgcolor = bgcolor
        self.borderstroke = borderstroke
        self.bordercolor = bordercolor
        self.updateBox()

    def getText(self) : return seld.__text
    def setText(self, st) :
        self.__text = text
        self.updateBox()
    text = property(getText, setText)

    def updateBox(self) :
        self.width = len(self.text)*5.2 # 4 px per character
        self.height = self.size

##    def render(self,e) :
##        boxx = self.x + self.width/2
##        boxy = self.y - self.height/2
##        if not self.bgtransparent :
##            e.drawRect(boxx, boxy, self.z, self.width, self.height, self.bgcolor)
##        if self.borderstroke > 0 :
##            e.drawRect(boxx, boxy, self.z, self.width, self.height, self.bordercolor, self.borderstroke)
##        Text.render(self, e)



class Selection(Polygon) :
    """ recibes objects that can be selected
    """
    def __init__(self, objectsArray) :
        Polygon.__init__(self, [(0,0),(0,0),(0,0),(0,0)], 999, color=(0,0,0,0.4))#, stroke=1)
        self.objectsArray = objectsArray
        Selectable.selection = self # tell their class about me
##        self.objectsArray[0].setSelectionObj(self) # tell their class about me
##        self.objectsArray[0].__class__.selection = self # tell their class about me
        self.selected = [] # to store current selection
        self.startP = 0,0
        self.visible = 0
        self.bgcolor = 0,0,0,0.6

    def select(self, x,y) :
        for o in self.selected:
            o.doDeselect() # unmark as selected
        self.selected = [] # prepare
        self.startP = x,y
        self.visible = 1

    def stop(self) :
        self.visible = 0
        self.doSelection() # calculate wich objects are intersected by me
        self.v = [] # reset to avoid flashings

    def step(self) :
        Polygon.step(self)
        if self.visible:
            x,y = self.getMouseLoc()    #current mouseloc
            self.v = [self.startP, (x, self.startP[1]), (x,y), (self.startP[0], y)]
##            a = self.startP     #topleft
##            b = x, self.startP[1]   #topright
##            c = x,y     #bottomright
##            d = self.startP[0], y   #bottomleft
##            self.v = [a, b, c, d]   #update

    def render(self) : #,e) :
        if self.visible : # dont draw if non visible
            # super(Selection, self).render(z,e)
##            Polygon.render(self, z, e)
##            e.drawVertex(self.x, self.y, z, self.v2, self.bgcolor, stroke=1) # marquee
            engine.drawPolygon(self.v, self.z, self.color) # marquee
            engine.drawPolygon(self.v, self.z, self.bgcolor, stroke=1) # marquee

    def doSelection(self) :
        self.selected = []
        rect = utilities.calcPolygonRect(self.v)
        for o in self.objectsArray: # first find all selected ones
            if utilities.pointInRect(o.getLoc(), rect) : # if loc inside selection rect
                self.selected.append(o) # store
                o.doSelect()
##        self.selected = [self.selected.append(o) o.doSelect() for o in self.objectsArray if utilities.pointInRect(o.getLoc(), rect)]





##
class Selectable:
    """ mixin with methods and props for being selected by Selection object
    """
    selection = 0 # selection object

##    def setSelectionObj(inst) :
##        if not Selectable.selection:
##            Selectable.selection = inst
##    setSelectionObj = staticmethod(setSelectionObj)

    def __init__(self) :
        self.offsetList = []

    def doSelect(self) : pass
    def doDeselect(self) : pass

    def prepareMultipleDrag(self, x,y) : # on mouseudown
         if len(Selectable.selection.selected) > 1 : # multiple drag
            for o in Selectable.selection.selected:
                if o != self: # not me
                    x,y = o.getLoc()
                    p = x - self.x, y - self.y # calc this offset
                    self.offsetList.append(p)

    def endMultipleDrag(self, x,y) : # on mouseup
        self.offsetList = []

    def multipleDrag(self,x,y) : # on drag
        if len(Selectable.selection.selected) > 1 and self.clicked : # multimple drag if i am the one dragged
            i = 0 # it doesnt work with enumerate() maybe because of the if o!=self
            for o in Selectable.selection.selected :
                if o != self :# not me
                    o.drag(self.x + self.offsetList[i][0], self.y + self.offsetList[i][1])
                    i+=1



class SRect(Rect, Selectable) :
    def __init__(self, x=10, y=10, z=0, width=10, height=10, color=(0,0,0,1), stroke=0,
                 rotation=0.0) :
        Rect.__init__(self, x, y, z, width, height, color, stroke, rotation)
        Selectable.__init__(self) # required

    def mouseUp(self, x,y) :
        Rect.mouseUp(self, x,y)
        Selectable.endMultipleDrag(self, x,y)
        if SRect.selection.visible:
            SRect.selection.stop() # this tries to stop selection object when mouseUp on me !!!
            
    def mouseDown(self, x,y) :
        Rect.mouseDown(self, x,y)
        Selectable.prepareMultipleDrag(self, x,y)

    def drag(self, x,y) :
        Rect.drag(self, x,y)
        Selectable.multipleDrag(self, x,y)



class SPolygon(Polygon, Selectable) :
    def __init__(self, v=[], z=0, color=(0,0,0,1), stroke=0, rotation=0.0) :
        Polygon.__init__(self, v, z, color, stroke, rotation)
        Selectable.__init__(self) # required

    def mouseUp(self, x,y) :
        Polygon.mouseUp(self, x,y)
        Selectable.endMultipleDrag(self, x,y)
        if SPolygon.selection.visible:
            SPolygon.selection.stop() # this tries to stop selection object when mouseUp on me !!!

    def mouseDown(self, x,y) :
        Polygon.mouseDown(self, x,y)
        Selectable.prepareMultipleDrag(self, x,y)

    def drag(self, x,y) :
        Polygon.drag(self, x,y)
        Selectable.multipleDrag(self, x,y)



class SCircle(Circle, Selectable) :
    def __init__(self, x=10, y=10, z=0, width=10, color=(0,0,0,1), stroke=0, rotation=0.0) :#,
        Circle.__init__(self, x,y, z, width, color, stroke, rotation)
        Selectable.__init__(self) # required

    def mouseUp(self, x,y) :
        Circle.mouseUp(self, x,y)
        Selectable.endMultipleDrag(self, x,y)
        if SCircle.selection.visible:
            SCircle.selection.stop() # this tries to stop selection object when mouseUp on me !!! 

    def mouseDown(self, x,y) :
        Circle.mouseDown(self, x,y)
        Selectable.prepareMultipleDrag(self, x,y)

    def drag(self, x,y) :
        Circle.drag(self, x,y)
        Selectable.multipleDrag(self, x,y)



##class SBitmap(Bitmap, Selectable) :
##    def __init__(self, file='', x=10, y=10, z=0, width=10, height=10, rotation=0.0) :
##        Bitmap.__init__(self, file, x, y, z, width, height, rotation)
##        Selectable.__init__(self) # required
##
##    def mouseUp(self, x,y) :
##        Bitmap.mouseUp(self, x,y)
##        Selectable.endMultipleDrag(self, x,y)
##        if SBitmap.selection.visible:
##            SBitmap.selection.stop() # this tries to stop selection object when mouseUp on me !!! 
##
##    def mouseDown(self, x,y) :
##        Bitmap.mouseDown(self, x,y)
##        Selectable.prepareMultipleDrag(self, x,y)
##
##    def drag(self, x,y) :
##        Bitmap.drag(self, x,y)
##        Selectable.multipleDrag(self, x,y)
##
##
##
##class SBitmapPolygon(BitmapPolygon, Selectable) :
##    def __init__(self, file='', v=[], z=0, rotation=0.0) :
##        BitmapPolygon.__init__(self, file, v, z, rotation)
##        Selectable.__init__(self) # required
##
##    def mouseUp(self, x,y) :
##        BitmapPolygon.mouseUp(self, x,y)
##        Selectable.endMultipleDrag(self, x,y)
##        if SBitmapPolygon.selection.visible :
##            SBitmapPolygon.selection.stop() # this tries to stop selection object when mouseUp on me !!!
##            
##    def mouseDown(self, x,y) :
##        BitmapPolygon.mouseDown(self, x,y)
##        Selectable.prepareMultipleDrag(self, x,y)
##
##    def drag(self, x,y) :
##        BitmapPolygon.drag(self, x,y)
##        Selectable.multipleDrag(self, x,y)









