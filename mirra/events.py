from __future__ import absolute_import
from . import engine 

class EventListener:
    """ describes the basic events and props that we will modify and use
    """
    def __init__(self, a) : 
        self.app = a # remember were I live to pass events to it
        self.mouseLoc = 0,0

##    def mouseMoved(self, x,y):
##	     pass
        #self.app.mouseLoc = x,y # and the application
        #if self.engine.checkMouseIntersection(x,y, "mouseMoved") is None: # if none was intersected...
##      try:                            # then try to pass the event to the main app
##          self.app.setMouseLoc(x,y)#.mouseMoved(x,y)      # .. same for the rest below...
##      except AttributeError:
##          print "no mouseMoved defined on app"
    def mousePress(self, x,y, button):
        if button == 2 :
            self.rightMouseDown(x,y)
        else:
            self.mouseDown(x,y)

    def mouseRelease(self, x,y, button):
        if button == 2 :
            self.rightMouseUp(x,y)
        else:
            self.mouseUp(x,y)

    def mouseDrag(self, x,y):
        self.mouseLoc = x,y
        if engine.checkMouseIntersection(x,y, "mouseDragged") == None: # << in case it was not defined avoid error. same below
            self.app.mouseDragged(x,y)


    def mouseMove(self,e):
        self.mouseLoc = e.x(), e.y()

    def mouseDown(self,x,y):
        if engine.checkMouseIntersection(x,y, "mouseDown") == None:
            self.app.mouseDown(x,y) 

    def mouseUp(self,x,y):
        if engine.checkMouseIntersection(x,y, "mouseUp") == None:
            self.app.mouseUp(x,y)

    def rightMouseDown(self,x,y):
        if engine.checkMouseIntersection(x,y, "rightMouseDown") == None:
            self.app.rightMouseDown(x,y)

    def rightMouseUp(self,x,y):
        if engine.checkMouseIntersection(x,y, "rightMouseUp") == None:
            self.app.rightMouseUp(x,y)

    # key events #
    def keyDown(self, k):
        self.app.keyPressed = k
        self.app.keyDown(k)
    
    def keyUp(self, k):
        self.app.keyPressed = None
        self.app.keyUp(k)

    # joystick events #
    def joyAxisMotion(self, joystick, index, value):
        self.app.joyAxisMotion(joystick, index, value)

    def joyBallMotion(self, joystick, index, value):
        self.app.joyBallMotion(joystick, index, value)

    def joyHatMotion(self, joystick, index, value):
        self.app.joyHatMotion(joystick, index, value)

    def joyButtonDown(self, joystick, button):
        self.app.joyButtonDown(joystick, button)

    def joyButtonUp(self, joystick, button):
        self.app.joyButtonUp(joystick, button)


    ########################################
