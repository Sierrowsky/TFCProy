import pygame
import random

pygame.init()
SCREEN_WIDTH = 600
SCRING_HEIGHT = 400

screen = pygame.display.set_mode((SCREEN_WIDTH,SCRING_HEIGHT))
pygame.display.set_caption("TEXT INPUT")


#define colours
WHITE = (255,255,255)
BG=(50,50,50)
GREEN=(0,255,0)
RED=(255,0,0)
BLUE=(0,0,255)

#define font
font_size = 60
font = pygame.font.SysFont("Futura",font_size)

#create empty text string
text=[""]

# function for outputting text onto the screen
def draw_text(text, font,text_col,x,y):
    img = font.render(text,True,text_col)
    width = img.get_width()
    screen.blit(img,(x-(width/2),y))

run = True
while run:
    #update background
    screen.fill(BG)

    #display  text input
    for row, line in enumerate(text):
        draw_text(line,font,RED,SCREEN_WIDTH/2,200+(row * font_size))

    for event in pygame.event.get():

        #handle text input
        if event.type == pygame.TEXTINPUT:
            text[-1] += event.text

        #handle special keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                text[-1] = text[-1][:-1]
                if len(text[-1]) == 0:
                    if len(text) >1:
                        text = text[:-1]
            elif event.key == pygame.K_RETURN:
                text.append("")

        if event.type == pygame.QUIT:
            run = False

    #update display
    pygame.display.flip()
pygame.quit()
