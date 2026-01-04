# src/core/constants.py
import os

class _GameConstants:
    """
    Constantes à utiliser qui ne changerons pas
    """
    FPS = 60
    
    SPEED_FACTOR_X = 1.5
    SPEED_FACTOR_Y = 1.5
    GRAVITY_FACTOR = 5.0 
    
    class States:
        MENU = "menu"
        PLAYING = "playing"
        WIN = "win"
        RESET_GAME = "reset_game"
        PAUSE = "pause"
        CONTROLS = "controls"

    class ItemTypes:
        PORTALMAKER = "portalMaker"
        STUNMAKER = "stunMaker"
    
    class Frames:
        IDLEFRAMES = 27
        WALKFRAMES = 9
        CLIMBFRAMES = 6
    
    
    class Paths:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        LEVELS = os.path.join(BASE_DIR, "assets", "levels")
        IMAGES = os.path.join(BASE_DIR, "assets", "images")
        SOUNDS = os.path.join(BASE_DIR, "assets", "sounds")
        SETTINGS = os.path.join(BASE_DIR, "assets", "levels","levels_settings.json")


FPS = _GameConstants.FPS
SPEED_FACTOR_X = _GameConstants.SPEED_FACTOR_X
SPEED_FACTOR_Y = _GameConstants.SPEED_FACTOR_Y
GRAVITY_FACTOR = _GameConstants.GRAVITY_FACTOR
GameState = _GameConstants.States
Paths = _GameConstants.Paths
ItemTypes = _GameConstants.ItemTypes
Frames = _GameConstants.Frames