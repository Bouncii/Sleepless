# Fichier: src/entities/objects
import pygame
from src.core.config import *
from src.core.constants import ItemTypes
import math

class Item():
    def __init__(self, grid_x:int, grid_y:int,ItemType:ItemTypes):
        self.height = 0.2*config.TILE_SIZE
        self.width = 0.2*config.TILE_SIZE

        self.grid_x = grid_x
        self.grid_y = grid_y

        self.pixel_x = self.grid_x * config.TILE_SIZE + (config.TILE_SIZE - self.width) // 2
        self.pixel_y = self.grid_y * config.TILE_SIZE + int(config.TILE_SIZE*0.7) - self.height
        self.base_mid_vertival_point = self.pixel_y + (self.height // 2) 
        self.current_mid_vertival_point = self.pixel_y + (self.height // 2) 

        self.rect = pygame.Rect(self.pixel_x,self.pixel_y,self.width,self.height)

        self.type = ItemType

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

    def display(self, screen, asset_manager, offset):
        image = asset_manager.get_scaled_image(self.type, self.width, self.height)
        screen.blit(image, (self.pixel_x + offset[0], self.pixel_y + offset[1]))