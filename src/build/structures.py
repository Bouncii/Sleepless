import pygame
from src.systems import SpriteSheet
class Ground:
    def __init__(self,pixel_x,pixel_y,tile_width,tile_height):
        self.type = "ground"

        self.pixel_x = pixel_x
        self.pixel_y = pixel_y+(0.8*tile_height)

        self.width = tile_width
        self.height = tile_height*0.2

        self.rect = pygame.Rect(self.pixel_x, self.pixel_y,self.width,self.height)

        self.color = (100,100,0)

    def draw(self, screen, asset_manager):
        image = asset_manager.get_scaled_image('ground', self.width, self.height) 
        visual_offset = 0
        draw_position_y = self.pixel_y - visual_offset
        
        screen.blit(image, (self.pixel_x, draw_position_y))

        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)

class Ladder:
    def __init__(self,pixel_x,pixel_y,tile_width,tile_height):
        self.type = "ladder"

        self.pixel_x = pixel_x
        self.pixel_y = pixel_y

        self.width = tile_width*0.8
        self.height = tile_height*0.8

        self.rect = self.rect = pygame.Rect(self.pixel_x+tile_height*0.1, self.pixel_y,self.width,self.height)
        self.color = (100,100,0)

    def draw(self, screen, asset_manager):
        '''Dessine le sol avec une image'''
        image = asset_manager.get_scaled_image('ladder', self.width, self.height)
        screen.blit(image, self.rect.topleft)

class End:
    def __init__(self,pixel_x,pixel_y,tile_width,tile_height):
        self.type = "ground"

        self.width = tile_width * 5/6
        self.height = tile_height * 4/6

        self.pixel_x = pixel_x + (1/12 * tile_width) 
        self.pixel_y = pixel_y  + tile_height - tile_height*0.2 - self.height


        self.rect = pygame.Rect(self.pixel_x, self.pixel_y,self.width,self.height)
        self.color = (100,100,0)

    def draw(self, screen, asset_manager):
        '''Dessine le sol avec une image'''
        image = asset_manager.get_scaled_image('end', self.width, self.height)
        screen.blit(image, self.rect.topleft)


class Door:
    def __init__(self, pixel_x, pixel_y, tile_width, tile_height, door_id, side):   
        self.door_id = door_id

        self.pixel_x = pixel_x-1/5*tile_width
        self.pixel_y = pixel_y+5
    
        self.width = tile_width*0.6
        self.height = tile_height * 0.8

        self.tile_width = tile_width
        self.tile_height = tile_height

        if side == "left":
            self.type = "door_left"
            self.rect = pygame.Rect(self.pixel_x, self.pixel_y, self.width, self.height)
        else:
            self.type = "door_right"
            self.rect = pygame.Rect(self.pixel_x + self.tile_width - self.width, self.pixel_y, self.width, self.height)
        
        self.is_open = False
        self.side = side

        self.sprite_sheet = None
        self.total_frames = 17
        self.current_frame = 0
        
        self.last_update_time = 0
        self.frame_delay = 50

    def draw(self, screen, asset_manager):
        if self.sprite_sheet is None:
            self.sprite_sheet = SpriteSheet(asset_manager.get_image('door'), self.total_frames)

        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.frame_delay:
            self.last_update_time = current_time
            
            if self.is_open:
                if self.current_frame < self.total_frames - 1:
                    self.current_frame += 1
            else:
                if self.current_frame > 0:
                    self.current_frame -= 1

        if not self.is_open or self.current_frame != self.total_frames - 1:
            image = self.sprite_sheet.get_image(self.current_frame, asset_manager)
            scaled_image = pygame.transform.scale(image, (int(self.width), int(self.height)))
            
            screen.blit(scaled_image, (self.rect.x, self.rect.y))

    def open(self):
        self.is_open = True

    def close(self):
        self.is_open = False


class Button:
    def __init__(self,pixel_x,pixel_y,tile_width,tile_height,button_id):
        self.type = "button"
        self.button_id = button_id

        self.pixel_x = pixel_x + (1/3 * tile_width) 
        self.pixel_y = pixel_y + 1/3*tile_height

        self.width = 1/3 * tile_width
        self.height = 1/3 * tile_height

        self.rect = pygame.Rect(self.pixel_x, self.pixel_y,self.width,self.height)

        self.color = (200, 200, 0)

        self.is_pressed = False

    def draw(self, screen, asset_manager):
        '''Dessine le bouton avec l'image appropriée'''
        image = asset_manager.get_scaled_image('button', self.width, self.height)
        screen.blit(image, (self.pixel_x, self.pixel_y))

    def press(self):
        self.is_pressed = True
        self.color = (255, 100, 0)

    def release(self):
        self.is_pressed = False
        self.color = (200, 200, 0)
