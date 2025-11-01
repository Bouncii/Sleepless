from src.core.constants import *
from .tile import Tile

def level_builder(grid_width: int, grid_height: int, level_str: str, interactionManagerDoorButton) -> list:
    '''
    Fonction qui construit le niveau sous forme de tableau 2 dimension d'objet Tile 
    entrées: 
        grid_height : int  
        grid_width : int  
        tile_size : int  
        level_str : str  
        interactionManagerDoorButton : InteractionManagerButtonsDoors
    sorties: 
        res : list
    '''
    res = []
    for row in range(grid_height):
        tab_row = []
        for col in range(grid_width):
            type = level_str[row][col]
            tile = Tile(col, row, TILE_SIZE, TILE_SIZE, type, TILE_SIZE)
            link_door_button(tile,interactionManagerDoorButton)
            tab_row.append(tile)
        res.append(tab_row)
    return res


def link_door_button(tile,interaction_manager):
    '''
    Fonction qui enregistre les doors, buttons et leur relation
    entrées:
        tile : Tile
        interactionManagerDoorButton : InteractionManagerButtonsDoors
    sortie : None
    '''
    if "door" in tile.structures:
        interaction_manager.register_door(tile.structures["door"].door_id, tile.structures["door"])
        # Connecte automatiquement les boutons et portes de même ID
        interaction_manager.add_connection(tile.structures["door"].door_id, tile.structures["door"].door_id)
    elif "button" in tile.structures:
        interaction_manager.register_button(tile.structures["button"].button_id, tile.structures["button"])