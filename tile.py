from player import *
from structures import *
import pygame
class Tile:
    def __init__ (self, grid_x:int, grid_y:int, width:int, height:int, tile_type:str, tile_size):
        self.grid_x = grid_x
        self.grid_y = grid_y

        self.pixel_x = self.grid_x*tile_size
        self.pixel_y = self.grid_y*tile_size

        self.width = width
        self.height = height

        self.tile_type = tile_type # type de la tile (exemple : "sol", "échelle", "bouton", "vide")

        self.background = self.find_color()

        self.structures = self.structures_builder() #Tab contenant l'ensemble des structures (sous forme d'objet rect pygames) présentent dans la tile


    def find_color(self):
        '''
        Fonction qui choisit la couleur en fonction du type de la tile
        sorties: la couleur en rgb
        '''
        if self.tile_type == "sol" or self.tile_type == "vide"or self.tile_type == "ladder" or self.tile_type == "left_door":
            return (100,100,150)
        elif self.tile_type == "start":
            return (000,250,50)
        elif self.tile_type == "end":
            return (000,50,250)
        elif self.tile_type == "button":
            return (100,0,100)
    def draw(self,screen):
        '''
        Fonction qui dessine la tile puis les structures qu'elle conttient
        entrées: screen
        sorties: none
        '''
        pygame.draw.rect(screen,self.background,(self.pixel_x, self.pixel_y, self.width, self.height))
        for structure in self.structures:
            pygame.draw.rect(screen,structure.color,structure.rect)


    def structures_builder(self) -> list:
        '''
        Fonction qui construit un tableau avec toute les structures de la tile en fonction de son type
        entrées: 
            self
        sorties: 
            la liste contenant les structures
        '''
        res= []
        if self.tile_type == "sol" or self.tile_type == "start" or self.tile_type=="end" or self.tile_type=="ladder" or self.tile_type == "left_door" or self.tile_type == "button":
            res.append(Ground(self.pixel_x,self.pixel_y,self.width,self.height))
        if self.tile_type == "left_door":
            res.append(Door(self.pixel_x,self.pixel_y,self.width,self.height))
        
        
        return res