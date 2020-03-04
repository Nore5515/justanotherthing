##########################################################################################################################################################
#DESIGN LAYOUT
##########################################################################################################################################################

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

class Room:
    
    # Takes in width and height on initialization
    def __init__ (self, width, height):
        self.width = width
        self.height = height
    
    # Displays a box of dots with the rooms proportions
    def display (self):
        s = ""
        for x in range (0, self.height):
            for y in range (0, self.width):
                s += (".")
                #print (".", end = "", sep = '')
            s += ("\n")
            #print ("\n", end = "", sep = '')
        return s

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
        self.tempCount = 0
        self.tempTemp = self.hit.get_num_channels()
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
    room = Room(10,4)
    print(room.display())
    
    # create a surface on screen that has 240x180 size
    screen = pygame.display.set_mode((1080,680))
    
    # initialize pygame and the sound mixer
    pygame.mixer.init(44100, -16, 2, 4096)
    pygame.init()
    
    # create a few tools to help make everything run smoothly.
    clock = pygame.time.Clock()     # helps regulate FPS
    hitEffect = pygame.mixer.Sound('thump.ogg')       # the enemy hit sound
    
    # fill it with white!
    white = [255, 255, 255] 
    green = [0, 255, 0] 
    blue = [0, 0, 128]
    screen.fill(white)
    
    # Set it's caption to...Battle.yeah?
    pygame.display.set_caption('Battle.yeah') 
    
    # Create a font for text to be used on screen
    font = pygame.font.Font('freesansbold.ttf', 32) 
    
    # Display text
    screen.blit(font.render(room.display(), True, (blue)), (250, 115))

    # Updates screen to match new changes.
    pygame.display.update()

    # put all enemies in here
    enemies = []
    enemies.append(Enemy(300,300,50,50, 200, blue, 100, hitEffect, pygame.mixer.find_channel()))
    
    running = True

    # Some variables for player position
    playX = 100
    playY = 100
    movementBools = {
        "up": False,
        "down": False,
        "left": False,
        "right": False
    }
    
    # Line variables
    drawingLine = False
    startX, startY = 0, 0
    endX, endY = 10, 10
    lineLength = 150
    
    # put all bullets in here
    bullets = []
    #bullets.append(Bullet(3, 50, startX, startY, endX, endY, 0.4))
    #line = bullets[0]

    while running:
        screen.fill(white)
            
        # Gets ALL events from the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            # If event is WASD, modify player movement bools
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    movementBools["up"] = True
                if event.key == pygame.K_s:
                    movementBools["down"] = True
                if event.key == pygame.K_a:
                    movementBools["left"] = True
                if event.key == pygame.K_d:
                    movementBools["right"] = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    movementBools["up"] = False
                if event.key == pygame.K_s:
                    movementBools["down"] = False
                if event.key == pygame.K_a:
                    movementBools["left"] = False
                if event.key == pygame.K_d:
                    movementBools["right"] = False
                    
            # On click, fire a bullet from player aimed at the cursor
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x1, y1 = font.size("@")
                startX, startY = playX + (0.5*x1), playY+(0.5*y1)
                bullets.append(Bullet(3, 50, startX, startY, x, y, 0.5))
        
        # create cursor
        pygame.draw.rect(screen, blue, pygame.Rect(pygame.mouse.get_pos(),(10,10)))
        
        # for all enemies, update them!
        for i in range (0, len(enemies)):
            enemies[i].Update()
        
        # for all enemies, draw them, then check to see if any of them were hit by bullets
        for i in range (0, len(enemies)):
            pygame.draw.rect(screen, enemies[i].color, enemies[i].body)
            enemies[i].BulletHit(bullets)
        
        # remove all hit enemies enemies[]
        temp = []
        for i in range (0, len(enemies)):
            if not enemies[i].dead:
                temp.append(enemies[i])
        enemies = temp
        
        # move all bullets, then draw them!
        for i in range (0, len(bullets)):
            bullets[i].Move()
            pygame.draw.line(screen, blue, (int(bullets[i].startVector[0]), int(bullets[i].startVector[1])), (int(bullets[i].endVector[0]), int(bullets[i].endVector[1])), bullets[i].width)
            
        # if any bullets are out of bounds, remove them from bullets[]
        temp = []
        for i in range (0, len(bullets)):
            if not bullets[i].dead:
                temp.append(bullets[i])
        bullets = temp

        # move player
        if movementBools["up"]:
            playY -= 0.2
        if movementBools["down"]:
            playY += 0.2
        if movementBools["left"]:
            playX -= 0.2
        if movementBools["right"]:
            playX += 0.2
        
        # Now manipulate all the on screen objects
        screen.blit(font.render("@", True, (blue)), (int(playX), int(playY)))
        pygame.display.update()
        
        # how many frames AT MAX you want per second
        clock.tick(3000)

main()
print ("\nHello World!")































