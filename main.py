import pygame

pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

player = pygame.Rect((300,250,50,50))

top = pygame.Rect(0,0,SCREEN_WIDTH,10)
left = pygame.Rect(0,0,10,SCREEN_HEIGHT)
bot = pygame.Rect(0,SCREEN_HEIGHT-10,SCREEN_WIDTH,10)
right = pygame.Rect(SCREEN_WIDTH-10,0,10,SCREEN_HEIGHT)
 
run = True
while run:

    screen.fill((0,0,0))
    
    pygame.draw.rect(screen,(125,125,125),top)
    pygame.draw.rect(screen,(125,125,125),left)
    pygame.draw.rect(screen,(125,125,125),right)
    pygame.draw.rect(screen,(125,125,125),bot)

    pygame.draw.rect(screen,(255,0,0),player)

    key = pygame.key.get_pressed()
    if key[pygame.K_a]==True and not player.colliderect(left):
        player.move_ip(-1,0)
    elif key[pygame.K_d]==True and not player.colliderect(right):
        player.move_ip(1,0)
    elif key[pygame.K_w]==True and not player.colliderect(top):
        player.move_ip(0,-1)
    elif key[pygame.K_s]==True and not player.colliderect(bot):
        player.move_ip(0,1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()