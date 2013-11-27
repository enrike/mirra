from mirra.graphics import *
from mirra import utilities



class StatusBar(Rect) :
    
    def start(self) :
        self.text = 'status bar'

    def render(self) : #,e) :
        Rect.render(self) #, e)
        engine.drawLine((self.rect.left, self.rect.top), (self.rect.right, self.rect.top), self.z, color=(0.2,0.2,0.2, 1))
        
        engine.drawText(self.text, 10, self.y, self.z)

        
class Label(Text) :
    """ text box with background color and outline
    """
    def __init__(self,st, x, y, z, font='typewriter', size=13, textcolor=(0,0,0), bgtransparent=0, bgcolor=(1,1,1),
                 borderstroke=0, bordercolor=(0,0,0)) :
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
    def __init__(self, x=10, y=10, z=0, width=10, height=10, color=(0,0,0,1), stroke=0, rotation=0.0) :
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



class SBitmap(Bitmap, Selectable) :
    def __init__(self, file='', x=10, y=10, z=0, width=10, height=10, rotation=0.0) :
        Bitmap.__init__(self, file, x, y, z, width, height, rotation)
        Selectable.__init__(self) # required

    def mouseUp(self, x,y) :
        Bitmap.mouseUp(self, x,y)
        Selectable.endMultipleDrag(self, x,y)
        if SBitmap.selection.visible:
            SBitmap.selection.stop() # this tries to stop selection object when mouseUp on me !!! 

    def mouseDown(self, x,y) :
        Bitmap.mouseDown(self, x,y)
        Selectable.prepareMultipleDrag(self, x,y)

    def drag(self, x,y) :
        Bitmap.drag(self, x,y)
        Selectable.multipleDrag(self, x,y)



class SBitmapPolygon(BitmapPolygon, Selectable) :
    def __init__(self, file='', v=[], z=0, rotation=0.0) :
        BitmapPolygon.__init__(self, file, v, z, rotation)
        Selectable.__init__(self) # required

    def mouseUp(self, x,y) :
        BitmapPolygon.mouseUp(self, x,y)
        Selectable.endMultipleDrag(self, x,y)
        if SBitmapPolygon.selection.visible :
            SBitmapPolygon.selection.stop() # this tries to stop selection object when mouseUp on me !!!
            
    def mouseDown(self, x,y) :
        BitmapPolygon.mouseDown(self, x,y)
        Selectable.prepareMultipleDrag(self, x,y)

    def drag(self, x,y) :
        BitmapPolygon.drag(self, x,y)
        Selectable.multipleDrag(self, x,y)



############### panels #################
##
##
##import wx
##import sc
##
##
##
### PANELS #
##
##    
##class MirraWxPanel(wx.Frame) :
##    """ general panel
##    """
##    def __init__(self, *args, **kwds) :
##        kwds["style"] = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.MAXIMIZE_BOX|wx.STAY_ON_TOP|wx.SYSTEM_MENU|wx.RESIZE_BORDER|wx.CLIP_CHILDREN
##        wx.Frame.__init__(self, *args, **kwds)
##        self.doWidgets()
##
##    def doWidgets(self) : pass
##    def setProperties(self, a) : self.app = a
##
##
##
##class SCWxPanel(MirraWxPanel) :
##    """ panel that wraps a SuperCollider synthdef with sc.py module
##    """
##    def __init__(self, *args, **kwds) :
##        self.initValues() ## first
##        kwds["style"] = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.MAXIMIZE_BOX|wx.STAY_ON_TOP|wx.SYSTEM_MENU|wx.RESIZE_BORDER|wx.CLIP_CHILDREN
##        MirraWxPanel.__init__(self, *args, **kwds)
##        self.synth = 0
##        self.addaction = 1
##        self.tgt = 0
##        self.inbus = 4
##        self.outbus = 0
##        
##    def initWidgets(self) : pass
##        
##    def loadSynthDef(self, *args, **kwds) :
##        self.synth = sc.Synth( *args, **kwd )
##
##
##
##
##
##class Panel_Effect(SCWxPanel) :
##    """ general effect panel with no sliders
##    """
##    def doSliders(self, row) : return row
##    
##    def doWidgets(self) :           
##        choices = []
##        for bufIndex in xrange(52) :
##            if bufIndex % 2 == 1 : 
##                bnum = "%i, %i" % ( last, bufIndex ) # creates pair of nums : 0,1 - 2,3 - 4,5
##                choices.append(bnum)
##            last = bufIndex # remember for next time
##        
##        menusize = (90, 25)
##        slidersize = (210, 40)
##        textctrlsize = (45, 20)
##        row = 8
##        column1 = 10
##        column2 = 70
##        column3 = 285
##
##        slidergap = 25
##        if sys.platform == 'darwin' :
##            firstslider = slidergap + 15 ## first slider
##        else :
##            firstslider = slidergap + 5 ## first slider
##
####        wx.EVT_CLOSE_WINDOW
##        # inbus
##        self.inlist_label = wx.StaticText( self, -1, "in", pos=(column1, row) )
##        self.inlist = wx.Choice(self, -1, pos=(30, 5), size=menusize, choices=choices )
##        self.Bind(wx.EVT_CHOICE, self.inlistevent, self.inlist)
##        # outbus
##        self.outlist_label = wx.StaticText( self, -1, "out", pos=(130, row) )
##        self.outlist = wx.Choice(self, -1, pos=(160, 5), size=menusize, choices=choices )
##        self.Bind(wx.EVT_CHOICE, self.outlistevent, self.outlist)
##        # ON/OFF button
##        self.toggle_button = wx.ToggleButton(self, -1, "On", pos=(275, 5),  size=(55,25) )
##        self.Bind( wx.EVT_TOGGLEBUTTON, self.toggleevent, self.toggle_button)
##
##        row = self.doSliders(row, column1, column2, column3, slidersize, textctrlsize, firstslider, slidergap)
##        
##        # bottom
##        row += 25 ## last row
##        self.nodeID_label = wx.StaticText( self, -1, "nodeID", pos=(column1, row) )
##        self.nodeID = wx.StaticText( self, -1, 'none', pos=(70, row) )
##
##    # events #
##    def inlistevent(self, e) :
##        self.inbus = self.inlist.GetSelection () * 2 #  to get even numbers
####        print self.inbus, 'inbus from panel'
##        if self.toggle_button.GetValue() : self.synth.inbus = self.inlist.GetSelection () * 2
##        e.Skip()
##
##    def outlistevent(self, e) :
##        self.outbus = self.outlist.GetSelection () * 2 #  to get even numbers
##        if self.toggle_button.GetValue() : self.synth.outbus = self.outlist.GetSelection () * 2
##        e.Skip()
##
##    def toggleevent(self, e) :
##        if self.toggle_button.GetValue() :
##            self.loadSynthDef() # start synth
##            self.toggle_button.SetBackgroundColour( (255,0,0) )
##        else :
##            self.synth.free() # kill synth
##            self.toggle_button.SetBackgroundColour( (210,210,210) )
##        self.synth.toggle = self.toggle_button.GetValue()
##        e.Skip()
##
##    def close(self, e) :
##        self.synth.free() # kill synth
##        e.Skip()



































