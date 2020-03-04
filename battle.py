##########################################################################################################################################################
#DESIGN LAYOUT
##########################################################################################################################################################

#C:\Users\Nore5\AppData\Local\Programs\Python\Python38-32\python.exe "$(C:\Users\Nore5\Projects\Python\Battle\battle.py)"

# There are three paths, and each path has 10 perks.
# Whenever you level up, you're offered three perks at random, and one perk from your path that you chose.
# Max Level is 10. There are 11 Floors, 11th Floor is the boss, everything else is randomly generated monsters.

# BUILD 1
# You can begin the game, be able to move, attack and defeat an enemy, move up to the 11th floor and win.
# OUTDATED: NOW LIVE MOVEMENT     It's placed on a 2D ascii array.

# BUILD 2
# Everything in Build 1, and...
# There are at least three different options to do in combat. Enemies can deal damage and kill you. You can lose.
# Enemies can move on the ascii array.

# BUILD 3
# Everything in Build 1 and 2, and...
# When finishing a level, you can select a perk from 3 randomly provided perks. There are at least 10 perks. You cannot pick the same perk more than once.

# BUILD 4
# Everything in Build 1, 2, 3, and...
# There are at least 15 Perks. You may pick a path when the game starts. Three perks are randomly provided, and a fourth in a perk selected from your path (at random).
# You only provide perks you don't have.

# BUILD 5
# Everything in Build 1, 2, 3, 4, and...
# There is a boss on floor 11 which requires some strategy to beat. There are at least 20 Perks. Perks synergize with other perks from the same path.
# There can be multiple enemies per floor.

# BUILD 6
# Everything in Build 1, 2, 3, 4, 5, and...
# Floors have a variety of designs, which can be used to your advantage. Environmental hazzards and ways to manipulate it to your advantage.
# Enemies drop money and items, which can be picked up. There are at least 3 items. There are at least 25 Perks.

# BUILD 7
# Everything in Build 1, 2, 3, 4, 5, 6, and...
# There is a shop every 3rd floor, and before the 11th floor (the 10.5th floor). You can spend collected money here for items and perks. At least 10 items exist.
# Enemies can utilize environmental traits to their advantage. Other environmental effects can cross-affect other environmental effects.

# BUILD 8
# Everything is in place...
# There is a main menu, a settings menu, various game modes (Arena? Speedrun?), at least 30 Perks, and 20 items.
# At least 6 different types of enemies, and 2 types of bosses. 

# Idea, what if every second it paused and you could do stuff? live action turn based?

##########################################################################################################################################################
#CODE AND STUFF
####################################################################################################################################################################################################################################################################################################################

import pygame
import math
import os

print ()

