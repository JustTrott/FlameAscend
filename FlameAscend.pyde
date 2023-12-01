CANVAS_WIDTH = 1280
CANVAS_HEIGHT = 720
BACKGROUND_COLOR = color(215)
FREE_FALL_ACCELERATION = 0.6
MAX_FALL_SPEED = 12
MC_JUMP_SPEED = 15
BULLETS = []
PLATFORM_SEEDS = ["GNJGGJNG", "GJGJJGJG"]
START_SEED = "NNNNNNNJ"


import os


class Utils:
    def isLineSegmentIntersectCircle(self, segmentX1, segmentY1, segmentX2, segmentY2, centerX, centerY, radius):
        
        # math reference: https://math.stackexchange.com/questions/103556/circle-and-line-segment-intersection/103592#103592

        a = float((segmentX2 - segmentX1)) ** 2 + (segmentY2 - segmentY1) ** 2
        b = float(2) * (segmentX2 - segmentX1) * (segmentX1 - centerX) + 2 * (segmentY2 - segmentY1) * (segmentY1 - centerY)
        c = float((segmentX1 - centerX)) ** 2 + (segmentY1 - centerY) ** 2 - radius ** 2
        # we need to solve a quadratic at^2 + bx + c = 0 
        
        discriminant = b ** 2 - 4 * a * c
        # print(discriminant)
        
        if discriminant < 0:
            return False
        elif discriminant == 0:
            # print(a, b)
            t = -b / (2 * a)
            # print(t)
            if 0 <= t <= 1:
                return True
        else:
            t1 = (-b + (discriminant) ** (0.5)) / (2 * a)
            t2 = (-b - (discriminant) ** (0.5)) / (2 * a)
            # print(t1, t2)
            if (0 <= t1 <= 1) or (0 <= t2 <= 1):
                return True
        return False


utils = Utils()


class Game:
    def __init__(self, w, h, groundY):
        self.w = w
        self.h = h
        self.groundY = groundY
        self.mainCharacter = MainCharacter(CANVAS_WIDTH / 2 - 35, 500, 40, 40)  # arbitrary values for now
        self.enemy = Enemy(640, 10, 70, 70)  # arbitrary values for now
        self.fallAcceleration = FREE_FALL_ACCELERATION
        self.topPlatformY = 600
        self.platformLayers = []
        self.generatePlatforms()
    
    def display(self):
        GROUND_STROKE_WIDTH = 0
        background(BACKGROUND_COLOR)
        stroke(GROUND_STROKE_WIDTH)
        line(0, self.groundY, self.w, self.groundY)
        self.mainCharacter.display()
        self.enemy.display()
        for bullet in BULLETS:
            bullet.display()
        for platforms in self.platformLayers:
            for platform in platforms:
                platform.display()
    
    def update(self):
        currentGroundY = self.getHighestPlatformY(self.mainCharacter)
        mc = self.mainCharacter
        mc.move(currentGroundY)
        self.applyMovement(mc, True, currentGroundY)
        if not mc.flyMode:
            if self.isOnJumpPlatform(mc):
                mc.jump()
            self.applyGravity(mc, self.fallAcceleration)
        if mc.keyHandler[DOWN] and mc.y + mc.h == currentGroundY:
            mc.velocityY += self.fallAcceleration
        self.enemy.update()
        for bullet in BULLETS:
            self.applyMovement(bullet)
            if self.isCollidingRectangleCircle(mc.x, mc.y, mc.w, mc.h, bullet.x, bullet.y, bullet.w / 2):
                print("Collision of " + str(mc) + " and " + str(bullet))
                            
        if self.mainCharacter.isCollidingGround():
            print("Collision of " + str(self.mainCharacter) + " and ground")

    def getHighestPlatformY(self, entity):
        minPlatformY = self.groundY
        for platforms in self.platformLayers:
            for platform in platforms:
                isEntityInPlatformX = (platform.x <= entity.x <= platform.x + platform.w) or (platform.x <= entity.x + entity.w <= platform.x + platform.w)
                if isEntityInPlatformX and platform.y < minPlatformY and entity.y + entity.h <= platform.y:
                    minPlatformY = platform.y                        
        return minPlatformY
    
    def isOnJumpPlatform(self, entity):
        for platforms in self.platformLayers:
            for platform in platforms:
                isEntityInPlatformX = (platform.x <= entity.x <= platform.x + platform.w) or (platform.x <= entity.x + entity.w <= platform.x + platform.w)
                if isinstance(platform, JumpPlatform) and entity.y + entity.h == platform.y and isEntityInPlatformX:
                    print("true")
                    return True
        return False
    
    def applyMovement(self, entity, isFallCapped = False, fallCap = 0):
        entity.x += entity.velocityX
        if entity.y + entity.h != fallCap and isFallCapped and entity.velocityY > 0:
            entity.y = min(entity.y + entity.h + entity.velocityY, fallCap) - entity.h
        else:
            entity.y += entity.velocityY
                
    def applyGravity(self, entity, fallAcceleration, isSkippingPlatform = False):
        highestPlatformY = self.getHighestPlatformY(entity)
        
        if entity.y + entity.h != highestPlatformY:
            if entity.velocityY < MAX_FALL_SPEED:
                entity.velocityY += fallAcceleration
        elif entity.velocityY > 0:
            entity.velocityY = 0
        return
        
    def isCollidingRectangleCircle(self, rectangleX, rectangleY, w, h, circleX, circleY, radius):
        if utils.isLineSegmentIntersectCircle(rectangleX, rectangleY, rectangleX + w, rectangleY, circleX, circleY, radius):
            return True
        if utils.isLineSegmentIntersectCircle(rectangleX, rectangleY, rectangleX, rectangleY + h, circleX, circleY, radius):
            return True
        if utils.isLineSegmentIntersectCircle(rectangleX + w, rectangleY, rectangleX + w, rectangleY + h, circleX, circleY, radius):
            return True
        if utils.isLineSegmentIntersectCircle(rectangleX, rectangleY + h, rectangleX + w, rectangleY + h, circleX, circleY, radius):
            return True
        return False
    
    def generatePlatforms(self):
        self.platformLayers.append(self.generatePlatformLayer(START_SEED, self.topPlatformY))
        self.topPlatformY -= 185
        self.platformLayers.append(self.generatePlatformLayer(PLATFORM_SEEDS[0], self.topPlatformY))
        self.topPlatformY -= 185
        self.platformLayers.append(self.generatePlatformLayer(PLATFORM_SEEDS[1], self.topPlatformY))
        self.topPlatformY -= 185
    
    def generatePlatformLayer(self, seed, y):
        platforms = []
        for i, platform_type in enumerate(seed):
            if platform_type == 'G':
                continue
            elif platform_type == 'N':
                platforms.append(Platform(40 + (i * 150), y, 150, 15))
            else:
                platforms.append(JumpPlatform(40 + (i * 150), y, 150, 15))
        return platforms
    
    
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
        
    def __str__(self):
        return self.__class__.__name__ + " at " + str(self.x) + " " + str(self.y)
    
    def __repr__(self):
        return self.__class__.__name__ + " at " + str(self.x) + " " + str(self.y) 
        

