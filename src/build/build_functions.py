from src.core.config import *
from .tile import Tile

def level_builder(grid_width: int, grid_height: int, level_str: str, interactionManagerDoorButton) -> list:
    '''
    Fonction qui construit le niveau sous forme de tableau 2 dimension d'objet Tile 
    entrées: 
        grid_height : int  
        grid_width : int  
        config.TILE_SIZE : int  
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
            tile = Tile(col, row, config.TILE_SIZE, config.TILE_SIZE, type, config.TILE_SIZE)
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
    if "door_left" in tile.structures:
        interaction_manager.register_door(tile.structures["door_left"].door_id, tile.structures["door_left"])
        # Connecte automatiquement les boutons et portes de même ID
        interaction_manager.add_connection(tile.structures["door_left"].door_id, tile.structures["door_left"].door_id)
    elif "door_right" in tile.structures:
        interaction_manager.register_door(tile.structures["door_right"].door_id, tile.structures["door_right"])
        # Connecte automatiquement les boutons et portes de même ID
        interaction_manager.add_connection(tile.structures["door_right"].door_id, tile.structures["door_right"].door_id)
    elif "button" in tile.structures:
        interaction_manager.register_button(tile.structures["button"].button_id, tile.structures["button"])