# --------------------------------------------------------------------------- #
# FLOATSPIN Control wxPython IMPLEMENTATION
# Python Code By:
#
# Andrea Gavana, @ 16 Nov 2005
# Latest Revision: 16 Nov 2005, 21.50 CET
#
#
# TODO List/Caveats
#
# 1. Ay Idea?
#
# For All Kind Of Problems, Requests Of Enhancements And Bug Reports, Please
# Write To Me At:
#
# andrea.gavana@agip.it
# andrea_gavan@tin.it
#
# Or, Obviously, To The wxPython Mailing List!!!
#
#
# End Of Comments
# --------------------------------------------------------------------------- #


"""
Description:

FloatSpin Implements A Floating Point SpinCtrl. It Is Built Using A Custom
wx.PyControl, Composed By A wx.TextCtrl And A wx.SpinButton. In Order To
Correctly Handle Floating Points Numbers Without Rounding Errors Or Non-Exact
Floating Point Representations, FloatSpin Uses The Great FixedPoint Class
From Tim Peters.

What You Can Do:

- Set The Number Of Representative Digits For Your Floating Point Numbers;
- Set The Floating Point Format (%f, %F, %e, %E, %g, %G);
- Set The Increment Of Every EVT_FLOATSPIN Event;
- Set Minimum, Maximum Values For FloatSpin As Well As Its Range;
- Change Font And Colour For The Underline wx.TextCtrl.


Events Catched:

FloatSpin Catched 3 Different Types Of Events:

1) Spin Events: Events Generated By Spinning Up/Down The SpinButton;
2) Char Events: Playing With Up/Down Arrows Of The Keyboard Increase/Decrease
   The Value Of FloatSpin;
3) Mouse Wheel Event: Using The Wheel Will Change The Value Of FloatSpin.

In Addition, There Are Some Other Functionalities:

It Remembers The Initial Value As A Default Value, Call SetToDefaultValue, Or
Press <ESC> To Return To It

Shift + Arrow = 2 * Increment        (Or Shift + Mouse Wheel)
Ctrl  + Arrow = 10 * Increment       (Or Ctrl + Mouse Wheel)
Alt   + Arrow = 100 * Increment       (Or Alt + Mouse Wheel)

Combinations Of Shift, Ctrl, Alt Increment The FloatSpin Value By The Product
Of The Factors;

PgUp & PgDn = 10 * Increment * The Product Of The Shift, Ctrl, Alt Factors;

<SPACE> Sets The Control's Value To It's Last Valid State.


Usage:

FloatSpin Construction Can Be Summarized As Follows:

FloatSpin.__init__(self, parent, id, pos=wx.DefaultPosition,
                   size=wx.DefaultSize, style=0, value=0.0, min=0.0, max=100.0,
                   increment=1.0, digits=-1, extrastyle=FS_LEFT,
                   name="FloatSpin")

Where:

- value: Is The Current Value For FloatSpin;
- min: The Minimum Value;
- max: The Maximum Value;
- increment: The Increment For Every EVT_FLOATSPIN Events;
- digits: Number Of Representative Digits For Your Floating Point Numbers;
- extrastyle: One Of The Following:
  a) FS_LEFT: Align Underline wx.TextCtrl Left;
  b) FS_RIGHT: Align Underline wx.TextCtrl Right;
  c) FS_CENTER: Align Underline wx.TextCtrl Center;
  Plus The Possibility To Use FS_READONLY, That Makes The Underline wx.TextCtrl
  Read-Only (No Edits Possible).

See FloatSpin __init__() Method For The Definition Of Non Standard (Non
wxPython) Parameters.

FloatSpin Control Is Freeware And Distributed Under The wxPython License. 

Latest Revision: Andrea Gavana @ 16 Nov 2005, 21.50 CET

"""


#----------------------------------------------------------------------
# Beginning Of FLOATSPIN wxPython Code
#----------------------------------------------------------------------

import wx

# Set The Styles For The Underline wx.TextCtrl
FS_READONLY = 1
FS_LEFT = 2
FS_CENTRE = 4
FS_RIGHT = 8

# Define The FloatSpin Event
wxEVT_FLOATSPIN = wx.NewEventType()

#-----------------------------------#
#        FloatSpinEvent
#-----------------------------------#

EVT_FLOATSPIN = wx.PyEventBinder(wxEVT_FLOATSPIN, 1)

