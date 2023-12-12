CANVAS_WIDTH = 1280
CANVAS_HEIGHT = 800
START_SCREEN = 0
GAME_SCREEN = 1
END_SCREEN=2
current_screen = START_SCREEN 
BACKGROUND_COLOR = color(39, 100, 167)
FREE_FALL_ACCELERATION = 0.4
MAX_FALL_SPEED = 9
MC_JUMP_SPEED = -9.5
BULLET_2=[]
ACTIVE_LASERS=[]
PLATFORM_SEEDS = ["NNJGNJJNGJNN", "NJGGJNNJGGJN", "JGNJNGGNJNGJ", 
                  "GNNJGJJGJNNG", "JGGNJNNJNGGJ", "JGJNNGGNNJGJ", "GGGGNJJNGGGG", 
                  "GJNNGGGGNNJG", "NJNNGJJGNNJN", "NJNGNJJNGNJN", "GGGNJNNJNGGG",
                  "GJNNGJJGNNJG", "NNJNNGGNNJNN", "GGJNGGGGNJGG", "NJNGGJJGGNJN",
                  "JNGGGJJGGGNJ", "NJGGGJJGGGJN", "GGGJNNNNJGGG", "GGNJGGGGJNGG"]
LAYER_HEIGHT = 100
PLATFORM_WIDTH = 64
PLATFORM_HEIGHT = 16
START_SEEDS = ["NNNNNNNNNNNJ", "NNNJNNNNJNNN"]


import os

