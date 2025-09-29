import pygame
class Past_self:
    def __init__ (self,deplacements:list,width,height,tile_size):
        self.deplacements = deplacements

        self.pixel_x = self.grid_x*tile_size
        self.pixel_y = self.grid_y*tile_size

        self.width = width
        self.height = height