# ---------------------------------------------------------------------------- #
# Class FloatSpinEvent
# ---------------------------------------------------------------------------- #

class FloatSpinEvent(wx.PyCommandEvent) :
    """ This Event Will Be Sent When A EVT_FLOATSPIN Event Is Mapped In The Parent. """
    
    def __init__(self, eventType, id=1, nSel=-1, nOldSel=-1) :
        """ Default Class Constructor. """
        
        wx.PyCommandEvent.__init__(self, eventType, id)
        self._eventType = eventType


    def SetPosition(self, pos) :
        """ Sets Event Position. """
        
        self._position = pos
        

    def GetPosition(self) :
        """ Returns Event Position. """
        
        return self._position


#----------------------------------------------------------------------------
# FloatTextCtrl
#----------------------------------------------------------------------------


class FloatTextCtrl(wx.TextCtrl) :

    def __init__(self, parent, id=wx.ID_ANY, value="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.TE_NOHIDESEL | wx.TE_PROCESS_ENTER,
                 validator=wx.DefaultValidator,
                 name=wx.TextCtrlNameStr) :
        """
        Default Class Constructor.
        Used Internally. Do Not Call Directly This Class In Your Code!
        """
        
        wx.TextCtrl.__init__(self, parent, id, value, pos, size, style, validator, name)
        
        self._parent = parent
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)
        self.Bind(wx.EVT_CHAR, self.OnChar)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)


    def OnDestroy(self, event) :
        """ Tries To Correctly Handle The Control Destruction Under MSW. """
        
        if self._parent:
            self._parent._textctrl = None
            self._parent = None


    def OnChar(self, event) :
        """ Handles The wx.EVT_CHAR Event By Passing It To FloatSpin. """

        if self._parent:
            self._parent.OnChar(event)


    def OnKillFocus(self, event) :
        """ Synchronize The wx.SpinButton And The wx.TextCtrl When Focus Is Lost. """

        if self._parent:
            self._parent.SyncSpinToText(True)
            
        event.Skip()


#---------------------------------------------------------------------------- #
# FloatSpin
# This Is The Main Class Implementation
# ---------------------------------------------------------------------------- #

