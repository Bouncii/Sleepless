# src/core/game_misc_functions.py

from src.core import config

def are_all_past_self_idle(past_self_tab):
    '''
    Vérifie si les past self ont terminés leurs déplacement
    '''
    res = True
    for past_self in past_self_tab:
        res = res and not past_self.moving
    return res


def are_all_entities_idle(player,past_self_tab):
    '''
    Vérifie si toutes les entités ont terminé leurs déplacements
    '''
    entities_idle = not player.moving and are_all_past_self_idle(past_self_tab)
    return entities_idle

def get_start_location(level:list):
    '''
    Fonction qui renvoie les co de la tile de départ 
    entrées: 
        level : list  
    sorties: tuple
    '''
    res = None
    for y in range(len(level)):
        for x in range (len(level[0])):
            tile = level[y][x]
            if tile.tile_type == "start":
                res = (tile.grid_x,tile.grid_y)
    return res

def renderOffsetCalcul(GRID_WIDTH,GRID_HEIGHT,screen_width,screen_height):
    '''
    Retourne le décallage nécéssaire afin que le niveau soit centré
    '''
    level_pixel_width = GRID_WIDTH * config.TILE_SIZE
    level_pixel_height = GRID_HEIGHT * config.TILE_SIZE

    offset_x = (screen_width - level_pixel_width) // 2
    offset_y = (screen_height - level_pixel_height) // 2
    
    return (offset_x, offset_y)