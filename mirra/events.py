import engine 

class EventListener:
    """ describes the basic events and props that we will modify and use
    """
    def __init__(self, a) : 
        self.app = a # remember were I live to pass events to it

##    def mouseMoved(self, x,y):
##	     pass
        #self.app.mouseLoc = x,y # and the application
        #if self.engine.checkMouseIntersection(x,y, "mouseMoved") is None: # if none was intersected...
##      try:                            # then try to pass the event to the main app
##          self.app.setMouseLoc(x,y)#.mouseMoved(x,y)      # .. same for the rest below...
##      except AttributeError:
##          print "no mouseMoved defined on app"

    def mouseDragged(self, x,y):
        if engine.checkMouseIntersection(x,y, "mouseDragged") == None: # << in case it was not defined avoid error. same below
            self.app.mouseDragged(x,y)

    def mouseDown(self,x,y):
        if engine.checkMouseIntersection(x,y, "mouseDown") == None:
            self.app.mouseDown(x,y) 

    def mouseUp(self,x,y):
        if engine.checkMouseIntersection(x,y, "mouseUp") == None:
            self.app.mouseUp(x,y)

    #def doubleClick(self,x,y):
    #   if self.engine.checkMouseIntersection(x,y, "mouseDClick") == None:
    #       try:
    #           self.app.doubleClick(x,y)
    #       except AttributeError:
    #           pass #print "no mouseDClick defined on app"

    def rightMouseDown(self,x,y):
        if engine.checkMouseIntersection(x,y, "rightMouseDown") == None:
            self.app.rightMouseDown(x,y)

    def rightMouseUp(self,x,y):
        if engine.checkMouseIntersection(x,y, "rightMouseUp") == None:
            self.app.rightMouseUp(x,y)

    # key events #
    def keyDown(self, k):
        self.app.keyDown(k)

    def keyUp(self, k):
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



try :
    import pygame
    from pygame.locals import *

    class PygameEventsListener(EventListener):
        """ Pygame especific event handling
        """
        def __init__(self, app) : #, engine):
            EventListener.__init__(self, app) #, engine)
            self.down = '' # store mouse down button for mouseup

            try: # joystick
                pygame.joystick.init() # init main joystick device system
                for n in range(pygame.joystick.get_count()): #
                    stick = pygame.joystick.Joystick(n)
                    stick.init() # init instance
                    # report joystick charateristics #
                    #print '-'*20
                    print 'Enabled joystick: ' + stick.get_name()
                    #print 'it has the following devices :'
                    #print '--> buttons : '+ str(stick.get_numbuttons())
                    #print '--> balls : '+ str(stick.get_numballs())
                    #print '--> axes : '+ str(stick.get_numaxes())
                    #print '--> hats : '+ str(stick.get_numhats())
                    #print '-'*20
            except pygame.error:
                print 'no joystick found.'
          
        def getMouseLoc(self): return pygame.mouse.get_pos()
        #def setMouseLoc(self, f): pass
        mouseLoc = property(getMouseLoc)#, setMouseLoc)

        def deal(self):
            for e in pygame.event.get():                    # iterate over event stack
                if e.type == QUIT:
                    return -1   # quit
                #elif e.type is VIDEORESIZE:
                    #   pass
                elif e.type == VIDEOEXPOSE : # in case the window is overlaped by another app
                    pass
    ##                print 'overlapping'
    ##                pygame.event.pump()
    ##                pygame.event.wait()
    ##                pygame.display.flip()
                # KEYBOARD EVENTS
                elif e.type == KEYDOWN:           # keydown events
                    if e.key == K_ESCAPE : return -1 # esc key pressed
                    x,y = pygame.mouse.get_pos()
                    self.keyDown(e.key)
                    # etc...

                elif e.type == KEYUP: # keyUp events
                    x,y = pygame.mouse.get_pos()
                    self.keyUp(e.key)
                    # etc...

                # MOUSE EVENTS
                elif e.type == MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    # print pygame.mouse.get_pressed()
                    if pygame.mouse.get_pressed()[0] : #left click
                        self.mouseDown(x,y)
                        self.down = 'left'
                    #elif pygame.mouse.get_pressed()[1] : #centerclick. ***TO BE DONE***
                    #   self.centerMouseDown(x,y)
                    #   self.down = 'center'
                    elif pygame.mouse.get_pressed()[2] : #rightclick
                        self.rightMouseDown(x,y)
                        self.down = 'right'

                elif e.type == MOUSEBUTTONUP:
                    x,y = pygame.mouse.get_pos()
                    if self.down == 'left' : # it was left click down so now it is up
                        self.mouseUp(x,y)
                    #elif self.down == 'center':
                    #   self.centerMouseUp(x,y)
                    else : #if self.down == 'right':
                        self.rightMouseUp(x,y)

                elif e.type == MOUSEMOTION:
                    x,y = pygame.mouse.get_pos()
                    if pygame.mouse.get_pressed()[0] : # mouse moved when clicked (Drag)
                        self.mouseDragged(x,y)
    ##                else:
    ##                    self.mouseMoved(x,y) # mouse moved and not clicked

                # *some* JOYSTICK EVENTS #
                elif e.type == JOYAXISMOTION: # 7
                    self.joyAxisMotion(e.joy, e.axis, e.value)

                elif e.type == JOYBALLMOTION: # 8
                    self.joyBallMotion(e.joy, e.ball, e.value)

                elif e.type == JOYHATMOTION: # 9
                    self.joyHatMotion(e.joy, e.hat, e.value)

                elif e.type == JOYBUTTONDOWN: # 10
                    self.joyButtonDown(e.joy, e.button)

                elif e.type == JOYBUTTONUP: # 11
                    self.joyButtonUp(e.joy, e.button)