class StartPage:
    def __init__(self):
        self.button_width = CANVAS_WIDTH // 5
        self.button_height = CANVAS_HEIGHT // 15

        self.start_button_x = (CANVAS_WIDTH - self.button_width) // 2
        self.start_button_y = 450  # Adjust the y-coordinate as needed

        self.continue_button_x = (CANVAS_WIDTH - self.button_width) // 2
        self.continue_button_y = 550  # Adjust the y-coordinate as needed
        self.background_image = loadImage(os.getcwd() + "/images/background.jpg")
        self.text_image = loadImage(os.getcwd() + "/images/FLAME-ASCEND.png")
        self.start_image = loadImage(os.getcwd() + "/images/Start-Game.png")
        self.continue_image = loadImage(os.getcwd() + "/images/Continue.png")

    def display(self):
        background(self.background_image)
        
        image(self.text_image, 320, 150, CANVAS_WIDTH // 2, CANVAS_HEIGHT // 4)
        
        
        start_image_width = CANVAS_WIDTH // 5
        start_image_height = CANVAS_HEIGHT // 15
        start_image_x = (CANVAS_WIDTH - start_image_width) // 2
        start_image_y = 450  # Adjust the y-coordinate as needed
        image(self.start_image, start_image_x, start_image_y, start_image_width, start_image_height)
        
        
        continue_image_width = CANVAS_WIDTH // 5
        continue_image_height = CANVAS_HEIGHT // 15
        continue_image_x = (CANVAS_WIDTH - continue_image_width) // 2
        continue_image_y = 550  # Adjust the y-coordinate as needed
        image(self.continue_image, continue_image_x, continue_image_y, continue_image_width, continue_image_height)
    

    def isStartButtonClicked(self, mouseX, mouseY):
        return (
            self.start_button_x < mouseX < self.start_button_x + self.button_width
            and self.start_button_y < mouseY < self.start_button_y + self.button_height
        )

    def isContinueButtonClicked(self, mouseX, mouseY):
        return (
            self.continue_button_x < mouseX < self.continue_button_x + self.button_width
            and self.continue_button_y < mouseY < self.continue_button_y + self.button_height
        )
class EndPage:
    def __init__(self):
        self.button_width = CANVAS_WIDTH // 5
        self.button_height = CANVAS_HEIGHT // 15

        self.restart_button_x = (CANVAS_WIDTH - self.button_width) // 2
        self.restart_button_y = 450  # Adjust the y-coordinate as needed
        self.background_image = loadImage(os.getcwd() + "/images/background.jpg")
        self.text_image = loadImage(os.getcwd() + "/images/FLAME-ASCEND.png")
        self.start_image = loadImage(os.getcwd() + "/images/Restart-Game.png")

    def display(self):
        background(self.background_image)
        image(self.text_image, 320, 150, CANVAS_WIDTH // 2, CANVAS_HEIGHT // 4)
        
        
        start_image_width = CANVAS_WIDTH // 5
        start_image_height = CANVAS_HEIGHT // 15
        start_image_x = (CANVAS_WIDTH - start_image_width) // 2
        start_image_y = 450  # Adjust the y-coordinate as needed
        image(self.start_image, start_image_x, start_image_y, start_image_width, start_image_height)
        
    def isReStartButtonClicked(self, mouseX, mouseY):
        return (
            self.restart_button_x < mouseX < self.restart_button_x + self.button_width
            and self.restart_button_y < mouseY < self.restart_button_y + self.button_height
        )

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
        self.topPlatformY = groundY - 3 * LAYER_HEIGHT - PLATFORM_WIDTH * 0.5
        
        self.mainCharacter = MainCharacter(400, self.topPlatformY - 64, 32, 64, "mc-idle.png", "mc-walking-right.png", 4)  # arbitrary values for now
        self.startY = self.mainCharacter.y
        self.enemy = Enemy(CANVAS_WIDTH / 2 - 64, 10, 128, 113, "enemy.png")  # arbitrary values for now
        self.mcEnemyDiff = self.enemy.y - self.mainCharacter.y
        
        self.platformLayers = []
        self.generatePlatforms()
        self.platformLayers[0][-2] = PressurePlatform(self.platformLayers[0][-2].x, self.platformLayers[0][-2].y, self.platformLayers[0][-2].w, self.platformLayers[0][-2].h, "platform.png")
        self.bomb = Bomb(self.platformLayers[0][5], 32, 32, "bomb.png")
        self.isBombExploding = False
        self.flickerCount = 0
        self.changingFrame = None
        self.isLowestLayerVisible = True
        self.yOffset = 0
        self.background = loadImage(os.getcwd() + "/images/background.jpg")
        self.start_page = StartPage()
        self.end_page = EndPage()
        
        # Generate the power up on the top level
        randomPlatform = self.getRandomPlatform()
        self.powerUp = ShootingPowerUp(randomPlatform, 20, 20)
        
    def display(self):
        if current_screen == START_SCREEN:
            self.start_page.display()
        elif current_screen == GAME_SCREEN:
            GROUND_STROKE_WIDTH = 0
            background(self.background)
            stroke(GROUND_STROKE_WIDTH)
            line(0, self.groundY + self.yOffset, self.w, self.groundY + self.yOffset)
            platformLayersToDisplay = self.platformLayers if self.isLowestLayerVisible else self.platformLayers[1:]
            for platforms in platformLayersToDisplay:
                for platform in platforms:
                    platform.display(self.yOffset)
            shieldPowerUp.display(self.yOffset)
            self.bomb.display(self.yOffset)
            self.mainCharacter.display(self.yOffset)
            self.enemy.display(self.yOffset)
            self.powerUp.display(self.yOffset)
            
            for power_up in [game.powerUp]:
                power_up.display(self.yOffset)
            
            for bullet in BULLET_2:
                bullet.display(self.yOffset)
                bullet.update()
                
            for laser in ACTIVE_LASERS:
                laser.display(self.yOffset)
                laser.update()
            
    def mouseClicked(self):
        global current_screen  # Declare current_screen as global
        if current_screen == START_SCREEN:
            if self.start_page.isStartButtonClicked(mouseX, mouseY):
                current_screen = GAME_SCREEN  # Switch to the game screen
            elif self.start_page.isContinueButtonClicked(mouseX, mouseY):
                pass
                
        if current_screen == END_SCREEN:
            if self.end_page.isReStartButtonClicked(mouseX, mouseY):
                current_screen = GAME_SCREEN  # Switch to the game screen
            
            
    
    def update(self):
        # future rising lava
        # self.groundY -= 1
        mc = self.mainCharacter
        self.yOffset = self.startY - mc.y
        currentGroundY = self.getHighestPlatformY(mc)
        self.detectCollisions()
         
        self.enemy.y = self.mcEnemyDiff + self.mainCharacter.y
        mc.applyKeyPresses()
        if not mc.flyMode:
            self.applyMovement(mc, True, currentGroundY)
            self.applyGravity(mc, self.fallAcceleration)
        if mc.keyHandler[DOWN] and mc.y + mc.h == currentGroundY and not self.isOnLowestLayer(mc) and mc.velocityY == 0:
            mc.velocityY += self.fallAcceleration
        self.enemy.update()
        if self.isBombExploding:
            if self.changingFrame == None:
                self.changingFrame = frameCount % 20
            if frameCount % 20 == self.changingFrame:
                self.flickerCount += 1
                self.isLowestLayerVisible = not self.isLowestLayerVisible
            if self.flickerCount == 9:
                self.destroyLowestLayer()
                self.addNewLayer()
                self.isBombExploding = False
                self.isLowestLayerVisible = True
                self.flickerCount = 0
                self.changingFrame = None
                # self.yOffset += LAYER_HEIGHT
                self.groundY -= LAYER_HEIGHT
                # self.mainCharacter.y += LAYER_HEIGHT
                newPressurePlatform = self.getRandomPlatform()
                while isinstance(newPressurePlatform, JumpPlatform) or isinstance(newPressurePlatform, PressurePlatform):
                    newPressurePlatform = self.getRandomPlatform()
                
                for platforms in self.platformLayers:
                    for i in range(len(platforms)):
                        if isinstance(platforms[i], PressurePlatform):
                            platforms[i] = Platform(platforms[i].x, platforms[i].y, platforms[i].w, platforms[i].h, "platform.png")
                        if platforms[i] == newPressurePlatform:
                            platforms[i] = PressurePlatform(platforms[i].x, platforms[i].y, platforms[i].w, platforms[i].h, "platform.png")
                self.bomb = self.generateBomb()
                
        for power_up in [game.powerUp]:
            power_up.update()

    def detectCollisions(self):
        mc = self.mainCharacter
        ec= self.enemy #Enemy Character
        currentPlatforms = self.getCurrentPlatforms(mc)
        
        for bullet in self.enemy.bullets:
            self.applyMovement(bullet)
            if self.isCollidingRectangleCircle(mc, bullet):
                print("Collision of " + str(mc) + " and " + str(bullet))
                self.end_page.display()
                current_screen = END_SCREEN
                noLoop()

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
            self.end_page.display()
            current_screen = END_SCREEN
            noLoop()

        if self.isCollidingRectangleCircle(mc, self.powerUp):
            self.powerUp.shoot()
            self.powerUp.update()
            print("HAHAHA")
            self.powerUp.resetPowerUp()
            
        for bullet in BULLET_2:
            if self.isCollidingRectangleCircle(ec, bullet):
                ec.score()
            
        if self.isCollidingRectangles(mc, shieldPowerUp):
            shieldPowerUp.followPlayer(mc)
            
        for laser in ACTIVE_LASERS:
            if self.isCollidingRectangleCircle(mc, laser):
                print("Collision of Laser")
                self.end_page.display()
                current_screen = END_SCREEN
                noLoop()
            
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
    
    def isCollidingRectangleLine(self, entityRectangle, entityLine):
        rectangleX, rectangleY = entityRectangle.x, entityRectangle.y
        w, h = entityRectangle.w, entityRectangle.h
        lineX1, lineY1, lineX2, lineY2 = entityLine.x1, entityLine.y1, entityLine.x2, entityLine.y2

        # Check if any of the rectangle edges intersect with the line segment
        if utils.isLineSegmentIntersectLine(rectangleX, rectangleY, rectangleX + w, rectangleY, lineX1, lineY1, lineX2, lineY2):
            return True
        if utils.isLineSegmentIntersectLine(rectangleX, rectangleY, rectangleX, rectangleY + h, lineX1, lineY1, lineX2, lineY2):
            return True
        if utils.isLineSegmentIntersectLine(rectangleX + w, rectangleY, rectangleX + w, rectangleY + h, lineX1, lineY1, lineX2, lineY2):
            return True
        if utils.isLineSegmentIntersectLine(rectangleX, rectangleY + h, rectangleX + w, rectangleY + h, lineX1, lineY1, lineX2, lineY2):
            return True

        return False
    def isCollidingRectangles(self, entityRectangle1, entityRectangle2):
        rect1X, rect1Y = entityRectangle1.x, entityRectangle1.y
        rect1W, rect1H = entityRectangle1.w, entityRectangle1.h

        rect2X, rect2Y = entityRectangle2.x, entityRectangle2.y
        rect2W, rect2H = entityRectangle2.w, entityRectangle2.h

        if rect1X < rect2X + rect2W and rect1X + rect1W > rect2X:
            if rect1Y < rect2Y + rect2H and rect1Y + rect1H > rect2Y:
                return True

        return False
    
    def generatePlatforms(self):
        for seed in START_SEEDS:
            self.platformLayers.append(self.generatePlatformLayer(seed, self.topPlatformY))
            self.topPlatformY -= LAYER_HEIGHT
        for i in range(2):
            random_seed = PLATFORM_SEEDS[int(random(0, len(PLATFORM_SEEDS)))]
            self.platformLayers.append(self.generatePlatformLayer(random_seed, self.topPlatformY))
            self.topPlatformY -= LAYER_HEIGHT
    
    def generatePlatformLayer(self, seed, y):
        platforms = []
        for i, platform_type in enumerate(seed):
            if platform_type == 'G':
                continue
            elif platform_type == 'N':
                platforms.append(Platform(256 + (i * PLATFORM_WIDTH), y, PLATFORM_WIDTH, PLATFORM_HEIGHT, "platform.png"))
            else:
                platforms.append(JumpPlatform(256 + (i * PLATFORM_WIDTH), y, PLATFORM_WIDTH, PLATFORM_HEIGHT, "jump_platform.png", MC_JUMP_SPEED))
        return platforms
    
    def generateBomb(self):
        platform = self.getRandomPlatform()
        while isinstance(platform, PressurePlatform):
            platform = self.getRandomPlatform()
        return Bomb(platform, 32, 32, "bomb.png")
    
    def addNewLayer(self):
        random_seed = PLATFORM_SEEDS[int(random(0, len(PLATFORM_SEEDS)))]
        self.platformLayers.append(self.generatePlatformLayer(random_seed, self.topPlatformY))
        self.topPlatformY -= LAYER_HEIGHT
        
    def destroyLowestLayer(self):
        del self.platformLayers[0]

    def getRandomPlatform(self):
        random_layer_index = int(random(0, len(self.platformLayers)))
        random_platform_index = int(random(0, len(self.platformLayers[random_layer_index])))
        return self.platformLayers[random_layer_index][random_platform_index]
    
    def triggerBombExplosion(self):
        self.isBombExploding = True
        
    
class Entity:
    def __init__(self, initialX, initialY, w, h, imgName=None):
        self.x = initialX
        self.y = initialY
        self.w = w
        self.h = h
        self.velocityX = 0
        self.velocityY = 0
        if imgName is None:
            self.img = None
        else:
            self.img = loadImage(os.getcwd() + "/images/" + imgName)

    def display(self, yOffset):
        fill(255, 255, 255)
        if self.img is None:
            rect(self.x, self.y + yOffset, self.w, self.h)
        if self.img is not None:
            image(self.img, self.x, self.y + yOffset, self.w, self.h)
        
    def __str__(self):
        return self.__class__.__name__ + " at " + str(self.x) + " " + str(self.y)
    
    def __repr__(self):
        return self.__class__.__name__ + " at " + str(self.x) + " " + str(self.y) 
        

class Platform(Entity):
    def __init__(self, x, y, w, h, imgName):
        Entity.__init__(self, x, y, w, h, imgName)
        self.color = color(255)
    
    # def display(self, yOffset):
    #     stroke(0)
    #     fill(self.color)
    #     rect(self.x, self.y + yOffset, self.w, self.h)


class JumpPlatform(Platform):
    def __init__(self, x, y, w, h, imgName, jumpSpeed):
        Platform.__init__(self, x, y, w, h, imgName)
        self.color = color(100, 255, 100)
        self.jumpSpeed = jumpSpeed
    
    def onCollision(self, entity):
        entity.velocityY = self.jumpSpeed
        

class PressurePlatform(Platform):
    def __init__(self, x, y, w, h, imgName):
        Platform.__init__(self, x, y, w, h, imgName)
        self.isPressed = False
        
    def display(self, yOffset):
        Platform.display(self, yOffset)
        fill(255, 100, 100)
        if self.isPressed:
            rect(self.x + 10, self.y - 5 + yOffset, self.w - 20, 5)
        else: 
            rect(self.x + 10, self.y - 10 + yOffset, self.w - 20, 10)


class MainCharacter(Entity):
    def __init__(self, initialX, initialY, w, h, imgIdleName, imgWalkingName, totalFrames):
        Entity.__init__(self, initialX, initialY, w, h)
        self.keyHandler = {LEFT: False, RIGHT: False, UP: False, DOWN: False}
        self.flyMode = False
        self.imgIdle = loadImage(os.getcwd() + "/images/" + imgIdleName)
        self.imgWalking = loadImage(os.getcwd() + "/images/" + imgWalkingName)
        self.frame = 0
        self.totalFrames = totalFrames

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
            deltaX += 5
        if self.keyHandler[LEFT]:
            deltaX -= 5
        self.velocityX = deltaX

    def display(self, yOffset):
        if self.velocityX > 0:
            image(self.imgWalking, self.x, self.y + yOffset, self.w, self.h, int(self.frame) * self.w, 0, (int(self.frame) + 1) * self.w, self.h)
            self.frame = (self.frame + 0.15) % self.totalFrames
        elif self.velocityX < 0:
            image(self.imgWalking, self.x, self.y + yOffset, self.w, self.h, (int(self.frame) + 1) * self.w, 0, int(self.frame) * self.w, self.h)
            self.frame = (self.frame + 0.15) % self.totalFrames
        else:
            image(self.imgIdle, self.x, self.y + yOffset, self.w, self.h)

    def isCollidingGround(self):
        if self.y + self.h >= game.groundY:
            return True
        return False
   
   
class Bomb(Entity):
    def __init__(self, owner, w, h, imgName):
        Entity.__init__(self, 0, 0, w, h, imgName)
        self.owner = owner
        self.x, self.y = self.getCoords()
    
    def getCoords(self):
        return self.owner.x + self.owner.w / 2, self.owner.y - self.h / 2
    
    def display(self, yOffset):
        x, y = self.getCoords()
        if (isinstance(self.owner, PressurePlatform)):
            y -= 5
        # fill(95)
        # ellipse(x, y + yOffset, self.w, self.h)
        # display image with x and y converted to top right corner
        image(self.img, x - self.w / 2, y - self.h / 2 + yOffset, self.w, self.h)
    
        
class Enemy(Entity):
    def __init__(self, initialX, initialY, w, h, imgName):
        Entity.__init__(self, initialX, initialY, w, h, imgName)
        self.bullets = []
        self.shootInterval = int(random(50, 150))
        self.shootTimer = 0
        self.bulletCount=0
        self.laserVisible = False
        self.canShootBullet = True  
        self.laserTimer = 0
        # self.bulletTypes= int(random(0,3))
        self.hp = 1000
        
    def update(self):
        self.shootTimer += 1
        
        if self.hp == 0:
            print("You win!")
            return

        if self.shootTimer >= self.shootInterval:
            if self.canShootBullet:
                self.shoot()
                self.shootTimer = 0
                self.shootInterval = int(random(50, 150))
                # self.hp -= 1

        if 5 <= self.bulletCount <= 10:
            # self.bulletCount = 0
            self.canShootBullet = False  # Disable bullet shooting
            self.laserVisible = True
            self.laserTimer = 0
            self.generateRandomLaser()

        if self.laserVisible:
            self.laserTimer += 1
            if self.laserTimer >= 30:  # Adjust the duration the laser is visible
                self.laserVisible = False
                self.canShootBullet = True  # Enable bullet shooting after laser duration
    def score(self):
        self.hp -= 1
        
    def shoot(self):
        numBulletsPerShot = 1
        verticaDistanceBetweenbullets = 1

        targetX = game.mainCharacter.x
        targetY = game.mainCharacter.y
        
        # self.hp -= 1
        # print("sera")
        
        
        if 700< self.hp <= 900:
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
                        "fireball.png"
                    )
                )  # arbitrary values for now
                # self.bulletTypes= int(random(0,3))
                # self.hp -= 1
                
        elif 500 <= self.hp <= 700:
            numBulletsPerShot = 1
            for i in range(numBulletsPerShot):
                yOffset = i * verticaDistanceBetweenbullets
                dx = targetX - (self.x )
                dy = targetY - (self.y + self.h // 2) + yOffset
                angle = atan2(dy, dx)
                self.bullets.append(
                    Bullet(
                        self.x + self.w // 2,
                        self.y + self.h /2,
                        30,
                        30,
                        10,
                        angle,
                        "fireball.png"
                    )
                )  # arbitrary values for now
                # self.bulletTypes= int(random(0,3))
                # self.hp -= 1
                
        elif 3< self.hp < 500:
            numBulletsPerShot = 5
            for i in range(numBulletsPerShot):
                yOffset = i * verticaDistanceBetweenbullets
                dx = targetX - (self.x )
                dy = targetY - (self.y + self.h // 2) + yOffset
                angle = atan2(dy, dx)
                self.bullets.append(
                    Bullet(
                        self.x + self.w // 2,
                        self.y + self.h /2,
                        40,
                        40,
                        10,
                        angle,
                        "fireball.png"
                    )
                )  # arbitrary values for now
                # self.bulletTypes= int(random(0,3))
                # self.hp -= 1
                self.generateRandomLaser()
    
        # else:
        #     print(self.hp)
        #     # pass
        #     self.generateRandomLaser()
            
    def generateRandomLaser(self):
        targetX = game.mainCharacter.x
        targetY = game.mainCharacter.y

        ACTIVE_LASERS.append(
            Laser(
                self.x + self.w // 2,
                self.y + self.h / 2,
                targetX + game.mainCharacter.w // 2,
                targetY + game.mainCharacter.h // 2,
                10,
                10,
                10,
            )
        )

    def display(self, yOffset):
        Entity.display(self, yOffset)
        for bullet in self.bullets:
            bullet.display(yOffset)

        for laser in ACTIVE_LASERS:
            laser.display(yOffset)


class Bullet(Entity):
    def __init__(self, initialX, initialY, w, h, speed, angle, imgName=None):
        Entity.__init__(self, initialX, initialY, w, h, imgName)
        self.speed = speed
        self.angle = angle
        self.velocityX = self.speed * cos(self.angle)
        self.velocityY = self.speed * sin(self.angle)
        
    def display(self, yOffset):
        fill(0, 0, 0)
        stroke(40)
        # ellipse(self.x, self.y + yOffset, self.w, self.h)
        if self.img is None:
            ellipse(self.x, self.y + yOffset, self.w, self.h)
        else:
            image(self.img, self.x - self.w / 2, self.y - self.h / 2 + yOffset, self.w, self.h)
        
    def update(self):
        self.x =self.x
        self.y -= self.speed
    
        
class ShootingPowerUp(Entity):
    def __init__(self, platform, w, h):
        x = platform.x + platform.w / 2 - w / 2
        y = platform.y - h  # Adjust the y-coordinate as needed
        Entity.__init__(self, x, y, w, h)
        self.color = color(255, 0, 0)
        self.shooting_duration = 10
        self.shooting_timer = 0
        self.is_shooting = False
        self.remaining_duration = self.shooting_duration
        self.shooting_delay = 10

    def display(self, yOffset):
        fill(self.color)
        stroke(0)
        ellipse(self.x + self.w / 2, self.y + self.h / 2 + yOffset, self.w, self.h)
        
    def shoot(self):
        if not self.is_shooting:
            self.is_shooting = True
            self.shooting_timer = 30
            self.remaining_duration = self.shooting_duration
            
        if frameCount % self.shooting_delay == 0:
            BULLET_2.append(
                Bullet(
                    game.mainCharacter.x + game.mainCharacter.w / 2,
                    game.mainCharacter.y + game.mainCharacter.h / 2,
                    10,
                    10,
                    10,
                    0,
                )
            )

    def update(self):
        if self.is_shooting:
            self.shooting_timer += 1
            if self.shooting_timer % 0.5 == 0:  
                self.shoot()
            if self.shooting_timer >= self.shooting_duration:
                self.is_shooting = False
                self.shooting_timer = 0
                self.remaining_duration = 0
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
        
class ShieldPowerUp(Entity):
    def __init__(self, initialX, initialY, w, h):
        Entity.__init__(self, initialX, initialY, w, h)
        self.flyMode = False
        self.timer = 0
        self.disappear_duration = 60 * 20  # Adjust the duration the rectangle disappears (in frames)
        self.reappear_duration = random(60 * 20, 60*30)
        self.cooldown_duration = 60 * 20  # Adjusts the cooldown duration (in frames)
        self.cooldown_timer = 0
        
    def display(self, yOffset):
        if self.timer < self.disappear_duration:
            if self.cooldown_timer == 0:
                self.placeOnRandomPlatform()
                self.cooldown_timer = self.cooldown_duration
            else:
                self.cooldown_timer -= 1
            stroke(0)
            fill(255, 255, 0)
            rect(self.x, self.y + yOffset, self.w, self.h)
        
        else:
            if self.timer >= self.disappear_duration + self.reappear_duration:
                self.placeOnRandomPlatform()
                self.timer = 0
        self.timer += 1

        
    def placeOnRandomPlatform(self):
        randomPlatform = game.getRandomPlatform()
        while isinstance(randomPlatform, PressurePlatform):
            randomPlatform = game.getRandomPlatform()
        self.x = randomPlatform.x + randomPlatform.w / 2 - self.w / 2
        self.y = randomPlatform.y - self.h

    def isCollidingGround(self):
        if (
            game.mainCharacter.x < self.x + self.w
            and game.mainCharacter.x + game.mainCharacter.w > self.x
            and game.mainCharacter.y < self.y + self.h
            and game.mainCharacter.y + game.mainCharacter.h > self.y
        ):
            # Adjust position behind the player
            self.x = game.mainCharacter.x - self.w
            self.y = game.mainCharacter.y
            return True
        return False
    
    def followPlayer(self, player):
        # Update shield power-up position to follow the main character
        self.x = game.mainCharacter.x+ (game.mainCharacter.w-self.w)//2
        self.y = game.mainCharacter.y- game.mainCharacter.h//3
   
    
shieldPowerUp = ShieldPowerUp(0, 0, 40, 40)
    
                
class Laser(Entity):
    def __init__(self, initialX, initialY, targetX, targetY, w, h, speed):
            Entity.__init__(self, initialX, initialY, w, h)
            self.speed = speed
            self.angle = atan2(targetY - initialY, targetX - initialX)
            self.velocityX = self.speed * cos(self.angle)
            self.velocityY = self.speed * sin(self.angle)
    
    def update(self):
        self.x += self.velocityX
        self.y += self.velocityY

    def display(self, yOffset):
        fill(255, 0, 0)  # Red color for the laser
        stroke(255, 0, 0)
        line(self.x, self.y + yOffset, self.x + cos(self.angle) * 1000, self.y + sin(self.angle) * 1000)
        
def setup():
    frameRate(60)
    size(game.w, game.h)


def draw():
    # rotate(PI/2)
    # translate(0, -800)
    shieldPowerUp.display(game.yOffset)
    game.display()
    game.update()
    
def mouseClicked():
    global current_screen
    if current_screen == START_SCREEN:
        if game.start_page.isStartButtonClicked(mouseX, mouseY):
            current_screen = GAME_SCREEN  # Switch to the game screen
        elif game.start_page.isContinueButtonClicked(mouseX, mouseY):
            current_screen = GAME_SCREEN  # Switch to the game screen
            loop()

    elif current_screen == GAME_SCREEN:
        game.mouseClicked()

    elif current_screen == END_SCREEN:
        if game.end_page.isReStartButtonClicked(mouseX, mouseY):
            current_screen = START_SCREEN  # Switch to the start screen
            loop()  # Resume the draw loop

    
def keyPressed():
    global current_screen
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
        game.enemy.bullets.append(Bullet(game.mainCharacter.x, game.mainCharacter.y, 112, 128, 0, 0, "fireball.png"))
    if key == 'l':
        loop()
    if key == 'p':
        if current_screen == GAME_SCREEN:
            current_screen = START_SCREEN
            game.start_page.display()
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
