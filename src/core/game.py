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
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()

        self.clock = pygame.time.Clock()
        self.dt = 0

        self.running = True
        self.state = GameState.MENU
        
        self.interactionManagerDoorButton = None
        self.interactionManagerPortal = None

        self.current_level_num = 0
        self.nb_levels = get_number_of_level()

        self.player = None
        self.past_self_group = pygame.sprite.Group()

        self.asset_manager = AssetManager()

        self.inventory = None

        self.SpriteSheet_move_horizontal = None
        self.SpriteSheet_idle = None

        self.SpriteSheet_past_move_horizontal = None
        self.SpriteSheet_past_idle = None

    def _init_screens(self):
        '''Initialise les différents écrans du jeu'''
        self.menu = Menu()
        self.pause = Pause()
        self.win_screen = Fin()
        self.current_screen = self.menu
        self.background = Background(self.screen_width,self.screen_height)

    

    def handle_events(self):
        '''Gère tous les événements du jeu'''
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT or keys[pygame.K_f]:
                self.running = False
            elif keys[pygame.K_ESCAPE]:
                self.state = GameState.PAUSE
            elif keys[pygame.K_r]: #reset le niveau avec R
                self.state = GameState.RESET_GAME
            elif keys[pygame.K_p]:
                self.state = GameState.WIN
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element.state == self.state:
                self.handle_button_events(event)
                
            # Traitement des événements par les managers UI
            self.menu.manager.process_events(event)
            self.win_screen.manager.process_events(event)
            self.pause.manager.process_events(event)


    def handle_button_events(self, event):
        '''Gère les événements de boutons'''
        if event.ui_element == self.menu.play_button:
            self.state = GameState.RESET_GAME
            
        elif event.ui_element == self.win_screen.replay_button:
            self.win_screen.message = random.choice(self.win_screen.level_messages)
            self.state = GameState.RESET_GAME

        elif event.ui_element == self.pause.continue_button:
            self.state = GameState.PLAYING
            
        elif event.ui_element == self.win_screen.next_button:
            self.win_screen.message = random.choice(self.win_screen.level_messages)
            self.current_level_num = (self.current_level_num + 1) % self.nb_levels
            self.state = GameState.RESET_GAME

    def getTileSize(self):
        '''
        Calcul automatiquement la taille des tiles selon la taille de l'écran
        '''
        tile_w = self.screen_width // self.GRID_WIDTH
        tile_h = self.screen_height // self.GRID_HEIGHT
        new_size = min(tile_w, tile_h)
        return new_size


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
        
        # Changement de la taille des tiles
        config.TILE_SIZE = self.getTileSize()

        # Construction du niveau
        self.interactionManagerDoorButton = InteractionManagerButtonsDoors()
        self.interactionManagerPortal = InteractionManagerPortal()
        self.level = level_builder(self.GRID_WIDTH, self.GRID_HEIGHT, self.level_str, self.interactionManagerDoorButton)
        add_item_to_tiles(settings["items"], self.level)

        # initialisation du background
        self.background = Background(self.screen_width,self.screen_height)

        # Initialisation de l'inventaire
        self.inventory = Inventory(self.level,self.interactionManagerPortal)
        
        # Mise à jour des UI
        self.menu.rebuild_ui()
        self.win_screen.rebuild_ui(message=random.choice(self.win_screen.level_messages))
        
        # Création des entités
        start_location = get_start_location(self.level)
        self.player = Player(start_location[0], start_location[1], self.level)
        self.past_self_group.empty()

        for delay in settings["past_selfs"]:
            self.past_self_group.add(Past_self(start_location[0], start_location[1],delay["past_self_timer_spawn"],self.level))
        self.state = GameState.PLAYING

        self.SpriteSheet_move_horizontal = SpriteSheet(self.asset_manager.get_image("walk"),Frames.WALKFRAMES)
        self.SpriteSheet_idle = SpriteSheet(self.asset_manager.get_image("idle"),Frames.IDLEFRAMES)

        self.SpriteSheet_past_move_horizontal = SpriteSheet(self.asset_manager.get_image("past_walk"),Frames.WALKFRAMES)
        self.SpriteSheet_past_idle = SpriteSheet(self.asset_manager.get_image("past_idle"),Frames.IDLEFRAMES)





    def update(self):
        '''Gère le changement de fenêtre'''
        
        if self.state == GameState.MENU:
            self.menu.update(self.dt)
            
        elif self.state == GameState.RESET_GAME:
            self.load_level(self.current_level_num)
            
        elif self.state == GameState.PLAYING:
            # Mise à jour du joueur
            self.background.update_camera(self.player.pixel_x)
            self.player.detection_key(self.GRID_WIDTH, self.GRID_HEIGHT, self.past_self_group)
            self.inventory.update(self.level,self.player)
            self.player.update(self.dt, self.level,self.inventory)
            self.player.update_dt(self.dt)

            for past_self in self.past_self_group:
                if past_self.timer_spawn == 0:
                    past_self.update_dt(self.dt)
            
            # animation objet
            for i in range(len(self.level)):
                for j in range(len(self.level[0])):
                    tile = self.level[i][j]
                    for item in tile.items:
                        item.animate(self.dt)
            
            # Mise à jour du past_self
            self.past_self_group.update(self.dt, self.level,self.interactionManagerPortal)

            #Verif meme case que past self
            self.verif_player_on_same_tile_as_past_self()

            if are_all_entities_idle(self.player,self.past_self_group):
                self.update_buttons_state()

                # Vérification de la victoire
                if self.player.on_finish():
                    self.state = GameState.WIN
                
        elif self.state == GameState.WIN:
            self.win_screen.update(self.dt)

        elif self.state == GameState.PAUSE:
            self.pause.update(self.dt)
        

    def update_buttons_state(self):
        '''
        Met à jour l'état des boutons basé sur la position des entités
        '''
        # Réinitialiser l'état de tous les boutons
        for button_id in list(self.interactionManagerDoorButton.pressed_buttons):
            self.interactionManagerDoorButton.button_released(button_id)
        
        # Vérif entités sur boutons
        entities = [self.player]
        for past_self in self.past_self_group:
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

    def verif_player_on_same_tile_as_past_self(self):
        '''
        Fonction qui vérifie si le joueur est sur la même case que past self et agit en conséquence
        '''
        for past_self in self.past_self_group:
            if self.player.rect.colliderect(past_self.rect) and past_self.timer_spawn == 0:
                self.state = GameState.RESET_GAME




    def render(self):
        '''Affiche le jeu'''
        self.screen.fill((0, 0, 0))
        
        if self.state == GameState.MENU:
            self.background.draw(self.screen,self.asset_manager)
            self.menu.draw(self.screen)
        
        if self.state == GameState.PAUSE:
            self.background.draw(self.screen,self.asset_manager)
            self.pause.draw(self.screen)
            
        elif self.state == GameState.PLAYING:
            # Dessin du niveau

            self.background.draw(self.screen,self.asset_manager)

            for row in range(self.GRID_HEIGHT):
                for col in range(self.GRID_WIDTH):
                    tile = self.level[row][col]
                    tile.draw(self.screen,self.asset_manager)
                    for item in tile.items:
                        item.display(self.screen,self.asset_manager)
                    
            # Dessin des entités
            if(self.player.moving == False):
                # animation Idle
                idle_frame_duration = 150
                num_frame_idle = int(self.player.idle_time // idle_frame_duration) % self.SpriteSheet_idle.nbr_animation
                
                last_move_dir = self.player.moves[-1][0] if self.player.moves else "right"
                facing_left = last_move_dir == "left"
                
                self.SpriteSheet_idle.draw(self.screen, self.player, num_frame_idle, self.asset_manager, scale=1, facing_left=facing_left)

            elif self.player.moves and self.player.moves[-1][0] in ["left","right"]:
                # animation droite/gauche
                num_frame_animation = abs(self.player.start_animation - self.player.pixel_x)//self.player.duree_pixel_animation
                num_frame_animation %= self.SpriteSheet_move_horizontal.nbr_animation
                
                if (self.player.moves[-1][0] == "left"):
                    self.SpriteSheet_move_horizontal.draw(self.screen, self.player, num_frame_animation, self.asset_manager, scale=1, facing_left=True)
                else:
                    self.SpriteSheet_move_horizontal.draw(self.screen, self.player, num_frame_animation, self.asset_manager)
            else:
                self.SpriteSheet_idle.draw(self.screen, self.player, 1, self.asset_manager)


            for past_self in self.past_self_group:
                if past_self.timer_spawn == 0:
                    
                    past_facing_left = past_self.current_direction == "left"

                    if(past_self.moving == False):
                        # animation Idle
                        past_idle_frame_duration = 150
                        past_num_frame_idle = int(past_self.idle_time // past_idle_frame_duration) % self.SpriteSheet_idle.nbr_animation
                        
                        self.SpriteSheet_past_idle.draw(self.screen, past_self, past_num_frame_idle, self.asset_manager, scale=1, facing_left=past_facing_left)
                    
                    elif(past_self.current_direction in ["left","right"]):
                        # animation droite/gauche
                        past_num_frame_animation = abs(past_self.start_animation - past_self.pixel_x)//past_self.duree_pixel_animation
                        past_num_frame_animation %= self.SpriteSheet_past_move_horizontal.nbr_animation
                        
                        self.SpriteSheet_past_move_horizontal.draw(self.screen, past_self, past_num_frame_animation, self.asset_manager, scale=1, facing_left=past_facing_left)
                    else:
                        self.SpriteSheet_past_idle.draw(self.screen, past_self, 1, self.asset_manager)
            
            self.inventory.display(self.screen,self.asset_manager,self.screen_width)
                
        elif self.state == GameState.WIN:
            self.background.draw(self.screen,self.asset_manager)
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

        