# Need to make this the "manager"
class Room:
    
    # Takes in width and height on initialization
    def __init__ (self, width, height):
    
        # create a surface on screen that has 240x180 size
        self.screen = pygame.display.set_mode((width, height))
        
        # fill it with white!
        self.white = [255, 255, 255] 
        self.green = [0, 255, 0] 
        self.blue = [0, 0, 128]
        self.screen.fill(self.white)
        
        # Create a font for text to be used on screen
        self.font = pygame.font.Font('freesansbold.ttf', 32) 
        
        # Some variables for player position
        self.playX = 100
        self.playY = 100
        self.floor = 1
        self.x1, self.y1 = self.font.size("@")
        self.playRect = pygame.Rect(self.playX, self.playY, self.x1, self.y1)
        self.movementBools = {
            "up": False,
            "down": False,
            "left": False,
            "right": False
        }
        
        # create a few tools to help make everything run smoothly.
        self.clock = pygame.time.Clock()     # helps regulate FPS
        self.hitEffect = pygame.mixer.Sound('thump.ogg')       # the enemy hit sound
        
        # assign variables
        self.width = width
        self.height = height
        self.roomEnemies = {}
        self.running = True
        
        # Line variables
        drawingLine = False
        startX, startY = 0, 0
        endX, endY = 10, 10
        lineLength = 150
        
        # generate all enemies for all floors (rn just one enemy per floor, but could be diff later)
        for i in range (0, 12):
            self.roomEnemies[i] = Enemy(300,300,50,50, 2, self.blue, 100, self.hitEffect, pygame.mixer.find_channel())

        # put all enemies in here
        self.enemies = []
        self.enemies.append(Enemy(300,300,50,50, 20, self.blue, 100, self.hitEffect, pygame.mixer.find_channel()))

        # generate all the stairs
        self.staircases = []
        self.staircases.append(Stairs("First Floor", int(width/2), int(3*height/4), 30, 30, self.blue, self))
        self.staircases[0].ExitPosition(int(width/2), int(height/4))
        
        # put all bullets in here
        self.bullets = []
        
    # note to self; break this big update into many smaller updates.
    def Update (self):
        self.screen.fill(self.white)
        
        # Gets ALL events from the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            # If event is WASD, modify player movement bools
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.movementBools["up"] = True
                if event.key == pygame.K_s:
                    self.movementBools["down"] = True
                if event.key == pygame.K_a:
                    self.movementBools["left"] = True
                if event.key == pygame.K_d:
                    self.movementBools["right"] = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.movementBools["up"] = False
                if event.key == pygame.K_s:
                    self.movementBools["down"] = False
                if event.key == pygame.K_a:
                    self.movementBools["left"] = False
                if event.key == pygame.K_d:
                    self.movementBools["right"] = False
                    
            # On click, fire a bullet from player aimed at the cursor
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x1, y1 = self.font.size("@")
                self.startX, self.startY = self.playX + (0.5*x1), self.playY+(0.5*y1)
                self.bullets.append(Bullet(3, 50, self.startX, self.startY, x, y, 0.5))
                
        # move player
        if self.movementBools["up"]:
            self.playY -= 0.2
        if self.movementBools["down"]:
            self.playY += 0.2
        if self.movementBools["left"]:
            self.playX -= 0.2
        if self.movementBools["right"]:
            self.playX += 0.2

        # update player collision rect
        self.playRect = pygame.Rect(int(self.playX), int(self.playY), self.x1, self.y1)

        # create top of screen GUI
        self.screen.blit(self.font.render(str(self.floor), True, self.blue), (int(self.width/32),int(self.height/32)))
        
        # create cursor
        pygame.draw.rect(self.screen, self.blue, pygame.Rect(pygame.mouse.get_pos(),(10,10)))

        # draw and update all staircases, check for player collision and enemy status.
        for i in range (0, len(self.staircases)):
            pygame.draw.rect(self.screen, self.staircases[i].color, self.staircases[i].body)
            self.playX, self.playY, self.floor, self.enemies = self.staircases[i].Update(self.playRect, self.playX, self.playY, self.floor, self.enemies)
        
        # move all bullets, then draw them!
        for i in range (0, len(self.bullets)):
            self.bullets[i].Move()
            pygame.draw.line(self.screen, self.blue, (int(self.bullets[i].startVector[0]), int(self.bullets[i].startVector[1])), (int(self.bullets[i].endVector[0]), int(self.bullets[i].endVector[1])), self.bullets[i].width)
            
        # if any bullets are out of bounds, remove them from bullets[]
        temp = []
        for i in range (0, len(self.bullets)):
            if not self.bullets[i].dead:
                temp.append(self.bullets[i])
        self.bullets = temp 
        
        # for all enemies, update them!
        for i in range (0, len(self.enemies)):
            self.enemies[i].Update()
        
        # for all enemies, draw them, then check to see if any of them were hit by bullets
        for i in range (0, len(self.enemies)):
            pygame.draw.rect(self.screen, self.enemies[i].color, self.enemies[i].body)
            self.enemies[i].BulletHit(self.bullets)
        
        # remove all hit enemies enemies[]
        temp = []
        for i in range (0, len(self.enemies)):
            if not self.enemies[i].dead:
                temp.append(self.enemies[i])
        self.enemies = temp
        
        # Now blit the player's icon onto the screen, and then update the whole display
        self.screen.blit(self.font.render("@", True, (self.blue)), (int(self.playX), int(self.playY)))
        pygame.display.update()
        
        # how many frames AT MAX you want per second
        self.clock.tick(3000)

class Stairs:

    def __init__ (self, name, posX, posY, width, height, color, room):
        self.name, self.color = name, color
        self.baseColor = self.color
        self.open = False
        self.body = pygame.Rect(posX, posY, width, height)
        self.room = room
    
    def ExitPosition (self, posX, posY):
        self.exitPoint = [posX, posY]
    
    def Update (self, player, playX, playY, floor, enemies):
        # if there are enemies, make the door red and inaccesable. otherwise, blue and open!
        if len(enemies) > 0:
            self.color = [128, 0, 0]
            self.open = False
        else:
            self.color = self.baseColor
            self.open = True

        # if the player collides, teleport the player to the exit point, and increase floor by 1
        if self.body.colliderect(player) and self.open:
            playX = self.exitPoint[0]
            playY = self.exitPoint[1]
            floor += 1
            if floor >= 12:
                print("WOOHOO!")
            else:
                enemies.append(self.room.roomEnemies[floor])
        return playX, playY, floor, enemies

