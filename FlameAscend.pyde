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
# BULLET_2=[]
# ACTIVE_LASERS=[]
PLATFORM_SEEDS = ["NNJGNJJNGJNN", "NJGGJNNJGGJN", "JGNJNGGNJNGJ", 
                  "GNNJGJJGJNNG", "JGGNJNNJNGGJ", "JGJNNGGNNJGJ", "GGGGNJJNGGGG", 
                  "GJNNGGGGNNJG", "NJNNGJJGNNJN", "NJNGNJJNGNJN", "GGGNJNNJNGGG",
                  "GJNNGJJGNNJG", "NNJNNGGNNJNN", "GGJNGGGGNJGG", "NJNGGJJGGNJN",
                  "JNGGGJJGGGNJ", "NJGGGJJGGGJN", "GGGJNNNNJGGG", "GGNJGGGGJNGG"]
LAYER_HEIGHT = 100
PLATFORM_WIDTH = 64
PLATFORM_HEIGHT = 16
START_SEEDS = ["NNNNNNNNNNNJ", "NNNJNNNNJNNN", "GJNNGGGGNNJG", "GGGJNNNNJGGG"]


import os
from random import randint, choice
import csv


add_library('minim')
player=Minim(this)
add_library('sound')

class ScreenController:
    def __init__(self):
        self.game = Game(CANVAS_WIDTH, CANVAS_HEIGHT, CANVAS_HEIGHT)
        self.start_page = StartPage()
        self.end_page = EndPage()
        self.current_screen = START_SCREEN

    def display(self):
        if self.current_screen == START_SCREEN:
            self.start_page.display()
        elif self.current_screen == GAME_SCREEN:
            self.game.display()
        elif self.current_screen == END_SCREEN:
            self.end_page.display()
    
    def mouseClicked(self, mouseX, mouseY):
        if self.current_screen == START_SCREEN:
            if self.start_page.isStartButtonClicked(mouseX, mouseY):
                self.game = Game(CANVAS_WIDTH, CANVAS_HEIGHT, CANVAS_HEIGHT)
                self.switchScreen(GAME_SCREEN)
            elif self.start_page.isContinueButtonClicked(mouseX, mouseY):
                self.switchScreen(GAME_SCREEN)
        elif self.current_screen == GAME_SCREEN:
            pass
        elif self.current_screen == END_SCREEN:
            if self.end_page.isReStartButtonClicked(mouseX, mouseY):
                self.game = Game(CANVAS_WIDTH, CANVAS_HEIGHT, CANVAS_HEIGHT)
                self.switchScreen(GAME_SCREEN)

    def update(self):
        if self.current_screen == START_SCREEN:
            pass
        elif self.current_screen == GAME_SCREEN:
            if self.game.isGameFinished:
                self.switchScreen(END_SCREEN)
            else:
                self.game.update()
        elif self.current_screen == END_SCREEN:
            pass
    
    def switchScreen(self, screen):
        self.current_screen = screen


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
        
        fill(0)
        textSize(30)
        textAlign(LEFT, TOP)
        text("Current Score: " + str(sc.game.current_score), CANVAS_WIDTH // 2.5, 550)
        textAlign(CENTER)
        # text("Current Score:" + str(sc.game.current_score))
        
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

    def isLineSegmentsIntersect(self, segmentX1, segmentY1, segmentX2, segmentY2, segmentX3, segmentY3, segmentX4, segmentY4):
        # math reference: https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
        # Return true if line segments AB and CD intersect
        def ccw(A, B, C):
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
        
        return ccw((segmentX1, segmentY1), (segmentX3, segmentY3), (segmentX4, segmentY4)) != ccw((segmentX2, segmentY2), (segmentX3, segmentY3), (segmentX4, segmentY4)) and ccw((segmentX1, segmentY1), (segmentX2, segmentY2), (segmentX3, segmentY3)) != ccw((segmentX1, segmentY1), (segmentX2, segmentY2), (segmentX4, segmentY4))
        
    def computeParallelLinesAtDistance(self, line, distance):
        k, b = line
        e = b + distance * (1 + k ** 2) ** 0.5
        f = b - distance * (1 + k ** 2) ** 0.5
        return [(k, e), (k, f)]

    def computeLineIntersectionWithScreenEdges(self, line, canvasWidth, canvasHeight):
        k, b = line
        # y = kx + b
        # x = (y - b) / k
        # y = canvasHeight
        # x = (canvasHeight - b) / k
        # x = 0
        # y = b
        # x = canvasWidth
        # y = k * canvasWidth + b
        bottomIntersection = ((canvasHeight - b) / k, canvasHeight)
        leftIntersection = (0, b)
        rightIntersection = (canvasWidth, k * canvasWidth + b)
        if k < 0:
            return [bottomIntersection, leftIntersection]
        else:
            return [bottomIntersection, rightIntersection]

    def distanceBetweenPoints(self, p1, p2):
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** (0.5)

utils = Utils()


class Game:
    def __init__(self, w, h, groundY):
        self.w = w
        self.h = h
        self.groundY = groundY
        self.groundImage = loadImage(os.getcwd() + "/images/lava.png")
        self.fallAcceleration = FREE_FALL_ACCELERATION
        self.topPlatformY = groundY - 3 * LAYER_HEIGHT - PLATFORM_WIDTH * 0.5
        self.isGameFinished = False

        self.mainCharacter = MainCharacter(400, self.topPlatformY - 64, 32, 64, "mc-idle.png", "mc-walking-right.png", 4, "shield-active.png", 10)  # arbitrary values for now
        self.startY = self.mainCharacter.y
        self.enemy = Enemy(CANVAS_WIDTH / 2 - 64, 10, 128, 113, "enemy.png")  # arbitrary values for now
        self.mcEnemyDiff = self.enemy.y - self.mainCharacter.y
        
        self.platformLayers = []
        self.generateStartPlatforms()
        self.platformLayers[0][-2] = PressurePlatform(self.platformLayers[0][-2].x, self.platformLayers[0][-2].y, self.platformLayers[0][-2].w, self.platformLayers[0][-2].h, "platform.png")
        self.bomb = Bomb(self.platformLayers[0][5], 32, 32, "bomb.png")
        self.isBombExploding = False
        self.flickerCount = 0
        self.changingFrame = None
        self.isLowestLayerVisible = True
        self.yOffset = 0
        self.background = loadImage(os.getcwd() + "/images/background.jpg")
        self.bgMusic= player.loadFile(os.getcwd()+ "/sounds/background.mp3")
        self.enemyDamage= player.loadFile(os.getcwd()+ "/sounds/enemy_damage.mp3")
        self.enemyDeath= player.loadFile(os.getcwd()+ "/sounds/enemy_death.mp3")
        self.fireBall= player.loadFile(os.getcwd()+ "/sounds/fireball.mp3")
        self.laser= player.loadFile(os.getcwd()+ "/sounds/laser.mp3")
        self.monster1= player.loadFile(os.getcwd()+ "/sounds/monster1.mp3")
        self.playerShoot= player.loadFile(os.getcwd()+ "/sounds/player_shoot.mp3")
        self.gameOver= player.loadFile(os.getcwd()+ "/sounds/gameover.MP3")
        self.playerDeath= player.loadFile(os.getcwd()+ "/sounds/player_death.mp3")
        
        
    
        self.bgMusic.loop()
        

        self.shieldPowerUps = []
        self.shootingPowerUps = []
        # self.shootingPowerUps.append(PowerUp(self.platformLayers[1][0], 32, 32))
        
        self.start_time = millis() 
        self.current_score = 0

    
    
    # def save_all_time_high_score(self):
    #     with open('highscores.csv','a') as table:
    #             w = csv.writer(table,lineterminator='\n')
    #             w.writerow(["{}".format(self.player_name).upper(),self.score])
    #             self.score_saved = True
    
    def update_scores(self):
        self.current_score = int((millis() - self.start_time)/100)
        

    def display_scores(self):
        fill(0)
        textSize(20)
        textAlign(LEFT, TOP)
        text("Current Score:" + str(self.current_score), 10, 10)


        # scores_temp = []
        # scores = []
        # file = open('highscores.csv','r')
        # for line in file:
        #     line_list = line.strip().split(",")
        #     if line_list[0] == "":
        #         line_list[0] = "-"
        #     scores_temp.append([line_list[0],int(line_list[1])])
        # file.close()
        # scores_temp.sort()
        
        # invalid = []
        # for i in range(len(scores_temp)-1):
        #     if scores_temp[i][0] == scores_temp[i+1][0]:
        #         invalid.append(i)
        # invalid.sort(reverse=True)
        # for index in invalid:
        #     del scores_temp[index]
            
        # for line in scores_temp:
        #     scores.append([line[1],line[0]])
        # scores.sort(reverse=True)
            
            
        # textAlign(RIGHT, TOP)
        # text("All-Time High Score:" + str(score[1]), CANVAS_WIDTH - 10, 10)
        
                
    def display(self):
        GROUND_STROKE_WIDTH = 0
        background(self.background)
        stroke(GROUND_STROKE_WIDTH)
        line(0, self.groundY + self.yOffset, self.w, self.groundY + self.yOffset)
        image(self.groundImage, 0, self.groundY + self.yOffset, self.w, self.h - self.groundY - self.yOffset, 0, 0, self.w, int(self.h - self.groundY - self.yOffset))
        platformLayersToDisplay = self.platformLayers if self.isLowestLayerVisible else self.platformLayers[1:]
        for platforms in platformLayersToDisplay:
            for platform in platforms:
                platform.display(self.yOffset)
        self.bomb.display(self.yOffset)
        self.mainCharacter.display(self.yOffset)
        self.enemy.display(self.yOffset)
        
        for shieldPowerUp in self.shieldPowerUps:
            shieldPowerUp.display(self.yOffset)
        for shootingPowerUp in self.shootingPowerUps:
            shootingPowerUp.display(self.yOffset)

            
    def update(self):
        self.update_scores()

        # Display scores
        self.display_scores()

        self.groundY -= 0.5
        mc = self.mainCharacter
        self.yOffset = self.startY - mc.y
        currentGroundY = self.getHighestPlatformY(mc)
        self.detectCollisions()
        if self.isGameFinished:
            return
        self.enemy.y = self.mcEnemyDiff + self.mainCharacter.y
        mc.applyKeyPresses()
        if not mc.flyMode:
            self.applyMovement(mc, True, currentGroundY)
            self.applyGravity(mc, self.fallAcceleration)
        if mc.keyHandler[DOWN] and mc.y + mc.h == currentGroundY and not self.isOnLowestLayer(mc) and mc.velocityY == 0:
            mc.velocityY += self.fallAcceleration
        self.enemy.update(mc)
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
                self.groundY = self.topPlatformY + 7 * LAYER_HEIGHT
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
                self.score(100)
        self.bomb.update()
        mc.update()
        self.cleanUp()

    def detectCollisions(self):
        mc = self.mainCharacter
        ec= self.enemy #Enemy Character
        currentPlatforms = self.getCurrentPlatforms(mc)
        
        for bullet in self.enemy.bullets:
            self.applyMovement(bullet) 
            if not mc.isShieldUp and self.isCollidingRectangleCircle(mc, bullet):
                print("Collision of " + str(mc) + " and " + str(bullet))
                self.gameOver.play()
                self.gameOver.rewind()
                self.bgMusic.pause()
                self.isGameFinished = True
                return

        if self.bomb.grabbedBy == mc:
            for platform in currentPlatforms:
                if isinstance(platform, PressurePlatform):
                    self.bomb.grab(platform)
                    platform.isPressed = True
                    self.triggerBombExplosion()
                    break
                
        if self.bomb.grabbedBy != mc and not isinstance(self.bomb.grabbedBy, PressurePlatform) and self.isCollidingRectangles(mc, self.bomb):
            self.bomb.grab(mc)
                                                                                    
        if mc.isCollidingGround(self.groundY):
            print("Collision of " + str(mc) + " and ground")
            self.isGameFinished = True
            self.playerDeath.play()
            delay(400)
            self.gameOver.play()
            self.gameOver.rewind()
            self.bgMusic.pause()
            return

        if not mc.isShieldUp:
            for laser in self.enemy.lasers:
                if not laser.isShooting:
                    continue
                # construct two line segments from laser.edges
                segment1X1, segment1Y1, segment1X2, segment1Y2 = laser.edges[0], laser.edges[1], laser.edges[6], laser.edges[7]
                segment2X1, segment2Y1, segment2X2, segment2Y2 = laser.edges[2], laser.edges[3], laser.edges[4], laser.edges[5]
                if self.isCollidingRectangleLine(mc, (segment1X1, segment1Y1, segment1X2, segment1Y2)) or self.isCollidingRectangleLine(mc, (segment2X1, segment2Y1, segment2X2, segment2Y2)):
                    print("Collision of " + str(mc) + " and " + str(laser))
                    self.gameOver.play()
                    self.gameOver.rewind()
                    self.isGameFinished = True
                    return
            
        for shieldPowerUp in self.shieldPowerUps:
            if self.isCollidingRectangleCircle(mc, shieldPowerUp):
                self.shieldPowerUps.remove(shieldPowerUp)
                mc.isShieldUp = True
                self.monster1.play()
                self.monster1.rewind()
                break
        
        for shootingPowerUp in self.shootingPowerUps:
            if self.isCollidingRectangleCircle(mc, shootingPowerUp):
                self.shootingPowerUps.remove(shootingPowerUp)
                mc.startShooting()
                break
        
        for bullet in self.mainCharacter.bullets:
            if self.isCollidingRectangleCircle(ec, bullet):
                self.enemyDamage.play()
                self.enemyDamage.rewind()
                self.score(10)
                self.mainCharacter.bullets.remove(bullet)
            
        if not mc.isShieldUp:
            for laser in self.enemy.lasers:
                if self.isCollidingRectangleCircle(mc, laser):
                    print("Collision of" + str(mc) + " and " + str(laser))
                    self.gameOver.play()
                    self.gameOver.rewind()
                    self.isGameFinished = True
                    return
            
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
    
    def isCollidingRectangleLine(self, entityRectangle, lineSegment):
        rectangleX, rectangleY = entityRectangle.x, entityRectangle.y
        w, h = entityRectangle.w, entityRectangle.h
        segmentX1, segmentY1, segmentX2, segmentY2 = lineSegment
        if utils.isLineSegmentsIntersect(rectangleX, rectangleY, rectangleX + w, rectangleY, segmentX1, segmentY1, segmentX2, segmentY2):
            return True
        if utils.isLineSegmentsIntersect(rectangleX, rectangleY, rectangleX, rectangleY + h, segmentX1, segmentY1, segmentX2, segmentY2):
            return True
        if utils.isLineSegmentsIntersect(rectangleX + w, rectangleY, rectangleX + w, rectangleY + h, segmentX1, segmentY1, segmentX2, segmentY2):
            return True
        if utils.isLineSegmentsIntersect(rectangleX, rectangleY + h, rectangleX + w, rectangleY + h, segmentX1, segmentY1, segmentX2, segmentY2):
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
    
    def generateStartPlatforms(self):
        for seed in START_SEEDS:
            self.platformLayers.append(self.generatePlatformLayer(seed, self.topPlatformY))
            self.topPlatformY -= LAYER_HEIGHT
        
    def generatePlatformLayer(self, seed, y):
        platforms = []
        margin = (CANVAS_WIDTH - len(seed) * PLATFORM_WIDTH) / 2
        for i, platform_type in enumerate(seed):
            if platform_type == 'G':
                continue
            elif platform_type == 'N':
                platforms.append(Platform(margin + (i * PLATFORM_WIDTH), y, PLATFORM_WIDTH, PLATFORM_HEIGHT, "platform.png"))
            else:
                platforms.append(JumpPlatform(margin + (i * PLATFORM_WIDTH), y, PLATFORM_WIDTH, PLATFORM_HEIGHT, "jump_platform.png", MC_JUMP_SPEED))
        return platforms
    
    def generateBomb(self):
        platform = self.getRandomPlatform()
        while isinstance(platform, PressurePlatform):
            platform = self.getRandomPlatform()
        return Bomb(platform, 32, 32, "bomb.png")
    
    def addNewLayer(self):
        random_seed = PLATFORM_SEEDS[int(random(0, len(PLATFORM_SEEDS)))]
        newLayer = self.generatePlatformLayer(random_seed, self.topPlatformY)
        self.platformLayers.append(newLayer)
        self.topPlatformY -= LAYER_HEIGHT
        # with a 25% chance, add a shield power up or a shoot power up (50% chance each)
        if random(0, 1) < 1:
            if random(0, 1) < 0.5:
                self.shieldPowerUps.append(PowerUp(choice(newLayer), 32, 32, "shield-inactive.png"))
            else:
                self.shootingPowerUps.append(PowerUp(choice(newLayer), 32, 32))
        
    def destroyLowestLayer(self):
        for powerUp in self.shieldPowerUps:
            if powerUp.grabbedBy in self.platformLayers[0]:
                self.shieldPowerUps.remove(powerUp)
        for powerUp in self.shootingPowerUps:
            if powerUp.grabbedBy in self.platformLayers[0]:
                self.shootingPowerUps.remove(powerUp)
        del self.platformLayers[0]

    def getRandomPlatform(self):
        randomLayer = choice(self.platformLayers)
        randomPlatform = choice(randomLayer)
        return randomPlatform 

    def triggerBombExplosion(self):
        self.isBombExploding = True
        
    def score(self, score):
        self.enemy.hp -= score
        print(self.enemy.hp)
        if self.enemy.hp <= 0:
            self.enemyDeath.play()
            self.enemyDeath.rewind()
            self.isGameFinished = True
            self.bgMusic.pause()
            return

    def isOffScreen(self, entity):
        # take self.yOffset into account
        return entity.y + entity.h + self.yOffset < 0 or entity.y + self.yOffset > self.h or entity.x + entity.w < 0 or entity.x > self.w

    def cleanUp(self):
        self.mainCharacter.bullets = [bullet for bullet in self.mainCharacter.bullets if not self.isOffScreen(bullet)]
        self.enemy.bullets = [bullet for bullet in self.enemy.bullets if not self.isOffScreen(bullet)]
        self.enemy.lasers = [laser for laser in self.enemy.lasers if not laser.isFinished]
        # self.enemy.lasers = [laser for laser in self.enemy.lasers if not self.isOffScreen(laser)]
        # self.shieldPowerUps = [shieldPowerUp for shieldPowerUp in self.shieldPowerUps if not self.isOffScreen(shieldPowerUp)]
        # self.shootingPowerUps = [shootingPowerUp for shootingPowerUp in self.shootingPowerUps if not self.isOffScreen(shootingPowerUp)]
    

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
    def __init__(self, initialX, initialY, w, h, imgIdleName, imgWalkingName, totalFrames, imgShieldName, shieldFrames):
        Entity.__init__(self, initialX, initialY, w, h)
        self.keyHandler = {LEFT: False, RIGHT: False, UP: False, DOWN: False}
        self.flyMode = False
        self.imgIdle = loadImage(os.getcwd() + "/images/" + imgIdleName)
        self.imgWalking = loadImage(os.getcwd() + "/images/" + imgWalkingName)
        self.imgShield = loadImage(os.getcwd() + "/images/" + imgShieldName)
        self.shieldFrames = shieldFrames
        self.shieldFrame = 0
        self.frame = 0
        self.totalFrames = totalFrames
        self.isShieldUp = False
        self.shieldTimer = 0
        self.shieldDuration = 60 * 20
        self.isShooting = False
        self.shootInterval = 10
        self.shootTimer = 0
        self.bulletsRemaining = 0
        self.bullets = []

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
        if self.isShieldUp:
            fw = 200
            fh = 200
            imageMode(CENTER)
            image(self.imgShield, self.x + self.w / 2, self.y + self.h / 2 + yOffset, self.h, self.h, int(self.shieldFrame) * fw, 0, (int(self.shieldFrame) + 1) * fw, fh)
            imageMode(CORNER)
            self.shieldFrame = (self.shieldFrame + 0.2) % self.shieldFrames
        if self.velocityX > 0:
            image(self.imgWalking, self.x, self.y + yOffset, self.w, self.h, int(self.frame) * self.w, 0, (int(self.frame) + 1) * self.w, self.h)
            self.frame = (self.frame + 0.15) % self.totalFrames
        elif self.velocityX < 0:
            image(self.imgWalking, self.x, self.y + yOffset, self.w, self.h, (int(self.frame) + 1) * self.w, 0, int(self.frame) * self.w, self.h)
            self.frame = (self.frame + 0.15) % self.totalFrames
        else:
            image(self.imgIdle, self.x, self.y + yOffset, self.w, self.h)
        for bullet in self.bullets:
            bullet.display(yOffset)
        
    def startShooting(self):
        self.isShooting = True
        sc.game.playerShoot.play()
        sc.game.playerShoot.rewind()
        
        self.bulletsRemaining = 20

    def stopShooting(self):
        self.isShooting = False

    def shoot(self):
        if self.bulletsRemaining > 0:
            self.bullets.append(
                Bullet(
                    self.x + self.w / 2,
                    self.y + self.h / 2,
                    10,
                    10,
                    10,
                    0,
                )
            )
            self.bulletsRemaining -= 1

    def update(self):
        if self.isShooting and self.shootTimer >= self.shootInterval:
            self.shoot()
            self.shootTimer = 0
        else:
            self.shootTimer += 1
        for bullet in self.bullets:
            bullet.update()
        if self.isShieldUp:
            self.shieldTimer += 1
            if self.shieldDuration == self.shieldTimer:
                self.isShieldUp = False
                self.shieldTimer = 0

    def isCollidingGround(self, groundY):
        if self.y + self.h >= groundY:
            return True
        return False
   
   
class GrabbableEntity(Entity):
    def __init__(self, initialX, initialY, w, h, grabbedBy, imgName):
        Entity.__init__(self, initialX, initialY, w, h, imgName)
        self.grabbedBy = grabbedBy
        self.isGrabbed = False if grabbedBy is None else True
        self.update()
        
    def update(self):
        if self.isGrabbed:
            self.x = self.grabbedBy.x + self.grabbedBy.w / 2 - self.w / 2
            self.y = self.grabbedBy.y - self.h
    
    def grab(self, entity):
        self.isGrabbed = True
        self.grabbedBy = entity
    
    def release(self):
        self.isGrabbed = False
        self.grabbedBy = None


class Bomb(GrabbableEntity):
    def __init__(self, grabbedBy, w, h, imgName):
        GrabbableEntity.__init__(self, 0, 0, w, h, grabbedBy, imgName)

    def update(self):
        GrabbableEntity.update(self)
        if isinstance(self.grabbedBy, PressurePlatform):
            self.y -= 5
        

class Enemy(Entity):
    def __init__(self, initialX, initialY, w, h, imgName):
        Entity.__init__(self, initialX, initialY, w, h, imgName)
        self.bullets = []
        self.lasers = []
        self.shootInterval = int(random(50, 150))
        self.shootTimer = 0
        self.bulletCount=0
        self.hp = 1000
        
    def update(self, target):
        self.shootTimer += 1
        if self.hp == 0:
            print("You win!")
            return

        if self.shootTimer >= self.shootInterval:
            self.shoot(target)
            self.shootTimer = 0

        for laser in self.lasers:
            laser.update()
        
    def shoot(self, target):
        numBulletsPerShot = 1
        verticaDistanceBetweenbullets = 1

        targetX = target.x + target.w / 2
        targetY = target.y + target.h / 2
        
        if 700 < self.hp <= 900:
            for i in range(numBulletsPerShot):
                self.bullets.append(self.generateBullet(targetX, targetY, 32, 32))  # arbitrary values for now
                self.shootInterval = randint(50, 150)
                sc.game.fireBall.play()
                sc.game.fireBall.rewind()
                # self.bulletTypes= int(random(0,3))
                # self.hp -= 1        
        elif 500 <= self.hp <= 700:
            numBulletsPerShot = 1
            for i in range(numBulletsPerShot):
                self.bullets.append(self.generateBullet(targetX, targetY, 48, 48)) # arbitrary values for now
                
                self.shootInterval = randint(200, 250)
                sc.game.fireBall.play()
                sc.game.fireBall.rewind()
                # self.bulletTypes= int(random(0,3))
                # self.hp -= 1
        elif 3 < self.hp < 500:
            self.lasers.append(self.generateLaser(targetX, targetY, 15))
            self.shootInterval = randint(250, 300)
        elif self.hp<=0:
            game.enemyDeath.play()
            print("You win")
            
    def generateBullet(self, targetX, targetY, w, h):
        dx = targetX - (self.x + self.w / 2)
        dy = targetY - (self.y + self.h)
        angle = atan2(dy, dx)
        return Bullet(
            self.x + self.w / 2,
            self.y + self.h,
            w,
            h,
            5,
            angle,
            "fireball.png"
        )

    def generateLaser(self, targetX, targetY, w):
        return Laser(
            self.x + self.w // 2,
            self.y + self.h,
            targetX,
            targetY,
            w,
            2,
        )

    def display(self, yOffset):
        Entity.display(self, yOffset)
        for bullet in self.bullets:
            bullet.display(yOffset)

        for laser in self.lasers:
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


class PowerUp(GrabbableEntity):
    def __init__(self, grabbedBy, w, h, imgName=None):
        GrabbableEntity.__init__(self, 0, 0, w, h, grabbedBy, imgName)
        self.y -= 10
        self.color = color(255, 0, 0)
        self.duration = 60 * 20

    def display(self, yOffset):
        if self.img is None:
            fill(self.color)
            stroke(0)
            ellipse(self.x + self.w / 2, self.y + self.h / 2 + yOffset, self.w, self.h)
        else:
            GrabbableEntity.display(self, yOffset)

                
class Laser():
    def __init__(self, initialX, initialY, targetX, targetY, w, timeBeforeShooting):
            self.x = initialX
            self.y = initialY
            self.w = w
            self.timeBeforeShooting = timeBeforeShooting * 60
            k = (targetY - initialY) / (targetX - initialX)
            self.line = (k, initialY - k * initialX)
            self.isShooting = False
            self.shootingDuration = 30
            self.edges = self.findEdges()
            self.isFinished = False

    def update(self):
        self.timeBeforeShooting -= 1
        if self.timeBeforeShooting == 0:
            self.isShooting = True
        if self.isShooting:
            self.shootingDuration -= 1
            if self.shootingDuration == 0:
                self.isFinished = True


    def display(self, yOffset):
        fill(255, 0, 0)  # Red color for the laser
        stroke(255, 0, 0)
        # if not self.isShooting, display the laser line for half a second every second
        if not self.isShooting and frameCount % 30 < 15:
            self.displayLaserLine(yOffset)
        elif self.isShooting:
            # change the color of the laser to whit for the last 10 frames
            if self.shootingDuration <= 10:
                fill(255)
                stroke(255)
            self.displayLaser(yOffset)
            self.laser.play()
            self.laser.rewind()
        
    def displayLaserLine(self, yOffset):
        intersectionPoints = utils.computeLineIntersectionWithScreenEdges(self.line, CANVAS_WIDTH, CANVAS_HEIGHT)
        # append the point closest to the self.x, self.y
        closestPoint = intersectionPoints[0]
        for point in intersectionPoints:
            if utils.distanceBetweenPoints((self.x, self.y), point) < utils.distanceBetweenPoints((self.x, self.y), closestPoint):
                closestPoint = point
        line(self.x, self.y + yOffset, closestPoint[0], closestPoint[1] + yOffset)

    def displayLaser(self, yOffset):
        # draw the laser
        # quad(laserEdges[0][0], laserEdges[0][1] + yOffset, laserEdges[1][0], laserEdges[1][1] + yOffset, laserEdges[2][0], laserEdges[2][1] + yOffset, laserEdges[3][0], laserEdges[3][1] + yOffset)
        quad(self.edges[0], self.edges[1] + yOffset, self.edges[2], self.edges[3] + yOffset, self.edges[4], self.edges[5] + yOffset, self.edges[6], self.edges[7] + yOffset)

    def findEdges(self):
        # find two parallel lines at a distance of self.w from the laser line
        parallelLines = utils.computeParallelLinesAtDistance(self.line, self.w)
        # find the intersection points of the parallel lines and the screen edges
        laserEdges = [self.x - self.w, self.y, self.x + self.w, self.y]
        if self.line[0] > 0:
            parallelLines[0], parallelLines[1] = parallelLines[1], parallelLines[0]
        for parallelLine in parallelLines:
            intersectionPoints = utils.computeLineIntersectionWithScreenEdges(parallelLine, CANVAS_WIDTH, CANVAS_HEIGHT + 1000)
            # append the point closest to the self.x, self.y
            closestPoint = intersectionPoints[0]
            for point in intersectionPoints:
                if utils.distanceBetweenPoints((self.x, self.y), point) < utils.distanceBetweenPoints((self.x, self.y), closestPoint):
                    closestPoint = point
            laserEdges.append(closestPoint[0])
            laserEdges.append(closestPoint[1])
        return laserEdges


sc = ScreenController()

def setup():
    frameRate(60)
    size(sc.game.w, sc.game.h)


def draw():
    sc.display()
    sc.update()
    
def mouseClicked():
    sc.mouseClicked(mouseX, mouseY)

    
def keyPressed():
    if key == CODED:
        if keyCode == UP:
            sc.game.mainCharacter.keyHandler[UP] = True
        if keyCode == RIGHT:
            sc.game.mainCharacter.keyHandler[RIGHT] = True
        if keyCode == LEFT:
            sc.game.mainCharacter.keyHandler[LEFT] = True
        if keyCode == DOWN:
            sc.game.mainCharacter.keyHandler[DOWN] = True

    if key == 'c':
        del BULLETS[:]
    if key == 'k':
        # sc.game.enemy.shoot()
        sc.game.enemy.bullets.append(Bullet(sc.game.mainCharacter.x, sc.game.mainCharacter.y, 112, 128, 0, 0, "fireball.png"))
    if key == 'l':
        loop()
    if key == 'p':
        if sc.current_screen == GAME_SCREEN:
            sc.switchScreen(START_SCREEN)
    if key == 'f':
        sc.game.mainCharacter.flyMode = not sc.game.mainCharacter.flyMode
        
def keyReleased():
    if key == CODED:
        if keyCode == UP:
            sc.game.mainCharacter.keyHandler[UP] = False
        if keyCode == RIGHT:
            sc.game.mainCharacter.keyHandler[RIGHT] = False
        if keyCode == LEFT:
            sc.game.mainCharacter.keyHandler[LEFT] = False
        if keyCode == DOWN:
            sc.game.mainCharacter.keyHandler[DOWN] = False