class FloatSpin(wx.PyControl) :

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=(95,-1), style=0, value=0.0, min=0.0, max=100.0,
                 increment=1.0, digits=-1, extrastyle=FS_LEFT,
                 name="FloatSpin") :
        """
        Default Class Constructor. Non-Default Parameters Are:
        
        - value: Is The Current Value For FloatSpin;
        - min: The Minimum Value;
        - max: The Maximum Value;
        - increment: The Increment For Every EVT_FLOATSPIN Events;
        - digits: Number Of Representative Digits For Your Floating Point Numbers;
        - extrastyle: One Of The Following:
          a) FS_LEFT: Align Underline wx.TextCtrl Left;
          b) FS_RIGHT: Align Underline wx.TextCtrl Right;
          c) FS_CENTER: Align Underline wx.TextCtrl Center;
          Plus The Possibility To Use FS_READONLY, That Makes The Underline wx.TextCtrl
          Read-Only (No Edits Possible).
          
        """
        
        wx.PyControl.__init__(self, parent, id, pos, size, style|wx.NO_BORDER|
                              wx.NO_FULL_REPAINT_ON_RESIZE | wx.CLIP_CHILDREN,
                              wx.DefaultValidator, name)

        self._min = FixedPoint(str(min), 20)
        self._max = FixedPoint(str(max), 20)
        
        if value < min:
            value = min
        elif value > max:
            value = max
            
        self._value = FixedPoint(str(value), 20)
        self._defaultvalue = self._value
        self._increment = FixedPoint(str(increment), 20)
        self._spinmodifier = FixedPoint(str(1.0), 20)
        self._digits = digits
        self._snapticks = False
        self._spinbutton = None
        self._textctrl = None
        self._spinctrl_bestsize = wx.Size(-999, -999)

        self.SetLabel(name)
        self.SetBackgroundColour(parent.GetBackgroundColour())
        self.SetForegroundColour(parent.GetForegroundColour())

        width = size[0]
        height = size[1]
        best_size = self.DoGetBestSize()
        
        if width == -1:
            width = best_size.GetWidth()
        if height == -1:
            height = best_size.GetHeight()

        self.SetBestSize((width, height))
        
        self._validkeycode = [43, 45, 46, 69, 101, 127, 314]
        self._validkeycode.extend(range(48, 58))
        self._validkeycode.extend([wx.WXK_RETURN, wx.WXK_TAB, wx.WXK_BACK,
                                   wx.WXK_LEFT, wx.WXK_RIGHT])
       
        self._spinbutton = wx.SpinButton(self, wx.ID_ANY, wx.DefaultPosition,
                                         size=(-1, height),
                                         style=wx.SP_ARROW_KEYS | wx.SP_VERTICAL |
                                         wx.SP_WRAP)

        txtstyle = wx.TE_NOHIDESEL | wx.TE_PROCESS_ENTER
        
        if extrastyle & FS_RIGHT:
            txtstyle = txtstyle | wx.TE_RIGHT
        elif extrastyle & FS_CENTRE:
            txtstyle = txtstyle | wx.TE_CENTER

        if extrastyle & FS_READONLY:
            txtstyle = txtstyle | wx.TE_READONLY
        
        self._textctrl = FloatTextCtrl(self, wx.ID_ANY, str(self._value),
                                       wx.DefaultPosition,
                                       (width-self._spinbutton.GetSize().GetWidth(), height),
                                       txtstyle)

        self._mainsizer = wx.BoxSizer(wx.HORIZONTAL)
        self._mainsizer.Add(self._textctrl, 0)
        self._mainsizer.Add(self._spinbutton, 0)
        self.SetSizer(self._mainsizer)
        self._mainsizer.Layout()

        self.SetFormat()    
        self.SetDigits(digits)
        
        # set the value here without generating an event

        strs = ("%100." + str(self._digits) + self._textformat[1])%self._value
        
        strs = strs.strip()
        strs = self.ReplaceDoubleZero(strs)
        
        self._textctrl.SetValue(strs)

        self.Bind(wx.EVT_SPIN_UP, self.OnSpinUp)
        self.Bind(wx.EVT_SPIN_DOWN, self.OnSpinDown)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnTextEnter)
        self.Bind(wx.EVT_SET_FOCUS, self.OnFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
        self._spinbutton.Bind(wx.EVT_LEFT_DOWN, self.OnSpinMouseDown)
        

    def OnDestroy(self, event) :
        """ Tries To Correctly Handle The Control Destruction Under MSW. """
        
        # Null This Since MSW Sends KILL_FOCUS On Deletion 
        if self._textctrl: 
            self._textctrl._parent = None
            self._textctrl.Destroy()
            self._textctrl = None
        
        self._spinbutton.Destroy()
        self._spinbutton = None


    def DoGetBestSize(self) :
        """ Calculates The Best Size For FloatSpin. """
   
        if self._spinctrl_bestsize.x == -999:
            
            spin = wx.SpinCtrl(self, -1)
            self._spinctrl_bestsize = spin.GetBestSize()
            
            # oops something went wrong, set to reasonable value
            if self._spinctrl_bestsize.GetWidth() < 20:
                self._spinctrl_bestsize.SetWidth(95)
            if self._spinctrl_bestsize.GetHeight() < 10:
                self._spinctrl_bestsize.SetHeight(22)

            spin.Destroy()

        return self._spinctrl_bestsize


    def DoSendEvent(self) :
        """ Send The Event To The Parent. """

        event = wx.CommandEvent(wx.wxEVT_COMMAND_SPINCTRL_UPDATED, self.GetId())
        event.SetEventObject(self)
        event.SetInt(int(self._value + 0.5))
        
        if self._textctrl:
            event.SetString(self._textctrl.GetValue())

        self.GetEventHandler().ProcessEvent(event)

        eventOut = FloatSpinEvent(wxEVT_FLOATSPIN, self.GetId())
        eventOut.SetPosition(int(self._value + 0.5))
        eventOut.SetEventObject(self)
        self.GetEventHandler().ProcessEvent(eventOut)


    def OnSpinMouseDown(self, event) :

        modifier = FixedPoint(str(1.0), 20)
        if event.m_shiftDown:
            modifier = modifier*2.0
        if event.m_controlDown:
            modifier = modifier*10.0
        if event.m_altDown:
            modifier = modifier*100.0

        self._spinmodifier = modifier
        
        event.Skip()
        

    def OnSpinUp(self, event) :
        """ Handles The wx.EVT_SPIN_UP For FloatSpin. """

        if self._textctrl and self._textctrl.IsModified() : 
            self.SyncSpinToText(False)
  
        if self.InRange(self._value + self._increment*self._spinmodifier) :
        
            self._value = self._value + self._increment*self._spinmodifier
            self.SetValue(self._value)
            self.DoSendEvent()
    

    def OnSpinDown(self, event) :
        """ Handles The wx.EVT_SPIN_DOWN For FloatSpin. """
        
        if self._textctrl and self._textctrl.IsModified() : 
            self.SyncSpinToText(False)
        
        if self.InRange(self._value - self._increment*self._spinmodifier) :
        
            self._value = self._value - self._increment*self._spinmodifier
            self.SetValue(self._value)
            self.DoSendEvent()
    

    def OnTextEnter(self, event) :
        """ Handles The wx.EVT_TEXT_ENTER For The Underline wx.TextCtrl. """

        self.SyncSpinToText(True)
        event.Skip()


    def OnChar(self, event) :
        """ Handles The wx.EVT_CHAR For The Underline wx.TextCtrl. """

        modifier = FixedPoint(str(1.0), 20)
        if event.m_shiftDown:
            modifier = modifier*2.0
        if event.m_controlDown:
            modifier = modifier*10.0
        if event.m_altDown:
            modifier = modifier*100.0

        keycode = event.GetKeyCode()

        if keycode == wx.WXK_UP:
        
            if self._textctrl and self._textctrl.IsModified() :
                self.SyncSpinToText(False)

            self.SetValue(self._value + self._increment*modifier)
            self.DoSendEvent()
        
        elif keycode == wx.WXK_DOWN:
        
            if self._textctrl and self._textctrl.IsModified() :
                self.SyncSpinToText(False)
                
            self.SetValue(self._value - self._increment*modifier)
            self.DoSendEvent()
        
        elif keycode == wx.WXK_PRIOR:

            if self._textctrl and self._textctrl.IsModified() :
                self.SyncSpinToText(False)

            self.SetValue(self._value + 10.0*self._increment*modifier)
            self.DoSendEvent()
            
        elif keycode == wx.WXK_NEXT:

            if self._textctrl and self._textctrl.IsModified() :
                self.SyncSpinToText(False)

            self.SetValue(self._value - 10.0*self._increment*modifier)
            self.DoSendEvent()
                    
        elif keycode == wx.WXK_SPACE:
        
            self.SetValue(self._value)
            event.Skip(False)

        elif keycode == wx.WXK_ESCAPE:
        
            self.SetToDefaultValue()
            self.DoSendEvent()
        
        elif keycode == wx.WXK_TAB:
        
            new_event = wx.NavigationKeyEvent()
            new_event.SetEventObject(self.GetParent())
            new_event.SetDirection(not event.ShiftDown())
            # CTRL-TAB changes the (parent) window, i.e. switch notebook page
            new_event.SetWindowChange(event.ControlDown())
            new_event.SetCurrentFocus(self)
            self.GetParent().GetEventHandler().ProcessEvent(new_event)

        else:
            if keycode not in self._validkeycode:
                return
            
            event.Skip()
    

    def OnMouseWheel(self, event) :
        """ Handles The wx.EVT_MOUSEWHEEL For FloatSpin. """

        modifier = FixedPoint(str(1.0), 20)
        if event.m_shiftDown:
            modifier = modifier*2.0
        if event.m_controlDown:
            modifier = modifier*10.0
        if event.m_altDown:
            modifier = modifier*100.0

        if self._textctrl and self._textctrl.IsModified() :
            self.SyncSpinToText(False)

        if event.GetWheelRotation() > 0:
            self.SetValue(self._value + self._increment*modifier)
            self.DoSendEvent()

        else:

            self.SetValue(self._value - self._increment*modifier)
            self.DoSendEvent()
            

    def ReplaceDoubleZero(self, strs) :
        """ Replaces The (Somewhat) Python Ugly '+e000' With +e00. """

        if self._textformat not in ["%g", "%e", "%E", "%G"]:
            return strs

        if strs.find("e+00") >= 0:
            strs = strs.replace("e+00", "e+0")
        elif strs.find("e-00") >= 0:
            strs = strs.replace("e-00", "e-0")
        elif strs.find("E+00") >= 0:
            strs = strs.replace("E+00", "E+0")
        elif strs.find("E-00") >= 0:
            strs = strs.replace("E-00", "E-0")

        return strs
    

    def SetValue(self, value) :
        """ Sets The FloatSpin Value. """

        if not self._textctrl or not self.InRange(value) :
            return

        if self._snapticks and self._increment != 0.0:
        
            finite, snap_value = self.IsFinite(value)

            if not finite: # FIXME What To Do About A Failure?
    
                if (snap_value - floor(snap_value) < ceil(snap_value) - snap_value) :
                    value = self._defaultvalue + floor(snap_value)*self._increment
                else:
                    value = self._defaultvalue + ceil(snap_value)*self._increment

        strs = ("%100." + str(self._digits) + self._textformat[1])%value
        strs = strs.strip()
        strs = self.ReplaceDoubleZero(strs)

        if value != self._value or strs != self._textctrl.GetValue() :
        
            self._textctrl.SetValue(strs)
            self._textctrl.DiscardEdits()
            self._value = value


    def GetValue(self) :
        """ Returns The FloatSpin Value. """
        
        return self._value


    def SetRange(self, min_val, max_val) :
        """
        Set The Allowed Range, If max_val < min_val Then No Range And All
        Values Are Allowed.
        """
        
        self._min = FixedPoint(str(min_val), 20)
        self._max = FixedPoint(str(max_val), 20)

        if self.HasRange() :
            if self._value > self._max:
                self.SetValue(self._max)
            elif self._value < self._min:
                self.SetValue(self._min)
    

    def SetIncrement(self, increment) :
        """ Sets The Increment For Every EVT_FLOATSPIN Event. """

        if increment < 1./10.0**self._digits:
            raise "\nERROR: Increment Should Be Greater Or Equal To 1/(10**digits)."
        
        self._increment = FixedPoint(str(increment), 20)
        self.SetValue(self._value)

    
    def GetIncrement(self) :
        """ Returns The Increment For Every EVT_FLOATSPIN Event. """

        return self._increment
    

    def SetDigits(self, digits=-1) :
        """
        Sets The Number Of Digits To Show. If digits < 0, FloatSpin Tries To
        Calculate The Best Number Of Digits Based On Input __init__ Values.
        """
        
        if digits < 0:
            incr = str(self._increment)
            if incr.find(".") < 0:
                digits = 0
            else:
                digits = len(incr[incr.find(".")+1:])
                
        self._digits = digits
        
        self.SetValue(self._value)


    def GetDigits(self) :
        """ Returns The Number Of Digits Shown. """

        return self._digits
    

    def SetFormat(self, fmt="%f") :
        """ Set The String Format To Use. """
        
        if fmt not in ["%f", "%g", "%e", "%E", "%F", "%G"]:
            raise '\nERROR: Bad Float Number Format: ' + repr(fmt) + '. It Should Be ' \
                  'One Of "%f", "%g", "%e", "%E", "%F", "%G"'

        self._textformat = fmt

        if self._digits < 0:
            self.SetDigits()
            
        self.SetValue(self._value)
        

    def GetFormat(self) :
        """ Returns The String Format In Use. """

        return self._textformat
    

    def SetDefaultValue(self, defaultvalue) :
        """ Sets The FloatSpin Default Value. """

        if self.InRange(defaultvalue) :        
            self._defaultvalue = FixedPoint(str(defaultvalue), 20)


    def GetDefaultValue(self) :
        """ Returns The FloatSpin Default Value. """

        return self._defaultvalue


    def IsDefaultValue(self) :
        """ Returns Whether The Current Value Is The Default Value Or Not. """
        
        return self._value == self._defaultvalue
    

    def SetToDefaultValue(self) :
        """ Sets FloatSpin Value To Its Default Value. """

        self.SetValue(self._defaultvalue)        


    def SetSnapToTicks(self, forceticks=True) :
        """
        Force The Value To Always Be Divisible By The Increment. Initially False.
        This Uses The Default Value As The Basis, You Will Get Strange Results
        For Very Large Differences Between The Current Value And Default Value
        When The Increment Is Very Small.
        """

        if self._snapticks != forceticks:
        
            self._snapticks = forceticks
            self.SetValue(self._value)


    def GetSnapToTicks(self) :
        """ Returns Whether The Snap To Ticks Option Is Active Or Not. """
        
        return self._snapticks        
    

    def OnFocus(self, event) :
        """ Handles The wx.EVT_SET_FOCUS Event For FloatSpin. """

        if self._textctrl:
            self._textctrl.SetFocus()

        event.Skip()


    def OnKillFocus(self, event) :
        """ Handles The wx.EVT_KILL_FOCUS Event For FloatSpin. """
        
        self.SyncSpinToText(True)
        event.Skip()


    def SyncSpinToText(self, send_event=True, force_valid=True) :
        """ Synchronize The Underline wx.TextCtrl With wx.SpinButton. """
        
        if not self._textctrl:
            return

        curr = self._textctrl.GetValue()
        curr = curr.strip()
        
        if curr:
            try:
                curro = float(curr)
                curr = FixedPoint(curr, 20)
            except:
                self.SetValue(self._value)
                return
            
            if force_valid or not self.HasRange() or self.InRange(curr) :
            
                if force_valid and self.HasRange() :
                
                    if curr > self.GetMax() :
                        curr = self.GetMax()
                    elif curr < self.GetMin() : 
                        curr = self.GetMin()
                
                if self._value != curr:
                    self.SetValue(curr)
                    
                    if send_event:
                        self.DoSendEvent()
                
        elif force_valid:
          
            # textctrl is out of sync, discard and reset
            self.SetValue(self.GetValue())
        

    def SetFont(self, font=None) :
        """ Set The Underline wx.TextCtrl Font. """

        if font is None:
            font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)

        if not self._textctrl:
            return False

        return self._textctrl.SetFont(font)


    def GetFont(self) :
        """ Returns The Underline wx.TextCtrl Font. """

        if not self._textctrl:
            return self.GetFont()
        
        return self._textctrl.GetFont()


    def GetMin(self) :
        """ Returns The Minimum Value For FloatSpin. """
        
        return self._min


    def GetMax(self) :
        """ Returns The Maximum Value For FloatSpin. """

        return self._max


    def HasRange(self) :
        """ Returns Whether FloatSpin Has A Range Or Not. """
        
        return self._min <= self._max        


    def InRange(self, value) :
        """ Returns Whether A Value Is Inside FloatSpin Range. """

        return not self.HasRange() or (value >= self._min and value <= self._max)


    def GetTextCtrl(self) :
        """ Returns The Underline wx.TextCtrl. """

        return self._textctrl


    def IsFinite(self, value) :
        """ Tries To Determine If A Value Is Finite Or Infinite/NaN. """

        try:
            snap_value = (value - self._defaultvalue)/self._increment
            finite = True
        except:
            finite = False
            snap_value = None

        return finite, snap_value            



