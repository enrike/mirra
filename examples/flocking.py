#!/usr/bin/env python

from mirra import main
from mirra.graphics import *
from mirra import utilities

""" Mirra : 2D graphic engine in OpenGL by www.ixi-software.net
    Check out documentation files

    Voids example based on Craig W. Reynold's home page, http://www.red3d.com/cwr/ voids description
"""


class MirraApp(main.App) :
    """ main appplication class, handles window contains events and graphics manager.
        Subclasses main.App and extends its public methods
    """
    def setUp(self) :
        """ set here the main window properties and characteristics
        """
        self.caption = "mirra template" # window name
        self.size = 640, 480 #window size
        self.pos = 100,100 # window top left location
        self.fullScreen = 0 # if fullScreen is on it will overwrite your pos and size to match the display's resolution
        self.frameRate = 15 # set refresh framerate

    def start(self) :
        """ First thing to happen after the instance has been initalisiated
            good place to instanciate classes and init stuff
        """
        # set global forces, states and limits
        self.followtheflockF = 0.01
        self.avoidothersF = 0.0003
        self.matchyrspeedF = 0.001
        self.followmouse = 0
##        self.followmouseF = 0.005  
        self.maxspeed = 7
##        self.gravityF = 0
##        self.wind = 0,0
        
        self.objs = []
        for z in range(50):
            self.objs.append(Shape())

        self.massCenter = self.averageCenter()
        self.flockSpeed = self.averageSpeed()

    def mouseDown(self,x,y) :
        self.followmouse = not self.followmouse # switch

    def step(self) :
        self.massCenter = self.averageCenter()
        self.flockSpeed = self.averageSpeed()

    def averageCenter(self) :
        x = y = 0
        for o in self.objs : 
            x += o.x
            y += o.y
        num = float(len(self.objs))  # minus me. note float 1.
        return x/num, y/num 

    def averageSpeed(self) :
        x = y = 0
        for o in self.objs :
            x += o.nextstep[0]
            y += o.nextstep[1]
        num =  float(len(self.objs))  # minus me. Note float 1.
        return x/num, y/num 





class Shape(Rect) :
    
    def start(self) :
        self.nextstep = [0,0] # note is array and not tupple. Speed of each step
##        self.perching = 0
##        self.perch_timer = 0
        self.f1 = 0
        self.f2 = 0
        self.f3 = 0

        self.loc = utilities.randPoint(0, 0, self.app.width, self.app.height)
        self.color = utilities.randRGBA()
        self.width = utilities.randint(6,12)
        self.height = utilities.randint(6,12)

    def step(self) :
        a = (self.app.massCenter[0] - self.x)* self.app.followtheflockF
        b = (self.app.massCenter[1] - self.y)* self.app.followtheflockF
        self.f1 = a,b 
        
        c,d = self.avoidOthers()
        self.f2 =  c * self.app.avoidothersF, d * self.app.avoidothersF
        
        e = (self.app.flockSpeed[0] - self.nextstep[0])* self.app.matchyrspeedF
        f = (self.app.flockSpeed[1] - self.nextstep[1])* self.app.matchyrspeedF
        self.f3 = e,f 
        
##        if self.app.followmouse :
##            mouse = self.tend_to_point(self.app.mouseLoc)
##        else:
##            mouse = self.avoid_point(self.app.mouseLoc)

        x = self.nextstep[0] + self.f1[0] + self.f2[0] + self.f3[0]  #\
##          + mouse[0] + self.app.wind[0]
        y = self.nextstep[1] + self.f1[1] + self.f2[1] + self.f3[1]  #\
##            + mouse[1] + self.app.wind[1] + self.app.gravityF
        
        self.nextstep = self.limitSpeed( [x,y] )  #limit if too fast 
        
        nextx = self.x + self.nextstep[0]
        nexty = self.y + self.nextstep[1]  # calc new step

        self.rotation = utilities.getAng(self.loc, (nextx, nexty))
        limitedX, limitedY =  utilities.constrainToRect(nextx, nexty, (0,0,self.app.width, self.app.height))
        self.loc = limitedX, limitedY # here we go
        

    def limitSpeed(self, speed) :
        if self.app.maxspeed == 0 : self.app.maxspeed = 1 # avoid 0
        if speed[0] != 0 :
            if abs(speed[0]) > self.app.maxspeed :
                speed[0] = (speed[0]/abs(speed[0])) * self.app.maxspeed
        if speed[1] != 0 :
            if abs(speed[1]) > self.app.maxspeed :
                speed[1] = (speed[1]/abs(speed[1])) * self.app.maxspeed
        return speed

    def tend_to_point(self, p) :
        return (p[0] - self.x)*self.app.followmouseF, (p[1] - self.y)*self.app.followmouseF
    
    def avoid_point(self, p):
        return (self.x - p[0])*self.app.followmouseF, (self.y - p[1])*self.app.followmouseF

    def avoidOthers(self) :
        x = y = 0
        for o in self.app.objs :
            if o is not self :
                if utilities.distance(self.loc, o.loc) < 100:
                    x -= (o.x - self.x)
                    y -= (o.y - self.y)
        return x,y

        

        
            

MirraApp() # init always here your main app class that extends main.App




