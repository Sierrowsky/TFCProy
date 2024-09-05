import pygame
from pygame.sprite import Group
pygame.init()

#define screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("MASKS")

#define colours
WHITE = (255,255,255)
BG=(0,0,0)
GREEN=(0,255,0)
RED=(255,0,0)
BLUE=(0,0,255)

#create soldier 
class Soldier(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("soldier.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft=(x,y)
        self.mask = pygame.mask.from_surface(self.image)

#create bullet and mask
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 5))
        self.rect = self.image.get_rect()
        self.image.fill(RED)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, colour):
        pos = pygame.mouse.get_pos()
        self.rect.center = (pos)
        self.image.fill(colour)

#hide cursor
pygame.mouse.set_visible(False)

#create instances of soldier and bullet
soldier = Soldier(350,250)
bullet = Bullet()

#create soldier and bullet groups 
soldier_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

#add instances to groups
soldier_group.add(soldier)
bullet_group.add(bullet)

#game loop
run = True
while run:

    #update background
    screen.fill(BG)
    
    if pygame.sprite.spritecollide(bullet,soldier_group,False):
        col = BLUE
        if pygame.sprite.spritecollide(bullet,soldier_group,False,pygame.sprite.collide_mask):
            col = RED
    else:
        col = GREEN

    bullet_group.update(col)
    
    soldier_group.draw(screen)
    bullet_group.draw(screen)
    pygame.draw.rect(screen,WHITE,soldier.rect,1)

    

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    #update display
    pygame.display.flip()

pygame.quit()