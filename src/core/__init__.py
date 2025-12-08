# Fichier: src/core/__init__.py
"""
Package core
"""
from .constants import (
    FPS, 
    SPEED_FACTOR_X,
    SPEED_FACTOR_Y,
    GRAVITY_FACTOR,
    GameState,
    Paths,
    ItemTypes,
    Frames
)

from .config import config
from .game_misc_functions import *

from .game import Game 

__all__ = [
    # Constantes
    'FPS', 
    'SPEED_FACTOR_X',
    'SPEED_FACTOR_Y',
    'GRAVITY_FACTOR',
    'GameState',
    'Paths',
    'ItemTypes',
    'Frames',

    # Config modifiable
    'config',

    #GameMiscFunctions
    'are_all_past_self_idle',
    'are_all_entities_idle',
    

    'Game'
]