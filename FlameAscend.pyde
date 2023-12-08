CANVAS_WIDTH = 1280
CANVAS_HEIGHT = 800
BACKGROUND_COLOR = color(215)
FREE_FALL_ACCELERATION = 0.6
MAX_FALL_SPEED = 12
MC_JUMP_SPEED = -13.5
# BULLETS = []
BULLET_2=[]
PLATFORM_SEEDS = ["GNJGNJJNGJNG", "NJGGJNNJGGJN", "JGNJNGGNJNGJ", "GJGJGJJGJGJG", "GNNJGJJGJNNG", "JGGNJNNJNGGJ", "JGJNJGGJNJGJ"]
LAYER_HEIGHT = 150
PLATFORM_WIDTH = 80
START_SEED = "NNNNNNNNNNNJ"


import os



class Utils:
    def isLineSegmentIntersectCircle(self, segmentX1, segmentY1, segmentX2, segmentY2, centerX, centerY, radius):
        
        # math reference: https://math.stackexchange.com/questions/103556/circle-and-line-segment-intersection/103592#103592

        a = float((segmentX2 - segmentX1)) ** 2 + (segmentY2 - segmentY1) ** 2
        b = float(2) * (segmentX2 - segmentX1) * (segmentX1 - centerX) + 2 * (segmentY2 - segmentY1) * (segmentY1 - centerY)
        c = float((segmentX1 - centerX)) ** 2 + (segmentY1 - centerY) ** 2 - radius ** 2
        # we need to solve a quadratic at^2 + bx + c = 0 
        
        discriminant = b ** 2 - 4 * a * c

        if discriminant < 0:
            return False
        elif discriminant == 0:
            t = -b / (2 * a)
            if 0 <= t <= 1:
                return True
        else:
            t1 = (-b + (discriminant) ** (0.5)) / (2 * a)
            t2 = (-b - (discriminant) ** (0.5)) / (2 * a)
            if (0 <= t1 <= 1) or (0 <= t2 <= 1):
                return True
        return False


utils = Utils()


