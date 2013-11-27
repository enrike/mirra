#!/usr/bin/env python

#
from mirra import main
from mirra.graphics import *
from mirra import utilities


""" Mirra : 2D graphic engine in OpenGL by www.ixi-software.net
    Check out documentation files
"""


class MirraApp(main.App):
    """ main appplication class, handles window contains events and graphics manager.
        Subclasses main.App and extends its public methods
    """
    def setUp(self):
        """ set here the main window properties and characteristics
        """
        self.caption = "pong" # window name
        self.size = 640, 480 #window size
        self.pos = 100,100 # window top left location
        self.fullScreen = 0 # if fullScreen is on it will overwrite your pos and size to match the display's resolution
        self.frameRate = 15 # set refresh framerate

    def start(self):
        self.bgColor = 0,0,0
        self.ball = Ball(0,0,width= 5, color=(0,1,0))
        self.batt = Batt(self.width-20, self.height/2, width=10, height=70, color=(0,1,0))
        self.gameLabel = Text("Press space to start", self.width/2.7, self.size[1]/3, color=(0,1,0))

    def keyDown(self, key): 
        if key == 32 : self.startGame() # space bar 
        
    def startGame(self):
        self.gameLabel.visible = 0
        self.ball.visible = 1
        self.ball.startGame()
        
    def stopGame(self):
        self.gameLabel.visible =  1
        self.ball.visible = 0
        self.gameLabel.text ="Game Over!, press space to start again"



class Ball(Circle):

    def start(self): 
        self.vector = 0,0
            
    def startGame(self) : 
        self.loc = 0, utilities.randint(0,self.app.height)
        self.vector = utilities.randint(4,8), utilities.randint(-8,8)
            
    def stopGame(self):
        self.loc = 0,0
        self.vector = 0,0
            
    def step(self):
         newloc = self.loc[0]+self.vector[0], self.loc[1]+self.vector[1]   # next location   
         if newloc[0]> self.app.width : 
             self.app.stopGame()
             self.stopGame()
         if newloc[1]>=self.app.height or newloc[1]<=0   :
              self.vector = self.vector[0], -self.vector[1] # reverse vertcal vector
         if utilities.pointInRect(self.loc, self.app.batt.calcRect()) :
             newloc = self.app.batt.x-self.app.batt.width, newloc[1]
             self.vector = -self.vector[0], self.vector[1] # reverse horizntal vector
         elif newloc[0] <= 0:
             self.vector = -self.vector[0], self.vector[1] # reverse horizntal vector
         self.loc = newloc   # update loc
               
               
               
class Batt(Rect):               
    def calcRect(self) : 
        return utilities.calcRectRect(self.x, self.y, self.width, self.height)
           
    def step(self): self.y = self.app.mouseLoc[1]

    

MirraApp() # init always here your main app class that extends main.App




