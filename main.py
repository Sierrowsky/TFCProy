import pygame as pg
import json
import constants as c
import sys
from enemy import Enemy
from turrets import Turret
from world import World
from button import Button
from imagentexto import ImageTextButton


 #initialise pygame
pg.init()

#create clock
clock = pg.time.Clock()



# create game window
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.Side_Panel,c.SCREEN_HEIGHT))
pg.display.set_caption("Last Bastion TD")

#load fonts for displaying text on the screen
text_font = pg.font.SysFont("Consolas",24,bold = True)
large_font = pg.font.SysFont("Consolas",36)

# function for outputting text with img in the menu



#functio0n for outputting text opn the screen
def draw_text(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    screen.blit(img,(x,y))


 

def main_menu():

    # Load button images
    start_btn_img = pg.image.load("assets/images/gui/start.png").convert_alpha()
    exit_btn_img = pg.image.load("assets/images/gui/exit.png").convert_alpha()

    # Create exit and start Buttons 
    start_btn = ImageTextButton(c.SCREEN_WIDTH/2 - 100, 300, start_btn_img, "Start" , large_font , "Black")
    exit_btn = ImageTextButton(c.SCREEN_WIDTH/2 -100, 400 , exit_btn_img, "Exit" , large_font , "Black")


    running = True
    while running:
        screen.fill("gray")
        draw_text("Steel Legions",large_font,"Black", c.SCREEN_WIDTH / 2, 100)
        
        
        #Draw Buttons
        start_btn.draw(screen)
        exit_btn.draw(screen)
        


        #Menu event handler
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if start_btn.is_clicked(event.pos):
                    game_Screen()
                    running = False
                elif exit_btn.is_clicked(event.pos):
                    running = False

        # Actualizar pantalla 
        pg.display.update()
        
        
# Función de pausa
def pause_menu():
    # Cargar imágenes para los botones del menú de pausa
    resume_icon = pg.image.load("assets/images/gui/start.png").convert_alpha()
    main_menu_icon = pg.image.load("assets/images/gui/home.png").convert_alpha()

    # Crear botones para reanudar el juego y volver al menú principal
    resume_button = ImageTextButton(c.SCREEN_WIDTH // 2 - 100, 300, resume_icon, "Resume", large_font, "black")
    main_menu_button = ImageTextButton(c.SCREEN_WIDTH // 2 - 100, 400, main_menu_icon, "Main Menu", large_font, "black")

    paused = True
    while paused:
        screen.fill("gray")
        draw_text("Paused", large_font, "white", c.SCREEN_WIDTH / 2, 150)

        # Dibujar botones
        resume_button.draw(screen)
        main_menu_button.draw(screen)

        # Actualizar pantalla
        pg.display.update()

        # Manejar eventos del menú de pausa
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if resume_button.is_clicked(event.pos):
                    return False  # Salir del menú de pausa y reanudar el juego
                elif main_menu_button.is_clicked(event.pos):
                    main_menu()  # Volver al menú principal
                    return True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    paused = False  # Salir del menú de pausa

def game_Screen():

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
    restart_img = pg.image.load('assets/images/side_panel/restart.png').convert_alpha()
    ffw_img = pg.image.load('assets/images/side_panel/fast_forward.png').convert_alpha()


        #gui
    heart_img = pg.image.load('assets/images/gui/heart.png').convert_alpha()
    coin_img = pg.image.load('assets/images/gui/coin.png').convert_alpha()
    logo_img = pg.image.load('assets/images/gui/logo.png').convert_alpha()
    reset_img = pg.image.load('assets/images/gui/restart.png').convert_alpha()

        #load sounds
    shot_fx = pg.mixer.Sound('assets/sound/shot.wav')
    shot_fx.set_volume(0.5)

        #create groups
    enemy_group = pg.sprite.Group()
    turret_group = pg.sprite.Group()

        # create buttons
    turret_buttons = Button(c.SCREEN_WIDTH + 30, 120, buy_turret_img, True)
    cancel_buttons = Button(c.SCREEN_WIDTH + 50, 180, cancel_img, True)
    upgrade_buttons = Button(c.SCREEN_WIDTH + 5, 180, upgrade_img, True)
    begin_buttons = Button(c.SCREEN_WIDTH + 30, 240, start_img,True)
    restart_buttons = Button(310, 300, restart_img,True)
    ffw_buttons = Button(c.SCREEN_WIDTH + 50, 300, ffw_img,False)
    main_menu_btn = Button(310,230,reset_img,True)
        #load json data
    with open('assets/images/levels/level.tmj' ) as file:
            world_data = json.load(file)

            
    def display_data():
            #draw panel
            pg.draw.rect(screen, "maroon", (c.SCREEN_WIDTH, 0, c.Side_Panel, c.SCREEN_HEIGHT))
            pg.draw.rect(screen, "grey0", (c.SCREEN_WIDTH, 0, c.Side_Panel, 400),2)

            screen.blit(logo_img,( c.SCREEN_WIDTH, 400))
            #display data 
            draw_text("LEVEL : " + str(world.level),text_font,"grey100",c.SCREEN_WIDTH+10 , 10)
            screen.blit(heart_img,(c.SCREEN_WIDTH + 10 , 65))
            draw_text(str(world.money),text_font,"grey100",c.SCREEN_WIDTH + 50 ,40)
            screen.blit(coin_img,(c.SCREEN_WIDTH + 10 , 35))
            draw_text(str(world.health),text_font,"grey100",c.SCREEN_WIDTH + 50 ,70)


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
                    new_turret= Turret(turret_spritesheets, mouse_tile_x, mouse_tile_y,shot_fx)
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
            #check if player won
            if world.level > c.Total_levels:
                game_over = True
                game_outcome = 1 #Win
            #update groups
            enemy_group.update(world)
            turret_group.update(enemy_group,world)

            #highlight selected turret
            if selected_turret:
                selected_turret.selected = True

        ###############################
        # DRAWING SECTION
        ##############################



        #draw level
        world.draw(screen)

        #create groups
        enemy_group.draw(screen)
        for turret in turret_group:
            turret.draw(screen)


        display_data()


        if game_over ==False:
            #check if level has been started or not
            if level_started != True:
                if begin_buttons.draw(screen):
                    level_started = True
            else:
                #fast forward
                world.game_speed = 1
                if ffw_buttons.draw(screen):
                    world.game_speed  = 2
                
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
            #for the turret button show cost and the button
            draw_text(str(c.Buy_cost),text_font,"grey100",c.SCREEN_WIDTH + 215 ,135)
            screen.blit(coin_img,(c.SCREEN_WIDTH + 260 , 130))
            if turret_buttons.draw(screen):
                placing_turrets= True
            #if placing turrets then show cancel button
            if placing_turrets == True:
            #show cursor turret
                cursor_rect = cursor_turret.get_rect()
                cursor_pos = pg.mouse.get_pos()
                cursor_rect.center = cursor_pos
                if cursor_pos[0] <= c.SCREEN_WIDTH:
                    screen.blit(cursor_turret, cursor_rect)
                if cancel_buttons.draw(screen):
                    placing_turrets = False
            #if a turret is selected shjow upgrade button
            if selected_turret:
                #if a turret can be upgraded the show the upgrade button
                if selected_turret.upgrade_level < c.Turret_levels:
                    #show cost of upgrade
                    draw_text(str(c.Upgrade_cost),text_font,"grey100",c.SCREEN_WIDTH + 215 ,195)
                    screen.blit(coin_img,(c.SCREEN_WIDTH + 260 , 190))
                    if upgrade_buttons.draw(screen):
                        if world.money >= c.Buy_cost:
                            selected_turret.upgrade()
                            world.money -= c.Upgrade_cost




            

        

        #draw enemy path
    #    pg.draw.lines(screen,"gray0",False,world.waypoints)


        else:
            pg.draw.rect(screen,"dodgerblue",(200,200,400,200),border_radius = 30)
            if game_outcome == -1 :
                draw_text("You Lose",large_font ,"grey0",310,230)
                #if main_menu_btn.draw(screen):
                #    main_menu()
                #    pg.quit()                    
            elif game_outcome == 1:
                draw_text("Congratulations",large_font ,"grey0",250,230)
            #restart level
            if restart_buttons.draw(screen):
                game_over = False
                level_started = False
                placing_turrets = False
                select_turret = None
                last_enemy_spawn = pg.time.get_ticks()
                world = World(world_data,map_image)
                world.process_data()
                world.process_enemys()
                #empty groups
                enemy_group.empty()
                turret_group.empty()
            




        #event handler
        for event in pg.event.get():
            #quit program
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if pause_menu():  # Activar menú de pausa
                        return False
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

main_menu()