class Game:
    def __init__(self, w, h, groundY):
        self.w = w
        self.h = h
        self.groundY = groundY
        self.fallAcceleration = FREE_FALL_ACCELERATION
        self.topPlatformY = groundY - LAYER_HEIGHT
        
        self.platformLayers = []
        self.generatePlatforms()
        self.platformLayers[0][-2] = PressurePlatform(self.platformLayers[0][-2].x, self.platformLayers[0][-2].y, self.platformLayers[0][-2].w, self.platformLayers[0][-2].h)
        self.bomb = Bomb(self.platformLayers[0][5], 25, 25)
        self.isBombExploding = False
        self.flickerCount = 0
        self.changingFrame = None
        self.isLowestLayerVisible = True
        
        self.mainCharacter = MainCharacter(180, groundY - LAYER_HEIGHT - PLATFORM_WIDTH * 0.6, PLATFORM_WIDTH * 0.6, PLATFORM_WIDTH * 0.6)  # arbitrary values for now
        self.enemy = Enemy(640, 10, 70, 70)  # arbitrary values for now
        
        # Generate the power up on the top level
        random_layer_index = int(random(1, len(self.platformLayers) - 1))
        random_platform_index = int(random(1, len(self.platformLayers[random_layer_index]) - 1))
        self.powerUp = ShootingPowerUp(self.platformLayers[random_layer_index][random_platform_index], 20, 20)
        
        # self.CIRCLES=[]
        # self.generateCircles()
        
        
    def display(self):
        GROUND_STROKE_WIDTH = 0
        background(BACKGROUND_COLOR)
        stroke(GROUND_STROKE_WIDTH)
        line(0, self.groundY, self.w, self.groundY)
        platformLayersToDisplay = self.platformLayers if self.isLowestLayerVisible else self.platformLayers[1:]
        for platforms in platformLayersToDisplay:
            for platform in platforms:
                platform.display()
        self.bomb.display()
        self.mainCharacter.display()
        self.enemy.display()
        self.powerUp.display()
            
    
    def update(self):
        # future rising lava
        # self.groundY -= 1
        mc = self.mainCharacter
        currentGroundY = self.getHighestPlatformY(mc)
        self.detectCollisions()
         
        mc.applyKeyPresses()
        if not mc.flyMode:
            self.applyMovement(mc, True, currentGroundY)
            self.applyGravity(mc, self.fallAcceleration)
        if mc.keyHandler[DOWN] and mc.y + mc.h == currentGroundY and not self.isOnLowestLayer(mc) and mc.velocityY == 0:
            mc.velocityY += self.fallAcceleration
        self.enemy.update()
        
        # if self.isBombExploding:
        #     if self.changingFrame == None:
        #         self.changingFrame = frameCount % 30
        #     if frameCount % 30 == self.changingFrame:
        #         self.flickerCount += 1
        #         self.isLowestLayerVisible = not self.isLowestLayerVisible
        #     if self.flickerCount == 6:
        #         self.destroyLowestLayer()
        #         self.addNewLayer()
        #         self.isBombExploding = False
        #         self.isLowestLayerVisible = True
        #         self.flickerCount = 0
        #         self.changingFrame = None
        # for circles in self.CIRCLES:
        #     if self.isCollidingRectangleCircle(self.enemy, circles):
        #         print("hhhhhhhhhhhhhhhhhhhhh")
                

    def detectCollisions(self):
        mc = self.mainCharacter
        currentPlatforms = self.getCurrentPlatforms(mc)
        
        for bullet in self.enemy.bullets:
            self.applyMovement(bullet)
            if self.isCollidingRectangleCircle(mc, bullet):
                print("Collision of " + str(mc) + " and " + str(bullet))

        if self.bomb.owner == mc:
            for platform in currentPlatforms:
                if isinstance(platform, PressurePlatform):
                    self.bomb.owner = platform
                    platform.isPressed = True
                    self.triggerBombExplosion()
                    break
                
        if self.bomb.owner != mc and not isinstance(self.bomb.owner, PressurePlatform) and self.isCollidingRectangleCircle(mc, self.bomb):
            self.bomb.owner = mc
                                                                                    
        if mc.isCollidingGround():
            print("Collision of " + str(mc) + " and ground")

        if self.isCollidingRectangleCircle(mc, self.powerUp):
            self.powerUp.shoot()
            self.powerUp.update()
            print("HAHAHA")
            
            self.powerUp.resetPowerUp()
        
        for platform in currentPlatforms:
            if isinstance(platform, JumpPlatform):
                platform.onCollision(mc)
                break
                    
    def getHighestPlatformY(self, entity):
        minPlatformY = self.groundY
        for platforms in self.platformLayers:
            for platform in platforms:
                isEntityInPlatformX = (platform.x <= entity.x <= platform.x + platform.w) or (platform.x <= entity.x + entity.w <= platform.x + platform.w)
                if isEntityInPlatformX and platform.y < minPlatformY and entity.y + entity.h <= platform.y:
                    minPlatformY = platform.y                        
        return minPlatformY
    
    def getCurrentPlatforms(self, entity):
        currentPlatforms = []
        for platforms in self.platformLayers:
            for platform in platforms:
                isEntityInPlatformX = (platform.x <= entity.x <= platform.x + platform.w) or (platform.x <= entity.x + entity.w <= platform.x + platform.w)
                if entity.y + entity.h == platform.y and isEntityInPlatformX:
                    currentPlatforms.append(platform)
        return currentPlatforms
    
    def isOnJumpPlatform(self, entity):
        platforms = self.getCurrentPlatforms(entity)
        for platform in platforms:
            if isinstance(platform, JumpPlatform):
                return platform
        return None
    
    def isOnLowestLayer(self, entity):
        return entity.y + entity.h == self.platformLayers[0][0].y
    
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
        
    def isCollidingRectangleCircle(self, entityRectangle, entityCircle):
        rectangleX, rectangleY = entityRectangle.x, entityRectangle.y
        w, h = entityRectangle.w, entityRectangle.h
        circleX, circleY, radius = entityCircle.x, entityCircle.y, entityCircle.w / 2
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
        self.topPlatformY -= LAYER_HEIGHT
        for i in range(3):
            random_seed = PLATFORM_SEEDS[int(random(0, len(PLATFORM_SEEDS)))]
            self.platformLayers.append(self.generatePlatformLayer(random_seed, self.topPlatformY))
            self.topPlatformY -= LAYER_HEIGHT
    
    def generatePlatformLayer(self, seed, y):
        platforms = []
        PLATFORM_HEIGHT = 15
        for i, platform_type in enumerate(seed):
            if platform_type == 'G':
                continue
            elif platform_type == 'N':
                platforms.append(Platform(2*PLATFORM_WIDTH + (i * PLATFORM_WIDTH), y, PLATFORM_WIDTH, PLATFORM_HEIGHT))
            else:
                platforms.append(JumpPlatform(2*PLATFORM_WIDTH + (i * PLATFORM_WIDTH), y, PLATFORM_WIDTH, PLATFORM_HEIGHT, MC_JUMP_SPEED))
        return platforms
    
    def addNewLayer(self):
        random_seed = PLATFORM_SEEDS[int(random(0, len(PLATFORM_SEEDS)))]
        self.platformLayers.append(self.generatePlatformLayer(random_seed, self.topPlatformY))
        self.topPlatformY -= LAYER_HEIGHT
        
    def destroyLowestLayer(self):
        del self.platformLayers[0]
    
    # def generateCircles(self):
    #     num_circles = 5  # You can adjust the number of circles
    #     for i in range(num_circles):
    #         x = int(random(0, self.w))
    #         y = int(random(self.groundY - LAYER_HEIGHT * 3, self.groundY - LAYER_HEIGHT))
    #         radius = int(random(20, 50))
    #         self.CIRCLES.append(Entity(x, y, radius * 2, radius * 2))
    
    def triggerBombExplosion(self):
        self.isBombExploding = True
        
    
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
        

