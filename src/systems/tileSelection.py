import pygame
from src.core.config import*
class TileSelection:
    def __init__(self):
        self.active = False
        self.pointedTile = None
        self.selectedTile = None
        self.activation_time = 0

    def getTileWithPixel(self,mousePos:tuple,level:list):
        for i in range(len(level)):
            for j in range(len(level[0])):
                tile = level[i][j]
                if tile.rect.collidepoint(mousePos):
                    return tile
        return None



    def updatePointedTile(self,level:list):
        mousePos = pygame.mouse.get_pos()
        self.pointedTile = self.getTileWithPixel(mousePos,level)

    def update(self,level:list):
        if self.active:
            self.updatePointedTile(level)
            self.selectionListener()

    def activate(self):
        self.active = True
        self.pointedTile = None
        self.selectedTile = None
        self.activation_time = pygame.time.get_ticks()


    def selectionListener(self):
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] and self.pointedTile and pygame.time.get_ticks() - self.activation_time >= 200:
            self.selectedTile = self.pointedTile
            self.active = False
            return True
        return False

    def display(self,screen):
        if self.active and self.pointedTile:
            pygame.draw.line(screen,(0,200,100),(config.TILE_SIZE*self.pointedTile.grid_x,self.pointedTile.grid_y*config.TILE_SIZE),(config.TILE_SIZE*self.pointedTile.grid_x+config.TILE_SIZE,self.pointedTile.grid_y*config.TILE_SIZE),10)
            pygame.draw.line(screen,(0,200,100),(config.TILE_SIZE*self.pointedTile.grid_x+config.TILE_SIZE,self.pointedTile.grid_y*config.TILE_SIZE),(config.TILE_SIZE*self.pointedTile.grid_x+config.TILE_SIZE,self.pointedTile.grid_y*config.TILE_SIZE + config.TILE_SIZE),10)
            pygame.draw.line(screen,(0,200,100),(config.TILE_SIZE*self.pointedTile.grid_x+config.TILE_SIZE,self.pointedTile.grid_y*config.TILE_SIZE + config.TILE_SIZE),(config.TILE_SIZE*self.pointedTile.grid_x,self.pointedTile.grid_y*config.TILE_SIZE + config.TILE_SIZE),10)
            pygame.draw.line(screen,(0,200,100),(config.TILE_SIZE*self.pointedTile.grid_x,self.pointedTile.grid_y*config.TILE_SIZE + config.TILE_SIZE),(config.TILE_SIZE*self.pointedTile.grid_x,self.pointedTile.grid_y*config.TILE_SIZE),10)
    