# Class FixedPoint, version 0.0.4.
# Released to the public domain 28-Mar-2001,
# by Tim Peters (tim.one@home.com).

# Provided as-is; use at your own risk; no warranty; no promises; enjoy!

"""
FixedPoint objects support decimal arithmetic with a fixed number of
digits (called the object's precision) after the decimal point.  The
number of digits before the decimal point is variable & unbounded.

The precision is user-settable on a per-object basis when a FixedPoint
is constructed, and may vary across FixedPoint objects.  The precision
may also be changed after construction via FixedPoint.set_precision(p).
Note that if the precision of a FixedPoint is reduced via set_precision,
information may be lost to rounding.

>>> x = FixedPoint("5.55")  # precision defaults to 2
>>> print x
5.55
>>> x.set_precision(1)      # round to one fraction digit
>>> print x
5.6
>>> print FixedPoint("5.55", 1)  # same thing setting to 1 in constructor
5.6
>>> repr(x) #  returns constructor string that reproduces object exactly
"FixedPoint('5.6', 1)"
>>>

When FixedPoint objects of different precision are combined via + - * /,
the result is computed to the larger of the inputs' precisions, which also
becomes the precision of the resulting FixedPoint object.

>>> print FixedPoint("3.42") + FixedPoint("100.005", 3)
103.425
>>>

When a FixedPoint is combined with other numeric types (ints, floats,
strings representing a number) via + - * /, then similarly the computation
is carried out using-- and the result inherits --the FixedPoint's
precision.

>>> print FixedPoint(1) / 7
0.14
>>> print FixedPoint(1, 30) / 7
0.142857142857142857142857142857
>>>

The string produced by str(x) (implictly invoked by "print") always
contains at least one digit before the decimal point, followed by a
decimal point, followed by exactly x.get_precision() digits.  If x is
negative, str(x)[0] == "-".

The FixedPoint constructor can be passed an int, long, string, float,
FixedPoint, or any object convertible to a float via float() or to a
long via long().  Passing a precision is optional; if specified, the
precision must be a non-negative int.  There is no inherent limit on
the size of the precision, but if very very large you'll probably run
out of memory.

Note that conversion of floats to FixedPoint can be surprising, and
should be avoided whenever possible.  Conversion from string is exact
(up to final rounding to the requested precision), so is greatly
preferred.

>>> print FixedPoint(1.1e30)
1099999999999999993725589651456.00
>>> print FixedPoint("1.1e30")
1100000000000000000000000000000.00
>>>

The following Python operators and functions accept FixedPoints in the
expected ways:

    binary + - * / % divmod
        with auto-coercion of other types to FixedPoint.
        + - % divmod  of FixedPoints are always exact.
        * / of FixedPoints may lose information to rounding, in
            which case the result is the infinitely precise answer
            rounded to the result's precision.
        divmod(x, y) returns (q, r) where q is a long equal to
            floor(x/y) as if x/y were computed to infinite precision,
            and r is a FixedPoint equal to x - q * y; no information
            is lost.  Note that q has the sign of y, and abs(r) < abs(y).
    unary -
    == != < > <= >=  cmp
    min  max
    float  int  long    (int and long truncate)
    abs
    str  repr
    hash
    use as dict keys
    use as boolean (e.g. "if some_FixedPoint:" -- true iff not zero)

Methods unique to FixedPoints:
   .copy()              return new FixedPoint with same value
   .frac()              long(x) + x.frac() == x
   .get_precision()
   .set_precision(p)
"""

