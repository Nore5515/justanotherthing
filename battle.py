##########################################################################################################################################################
#DESIGN LAYOUT
##########################################################################################################################################################

#C:\Users\Nore5\AppData\Local\Programs\Python\Python38-32\python.exe "$(C:\Users\Nore5\Projects\Python\Battle\battle.py)"

# There are three paths, and each path has 10 perks.
# Whenever you level up, you're offered three perks at random, and one perk from your path that you chose.
# Max Level is 10. There are 11 Floors, 11th Floor is the boss, everything else is randomly generated monsters.

######### BUILD 1
######### You can begin the game, be able to move, attack and defeat an enemy, move up to the 11th floor and win.
######### OUTDATED: NOW LIVE MOVEMENT     It's placed on a 2D ascii array.

######### BUILD 2
######### Everything in Build 1, and...
######### There are at least three different options to do in combat. Enemies can deal damage and kill you. You can lose.
######### Enemies can move on the [NOW MAP] ascii array.

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
# TODO; Make a player class.
# TODO; Going up a floor clears all bullets    <-- should be easy?

##########################################################################################################################################################
#CODE AND STUFF
####################################################################################################################################################################################################################################################################################################################

import pygame
import math
import os
import copy
import random

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
        
        # Some variables for player position and movement and other playerly things
        self.playX = 100
        self.playY = 100
        self.floor = 1
        self.playHP = 30
        self.playSpeed = 0.2
        self.playBaseSpeed = self.playSpeed
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
        self.weapon = "Arrow"
        
        # Line variables
        drawingLine = False
        startX, startY = 0, 0
        endX, endY = 10, 10
        lineLength = 150
        
        # bullet bool dicts
        self.friendlyBullet = {
            "Enemy": False,
            "Player": True
        }
        self.enemyBullet = {
            "Enemy": True,
            "Player": False
        }
        
        # weapon stats. underscores mean defaults.
        self.weapons = {
            "Sword": Weapon("Sword", self),
            "Dagger": Weapon("Dagger", self),
            "Arrow": Weapon("Arrow", self),
            "Enemy": Weapon("Enemy", self)
        }
        
        # generate the dict of bullet types
        # width, length, speed, lifetime, deceleration, damage
        self.bulletDict = {
            "Arrow": self.weapons["Arrow"].bullet,
            "Sword": self.weapons["Sword"].bullet,
            "Dagger": self.weapons["Dagger"].bullet,
            "Enemy": self.weapons["Enemy"].bullet
        }
        
        # put all bullets in here
        self.bullets = []
        
        # generate all enemies for all floors (rn just one enemy per floor, but could be diff later)
        for i in range (0, 12):
            self.roomEnemies[i] = Enemy(300,300,50,50, 20, self.blue, 100, self.hitEffect, pygame.mixer.find_channel(), 0.1, self.bulletDict["Enemy"], 100)

        # TODO; CREATE ENEMY DICTIONARY

        # put all enemies in here
        self.enemies = []
        self.enemies.append(self.roomEnemies[self.floor])

        # generate all the stairs
        self.staircases = []
        self.staircases.append(Stairs("First Floor", int(width/2), int(3*height/4), 30, 30, self.blue, self))
        self.staircases[0].ExitPosition(int(width/2), int(height/4))
        
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
            # mouse binds are as follows;
            # M1 - 1, M2 - 3, scroll wheel click - 2
            # scroll wheel up - 4, scroll wheel down - 5
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x1, y1 = self.font.size("@")
                self.startX, self.startY = self.playX + (0.5*x1), self.playY+(0.5*y1)
                
                # fire a bullet towarsd your cursor!
                if event.button == 1:
                    self.bullets.append(self.bulletDict[self.weapon].start(self.startX, self.startY, x, y))
                    
                    # if alt-fire sword buffed, reset it.
                    #if self.sword["altBuffed"]:
                        #print (self.bulletDict["Sword"].damage)
                        #self.sword["Damage"] = self.sword["_Damage"]
                        #self.sword["Speed"] = self.sword["_Speed"]
                        #self.sword["altBuffed"] = False
                        #print ("REMOVING BUFF")
                        
                # alt fires!
                elif event.button == 3:
                
                    # a "dash", more liek a short ranged teleport
                    if self.weapon == "Dagger":
                        self.playSpeed *= 200
                    
                    # boost your next attack's speed and strength!
                    #elif self.weapon == "Sword" and not self.sword["altBuffed"]:
                        #self.sword["Damage"] *= 3
                        #self.sword["Speed"] *= 3
                        #self.sword["altBuffed"] = True
                        #print ("APPLYING BUFF")
                
                # switch weapons on mouse scroll
                elif event.button == 4:
                    if self.weapon == "Arrow":
                        self.weapon = "Sword"
                    elif self.weapon == "Sword":
                        self.weapon = "Dagger"
                    elif self.weapon == "Dagger":
                        self.weapon = "Arrow"
                elif event.button == 5:
                    if self.weapon == "Arrow":
                        self.weapon = "Dagger"
                    elif self.weapon == "Sword":
                        self.weapon = "Arrow"
                    elif self.weapon == "Dagger":
                        self.weapon = "Sword"
                
        # move player
        if self.movementBools["up"]:
            self.playY -= self.playSpeed
        if self.movementBools["down"]:
            self.playY += self.playSpeed
        if self.movementBools["left"]:
            self.playX -= self.playSpeed
        if self.movementBools["right"]:
            self.playX += self.playSpeed
        
        # if moving faster than base, reduce to base.
        # also could decelerte!
        if self.playSpeed > self.playBaseSpeed:
            self.playSpeed = self.playBaseSpeed

        # update player collision 
        self.playRect = pygame.Rect(int(self.playX), int(self.playY), self.x1, self.y1)

        # create top of screen GUI
        self.screen.blit(self.font.render(str(self.floor), True, self.blue), (int(self.width/32),int(self.height/32)))
        self.screen.blit(self.font.render(self.weapon, True, self.blue), (int(self.width/32), int(self.height/14)))
        self.screen.blit(self.font.render(str(self.playHP), True, self.blue), (int(self.width/2), int(self.height/32)))
        
        # create cursor
        pygame.draw.rect(self.screen, self.blue, pygame.Rect(pygame.mouse.get_pos(),(10,10)))

        # draw and update all staircases, check for player collision and enemy status.
        for i in range (0, len(self.staircases)):
            pygame.draw.rect(self.screen, self.staircases[i].color, self.staircases[i].body)
            self.playX, self.playY, self.floor, self.enemies = self.staircases[i].Update(self.playRect, self.playX, self.playY, self.floor, self.enemies)
        
        # move all bullets, then draw them!
        for i in range (0, len(self.bullets)):
            self.bullets[i].Move()
            #width = self.bullets[i].width
            #starVec, endVec = self.bullets[i].startVector, self.bullets[i].endVector
            pygame.draw.polygon(self.screen, self.blue, self.bullets[i].body)
            #pygame.draw.line(self.screen, self.blue, (int(starVec[0]), int(starVec[1])), (int(endVec[0]), int(endVec[1])), self.bullets[i].width)
            
        # if any bullets are out of bounds, remove them from bullets[]
        temp = []
        for i in range (0, len(self.bullets)):
            if not self.bullets[i].dead:
                temp.append(self.bullets[i])
        self.bullets = temp 
        
        # for all enemies, update them!
        for i in range (0, len(self.enemies)):
            self.enemies[i].Update(self)
        
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
        
        # now, for all remaining bullets, check to see if they hit player.
        for i in range (0, len(self.bullets)):
            if not self.bullets[i].friendlyBools["Player"]:
                for j in range (0, 4):
                    if self.playRect.collidepoint(self.bullets[i].body[j]):
                        self.playHP -= 1
                        self.bullets[i].dead = True
                        break
        
        # Now blit the player's icon onto the screen, and then update the whole display
        self.screen.blit(self.font.render("@", True, (self.blue)), (int(self.playX), int(self.playY)))
        pygame.display.update()
        
        # how many frames AT MAX you want per second
        self.clock.tick(3000)