class Platform:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color(255)
    
    def display(self):
        stroke(0)
        fill(self.color)
        rect(self.x, self.y, self.w, self.h)


class JumpPlatform(Platform):
    def __init__(self, x, y, w, h):
        Platform.__init__(self, x, y, w, h)
        self.color = color(100, 255, 100)
    
    def onCollision(self, entity):
        entity.jump()


class MainCharacter(Entity):
    def __init__(self, initialX, initialY, w, h):
        Entity.__init__(self, initialX, initialY, w, h)
        self.keyHandler = {LEFT: False, RIGHT: False, UP: False, DOWN: False}
        self.flyMode = False

    def jump(self):
        self.velocityY = -MC_JUMP_SPEED

    # name could be better
    def move(self, groundY):
        deltaX = 0
        if self.flyMode:
            self.velocityY = 0
            self.velocityX = 0
            if self.keyHandler[UP]:
                self.y -= 5
            if self.keyHandler[RIGHT]:
                self.x += 5
            if self.keyHandler[LEFT]:
                self.x -= 5
            if self.keyHandler[DOWN]:
                self.y += 5
            return
        if self.keyHandler[RIGHT]:
            deltaX += 7
        if self.keyHandler[LEFT]:
            deltaX -= 7
        # manual jumping is deprecated 
        # if self.keyHandler[UP] and (self.y + self.h == groundY):
            # self.jump()
        self.velocityX = deltaX

    def isCollidingGround(self):
        if self.y + self.h >= game.groundY:
            return True
        return False


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
        ellipse(self.x, self.y, self.w, self.h)
        

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
        numBulletsPerShot = 1
        verticaDistanceBetweenbullets = 1

        targetX = game.mainCharacter.x

        for i in range(numBulletsPerShot):
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
                    self.y + self.h + 10,
                    20,
                    20,
                    10,
                    angle,
                )
            )  # arbitrary values for now


game = Game(CANVAS_WIDTH, CANVAS_HEIGHT, 720)


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
        if keyCode == DOWN:
            game.mainCharacter.keyHandler[DOWN] = True
    if key == 'c':
        del BULLETS[:]
    if key == 'k':
        # game.enemy.shoot()
        BULLETS.append(Bullet(game.mainCharacter.x, game.mainCharacter.y, 100, 100, 0, 0))
    if key == 'l':
        loop()
    if key == 'p':
        noLoop()
    if key == 'f':
        game.mainCharacter.flyMode = not game.mainCharacter.flyMode
        
        


def keyReleased():
    if key == CODED:
        if keyCode == UP:
            game.mainCharacter.keyHandler[UP] = False
        if keyCode == RIGHT:
            game.mainCharacter.keyHandler[RIGHT] = False
        if keyCode == LEFT:
            game.mainCharacter.keyHandler[LEFT] = False
        if keyCode == DOWN:
            game.mainCharacter.keyHandler[DOWN] = False