except ImportError:
    print 'no pygame found in your system'


    ########################################
##import wx

class WxEventsListener (EventListener) :
    """ WX event handling
    """

    def __init__(self, a) : 
        EventListener.__init__(self,a) #,e)
        self.app = a # remember were I live to pass events to it
        self.mouseLoc = 0,0

    # mouse events
    def wxmouseMoved(self, glcanvas, evt):
        self.mouseLoc = evt.GetPosition() #STORE MOUSELOC
        if evt.Dragging() and evt.LeftIsDown() :
            if engine.checkMouseIntersection(self.mouseLoc[0], self.mouseLoc[1], "mouseDragged") == None: # << in case it was not defined avoid error. same below
                self.app.mouseDragged(self.mouseLoc[0], self.mouseLoc[1])
##        else: #
##            self.mouseMoved(x,y)

    def wxmouseDown(self, glcanvas, evt) :
        glcanvas.CaptureMouse()
        x,y = evt.GetPosition()
        if engine.checkMouseIntersection(x,y, "mouseDown") == None:
            self.app.mouseDown(x,y) 

    def wxmouseUp(self, glcanvas, evt) :
        if glcanvas.HasCapture() : 
            glcanvas.ReleaseMouse()
            x,y = evt.GetPosition()
            if engine.checkMouseIntersection(x,y, "mouseUp") == None:
                self.app.mouseUp(x,y)

    #def wxmouseDClick(self, glcanvas, evt):
    #   glcanvas.CaptureMouse()
    #   self.mouseDClick(evt.GetPosition())

    def wxrightMouseDown(self, glcanvas, evt) :
        glcanvas.CaptureMouse()
        x,y = evt.GetPosition()
        if engine.checkMouseIntersection(x,y, "rightMouseDown") == None:
            self.app.rightMouseDown(x,y)

    def wxrightMouseUp(self, glcanvas, evt) :
        if glcanvas.HasCapture() : 
            glcanvas.ReleaseMouse()
            x,y = evt.GetPosition()
            if engine.checkMouseIntersection(x,y, "rightMouseUp") == None:
                 self.app.rightMouseUp(x,y)

    # key events
    def wxkeyDown(self, glcanvas, evt) :
        self.app.keyDown(evt.GetKeyCode())

    def wxkeyUp(self, glcanvas, evt):
        self.app.keyUp(evt.GetKeyCode())

    # joystick events # TO DO !!!!
##    def joyAxisMotion(self, glcanvas, evt) :
##        print evt
####        self.app.joyAxisMotion(joystick, index, value)
##
##    def joyBallMotion(self, glcanvas, evt) :
##        print evt
####        self.app.joyBallMotion(joystick, index, value)
##
##    def joyHatMotion(self, glcanvas, evt) :
##        print evt
####        self.app.joyHatMotion(joystick, index, value)
##    def joyMove(self, glcanvas, evt) :
##        print "move",  evt
##    def joyZMove(self, glcanvas, evt) :
##        print "zmove", evt
##    def joyEvents(self, glcanvas, evt) :
##        print "joy events", evt
##
##    def joyButtonDown(self, glcanvas, evt) :
##        print "button up", evt
####        self.app.joyButtonDown(joystick, button)
##
##    def joyButtonUp(self, glcanvas, evt) :
##        print "button down", evt
##        self.app.joyButtonUp(joystick, button)