class Weapon:

    # all you do is pass it the name, it handles the rest.
    # this is because I can't pass by reference >:(
    def __init__ (self, name, room):
        if name == "Sword":
            self.stats = {
                "Damage": 5,
                "_Damage": 5,
                "Speed": 0.5,
                "_Speed": 0.5,
                "Size": [30, 20],
                "_Size": [30,20],
                "Lifetime": 1000,
                "_Lifetime": 1000,
                "Decel": 0.0005,
                "_Decel": 0.0005,
                "altBuffed": False,
                "friendlyBools": room.friendlyBullet
            }
        elif name == "Dagger":
            self.stats = {
                "Damage": 2,
                "_Damage": 2,
                "Speed": 1.25,
                "_Speed": 1.25,
                "Size": [6, 30],
                "_Size": [6,30],
                "Lifetime": 600,
                "_Lifetime": 600,
                "Decel": 0.002,
                "_Decel": 0.002,
                "altBuffed": False,
                "friendlyBools": room.friendlyBullet
            }
        elif name == "Arrow":
            self.stats = {
                "Damage": 1,
                "_Damage": 1,
                "Speed": 1.50,
                "_Speed": 1.50,
                "Size": [3, 45],
                "_Size": [3,45],
                "Lifetime": 800,
                "_Lifetime": 800,
                "Decel": 0.001,
                "_Decel": 0.001,
                "altBuffed": False,
                "friendlyBools": room.friendlyBullet
            }
        elif name == "Enemy":
            self.stats = {
                "Damage": 1,
                "_Damage": 1,
                "Speed": 0.75,
                "_Speed": 0.75,
                "Size": [5, 30],
                "_Size": [5, 30],
                "Lifetime": 800,
                "_Lifetime": 800,
                "Decel": 0.001,
                "_Decel": 0.001,
                "altBuffed": False,
                "friendlyBools": room.enemyBullet
            }
        self.bullet = Bullet(self.stats["Size"][0], self.stats["Size"][1], self.stats["Speed"], self.stats["Lifetime"], self.stats["Decel"], self.stats["Damage"], self.stats["friendlyBools"])

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

