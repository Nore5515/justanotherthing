##########################################################################################################################################################
#DESIGN LAYOUT
##########################################################################################################################################################

# There are three paths, and each path has 10 perks.
# Whenever you level up, you're offered three perks at random, and one perk from your path that you chose.
# Max Level is 10. There are 11 Floors, 11th Floor is the boss, everything else is randomly generated monsters.

# BUILD 1
# You can begin the game, be able to move, attack and defeat an enemy, move up to the 11th floor and win.
# It's placed on a 2D ascii array.

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


##########################################################################################################################################################
#CODE AND STUFF
####################################################################################################################################################################################################################################################################################################################

import pygame
import math

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
    
    def __init__ (self, width, length, startX, startY, directionX, directionY, speed):
        self.width, self.length, self.startX, self.startY, self.speed  = width, length, startX, startY, speed
        deltaX = directionX - startX
        deltaY = directionY - startY
        length = math.sqrt((deltaX * deltaX) + (deltaY * deltaY))
        self.directionVector = [(deltaX/length), (deltaY/length)]
        if math.sqrt((self.directionVector[0] * self.directionVector[0]) + (self.directionVector[1] * self.directionVector[1])) > 1:
            print ("TOO BIG!")
        self.startVector = [self.startX, self.startY]
        self.endVector = [self.startX + self.directionVector[0]*self.length, self.startY + self.directionVector[1]*self.length]
        
    # updates self on position based on direction and speed
    def Move(self):
        self.startVector[0] += self.speed * self.directionVector[0]
        self.startVector[1] += self.speed * self.directionVector[1]
        self.endVector[0] += self.speed * self.directionVector[0]
        self.endVector[1] += self.speed * self.directionVector[1]
        


def main():
    room = Room(10,4)
    print(room.display())
    pygame.init()
    
    # create a surface on screen that has 240x180 size
    screen = pygame.display.set_mode((1080,680))
    
    # fill it with white!
    white = (255, 255, 255) 
    green = (0, 255, 0) 
    blue = (0, 0, 128) 
    screen.fill(white)
    
    # Set it's caption to...Battle.yeah?
    pygame.display.set_caption('Battle.yeah') 
    
    # Create a font for text to be used on screen
    font = pygame.font.Font('freesansbold.ttf', 32) 
    
    # Display text
    screen.blit(font.render(room.display(), True, (blue)), (250, 115))

    # Updates screen to match new changes.
    pygame.display.update()

    
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
    bullets.append(Bullet(3, 50, startX, startY, endX, endY, 0.4))
    line = bullets[0]

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
                    
            # On click, draw line from player to cursor
            elif event.type == pygame.MOUSEBUTTONDOWN:
                drawingLine = True
                x, y = pygame.mouse.get_pos()
                x1, y1 = font.size("@")
                startX, startY = playX + (0.5*x1), playY+(0.5*y1)
                bullets.append(Bullet(3, 50, startX, startY, x, y, 0.5))
            elif event.type == pygame.MOUSEBUTTONUP:
                drawingLine = False
        
        # create cursor
        pygame.draw.rect(screen, blue, pygame.Rect(pygame.mouse.get_pos(),(10,10)))
        
        """
        # draw line
        if drawingLine:
            x, y = font.size("@")
            startX, startY = playX + (0.5*x), playY+(0.5*y)
            endX, endY = pygame.mouse.get_pos()
            pygame.draw.line(screen, blue, (int(startX), int(startY)), (int(endX), int(endY)), 1)
        """
        
        # draw ALL bullets in bullets[]
        for i in range (0, len(bullets)):
            pygame.draw.line(screen, blue, (int(bullets[i].startVector[0]), int(bullets[i].startVector[1])), (int(bullets[i].endVector[0]), int(bullets[i].endVector[1])), bullets[i].width)
            bullets[i].Move()
        #pygame.draw.line(screen, blue, (int(line.startVector[0]), int(line.startVector[1])), (int(line.endVector[0]), int(line.endVector[1])), line.width)
        #line.Move()

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


    

main()
print ("\nHello World!")