class Bullet:
    
    # a lot is going on, but in reality its not that bad.
    def __init__ (self, width, length, startX, startY, directionX, directionY, speed):
        # assigning variables.
        self.width, self.speed  = width, speed
        self.dead = False
        
        # get the deltaX and Y of the position. This is essentially the X and Y length from start vector and direction vector.
        deltaX = directionX - startX
        deltaY = directionY - startY
        
        # get the distance between start and direction vector.
        endLength = math.sqrt((deltaX * deltaX) + (deltaY * deltaY))
        
        # create and save the direction vector, aka a 1 length vector pointing from the start vector to the direction vector
        self.directionVector = [(deltaX/endLength), (deltaY/endLength)]
        
        # if it breaks, say too big!
        if math.sqrt((self.directionVector[0] * self.directionVector[0]) + (self.directionVector[1] * self.directionVector[1])) > 1:
            print ("TOO BIG!")
            
        # save the start vector, then create and save the end vector by multiplying the length by the direction vector.
        self.startVector = [startX, startY]
        self.endVector = [startX + self.directionVector[0]*length, startY + self.directionVector[1]*length]
        
    # updates self on position based on direction and speed
    def Move(self):
        # update all variables to new positions
        self.startVector[0] += self.speed * self.directionVector[0]
        self.startVector[1] += self.speed * self.directionVector[1]
        self.endVector[0] += self.speed * self.directionVector[0]
        self.endVector[1] += self.speed * self.directionVector[1]
        
        # flag for removal if out of bounds
        w, h = pygame.display.get_surface().get_size()
        if self.startVector[0] > w and self.endVector[0] > w:
            self.dead = True
        if self.startVector[0] < 0 and self.endVector[0] < 0:
            self.dead = True
        if self.startVector[1] > h and self.endVector[1] > h:
            self.dead = True
        if self.startVector[1] < 0 and self.startVector[1] < 0:
            self.dead = True

# IDEA; enemy health tied to their color? like, darker = healtheri, lighter = injured?
class Enemy:

    def __init__ (self, posX, posY, sizeX, sizeY, health, color, duration, hitSound, hitChannel):
        self.body = pygame.Rect(posX, posY, sizeX, sizeY)
        self.dead = False
        self.health = health
        self.color = color
        self.originalColor = color
        self.flashColor = [(color[0]+60), (color[1]+60), (color[2]+60)]
        self.duration = 0
        self.flashDuration = duration
        self.hit = hitSound
        self.channel = hitChannel
        self.playingSound = False
    
    # runs every turn.
    def Update (self):
        
        # if you started a sound, countdown until sound is over. once its over, stop the channel.
        if self.playingSound:
            if self.tempCount > 0:
                self.tempCount -= 1
            else:
                self.tempCount = 0
                self.playingSound = False
                self.channel.stop()
        
        # manages the flashy flashy thing
        if self.duration > 0:
            self.duration -= 1
        if self.duration == 0:
            if self.color == self.flashColor:
                self.color = self.originalColor
    
    # use this whenever a bullet hits the enemy. Clears the channel, resets the sound timer, and starts a new sound
    def StartSound(self):
        self.channel.stop()
        self.tempCount = 190
        self.playingSound = True
        self.channel.play(self.hit)
    
    # when hit by a bullet, cause this to change color to flash color.
    def Flash (self):
    
        # when hit, play a sound
        self.StartSound()
        
        # also, if you're the base color, swap to the flash color. in update, you'll autoflip back after some frames
        if self.color == self.originalColor:
            self.color = self.flashColor
            self.duration = self.flashDuration
            
            
    # for all bullets, if a bullet has either end point inside this rect, reduce health by 1 and kill bullet. flash.
    def BulletHit (self, bullets):
        for i in range (0, len(bullets)):
            if not bullets[i].dead:
                if self.body.collidepoint(int(bullets[i].startVector[0]), int(bullets[i].startVector[1])):
                    self.health -= 1
                    bullets[i].dead = True
                    self.Flash()
                elif self.body.collidepoint(int(bullets[i].endVector[0]), int(bullets[i].endVector[1])):
                    self.health -= 1
                    bullets[i].dead = True
                    self.Flash()
        
        # If you're outta health, you're outta luck.
        if self.health < 0:
            self.dead = True
            self.hit.stop()

def main():
    
    # initialize pygame and the sound mixer
    pygame.mixer.init(44100, -16, 2, 4096)
    pygame.init()
    

    
    
    
    # Set it's caption to...Battle.yeah?
    pygame.display.set_caption('Battle.yeah') 
    
    # Create the "Room"
    roomish = Room(1080,680)
    
    # get the screen
    screen = roomish.screen

    # Updates screen to match new changes.
    pygame.display.update()

    # put all enemies in here
    enemies = roomish.enemies
    
    # TEMP colors
    white = [255, 255, 255] 
    green = [0, 255, 0] 
    blue = [0, 0, 128]
    screen.fill(white)

    # stairs!
    w, h = pygame.display.get_surface().get_size()
    staircases = roomish.staircases
    
    # generic objects and stage props to render
    stageText = {}
    stageProps = {}
    
    # put all bullets in here
    bullets = []
    #bullets.append(Bullet(3, 50, startX, startY, endX, endY, 0.4))
    #line = bullets[0]

    while roomish.running:
        roomish.Update()
        
        # create top of screen GUI
        screen.blit(roomish.font.render(str(roomish.floor), True, roomish.blue), (int(roomish.width/32),int(roomish.height/32)))


main()
print ("\nHello World!")



































