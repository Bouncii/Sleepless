from pygame import *
class Ground:
  def __init__(self,pixel_x,pixel_y,tile_width,tile_height):
    self.pixel_x = pixel_x
    self.pixel_y = pixel_y

    self.rect = Rect(pixel_x, pixel_y+(0.8*tile_height),tile_width,tile_height*0.2)

    self.color = (100,100,0)
