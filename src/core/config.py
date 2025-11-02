# src/core/config.py
import os
from .constants import Paths
class Config:
    """
    Configuration modifiable à l'exécution
    """
    
    def __init__(self):
        self.screen_size = (1920, 1080)
        self.debug_mode = False
        self.sound_volume = 1.0
    def get_level_path(self, level_num):
        """Retourne le chemin complet vers un fichier de niveau"""
        return os.path.join(Paths.LEVELS, f"level{level_num}.txt")
    def get_img_path(self, nom_image):
        """Retourne le chemin complet vers un fichier image"""
        return os.path.join(Paths.IMAGES, f"{nom_image}.png")
config = Config()
