# src/core/game.py

import pygame
import pygame_gui
import random
from .constants import *
from .config import *
from .game_misc_functions import *
from src.entities import *
from src.build import *
from src.ui import *
from src.systems import *

class Game:
    def __init__(self):
        '''
        Initialise le jeu et tous ses systèmes
        '''
        pygame.init()


        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.window_width, self.window_height = pygame.display.get_surface().get_size()

        self.clock = pygame.time.Clock()
        self.dt = 0

        self.running = True
        self.state = GameState.MENU
        
        self.interactionManagerDoorButton = None

        self.current_level_num = 0
        self.nb_levels = 2

        self.player = None #initialisés dans load level
        self.past_self_tab = []

        self.asset_manager = AssetManager()


    def _init_screens(self):
        '''Initialise les différents écrans du jeu'''
        self.menu = Menu()
        self.win_screen = Fin()
        self.current_screen = self.menu
        self.background = pygame.Surface((self.window_width, self.window_height))

    

    def handle_events(self):
        '''Gère tous les événements du jeu'''
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                self.running = False
            elif keys[pygame.K_r]: #reset le niveau avec R
                self.state = GameState.RESET_GAME
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                self.handle_button_events(event)
                
            # Traitement des événements par les managers UI
            self.menu.manager.process_events(event)
            self.win_screen.manager.process_events(event)


    def handle_button_events(self, event):
        '''Gère les événements de boutons'''
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
        '''
        Charge un niveau donné
        '''
        file_map = f"assets/levels/level{level_num}.txt"
        settings = get_settings_by_level_number(self.current_level_num)
        self.level_str = cree_tableau_de_la_map(file_map)
        
        # Mise à jour des dimensions
        self.GRID_WIDTH = len(self.level_str[0]) 
        self.GRID_HEIGHT = len(self.level_str)
        
        # Construction du niveau
        self.interactionManagerDoorButton = InteractionManagerButtonsDoors()
        self.level = level_builder(self.GRID_WIDTH, self.GRID_HEIGHT, self.level_str, self.interactionManagerDoorButton)
        
        # Redimensionnement de l'écran
        self.background = pygame.Surface((self.window_width, self.window_height))
        
        # Mise à jour des UI
        self.menu.rebuild_ui()
        self.win_screen.rebuild_ui(message=random.choice(self.win_screen.level_messages))
        
        # Création des entités
        self.player = Player(0, 0, self.level)
        self.past_self_tab = []
        self.past_self_tab.append(Past_self(0, 0,settings["past_self_timer_spawn"]))
        
        self.state = GameState.PLAYING





    def update(self):
        '''Gère le changement de fenêtre'''
        
        if self.state == GameState.MENU:
            self.menu.update(self.dt)
            
        elif self.state == GameState.RESET_GAME:
            self.load_level(self.current_level_num)
            
        elif self.state == GameState.PLAYING:
            # Mise à jour du joueur
            self.player.detection_key(self.GRID_WIDTH, self.GRID_HEIGHT, self.past_self_tab)
            self.player.update(self.dt, self.level)
            
            # Mise à jour du past_self
            for past_self in self.past_self_tab:
                if past_self.timer_spawn == 0:
                    past_self.update(self.dt, self.level)

            if are_all_entities_idle(self.player,self.past_self_tab):
                self.update_buttons_state()
                
                #Verif meme case que past self
                self.verif_same_tile_as_past_self()

                # Vérification de la victoire
                if self.player.on_finish():
                    self.state = GameState.WIN
                
        elif self.state == GameState.WIN:
            self.win_screen.update(self.dt)


    def update_buttons_state(self):
        '''
        Met à jour l'état des boutons basé sur la position des entités
        '''
        # Réinitialiser l'état de tous les boutons
        for button_id in list(self.interactionManagerDoorButton.pressed_buttons):
            self.interactionManagerDoorButton.button_released(button_id)
        
        # Vérif entités sur boutons
        entities = [self.player]
        for past_self in self.past_self_tab:
            if past_self.timer_spawn == 0:
                entities.append(past_self)
        
        pressed_buttons = []
        
        for entity in entities:
            tile_x = entity.grid_x
            tile_y = entity.grid_y
            
            if 0 <= tile_y < len(self.level) and 0 <= tile_x < len(self.level[0]):
                current_tile = self.level[tile_y][tile_x]
                
                # Vérifier si cette tile contient un bouton
                if current_tile.tile_type == "button":
                    pressed_buttons.append(current_tile.tile_id)
        
        # Activer les boutons pressés
        for button_id in pressed_buttons:
            if button_id not in self.interactionManagerDoorButton.pressed_buttons:
                self.interactionManagerDoorButton.button_pressed(button_id)

    def verif_same_tile_as_past_self(self):
        '''
        Fonction qui vérifie si le joueur est sur la même case que past self et agit en conséquence
        '''
        for past_self in self.past_self_tab:
            if past_self.grid_x == self.player.grid_x and past_self.grid_y == self.player.grid_y and past_self.timer_spawn == 0:
                self.state = GameState.RESET_GAME




    def render(self):
        '''Affiche le jeu'''
        self.screen.fill((0, 0, 0))
        
        if self.state == GameState.MENU:
            self.screen.blit(self.background, (0, 0))
            self.menu.draw(self.screen)
            
        elif self.state == GameState.PLAYING:
            # Dessin du niveau
            for row in range(self.GRID_HEIGHT):
                for col in range(self.GRID_WIDTH):
                    self.level[row][col].draw(self.screen,self.asset_manager)
            
            # Dessin des entités
            self.player.show(self.screen)
            for past_self in self.past_self_tab:
                if past_self.timer_spawn == 0:
                    past_self.show(self.screen)
                
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

        

