# Fichier: src/entities/objects
import pygame
from src.core.constants import *
import math

#Class qui va être hérité des différents types d'items
class Item():
    def __init__(self, grid_x:int, grid_y:int, durability:int):
        self.height = 0.2*TILE_SIZE
        self.width = 0.2*TILE_SIZE

        self.grid_x = grid_x
        self.grid_y = grid_y

        self.pixel_x = self.grid_x * TILE_SIZE + (TILE_SIZE - self.width) // 2
        self.pixel_y = self.grid_y * TILE_SIZE + int(TILE_SIZE*0.7) - self.height
        self.base_mid_vertival_point = self.pixel_y + (self.height // 2) 
        self.current_mid_vertival_point = self.pixel_y + (self.height // 2) 

        self.rect = pygame.Rect(self.pixel_x,self.pixel_y,self.width,self.height)

        self.durability = durability

        self.is_in_inventory = False

        self.animation_speed = 50
        self.current_animation_direction = 1 # 1 = bas, -1 = haut 
        self.vertical_animation_range = 20 # 20 pixel vers le bas + 20 pixel vers le bas

        self.time = 0

    def animate(self,dt):
        self.time += dt

        amplitude = 10
        speed = 2
        
        offset = math.sin(self.time * speed) * amplitude

        self.pixel_y = self.base_mid_vertival_point - (self.height // 2) + offset



class PortalMakerItem(Item):
    def __init__(self,grid_x:int, grid_y:int, durability:int):
        super().__init__(grid_x,grid_y,durability)
        self.type = "portalMaker"

    def display(self, screen, asset_manager):
        image = asset_manager.get_scaled_image(self.type, self.width, self.height)
        screen.blit(image, (self.pixel_x, self.pixel_y))
        
    def using(self):
        pass

class StunItem(Item):
    def __init__(self,grid_x:int, grid_y:int, durability:int):
        super().__init__(grid_x,grid_y,durability)
        self.type = "StunMaker"

    def display(self, screen, asset_manager):
        image = asset_manager.get_scaled_image(self.type, self.width, self.height)
        screen.blit(image, (self.pixel_x, self.pixel_y))

    def using(self):
        pass