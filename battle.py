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

    while running:
        screen.fill(white)
        # Gets ALL events from the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    

main()
print ("\nHello World!")































