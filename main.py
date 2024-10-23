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
game_over = False
game_outcome = 0 # -1 is lose & 1 is win
level_started = False
placing_turrets = False
selected_turret = None
last_enemy_spawn = pg.time.get_ticks()

#load images
#map
map_image = pg.image.load('assets/images/levels/level.png').convert_alpha()
#enemies
enemy_images = {
    'weak': pg.image.load('assets/images/enemies/enemy_1.png').convert_alpha(),
    'medium': pg.image.load('assets/images/enemies/enemy_2.png').convert_alpha(),
    'hard': pg.image.load('assets/images/enemies/enemy_3.png').convert_alpha(),
    'elite': pg.image.load('assets/images/enemies/enemy_4.png').convert_alpha()
}
#turret
cursor_turret = pg.image.load('assets/images/turrets/turret.png').convert_alpha()
#turret scpritesheet
turret_spritesheets = []
for x in range(1,c.Turret_levels + 1):
    turret_sheet = pg.image.load(f'assets/images/turrets/turret_{x}.png').convert_alpha()
    turret_spritesheets.append(turret_sheet)
#buttons
buy_turret_img = pg.image.load('assets/images/side_panel/buy_turret.png').convert_alpha()
cancel_img = pg.image.load('assets/images/side_panel/cancel.png').convert_alpha()
upgrade_img = pg.image.load('assets/images/side_panel/upgrade_turret.png').convert_alpha()
start_img = pg.image.load('assets/images/side_panel/begin.png').convert_alpha()

#load json data
with open('assets/images/levels/level.tmj' ) as file:
    world_data = json.load(file)

#load fonts for displaying text on the screen
text_font = pg.font.SysFont("Consolas",24,bold = True)
large_font = pg.font.SysFont("Consolas",36)

#functio0n for outputting text opn the screen
def draw_text(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    screen.blit(img,(x,y))


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
            new_turret= Turret(turret_spritesheets, mouse_tile_x, mouse_tile_y)
            turret_group.add(new_turret)
            #deduct cost of turret
            world.money -= c.Buy_cost



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
world.process_enemys()
 
#create groups
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

# create buttons
turret_burrons = Button(c.SCREEN_WIDTH + 30, 120, buy_turret_img, True)
cancel_burrons = Button(c.SCREEN_WIDTH + 50, 180, cancel_img, True)
upgrade_burrons = Button(c.SCREEN_WIDTH + 5, 180, upgrade_img, True)
begin_burrons = Button(c.SCREEN_WIDTH + 30, 240, start_img,True)
#game loop
run = True
while run:

    clock.tick(c.FPS)



    ###############################
    # UPDATING SECTION
    ##############################

    if game_over == False:
        #check if player has lost
        if world.health <= 0:
            game_over = True
            game_outcome = -1 #loss

        #update groups
        enemy_group.update(world)
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
    draw_text(str(world.health),text_font,"grey100",0,0)
    draw_text(str(world.money),text_font,"grey100",0,30)
    draw_text(str(world.level),text_font,"grey100",0,60)

    if game_over ==False:
        #check if level has been started or not
        if level_started != True:
            if begin_burrons.draw(screen):
                level_started = True
        else:
            #spawn enemies
            if pg.time.get_ticks() - last_enemy_spawn > c.Spawn_cooldown:
                if world.spawned_enemy < len(world.enemy_list):
                    enemy_type = world.enemy_list[world.spawned_enemy]
                    enemy = Enemy(enemy_type, world.waypoints,enemy_images)
                    enemy_group.add(enemy)
                    world.spawned_enemy += 1
                    last_enemy_spawn = pg.time.get_ticks()

        #check if the wave is finished
        if world.check_level_completed() == True:
            world.money += c.level_reward
            world.level += 1
            level_started = False
            last_enemy_spawn = pg.time.get_ticks()
            world.reset_level()
            world.process_enemys()

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
        #if a turret is selected shjow upgrade button
        if selected_turret:
            #if a turret can be upgraded the show the upgrade button
            if selected_turret.upgrade_level < c.Turret_levels:
                if upgrade_burrons.draw(screen):
                    if world.money >= c.Buy_cost:
                        selected_turret.upgrade()
                        world.money -= c.Upgrade_cost




        

    

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
                    #check money
                    if world.money >= c.Buy_cost:
                        create_turret(mouse_pos)
                else:
                    selected_turret = select_turret(mouse_pos)

    #update display
    pg.display.update()

pg.quit()
