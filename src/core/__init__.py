# Fichier: src/core/__init__.py
"""
Package core
"""
from .constants import (
    TILE_SIZE,
    FPS, 
    GRAVITY,
    ENTITIES_SPEED_X,
    ENTITIES_SPEED_Y,
    PAST_SELF_DELAY,
    GameState,
    Paths
)

from .config import config
from .game_misc_functions import *

from .game import Game 

__all__ = [
    # Constantes
    'TILE_SIZE',
    'FPS', 
    'GRAVITY',
    'ENTITIES_SPEED_X',
    'ENTITIES_SPEED_Y',
    'PAST_SELF_DELAY',
    'GameState',
    'Paths',

    # Config modifiable
    'config',

    #GameMiscFunctions
    'are_all_past_self_idle',
    'are_all_entities_idle',
    

    'Game'
]