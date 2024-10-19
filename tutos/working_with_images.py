import pygame
import random

pygame.init()
SCREEN_WIDTH = 600
SCRING_HEIGHT = 400

screen = pygame.display.set_mode((SCREEN_WIDTH,SCRING_HEIGHT))
pygame.display.set_caption("WORKIN WITH IMAGES")


#define colours
WHITE = (255,255,255)
BG=(50,50,50)
GREEN=(0,255,0)
RED=(255,0,0)
BLUE=(0,0,255)

soldier = pygame.image.load("soldier.png").convert_alpha()
#w=soldier.get_width()
#h=soldier.get_height()
soldier = pygame.transform.scale_by(soldier,1.5)
multiplier= 1
for x in range(10):
    soldier = pygame.transform.rotate(soldier,1* multiplier)
    multiplier *= -1


#soldier2 = pygame.transform.rotate(soldier,-5)
#soldier2 = pygame.transform.flip(soldier,False,True)

run = True
while run:
    #update background
    screen.fill(BG)

    #draw image
    screen.blit(soldier,(50,50))
    #screen.blit(soldier2,(100,100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update display
    pygame.display.flip()
pygame.quit()
