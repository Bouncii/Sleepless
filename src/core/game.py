# src/core/game.py

import pygame
import pygame_gui
import random
from .constants import *
from .config import *
from src.entities import Player, Past_self
from src.build import *
from src.ui import *

class Game:
    def __init__(self):
        """
        Initialise le jeu et tous ses systèmes
        """
        pygame.init()


        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.window_width, self.window_height = pygame.display.get_surface().get_size()

        self.clock = pygame.time.Clock()
        self.dt = 0

        self.running = True
        self.state = GameState.MENU
        

        self.current_level_num = 0
        self.nb_levels = 2

        self.player = None #initialisés dans load level
        self.past_self = []


    def _init_screens(self):
        """Initialise les différents écrans du jeu"""
        self.menu = Menu()
        self.win_screen = Fin()
        self.current_screen = self.menu
        self.background = pygame.Surface((self.window_width, self.window_height))


    def level_builder(self, grid_width: int, grid_height: int, level_str: str) -> list:
        """
        Fonction qui construit le niveau sous forme de tableau 2D d'objets Tile
        """
        res = []
        for row in range(grid_height):
            tab_row = []
            for col in range(grid_width):
                type = level_str[row][col]
                tile = Tile(col, row, TILE_SIZE, TILE_SIZE, type, TILE_SIZE)
                tab_row.append(tile)
            res.append(tab_row)
        return res
    

    def handle_events(self):
        """Gère tous les événements du jeu"""
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                self.running = False
                
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                self.handle_button_events(event)
                
            # Traitement des événements par les managers UI
            self.menu.manager.process_events(event)
            self.win_screen.manager.process_events(event)


    def handle_button_events(self, event):
        """Gère les événements de boutons"""
        if event.ui_element == self.menu.play_button:
            self.state = GameState.RESET_GAME
            
        elif event.ui_element == self.win_screen.replay_button:
            self.win_screen.message = random.choice(self.win_screen.level_messages)
            self.state = GameState.RESET_GAME
            
        elif event.ui_element == self.win_screen.next_button:
            self.win_screen.message = random.choice(self.win_screen.level_messages)
            self.current_level_num = (self.current_level_num + 1) % self.nb_levels
            self.state = GameState.RESET_GAME


    def load_level(self, level_num: int):
        """
        Charge un niveau donné
        """
        level_path = config.get_level_path(level_num)
        file_map = f"assets/levels/level{level_num}.txt"
        self.level_str = cree_tableau_de_la_map(file_map)
        
        # Mise à jour des dimensions
        self.GRID_WIDTH = len(self.level_str[0]) 
        self.GRID_HEIGHT = len(self.level_str)
        
        # Construction du niveau
        self.level = self.level_builder(self.GRID_WIDTH, self.GRID_HEIGHT, self.level_str)
        
        # Redimensionnement de l'écran
        self.background = pygame.Surface((self.window_width, self.window_height))
        
        # Mise à jour des UI
        self.menu.rebuild_ui()
        self.win_screen.rebuild_ui(message=random.choice(self.win_screen.level_messages))
        
        # Création des entités
        self.player = Player(0, 0, self.level)
        self.past_self = Past_self(0, 0)
        
        self.state = GameState.PLAYING





    def update(self):
        """Gère le changement de fenêtre"""
        
        if self.state == GameState.MENU:
            self.menu.update(self.dt)
            
        elif self.state == GameState.RESET_GAME:
            self.load_level(self.current_level_num)
            
        elif self.state == GameState.PLAYING:
            # Mise à jour du joueur
            self.player.detection_key(self.GRID_WIDTH, self.GRID_HEIGHT, self.past_self)
            self.player.update(self.dt, self.level)
            
            # Mise à jour du past_self
            if self.past_self.timer_spawn == 0:
                self.past_self.update(self.dt, self.level)
                
            # Vérification de la victoire
            if self.player.on_finish():
                self.state = GameState.WIN
                
        elif self.state == GameState.WIN:
            self.win_screen.update(self.dt)




    def render(self):
        """Affiche le jeu"""
        self.screen.fill((0, 0, 0))
        
        if self.state == GameState.MENU:
            self.screen.blit(self.background, (0, 0))
            self.menu.draw(self.screen)
            
        elif self.state == GameState.PLAYING:
            # Dessin du niveau
            for row in range(self.GRID_HEIGHT):
                for col in range(self.GRID_WIDTH):
                    self.level[row][col].draw(self.screen)
            
            # Dessin des entités
            self.player.show(self.screen)
            if self.past_self.timer_spawn == 0:
                self.past_self.show(self.screen)
                
        elif self.state == GameState.WIN:
            self.screen.blit(self.background, (0, 0))
            self.win_screen.draw(self.screen)
            
        pygame.display.flip()
    
    def run(self):
        '''
        Boucle principale du jeu
        '''
        ####################################  ceci est sencé virer plus tard
        self._init_screens()
        ####################################
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000  # Temps écoulé depuis la dernière frame en secondes
            self.handle_events()
            self.update()
            self.render()

        

