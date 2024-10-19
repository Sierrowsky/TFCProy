import pygame
import math

pygame.init()

#define screen size 
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

#create game window 
scree = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("ROTATING OBJECTS")

#define colouts
BG = (255,255,255)
BLACK = (0,0,0)

turret_ori = pygame.image.load("turret.png").convert_alpha()
x = 500
y = 300

#game loop
run = True
while run:
    #upfate backgroynd
    scree.fill(BG)

    #get mouse position 
    pos = pygame.mouse.get_pos()

    #calculate turret angle
    x_dist = pos[0] - x
    y_dist = -(pos[1] - y) # - ve because pygame y coordinates incriase down the screen
    angle = math.degrees(math.atan2(y_dist,x_dist))


    #rotate turret
    turret = pygame.transform.rotate(turret_ori,angle- 90)
    turret_rect=turret.get_rect(center = (x,y))

    #draw image
    scree.blit(turret,turret_rect)

    #event handler
    for event in pygame.event.get():
        #quit program
        if event.type == pygame.QUIT:
            run = False
    #update display
    pygame.display.flip()
pygame.quit()
