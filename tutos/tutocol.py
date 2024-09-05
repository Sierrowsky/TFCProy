import pygame
import random

pygame.init()
SCREEN_WIDTH = 600
SCRING_HEIGHT = 400

screen = pygame.display.set_mode((SCREEN_WIDTH,SCRING_HEIGHT))
pygame.display.set_caption("Collision")

#create main rectangle & obstacle rectangle
#rect_1 = pygame.Rect(0,0,25,25)

obstacles = []
for _ in range(16):
    obstacle_rect=pygame.Rect(random.randint(0,500),random.randint(0,300),25,25)
    obstacles.append(obstacle_rect)

line_start = (SCREEN_WIDTH/2,SCRING_HEIGHT/2)

#define colours
WHITE = (255,255,255)
BG=(50,50,50)
GREEN=(0,255,0)
RED=(255,0,0)
BLUE=(0,0,255)

#hide mouse cursor
#pygame.mouse.set_visible(False)

run = True
while run:
    #update background
    screen.fill(BG)

    pos = pygame.mouse.get_pos()
    pygame.draw.line(screen,WHITE,line_start,pos,5)



    #set colour
    #col = GREEN
    #if rect_1.collidelist(obstacles) >= 0:
    #    print(rect_1.collidelist(obstacles))
    #    col = RED

    #get mouse coordinates and use them to position the rectangle
    pos = pygame.mouse.get_pos()
    #rect_1.center=pos

    #draw all rectangles
    #pygame.draw.rect(screen,col,rect_1)
    for obstacle in obstacles:
        if obstacle.clipline((line_start,pos)):
            pygame.draw.rect(screen,RED,obstacle)
        else:
            pygame.draw.rect(screen,GREEN,obstacle)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update display
    pygame.display.flip()
pygame.quit()
