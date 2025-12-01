import pygame
from src.core.constants import*
class TileSelection:
    def __init__(self):
        self.active = True
        self.selectedTile = None

    def getTileWithPixel(self,mousePos:tuple,level:list):
        for i in range(len(level)):
            for j in range(len(level[0])):
                tile = level[i][j]
                if tile.rect.collidepoint(mousePos):
                    return tile
        return None



    def updateSelectedTile(self,level:list):
        mousePos = pygame.mouse.get_pos()
        self.selectedTile = self.getTileWithPixel(mousePos,level)

    def update(self,level:list):
        if self.active:
            self.updateSelectedTile(level)
            print(self.selectedTile)

    def display(self,screen):
        if self.active and self.selectedTile:
            pygame.draw.line(screen,(0,200,100),(TILE_SIZE*self.selectedTile.grid_x,self.selectedTile.grid_y*TILE_SIZE),(TILE_SIZE*self.selectedTile.grid_x+TILE_SIZE,self.selectedTile.grid_y*TILE_SIZE),10)
            pygame.draw.line(screen,(0,200,100),(TILE_SIZE*self.selectedTile.grid_x+TILE_SIZE,self.selectedTile.grid_y*TILE_SIZE),(TILE_SIZE*self.selectedTile.grid_x+TILE_SIZE,self.selectedTile.grid_y*TILE_SIZE + TILE_SIZE),10)
            pygame.draw.line(screen,(0,200,100),(TILE_SIZE*self.selectedTile.grid_x+TILE_SIZE,self.selectedTile.grid_y*TILE_SIZE + TILE_SIZE),(TILE_SIZE*self.selectedTile.grid_x,self.selectedTile.grid_y*TILE_SIZE + TILE_SIZE),10)
            pygame.draw.line(screen,(0,200,100),(TILE_SIZE*self.selectedTile.grid_x,self.selectedTile.grid_y*TILE_SIZE + TILE_SIZE),(TILE_SIZE*self.selectedTile.grid_x,self.selectedTile.grid_y*TILE_SIZE),10)
    

