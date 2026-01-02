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
            'button': config.get_img_path("Button"),
            'start': config.get_img_path("start"),
            'end': config.get_img_path("end"),
            'tile': config.get_img_path("tile"),
            'background': config.get_img_path("background"),
            'portalMaker': config.get_img_path("portalgun"),
            'portal': config.get_img_path("portal"),
            'portalCrack': config.get_img_path("portalCrack"),
            'stunMaker': config.get_img_path("StunMaker"),
            'BackgroundLayer1': config.get_img_path("BackgroundLayer1"),
            'BackgroundLayer2': config.get_img_path("BackgroundLayer2"),
            'BackgroundLayer3': config.get_img_path("BackgroundLayer3"),
            'missing_texture': config.get_img_path("missing_texture"),
            'Walking_Kid': config.get_img_path("Walking_Kid"),
            'Idle_Kid': config.get_img_path("Standing Kid"),
            'Walking_ghost': config.get_img_path("Walking ghost"),
            'Idle_Ghost': config.get_img_path("Standing Ghost"),
            'cadena': config.get_img_path("cadena"),
            'chain': config.get_img_path("chain")
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
    
    def getTransparentImage(self,target_width, target_height):
        image = pygame.Surface((target_width,target_height), pygame.SRCALPHA)
        return image
    
    def surface_to_grayscale(self,surface):
        '''
        Transforme une surface Pygame en noir et blanc (nuances de gris).
        '''
        surface_gris = pygame.Surface(surface.get_size())
        surface_gris = surface_gris.convert_alpha()
        
        # Parcourir tous les pixels
        for x in range(surface.get_width()):
            for y in range(surface.get_height()):
                couleur = surface.get_at((x, y))
                # Calculer la valeur de gris
                gris = int(0.299 * couleur.r + 0.587 * couleur.g + 0.114 * couleur.b)
                # Créer la nouvelle couleur en nuances de gris
                couleur_gris = (gris, gris, gris, couleur.a)  # Conserver l'alpha
                surface_gris.set_at((x, y), couleur_gris)
        
        return surface_gris