# src/core/game.py

import pygame
from .constants import *
from .config import *

class Game:
    def __init__(self):
        """
        Initialise le jeu et tous ses systèmes
        """
        pygame.init()
        self.screen = pygame.display.set_mode((config.screen_size(0), config.screen_size(1)))
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.running = True
        self.state = GameState.MENU
        self.current_level_num = config.current_level

        self.player = None #initialisés dans load level
        self.past_self = []

    def load_level(self, level_num:int):
        """
        Charge un niveau donné
        """
        level_path = config.get_level_path(level_num)
        pass