class Platform(Entity):
    def __init__(self, x, y, w, h):
        Entity.__init__(self, x, y, w, h)
        self.color = color(255)
    
    def display(self):
        stroke(0)
        fill(self.color)
        rect(self.x, self.y, self.w, self.h)


class JumpPlatform(Platform):
    def __init__(self, x, y, w, h, jumpSpeed):
        Platform.__init__(self, x, y, w, h)
        self.color = color(100, 255, 100)
        self.jumpSpeed = jumpSpeed
    
    def onCollision(self, entity):
        entity.velocityY = self.jumpSpeed
        

class PressurePlatform(Platform):
    def __init__(self, x, y, w, h):
        Platform.__init__(self, x, y, w, h)
        self.isPressed = False
        
    def display(self):
        Platform.display(self)
        fill(255, 100, 100)
        if self.isPressed:
            rect(self.x + 10, self.y - 5, self.w - 20, 5)
        else: 
            rect(self.x + 10, self.y - 10, self.w - 20, 10)


class MainCharacter(Entity):
    def __init__(self, initialX, initialY, w, h):
        Entity.__init__(self, initialX, initialY, w, h)
        self.keyHandler = {LEFT: False, RIGHT: False, UP: False, DOWN: False}
        self.flyMode = False

    def applyKeyPresses(self):
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
            deltaX += 6
        if self.keyHandler[LEFT]:
            deltaX -= 6
        self.velocityX = deltaX

    def isCollidingGround(self):
        if self.y + self.h >= game.groundY:
            return True
        return False
   
   
class Bomb(Entity):
    def __init__(self, owner, w, h):
        Entity.__init__(self, 0, 0, w, h)
        self.owner = owner
        self.x, self.y = self.getCoords()
    
    def getCoords(self):
        return self.owner.x + self.owner.w / 2, self.owner.y - self.h / 2
    
    def display(self):
        x, y = self.getCoords()
        if (isinstance(self.owner, PressurePlatform)):
            y -= 5
        fill(95)
        ellipse(x, y, self.w, self.h)
    
        
