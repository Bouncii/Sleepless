# Fichier: src/systems/background.py

import pygame

class Background():
    def __init__(self,witdh,heigth):
        self.width,self.height = witdh,heigth
        self.background = pygame.Surface((self.width,self.height)).convert_alpha()
        self.layers = {
            "BackgroundLayer1": 0.0,
            "BackgroundLayer2": 0.3,
        }

        self.camera_x = 0

    def update_camera(self, player_x):
        self.camera_x = player_x

    def _draw_layers(self, AssetManager):
        self.background.fill((0,0,0,0))
        
        for layer, factor in self.layers.items():

            if layer == "BackgroundLayer1":
                layer_image = AssetManager.get_scaled_image(layer, self.width, self.height)
                self.background.blit(layer_image, (0, 0))
                continue

            # Gestion couches parallax
            layer_image = AssetManager.get_image(layer)
            layer_width = layer_image.get_width()
            layer_height = layer_image.get_height()
            
            new_y = self.height - layer_height
            displacement = self.camera_x * factor
            
            start_x = - int(displacement % layer_width)
            
            if start_x > 0:
                 start_x -= layer_width

            current_tile_x = start_x
            
            overlap = 10

            while current_tile_x < self.width:
                self.background.blit(layer_image, (int(current_tile_x), new_y))
                
                current_tile_x += (layer_width - overlap)


    def draw(self,screen,AssetManager):
        self._draw_layers(AssetManager)
        screen.blit(self.background, (0, 0))