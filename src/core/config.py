# src/core/config.py
import os
from .constants import Paths
class Config:
    """
    Configuration modifiable à l'exécution
    """
    
    def __init__(self):
        self.current_level = 0
        self.nb_levels = 2
        self.screen_size = (1024, 768)
        self.debug_mode = False
        self.sound_volume = 1.0
    def get_level_path(self, level_num):
        """Retourne le chemin complet vers un fichier de niveau"""
        return os.path.join(Paths.LEVELS, f"level{level_num}.txt")
config = Config()