# 28-Mar-01 ver 0.0,4
#     Use repr() instead of str() inside __str__, because str(long) changed
#     since this was first written (used to produce trailing "L", doesn't
#     now).
#
# 09-May-99 ver 0,0,3
#     Repaired __sub__(FixedPoint, string); was blowing up.
#     Much more careful conversion of float (now best possible).
#     Implemented exact % and divmod.
#
# 14-Oct-98 ver 0,0,2
#     Added int, long, frac.  Beefed up docs.  Removed DECIMAL_POINT
#     and MINUS_SIGN globals to discourage bloating this class instead
#     of writing formatting wrapper classes (or subclasses)
#
# 11-Oct-98 ver 0,0,1
#     posted to c.l.py

__version__ = 0, 0, 4

# The default value for the number of decimal digits carried after the
# decimal point.  This only has effect at compile-time.
DEFAULT_PRECISION = 2

class FixedPoint:

    # the exact value is self.n / 10**self.p;
    # self.n is a long; self.p is an int

    def __init__(self, value=0, precision=DEFAULT_PRECISION) :
        self.n = self.p = 0
        self.set_precision(precision)
        p = self.p

        if isinstance(value, type("42.3e5")) :
            n, exp = _string2exact(value)
            # exact value is n*10**exp = n*10**(exp+p)/10**p
            effective_exp = exp + p
            if effective_exp > 0:
                n = n * _tento(effective_exp)
            elif effective_exp < 0:
                n = _roundquotient(n, _tento(-effective_exp))
            self.n = n
            return

        if isinstance(value, type(42)) or isinstance(value, type(42L)) :
            self.n = long(value) * _tento(p)
            return

        if isinstance(value, FixedPoint) :
            temp = value.copy()
            temp.set_precision(p)
            self.n, self.p = temp.n, temp.p
            return

        if isinstance(value, type(42.0)) :
            # XXX ignoring infinities and NaNs and overflows for now
            import math
            f, e = math.frexp(abs(value))
            assert f == 0 or 0.5 <= f < 1.0
            # |value| = f * 2**e exactly

            # Suck up CHUNK bits at a time; 28 is enough so that we suck
            # up all bits in 2 iterations for all known binary double-
            # precision formats, and small enough to fit in an int.
            CHUNK = 28
            top = 0L
            # invariant: |value| = (top + f) * 2**e exactly
            while f:
                f = math.ldexp(f, CHUNK)
                digit = int(f)
                assert digit >> CHUNK == 0
                top = (top << CHUNK) | digit
                f = f - digit
                assert 0.0 <= f < 1.0
                e = e - CHUNK

            # now |value| = top * 2**e exactly
            # want n such that n / 10**p = top * 2**e, or
            # n = top * 10**p * 2**e
            top = top * _tento(p)
            if e >= 0:
                n = top << e
            else:
                n = _roundquotient(top, 1L << -e)
            if value < 0:
                n = -n
            self.n = n
            return

        if isinstance(value, type(42-42j)) :
            raise TypeError("can't convert complex to FixedPoint: " +
                            `value`)

        # can we coerce to a float?
        yes = 1
        try:
            asfloat = float(value)
        except:
            yes = 0
        if yes:
            self.__init__(asfloat, p)
            return

        # similarly for long
        yes = 1
        try:
            aslong = long(value)
        except:
            yes = 0
        if yes:
            self.__init__(aslong, p)
            return

        raise TypeError("can't convert to FixedPoint: " + `value`)

    def get_precision(self) :
        """Return the precision of this FixedPoint.

           The precision is the number of decimal digits carried after
           the decimal point, and is an int >= 0.
        """

        return self.p

    def set_precision(self, precision=DEFAULT_PRECISION) :
        """Change the precision carried by this FixedPoint to p.

           precision must be an int >= 0, and defaults to
           DEFAULT_PRECISION.

           If precision is less than this FixedPoint's current precision,
           information may be lost to rounding.
        """

        try:
            p = int(precision)
        except:
            raise TypeError("precision not convertable to int: " +
                            `precision`)
        if p < 0:
            raise ValueError("precision must be >= 0: " + `precision`)

        if p > self.p:
            self.n = self.n * _tento(p - self.p)
        elif p < self.p:
            self.n = _roundquotient(self.n, _tento(self.p - p))
        self.p = p

    def __str__(self) :
        n, p = self.n, self.p
        i, f = divmod(abs(n), _tento(p))
        if p:
            frac = repr(f)[:-1]
            frac = "0" * (p - len(frac)) + frac
        else:
            frac = ""
        return "-"[:n<0] + \
               repr(i)[:-1] + \
               "." + frac

    def __repr__(self) :
        return "FixedPoint" + `(str(self), self.p)`

    def copy(self) :
        return _mkFP(self.n, self.p)

    __copy__ = __deepcopy__ = copy

    def __cmp__(self, other) :
        xn, yn, p = _norm(self, other)
        return cmp(xn, yn)

    def __hash__(self) :
        # caution!  == values must have equal hashes, and a FixedPoint
        # is essentially a rational in unnormalized form.  There's
        # really no choice here but to normalize it, so hash is
        # potentially expensive.
        n, p = self.__reduce()

        # Obscurity: if the value is an exact integer, p will be 0 now,
        # so the hash expression reduces to hash(n).  So FixedPoints
        # that happen to be exact integers hash to the same things as
        # their int or long equivalents.  This is Good.  But if a
        # FixedPoint happens to have a value exactly representable as
        # a float, their hashes may differ.  This is a teensy bit Bad.
        return hash(n) ^ hash(p)

    def __nonzero__(self) :
        return self.n != 0

    def __neg__(self) :
        return _mkFP(-self.n, self.p)

    def __abs__(self) :
        if self.n >= 0:
            return self.copy()
        else:
            return -self

    def __add__(self, other) :
        n1, n2, p = _norm(self, other)
        # n1/10**p + n2/10**p = (n1+n2)/10**p
        return _mkFP(n1 + n2, p)

    __radd__ = __add__

    def __sub__(self, other) :
        if not isinstance(other, FixedPoint) :
            other = FixedPoint(other, self.p)
        return self.__add__(-other)

    def __rsub__(self, other) :
        return (-self) + other

    def __mul__(self, other) :
        n1, n2, p = _norm(self, other)
        # n1/10**p * n2/10**p = (n1*n2/10**p)/10**p
        return _mkFP(_roundquotient(n1 * n2, _tento(p)), p)

    __rmul__ = __mul__

    def __div__(self, other) :
        n1, n2, p = _norm(self, other)
        if n2 == 0:
            raise ZeroDivisionError("FixedPoint division")
        if n2 < 0:
            n1, n2 = -n1, -n2
        # n1/10**p / (n2/10**p) = n1/n2 = (n1*10**p/n2)/10**p
        return _mkFP(_roundquotient(n1 * _tento(p), n2), p)

    def __rdiv__(self, other) :
        n1, n2, p = _norm(self, other)
        return _mkFP(n2, p) / self

    def __divmod__(self, other) :
        n1, n2, p = _norm(self, other)
        if n2 == 0:
            raise ZeroDivisionError("FixedPoint modulo")
        # floor((n1/10**p)/(n2*10**p)) = floor(n1/n2)
        q = n1 / n2
        # n1/10**p - q * n2/10**p = (n1 - q * n2)/10**p
        return q, _mkFP(n1 - q * n2, p)

    def __rdivmod__(self, other) :
        n1, n2, p = _norm(self, other)
        return divmod(_mkFP(n2, p), self)

    def __mod__(self, other) :
        return self.__divmod__(other)[1]

    def __rmod__(self, other) :
        n1, n2, p = _norm(self, other)
        return _mkFP(n2, p).__mod__(self)

    # caution! float can lose precision
    def __float__(self) :
        n, p = self.__reduce()
        return float(n) / float(_tento(p))

    # XXX should this round instead?
    # XXX note e.g. long(-1.9) == -1L and long(1.9) == 1L in Python
    # XXX note that __int__ inherits whatever __long__ does,
    # XXX and .frac() is affected too
    def __long__(self) :
        answer = abs(self.n) / _tento(self.p)
        if self.n < 0:
            answer = -answer
        return answer

    def __int__(self) :
        return int(self.__long__())

    def frac(self) :
        """Return fractional portion as a FixedPoint.

           x.frac() + long(x) == x
        """
        return self - long(self)

    # return n, p s.t. self == n/10**p and n % 10 != 0
    def __reduce(self) :
        n, p = self.n, self.p
        if n == 0:
            p = 0
        while p and n % 10 == 0:
            p = p - 1
            n = n / 10
        return n, p

