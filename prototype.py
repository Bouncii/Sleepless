# Example file showing a circle moving on screen
import pygame
import pygame_gui
from player import *
from past_self import *
from tile import *
from level_design import *

#################################### game initialization ####################################

FILE_MAP = "level.txt"

level_str = cree_tableau_de_la_map(FILE_MAP)

TILE_SIZE = 128 
GRID_WIDTH = len(level_str[0]) 
GRID_HEIGHT = len(level_str)

# pygame setup
pygame.init()
screen = pygame.display.set_mode((GRID_WIDTH*TILE_SIZE, GRID_HEIGHT*TILE_SIZE))
clock = pygame.time.Clock()
running = True
dt = 0

# pygame_gui setup
background = pygame.Surface((GRID_WIDTH*TILE_SIZE, GRID_HEIGHT*TILE_SIZE))
manager = pygame_gui.UIManager((GRID_WIDTH*TILE_SIZE, GRID_HEIGHT*TILE_SIZE), 'theme.json')
play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((GRID_WIDTH*TILE_SIZE//2 - 100//2, GRID_HEIGHT*TILE_SIZE//1.5 - 50//2), (100, 50)),
                                             text='Play',
                                             manager=manager)
text_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((0, GRID_HEIGHT*TILE_SIZE//3 - 100), (GRID_WIDTH*TILE_SIZE, 50)),
    text='SleepLess',
    manager=manager,
    object_id=pygame_gui.core.ObjectID(class_id="#menu_titre")
)
time_delta = clock.tick(60)/1000.0  #pareil que dt
play = False

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
         
level = level_builder(GRID_WIDTH,GRID_HEIGHT,TILE_SIZE,level_str)
print(level)
player = Player(0,0,TILE_SIZE)

past_self = Past_self(0,0,TILE_SIZE)
time_spawn_old_self = 3;

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == play_button:
                play = True

        manager.process_events(event)
    if play == False:
        manager.update(time_delta)

        screen.blit(background, (0, 0))
        manager.draw_ui(screen)
        pygame.display.update()
        
    else:
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

    # flip() the display to put your work on screen
        pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
        dt = clock.tick(60) / 1000

pygame.quit()

########
#TODO 
########