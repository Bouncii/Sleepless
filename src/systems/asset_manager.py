# src/systems/asset_manager.py
import os
import pygame
from src.core import config

class AssetManager:
    def __init__(self):
        self.images = {}
        self.load_images()

    def load_images(self):
        '''Charge toutes les images nécessaires'''
        image_paths = {
            'player': config.get_img_path("player.png"),
            'past_self': config.get_img_path("past_self"),
            'ground': config.get_img_path("ground"),
            'ladder': config.get_img_path("ladder"),
            'button': config.get_img_path("button"),
            'start': config.get_img_path("start"),
            'end': config.get_img_path("end"),
            'tile': config.get_img_path("tile"),
            'background': config.get_img_path("background"),
            'portalMakerItem': config.get_img_path("portalMakerItem"),
            'missing_texture': config.get_img_path("missing_texture")
        }
        
        for key, path in image_paths.items():
            if os.path.exists(path):
                
                self.images[key] = pygame.image.load(path).convert_alpha()
            # else:
            #     self.images[key] = pygame.image.load(image_paths["missing_texture"]).convert_alpha()

    def get_image(self, key):
        '''Récupère une image par sa clé'''

        return self.images.get(key, self.images['missing_texture'])
    

    def get_scaled_image(self, key, target_width, target_height):
        '''Récupère une image redimensionnée à la taille spécifiée'''
        original_image = self.get_image(key)
        return pygame.transform.scale(original_image, (int(target_width), int(target_height)))