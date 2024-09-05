import pygame

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
x = 0
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Working with Shapes")

run = True
while run:

    screen.fill((255,255,255))

    # Linea Recta
    #pygame.draw.rect(screen,(255,0,0),(200,100,150,150),width=5,border_bottom_right_radius=50,border_top_left_radius=50)
    
    # Circulo
    #pygame.draw.circle(screen,(0,0,0),(300,100),70)
    #pygame.draw.circle(screen,(255,255,0),(300,100),70,draw_top_right=True, draw_bottom_right=True)
    
    # Elipse
    #pygame.draw.ellipse(screen,(0,0,255),(200,150,150,75))

    # Arco
    #if pygame.mouse.get_pressed()[0]==True:
    #    x+=0.001
    #if pygame.mouse.get_pressed()[2]==True:
    #    x-=0.001
    #pygame.draw.arc(screen,(0,255,255),(200,100,150,150),0,x ,width=5)
    
    # Linea terminada en la posicion del mouse
    #pos = pygame.mouse.get_pos()
    #pygame.draw.line(screen,(255,0,255),(300,200),pos)

    # Poligono
    #pygame.draw.polygon(screen,(0,255,0),((100,200),(200,300),(500,100),(200,250)))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()

pygame.quit()