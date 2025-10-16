# Example file showing a circle moving on screen
import pygame
import pygame_gui
from player import *
from past_self import *
from tile import *
from level_design import *
from gui import *

#################################### game initialization ####################################
niveau = 0
NB_LEVEL = 2

file_map = f"level/level{niveau}.txt"
level_str = cree_tableau_de_la_map(file_map)

TILE_SIZE = 128 
GRID_WIDTH = len(level_str[0]) 
GRID_HEIGHT = len(level_str)

#################################### Pygame Setup ####################################

pygame.init()
screen = pygame.display.set_mode((GRID_WIDTH*TILE_SIZE, GRID_HEIGHT*TILE_SIZE))
clock = pygame.time.Clock()
running = True
dt = 0

#################################### Pygame_GUI Setup ####################################

background = pygame.Surface((GRID_WIDTH*TILE_SIZE, GRID_HEIGHT*TILE_SIZE))
# Pareil que dt sauf que dt est modif je crois pour l'anime de chute
time_delta = clock.tick(60) / 1000

#################################### Etape du jeu ####################################

menu = Menu(GRID_WIDTH, TILE_SIZE, GRID_HEIGHT)
reset_game = "reset_game"
game = "game"
win = Fin(GRID_WIDTH, TILE_SIZE, GRID_HEIGHT)

# Décide de ce que l'on affiche menu/game etc ...
current_screen = menu

##########################################################################################

def level_builder(grid_width:int,grid_height:int,tile_size:int,level_str:str) -> list:
    '''
    Fonction qui construit le niveau sous forme de tableau 2 dimension d'objet Tile 
    entrées: 
        grid_height : int  
        grid_width : int  
        tile_size : int  
        level_str : str  
    sorties: 
        res : list
    '''
    res=[]
    for row in range(grid_height):
        tab_row = []
        for col in range(grid_width):
            type = level_str[row][col]
            tile = Tile(col,row,tile_size,tile_size,type,TILE_SIZE)
            tab_row.append(tile)
        res.append(tab_row)
    return res



#################################### game ####################################

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == menu.play_button:
                current_screen = reset_game
            if event.ui_element == win.replay_button:
                # Reset le message de fin :)
                win.message = random.choice(win.level_messages)
                # On passe à l'étape reset la map pour le prochaine niveau
                current_screen = reset_game
            if event.ui_element == win.next_button:
                # Reset le message de fin :)
                win.message = random.choice(win.level_messages)
                # On passe au niveau + 1 et on retourne à 0 si on depasse le nombre de niveaux
                niveau = (niveau + 1) % NB_LEVEL
                print(niveau)
                # On passe à l'étape reset la map pour le prochaine niveau
                current_screen = reset_game
        menu.manager.process_events(event)
        win.manager.process_events(event)

    if current_screen == menu:
        # Affiche le menu du début
        menu.update(time_delta)
        screen.blit(background, (0, 0))
        menu.draw(screen)
    
    elif current_screen == reset_game:
        # On Cree le tableau de tableau de la nouvelle map
        file_map = f"level/level{niveau}.txt"
        level_str = cree_tableau_de_la_map(file_map)

        # Ce qui implique un possible changment de Hauteur/largeur
        GRID_WIDTH = len(level_str[0]) 
        GRID_HEIGHT = len(level_str)

        # On cree la map ici
        level = level_builder(GRID_WIDTH,GRID_HEIGHT,TILE_SIZE,level_str)

        # On change les propriété de hauteur/Largeur à pygame
        screen = pygame.display.set_mode((GRID_WIDTH*TILE_SIZE, GRID_HEIGHT*TILE_SIZE), pygame.RESIZABLE)
        background = pygame.Surface((GRID_WIDTH*TILE_SIZE, GRID_HEIGHT*TILE_SIZE))
        
        # On rebuild les menus pour être responsive aux changement de hauteur/Largeur
        menu.rebuild_ui(GRID_WIDTH, TILE_SIZE, GRID_HEIGHT)
        win.rebuild_ui(GRID_WIDTH, TILE_SIZE, GRID_HEIGHT, message=random.choice(win.level_messages))

        # On respawn le joueur/ghost au spawn
        player = Player(0,0,TILE_SIZE)
        past_self = Past_self(0,0,TILE_SIZE)
        # Je ne sais pas si c'est utile je l'ai laissé :
        time_spawn_old_self = 3

        # On a finis de reset la game on peut jouer maintenant
        current_screen = game

        
    elif current_screen == game:
        screen.fill((0,0,0))
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                level[row][col].draw(screen)

        player.detection_key(GRID_WIDTH,GRID_HEIGHT,TILE_SIZE,past_self,level)
        player.update(dt,level,TILE_SIZE)
        player.show(screen)

        if past_self.timer_spawn == 0:
            past_self.update(dt,level,TILE_SIZE)
            past_self.show(screen)

        if player.on_finish(level):
            current_screen = win

        # flip() the display to put your work on screen
        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    elif current_screen == win:
        # Affiche le menu de victoire
        win.update(time_delta)
        screen.blit(background, (0, 0))
        win.draw(screen)
    
    pygame.display.flip()
pygame.quit()

########
#TODO 
########