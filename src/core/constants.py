# src/core/constants.py
import os

class _GameConstants:
    """
    Constantes à utiliser qui ne changerons pas
    """
    TILE_SIZE = 200
    FPS = 60
    

    GRAVITY = 600
    ENTITIES_SPEED_X = 300  
    ENTITIES_SPEED_Y = 300 

    PAST_SELF_DELAY = 3
    
    class States:
        MENU = "menu"
        PLAYING = "playing"
        WIN = "win"
        RESET_GAME = "reset_game"
    
    
    class Paths:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        LEVELS = os.path.join(BASE_DIR, "assets", "levels")
        IMAGES = os.path.join(BASE_DIR, "assets", "images")
        SOUNDS = os.path.join(BASE_DIR, "assets", "sounds")


TILE_SIZE = _GameConstants.TILE_SIZE
FPS = _GameConstants.FPS
GRAVITY = _GameConstants.GRAVITY
ENTITIES_SPEED_X = _GameConstants.ENTITIES_SPEED_X  # ← EXPORTER
ENTITIES_SPEED_Y = _GameConstants.ENTITIES_SPEED_Y  # ← EXPORTER
PAST_SELF_DELAY = _GameConstants.PAST_SELF_DELAY    # ← EXPORTER
GameState = _GameConstants.States
Paths = _GameConstants.Paths