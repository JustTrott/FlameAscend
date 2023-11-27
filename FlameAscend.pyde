CANVAS_WIDTH = 1280
CANVAS_HEIGHT = 720
BACKGROUND_COLOR = color(215)

import os

class Game:
    def __init__(self, windowWidth, windowHeight, groundHeight):
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.groundHeight = groundHeight
        self.mainCharacter = MainCharacter(0, 0, 70, 70) # arbitrary values for now
        self.fallAcceleration = 0.6 # arbitrary free fall acceleration
        
    def update(self):
        # future TODO: gravity as a different function to generalize for any object
        self.mainCharacter.move(self.groundHeight)
        self.mainCharacter.applyGravity(self.fallAcceleration)
        if self.mainCharacter.y + self.mainCharacter.bodyHeight > self.groundHeight:
            self.mainCharacter.vy = 0
            self.mainCharacter.y = self.groundHeight - self.mainCharacter.bodyHeight
        
        
    def display(self):
        GROUND_STROKE_WIDTH = 0
        background(BACKGROUND_COLOR)
        stroke(GROUND_STROKE_WIDTH)
        line(0, self.groundHeight, self.windowWidth, self.groundHeight)
        self.mainCharacter.display()
      
          
class Creature:
    def __init__(self, initialX, initialY, bodyWidth, bodyHeight):
        self.x = initialX
        self.y = initialY
        self.bodyWidth = bodyWidth
        self.bodyHeight = bodyHeight
        self.vx = 0
        self.vy = 1
                             
    def display(self):
        rect(self.x, self.y, self.bodyHeight, self.bodyWidth)

    def applyGravity(self, fallAcceleration):
        self.y += self.vy
        self.x += self.vx
        self.vy += fallAcceleration

    
class MainCharacter(Creature):
    def __init__(self, initialX, initialY, bodyWidth, bodyHeight):
        Creature.__init__(self, initialX, initialY, bodyWidth, bodyHeight)
        self.keyHandler = {LEFT: False, RIGHT: False, UP: False}
        
    def jump(self):
        self.vy = -13 # arbitrary should be a constant
            
    # name could be better
    def move(self, groundHeight):
        dx = 0    
        if self.keyHandler[RIGHT]:
            dx += 7
        if self.keyHandler[LEFT]:
            dx -= 7
        if self.keyHandler[UP] and (self.y + self.bodyHeight == groundHeight):
            self.jump()
        self.vx = dx


game = Game(CANVAS_WIDTH, CANVAS_HEIGHT, 585)


def setup():
    frameRate(60)
    size(game.windowWidth, game.windowHeight)
    
def draw():
    game.display()
    game.update()
    
def keyPressed():
    if key == CODED:
        if keyCode == UP:
            game.mainCharacter.keyHandler[UP] = True
        if keyCode == RIGHT:
            game.mainCharacter.keyHandler[RIGHT] = True
        if keyCode  == LEFT:
            game.mainCharacter.keyHandler[LEFT] = True
        
def keyReleased():
    if key == CODED:
        if keyCode == UP:
            game.mainCharacter.keyHandler[UP] = False
        if keyCode == RIGHT:
            game.mainCharacter.keyHandler[RIGHT] = False
        if keyCode  == LEFT:
            game.mainCharacter.keyHandler[LEFT] = False
