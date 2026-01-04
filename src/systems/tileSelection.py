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



    def updatePointedTile(self,level:list, offset=(0, 0)):
        mousePos = pygame.mouse.get_pos()
        level_mouse_x = mousePos[0] - offset[0]
        level_mouse_y = mousePos[1] - offset[1]
        self.pointedTile = self.getTileWithPixel((level_mouse_x, level_mouse_y), level)

    def update(self,level:list, offset=(0, 0)):
        if self.active:
            self.updatePointedTile(level, offset)
            self.selectionListener()

    def activate(self):
        self.active = True
        self.pointedTile = None
        self.selectedTile = None
        self.activation_time = pygame.time.get_ticks()


    def selectionListener(self):
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] and self.pointedTile and pygame.time.get_ticks() - self.activation_time >= 200 and "ground" in self.pointedTile.structures.keys():
            self.selectedTile = self.pointedTile
            self.active = False
            return True
        return False

    def display(self, screen, offset=(0, 0)):
        '''
        Affiche le cadre de sélection autour de la tuile survolée.
        '''
        if self.active and self.pointedTile:
            x = self.pointedTile.grid_x * config.TILE_SIZE + offset[0]
            y = self.pointedTile.grid_y * config.TILE_SIZE + offset[1]
            size = config.TILE_SIZE
            color = (0, 200, 100)
            thickness = 10

            pygame.draw.line(screen, color, (x, y), (x + size, y), thickness)
            pygame.draw.line(screen, color, (x + size, y), (x + size, y + size), thickness)
            pygame.draw.line(screen, color, (x + size, y + size), (x, y + size), thickness)
            pygame.draw.line(screen, color, (x, y + size), (x, y), thickness)
    

