CANVAS_WIDTH = 1280
CANVAS_HEIGHT = 720
BACKGROUND_COLOR = color(215)
FREE_FALL_ACCELERATION = 0.6
BULLETS = []

import os


class Game:
    def __init__(self, w, h, groundY):
        self.w = w
        self.h = h
        self.groundY = groundY
        self.mainCharacter = MainCharacter(CANVAS_WIDTH / 2 - 35, 0, 70, 70)  # arbitrary values for now
        self.enemy = Enemy(640, 10, 70, 70)  # arbitrary values for now
        self.fallAcceleration = FREE_FALL_ACCELERATION
        self.platforms = []
        self.platforms.append(Platform(600, 500, 300, 20))

    def update(self):
        self.mainCharacter.move(self.getGroundY(self.mainCharacter))
        self.applyMovement(self.mainCharacter)
        self.applyGravity(self.mainCharacter, self.fallAcceleration)
        self.enemy.update()
        for bullet in BULLETS:
            self.applyMovement(bullet)

    def applyMovement(self, entity):
        entity.y += entity.velocityY
        entity.x += entity.velocityX

    def applyGravity(self, entity, fallAcceleration):
        currentgroundY = self.getGroundY(entity)
        if entity.y + entity.h >= currentgroundY and entity.velocityY > 0:
            entity.velocityY = 0
            entity.y = currentgroundY - self.mainCharacter.h
        else:
            entity.velocityY += fallAcceleration

    def getGroundY(self, entity):
        minAvailableGroundY = self.groundY
        for platform in self.platforms:
            isEntityInPlatformX = (platform.x <= entity.x <= platform.x + platform.w) or (platform.x <= entity.x + entity.w <= platform.x + platform.w)
            if isEntityInPlatformX and entity.y <= platform.y:
                minAvailableGroundY = platform.y
            
        return minAvailableGroundY

    def display(self):
        GROUND_STROKE_WIDTH = 0
        background(BACKGROUND_COLOR)
        stroke(GROUND_STROKE_WIDTH)
        line(0, self.groundY, self.w, self.groundY)
        self.mainCharacter.display()
        self.enemy.display()
        for bullet in BULLETS:
            bullet.display()
        for platform in self.platforms:
            platform.display()


class Entity:
    def __init__(self, initialX, initialY, w, h):
        self.x = initialX
        self.y = initialY
        self.w = w
        self.h = h
        self.velocityX = 0
        self.velocityY = 0

    def display(self):
        fill(255, 255, 255)
        rect(self.x, self.y, self.w, self.h)


class Platform:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def display(self):
        stroke(0)
        fill(255)
        rect(self.x, self.y, self.w, self.h)


class MainCharacter(Entity):
    def __init__(self, initialX, initialY, w, h):
        Entity.__init__(self, initialX, initialY, w, h)
        self.keyHandler = {LEFT: False, RIGHT: False, UP: False}

    def jump(self):
        self.velocityY = -13  # arbitrary should be a constant

    # name could be better
    def move(self, groundY):
        deltaX = 0
        if self.keyHandler[RIGHT]:
            deltaX += 7
        if self.keyHandler[LEFT]:
            deltaX -= 7
        if self.keyHandler[UP] and (self.y + self.h == groundY):
            self.jump()
        self.velocityX = deltaX


class Bullet(Entity):
    def __init__(self, initialX, initialY, w, h, speed, angle):
        Entity.__init__(self, initialX, initialY, w, h)
        self.speed = speed
        self.angle = angle
        self.velocityX = self.speed * cos(self.angle)
        self.velocityY = self.speed * sin(self.angle)
        
    def display(self):
        fill(0, 0, 0)
        stroke(40)
        rect(self.x, self.y, self.w, self.h)


class Enemy(Entity):
    def __init__(self, initialX, initialY, w, h):
        Entity.__init__(self, initialX, initialY, w, h)
        self.shootInterval = int(random(50, 150))
        self.shootTimer = 0

    def update(self):
        self.shootTimer += 1

        if self.shootTimer >= self.shootInterval:
            self.shoot()
            self.shootTimer = 0
            self.shootInterval = int(random(50, 150))

    def shoot(self):
        num_bullets = 1
        verticaDistanceBetweenbullets = 1

        targetX = game.mainCharacter.x + game.mainCharacter.w / 2

        for i in range(num_bullets):
            yOffset = i * verticaDistanceBetweenbullets
            scalingFactor = 0.65
            angle = atan2(
                scalingFactor
                * (CANVAS_HEIGHT - (self.y - (self.w // 2) + yOffset)),
                targetX - self.x,
            )
            BULLETS.append(
                Bullet(
                    self.x + self.w // 2,
                    self.y + self.h // 2,
                    20,
                    20,
                    10,
                    angle,
                )
            )  # arbitrary values for now


game = Game(CANVAS_WIDTH, CANVAS_HEIGHT, 600)


def setup():
    frameRate(60)
    size(game.w, game.h)


def draw():
    game.display()
    game.update()




def keyPressed():
    if key == CODED:
        if keyCode == UP:
            game.mainCharacter.keyHandler[UP] = True
        if keyCode == RIGHT:
            game.mainCharacter.keyHandler[RIGHT] = True
        if keyCode == LEFT:
            game.mainCharacter.keyHandler[LEFT] = True


def keyReleased():
    if key == CODED:
        if keyCode == UP:
            game.mainCharacter.keyHandler[UP] = False
        if keyCode == RIGHT:
            game.mainCharacter.keyHandler[RIGHT] = False
        if keyCode == LEFT:
            game.mainCharacter.keyHandler[LEFT] = False
