from pygame import *
class Ground:
    def __init__(self,pixel_x,pixel_y,tile_width,tile_height):
        self.type = "ground"

        self.pixel_x = pixel_x
        self.pixel_y = pixel_y+(0.8*tile_height)

        self.width = tile_width
        self.height = tile_height*0.2

        self.rect = Rect(self.pixel_x, self.pixel_y,self.width,self.height)

        self.color = (100,100,0)

    def draw(self, screen, asset_manager):
        '''Dessine le sol avec une image'''
        image = asset_manager.get_scaled_image('ground', self.width, self.height)
        screen.blit(image, (self.pixel_x, self.pixel_y))



class Door:
    def __init__(self,pixel_x,pixel_y,tile_width,tile_height,door_id):
        self.type = "door"
        self.door_id = door_id

        self.pixel_x = pixel_x
        self.pixel_y = pixel_y

        self.width = 20
        self.height = tile_height*0.8

        self.rect = Rect(self.pixel_x, self.pixel_y,self.width,self.height)

        self.color = (150, 0, 0)

        self.is_open = False

    def draw(self, screen, asset_manager):
        '''Dessine la porte avec l'image appropriée'''
        image = asset_manager.get_scaled_image('door', self.width, self.height)
        screen.blit(image, (self.pixel_x, self.pixel_y))



    def open(self):
        self.is_open = True
        self.color = (0, 200, 0)

    def close(self):
        self.is_open = False
        self.color = (150, 0, 0)


class Button:
    def __init__(self,pixel_x,pixel_y,tile_width,tile_height,button_id):
        self.type = "button"
        self.button_id = button_id

        self.pixel_x = pixel_x + (1/3 * tile_width) 
        self.pixel_y = pixel_y + (5/6 * tile_height) - tile_height*0.2

        self.width = 1/3 * tile_width
        self.height = 1/6 * tile_height

        self.rect = Rect(self.pixel_x, self.pixel_y,self.width,self.height)

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
