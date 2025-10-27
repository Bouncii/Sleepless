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
    Colors,
    GameState,
    Paths
)

from .config import config

# from .game import Game  # ← DÉCOMMENTER quand game.py sera prêt

__all__ = [
    # Constantes
    'TILE_SIZE',
    'FPS', 
    'GRAVITY',
    'ENTITIES_SPEED_X',
    'ENTITIES_SPEED_Y',
    'PAST_SELF_DELAY',
    'Colors',
    'GameState',
    'Paths',

    # Config modifiable
    'config',
    
    # Classes principales
    # 'Game'
]