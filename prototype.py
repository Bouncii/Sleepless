# Example file showing a circle moving on screen
import pygame
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

player = Player(0,0,TILE_SIZE)

past_self = Past_self(0,0,TILE_SIZE)
time_spawn_old_self = 3;

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0,0,0))

    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            level[row][col].draw(screen)

    
    player.detection_key(GRID_WIDTH,GRID_HEIGHT,TILE_SIZE,past_self,level)



    

    player.update(dt,level,TILE_SIZE)
    print(player.moving_vertical,past_self.moving_vertical)
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