# return 10L**n

def _tento(n, cache={}) :
    try:
        return cache[n]
    except KeyError:
        answer = cache[n] = 10L ** n
        return answer

# return xn, yn, p s.t.
# p = max(x.p, y.p)
# x = xn / 10**p
# y = yn / 10**p
#
# x must be FixedPoint to begin with; if y is not FixedPoint,
# it inherits its precision from x.
#
# Note that this is called a lot, so default-arg tricks are helpful.

def _norm(x, y, isinstance=isinstance, FixedPoint=FixedPoint,
                _tento=_tento) :
    assert isinstance(x, FixedPoint)
    if not isinstance(y, FixedPoint) :
        y = FixedPoint(y, x.p)
    xn, yn = x.n, y.n
    xp, yp = x.p, y.p
    if xp > yp:
        yn = yn * _tento(xp - yp)
        p = xp
    elif xp < yp:
        xn = xn * _tento(yp - xp)
        p = yp
    else:
        p = xp  # same as yp
    return xn, yn, p

def _mkFP(n, p, FixedPoint=FixedPoint) :
    f = FixedPoint()
    f.n = n
    f.p = p
    return f

# divide x by y, rounding to int via nearest-even
# y must be > 0
# XXX which rounding modes are useful?

def _roundquotient(x, y) :
    assert y > 0
    n, leftover = divmod(x, y)
    c = cmp(leftover << 1, y)
    # c < 0 <-> leftover < y/2, etc
    if c > 0 or (c == 0 and (n & 1) == 1) :
        n = n + 1
    return n

