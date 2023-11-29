CANVAS_WIDTH = 1280
CANVAS_HEIGHT = 720
BACKGROUND_COLOR = color(215)
FREE_FALL_ACCELERATION = 0.6
BULLETS = []

import os


class Game:
    def __init__(self, windowWidth, windowHeight, groundHeight):
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.groundHeight = groundHeight
        self.mainCharacter = MainCharacter(0, 0, 70, 70)  # arbitrary values for now
        self.enemy = Enemy(640, 10, 70, 70)  # arbitrary values for now
        self.fallAcceleration = FREE_FALL_ACCELERATION

    def update(self):
        # future TODO: gravity as a different function to generalize for any object
        self.mainCharacter.move(self.groundHeight)
        self.applyGravity(self.mainCharacter, self.fallAcceleration)

    def applyGravity(self, entity, fallAcceleration):
        entity.y += entity.vy
        entity.x += entity.vx
        currentGroundHeight = self.getGroundHeight(entity)
        if entity.y + entity.h >= currentGroundHeight:
            entity.vy = 0
            entity.y = currentGroundHeight - self.mainCharacter.h
        else:
            entity.vy += fallAcceleration

    def getGroundHeight(self, entity):
        return self.groundHeight

    def display(self):
        GROUND_STROKE_WIDTH = 0
        background(BACKGROUND_COLOR)
        stroke(GROUND_STROKE_WIDTH)
        line(0, self.groundHeight, self.windowWidth, self.groundHeight)
        self.mainCharacter.display()
        self.enemy.display()


class Creature:
    def __init__(self, initialX, initialY, w, h):
        self.x = initialX
        self.y = initialY
        self.w = w
        self.h = h
        self.vx = 0
        self.vy = 1

    def display(self):
        fill(255, 255, 255)
        rect(self.x, self.y, self.w, self.h)

    def applyGravity(self, fallAcceleration):
        self.y += self.vy
        self.x += self.vx
        self.vy += fallAcceleration


class MainCharacter(Creature):
    def __init__(self, initialX, initialY, w, h):
        Creature.__init__(self, initialX, initialY, w, h)
        self.keyHandler = {LEFT: False, RIGHT: False, UP: False}

    def jump(self):
        self.vy = -13  # arbitrary should be a constant

    # name could be better
    def move(self, groundHeight):
        dx = 0
        if self.keyHandler[RIGHT]:
            dx += 7
        if self.keyHandler[LEFT]:
            dx -= 7
        if self.keyHandler[UP] and (self.y + self.h == groundHeight):
            self.jump()
        self.vx = dx


class Bullet:
    def __init__(self, initialX, initialY, bodyWidth, bodyHeight, speed, angle):
        self.x = initialX
        self.y = initialY
        self.bodyWidth = bodyWidth
        self.bodyHeight = bodyHeight
        self.speed = speed
        self.angle = angle  # Angle in radians

    def move(self):
        self.x += self.speed * cos(self.angle)
        self.y += self.speed * sin(self.angle)

    def display(self):
        fill(0, 0, 0)
        stroke(40)
        rect(self.x, self.y, self.bodyWidth, self.bodyHeight)


class Enemy(Creature):
    def __init__(self, initialX, initialY, bodyWidth, bodyHeight):
        Creature.__init__(self, initialX, initialY, bodyWidth, bodyHeight)
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

        targetX = game.mainCharacter.x + game.mainCharacter.bodyWidth / 2

        for i in range(num_bullets):
            yOffset = i * verticaDistanceBetweenbullets
            scalingFactor = 0.65
            angle = atan2(
                scalingFactor
                * (CANVAS_HEIGHT - (self.y - (self.bodyWidth // 2) + yOffset)),
                targetX - self.x,
            )
            BULLETS.append(
                Bullet(
                    self.x + self.bodyWidth // 2,
                    self.y + self.bodyHeight // 2,
                    20,
                    20,
                    10,
                    angle,
                )
            )  # arbitrary values for now


game = Game(CANVAS_WIDTH, CANVAS_HEIGHT, 585)


def setup():
    frameRate(60)
    size(game.windowWidth, game.windowHeight)


def draw():
    game.display()
    game.update()

    for bullet in BULLETS:
        bullet.display()
        bullet.move()

    game.enemy.update()


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