# POTENTIAL ISSUE, SWORD BULLET CAN PASS OVER ENEMY IF AT THE RIGHT ANGLE
class Bullet:
    
    # just take in the basic information about the bullet. assing position using create.
    def __init__ (self, width, length, speed, lifetime, deceleration, damage, friendlyBools):
        # assigning variables.
        self.width, self.length, self.speed, self.lifetime, self.damage = width, length, speed, lifetime, damage
        self.dead = False
        self.deceleration = deceleration
        self.friendlyBools = friendlyBools

    """
    # a lot is going on, but in reality its not that bad.
    def __init__ (self, width, length, startX, startY, directionX, directionY, speed, lifetime, deceleration):
        # assigning variables.
        self.width, self.speed, self.lifetime = width, speed, lifetime
        self.dead = False
        self.deceleration = deceleration
        
        # create and assign the direction vector
        self.assignDirectionVector(startX, startY, directionX, directionY)
        
        # if it breaks, say too big!
        if math.sqrt((self.directionVector[0] * self.directionVector[0]) + (self.directionVector[1] * self.directionVector[1])) > 1:
            print ("TOO BIG!")
            
        # save the start vector, then create and save the end vector by multiplying the length by the direction vector.
        self.startVector = [startX, startY]
        self.endVector = [startX + self.directionVector[0]*length, startY + self.directionVector[1]*length]
    """
    
    # modified init, to allow for post-generation location updating, but not speed and stuff.
    # returns a copy of this class.
    def start (self, startX, startY, dirX, dirY):
        self.assignDirectionVector(startX, startY, dirX, dirY)
        self.startVector = [startX, startY]
        self.endVector = [startX + self.directionVector[0]*self.length, startY + self.directionVector[1]*self.length]
        self.generateBodyPoints()
        return copy.deepcopy(self)

    def generateBodyPoints(self):
        # create the bullet's rect body's points to draw
        self.body = [
            (int(self.endVector[0]-(self.width*self.directionVector[1])), int(self.endVector[1]+(self.width*self.directionVector[0]))),
            (int(self.startVector[0]-(self.width*self.directionVector[1])), int(self.startVector[1]+(self.width*self.directionVector[0]))),
            (int(self.startVector[0]+(self.width*self.directionVector[1])), int(self.startVector[1]-(self.width*self.directionVector[0]))),
            (int(self.endVector[0]+(self.width*self.directionVector[1])), int(self.endVector[1]-(self.width*self.directionVector[0])))
        ]
        #print (int(self.endVector[0]), int(self.endVector[1]), self.body)

    def assignDirectionVector(self, sX, sY, dX, dY):
        # get the deltaX and Y of the position. This is essentially the X and Y length from start vector and direction vector.
        deltaX = dX - sX
        deltaY = dY - sY
        
        # get the distance between start and direction vector.
        endLength = math.sqrt((deltaX * deltaX) + (deltaY * deltaY))
        
        # create and save the direction vector, aka a 1 length vector pointing from the start vector to the direction vector
        self.directionVector = [(deltaX/endLength), (deltaY/endLength)]

    # updates self on position based on direction and speed
    def Move(self):
    
        self.generateBodyPoints()
    
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
        
        # decelerate the speed if it's greater than 0!
        if self.speed > 0:
            self.speed -= self.deceleration
        
        # if not dead, tick down the lifetime. Once lifetime hits 0, its dead.
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.dead = True

