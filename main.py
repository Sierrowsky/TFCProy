import pygame as pg
import json
import constants as c
from enemy import Enemy
from turrets import Turret
from world import World
from button import Button


 #initialise pygame
pg.init()

#create clock
clock = pg.time.Clock()



# create game window
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.Side_Panel,c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defense")

#game variables
placing_turrets = False
selected_turret = None

#load images
#map
map_image = pg.image.load('assets/images/levels/level.png').convert_alpha()
#enemies
enemy_image = pg.image.load('assets/images/enemies/enemy_1.png').convert_alpha()
#turret
cursor_turret = pg.image.load('assets/images/turrets/turret.png').convert_alpha()
#turret scpritesheet
turret_sheet = pg.image.load('assets/images/turrets/turret_1.png').convert_alpha()
#buttons
buy_turret_img = pg.image.load('assets/images/side_panel/buy_turret.png').convert_alpha()
cancel_img = pg.image.load('assets/images/side_panel/cancel.png').convert_alpha()

#load json data
with open('assets/images/levels/level.tmj' ) as file:
    world_data = json.load(file)

def create_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.Tile_Size
    mouse_tile_y = mouse_pos[1] // c.Tile_Size
    #calculate the sequential number of tile
    mouse_tile_num = (mouse_tile_y * c.Cols) + mouse_tile_x
    #check if that tile is grass
    if world.tile_map[mouse_tile_num] == 7:
        #check is no turret
        space = True
        for turret in turret_group:
            if (mouse_tile_x,mouse_tile_y) == (turret.tile_x,turret.tile_y):
                space = False
        if space == True :
            new_turret= Turret(turret_sheet, mouse_tile_x, mouse_tile_y)
            turret_group.add(new_turret)
            
def select_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.Tile_Size
    mouse_tile_y = mouse_pos[1] // c.Tile_Size
    for turret in turret_group:
        if (mouse_tile_x,mouse_tile_y) == (turret.tile_x,turret.tile_y):
            return turret 
def clear_selection():
    for turret in turret_group:
        turret.selected = False
#create world
world = World(world_data, map_image)
world.process_data()


#create groups
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

enemy = Enemy(world.waypoints,enemy_image)
enemy_group.add(enemy)

# create buttons
turret_burrons = Button(c.SCREEN_WIDTH + 30, 120, buy_turret_img, True)
cancel_burrons = Button(c.SCREEN_WIDTH + 50, 180, cancel_img, True)
#turret_burrons = Button(c.SCREEN_WIDTH + 30, 120, buy_turret_img)
#game loop
run = True
while run:

    clock.tick(c.FPS)



    ###############################
    # UPDATING SECTION
    ##############################

    #update groups
    enemy_group.update()
    turret_group.update(enemy_group)

    #highlight selected turret
    if selected_turret:
        selected_turret.selected = True

    ###############################
    # DRAWING SECTION
    ##############################
    screen.fill("grey100")


    #draw level
    world.draw(screen)

    #create groups
    enemy_group.draw(screen)
    for turret in turret_group:
        turret.draw(screen)

    #draw buttons
    #place turret
    if turret_burrons.draw(screen):
        placing_turrets= True
    #if placing turrets then show cancel button
    if placing_turrets == True:
    #show cursor turret
        cursor_rect = cursor_turret.get_rect()
        cursor_pos = pg.mouse.get_pos()
        cursor_rect.center = cursor_pos
        if cursor_pos[0] <= c.SCREEN_WIDTH:
            screen.blit(cursor_turret, cursor_rect)
        if cancel_burrons.draw(screen):
            placing_turrets = False




    

    

    #draw enemy path
#    pg.draw.lines(screen,"gray0",False,world.waypoints)



    #event handler
    for event in pg.event.get():
        #quit program
        if event.type == pg.QUIT:
            run = False
        #mouse click
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
            #chec if mouse is on the game area
            if mouse_pos[0]< c.SCREEN_WIDTH and mouse_pos[1] <c.SCREEN_HEIGHT:
                #clear selected turrets
                selected_turret = None
                clear_selection()
                if placing_turrets == True :
                    create_turret(mouse_pos)
                else:
                    selected_turret = select_turret(mouse_pos)

    #update display
    pg.display.update()

pg.quit()