class Enemy(Entity):
    def __init__(self, initialX, initialY, w, h):
        Entity.__init__(self, initialX, initialY, w, h)
        self.bullets = []
        self.shootInterval = int(random(50, 150))
        self.shootTimer = 0

    def update(self):
        self.shootTimer += 1

        if self.shootTimer >= self.shootInterval:
            # self.shoot()
            self.shootTimer = 0
            self.shootInterval = int(random(50, 150))

    def shoot(self):
        numBulletsPerShot = 1
        verticaDistanceBetweenbullets = 1

        targetX = game.mainCharacter.x
        targetY = game.mainCharacter.y

        for i in range(numBulletsPerShot):
            yOffset = i * verticaDistanceBetweenbullets
            dx = targetX - (self.x )
            dy = targetY - (self.y + self.h // 2) + yOffset
            angle = atan2(dy, dx)
            self.bullets.append(
                Bullet(
                    self.x + self.w // 2,
                    self.y + self.h /2,
                    20,
                    20,
                    10,
                    angle,
                )
            )  # arbitrary values for now
            
    def display(self):
        Entity.display(self)
        for bullet in self.bullets:
            bullet.display()


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
        
    def update(self):
        self.x =self.x
        self.y -= self.speed
        
class ShootingPowerUp(Entity):
    def __init__(self, platform, w, h):
        x = platform.x + platform.w / 2 - w / 2
        y = platform.y - h  # Adjust the y-coordinate as needed
        Entity.__init__(self, x, y, w, h)
        self.color = color(255, 255, 0)
        self.shooting_duration = 10
        self.shooting_timer = 0
        self.is_shooting = False
        self.remaining_duration = 0

    def display(self):
        fill(self.color)
        ellipse(self.x + self.w / 2, self.y + self.h / 2, self.w, self.h)
        
    def shoot(self):
        if not self.is_shooting:
            self.is_shooting = True
            self.shooting_timer = 0
            self.remaining_duration = self.shooting_duration
            
        numBulletsPerShot = 3

        for i in range(numBulletsPerShot):
            BULLET_2.append(
                Bullet(
                    game.mainCharacter.x + game.mainCharacter.w / 2,
                    game.mainCharacter.y + game.mainCharacter.h / 2,
                    20,
                    20,
                    10,
                    0,
                )
            )
            
            
    def update(self):
        if self.is_shooting:
            self.shooting_timer += 1
            if self.shooting_timer >= self.shooting_duration:
                self.is_shooting = False
                self.shooting_timer = 0
                self.remaining_duration = 0
            else:
                self.remaining_duration -= 1
                
        if self.remaining_duration > 0:
            self.shoot()
            
    def resetPowerUp(self):
        if game.platformLayers and game.platformLayers[0]:
            random_layer_index = int(random(0, len(game.platformLayers)))
            if game.platformLayers[random_layer_index]:
                random_platform_index = int(random(0, len(game.platformLayers[random_layer_index])))
                platform = game.platformLayers[random_layer_index][random_platform_index]
                self.x = platform.x + platform.w / 2 - self.w / 2
                self.y = platform.y - self.h
 
game = Game(CANVAS_WIDTH, CANVAS_HEIGHT, CANVAS_HEIGHT)


def setup():
    frameRate(60)
    size(game.w, game.h)


def draw():
    game.display()
    game.update()
    
    for power_up in [game.powerUp]:
        power_up.display()
        power_up.update()
    
    global BULLET_2
    for bullet in BULLET_2:
        bullet.display()
        bullet.update()

    # Clean up bullets that are off-screen
    BULLET_2 = [bullet for bullet in BULLET_2 if bullet.y > 0 and bullet.y < CANVAS_HEIGHT]


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
