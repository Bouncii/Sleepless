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
            else:
                layer_image = AssetManager.get_image(layer)

            layer_height = layer_image.get_height()

            parallax_x = -self.camera_x * factor

            new_y = self.height - layer_height

            self.background.blit(layer_image, (parallax_x, new_y))


    def draw(self,screen,AssetManager):
        self._draw_layers(AssetManager)
        screen.blit(self.background, (0, 0))