# crud for parsing strings
import re

# There's an optional sign at the start, and an optional exponent
# at the end.  The exponent has an optional sign and at least one
# digit.  In between, must have either at least one digit followed
# by an optional fraction, or a decimal point followed by at least
# one digit.  Yuck.

_parser = re.compile(r"""
    \s*
    (?P<sign>[-+])?
    (
        (?P<int>\d+) (\. (?P<frac>\d*))?
    |
        \. (?P<onlyfrac>\d+)
    )
    ([eE](?P<exp>[-+]? \d+))?
    \s* $
""", re.VERBOSE).match

del re

# return n, p s.t. float string value == n * 10**p exactly

def _string2exact(s) :
    m = _parser(s)
    if m is None:
        raise ValueError("can't parse as number: " + `s`)

    exp = m.group('exp')
    if exp is None:
        exp = 0
    else:
        exp = int(exp)

    intpart = m.group('int')
    if intpart is None:
        intpart = "0"
        fracpart = m.group('onlyfrac')
    else:
        fracpart = m.group('frac')
        if fracpart is None or fracpart == "":
            fracpart = "0"
    assert intpart
    assert fracpart

    i, f = long(intpart), long(fracpart)
    nfrac = len(fracpart)
    i = i * _tento(nfrac) + f
    exp = exp - nfrac

    if m.group('sign') == "-":
        i = -i

    return i, exp
