import pygame

pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

soldier = pygame.image.load("Soldier.png").convert_alpha()

player = soldier.get_rect()

clock = pygame.time.Clock()

top = pygame.Rect(0,0,SCREEN_WIDTH,10)
left = pygame.Rect(0,0,10,SCREEN_HEIGHT)
bot = pygame.Rect(0,SCREEN_HEIGHT-10,SCREEN_WIDTH,10)
right = pygame.Rect(SCREEN_WIDTH-10,0,10,SCREEN_HEIGHT)
 

clicked = False

text_font= pygame.font.Font("turok.otf",30)

def draw_text(text,font,text_col,x,y):
    img = font.render(text, True, text_col)
    screen.blit(img,(x,y))
run = True
while run:
    clock.tick(60)

    screen.fill((0,0,0))
    
    pygame.draw.rect(screen,(125,125,125),top)
    pygame.draw.rect(screen,(125,125,125),left)
    pygame.draw.rect(screen,(125,125,125),right)
    pygame.draw.rect(screen,(125,125,125),bot)


    draw_text("Hello World", text_font,(255,255,255),220,115)
    screen.blit(soldier,player)
    key = pygame.key.get_pressed()
    if key[pygame.K_a]==True and not player.colliderect(left):
        player.move_ip(-1,0)
    elif key[pygame.K_d]==True and not player.colliderect(right):
        player.move_ip(1,0)
    elif key[pygame.K_w]==True and not player.colliderect(top):
        player.move_ip(0,-1)
    elif key[pygame.K_s]==True and not player.colliderect(bot):
        player.move_ip(0,1)

    #pos = pygame.mouse.get_pos()
    #print(pos)

    #if pygame.mouse.get_pressed()[0] == True:
    #    print("Left mouse click")
    #if pygame.mouse.get_pressed()[1] == True:
    #    print("Middle mouse click")
    #if pygame.mouse.get_pressed()[2] == True:
    #    print("Right mouse click")

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()

pygame.quit()