# IDEA; enemy health tied to their color? like, darker = healtheri, lighter = injured?
class Enemy:

    def __init__ (self, posX, posY, sizeX, sizeY, health, color, duration, hitSound, hitChannel, speed, bullet, inaccuracy):
        self.coordinates = [posX, posY]
        self.size = [sizeX, sizeY]
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
        self.speed = speed
        self.count = 0
        self.bullet = bullet
        self.inaccuracy = inaccuracy

    # runs every turn.
    # takes in a list of all current enemies, as well as the player's rect
    def Update (self, room):

        # every so often, fire a bullet at the player
        self.count += 1
        if self.count % 150 == 0:
            self.FireBullet(room)

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

        # chases the player
        if self.coordinates[0]+(0.5*self.size[0]) < room.playX-(0.5*room.playRect.width):
            self.coordinates[0] += self.speed
        elif self.coordinates[0]-(0.5*self.size[0]) > room.playX+(0.5*room.playRect.width):
            self.coordinates[0] -= self.speed
        if self.coordinates[1]+(0.5*self.size[1]) < room.playY-(0.5*room.playRect.height):
            self.coordinates[1] += self.speed
        elif self.coordinates[1]-(0.5*self.size[1]) > room.playY+(0.5*room.playRect.height):
            self.coordinates[1] -= self.speed

        # updates the enemy rect
        self.body = pygame.Rect(int(self.coordinates[0]), int(self.coordinates[1]), int(self.size[0]), int(self.size[1]))

    # fires a given bullet from this enemy towards the player, then adds the bullet to the bullet list
    # the destination point is a point that is 0 to Inaccuracy away from the player.
    def FireBullet(self, room):
        aimVec = [room.playX + (random.uniform(-1,1) * self.inaccuracy), room.playY + (random.uniform(-1,1) * self.inaccuracy)]
        room.bullets.append(self.bullet.start(self.coordinates[0]+(self.size[0]*0.5), self.coordinates[1]+(self.size[1]*0.5), aimVec[0], aimVec[1]))

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
            if not bullets[i].dead and not bullets[i].friendlyBools["Enemy"]:
                for j in range (0, 4):
                    if self.body.collidepoint(bullets[i].body[j]):
                        self.health -= bullets[i].damage
                        bullets[i].dead = True
                        self.Flash()
                        break
        
        # If you're outta health, you're outta luck.
        if self.health <= 0:
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
        
        if roomish.playHP <= 0:
            roomish.running = False
            print ("GAME OVER!")
        
        # create top of screen GUI
        screen.blit(roomish.font.render(str(roomish.floor), True, roomish.blue), (int(roomish.width/32),int(roomish.height/32)))

main()
print ("\nHello World!")



































