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



class Door:
  def __init__(self,pixel_x,pixel_y,tile_width,tile_height):
    self.type = "door"

    self.pixel_x = pixel_x
    self.pixel_y = pixel_y

    self.width = 20
    self.height = tile_height*0.8
 
    self.rect = Rect(self.pixel_x, self.pixel_y,self.width,self.height)

    self.color = (0,150,0)

class Button:
  def __init__(self,pixel_x,pixel_y,tile_width,tile_height,door):
    self.type = "button"

    self.pixel_x = pixel_x
    self.pixel_y = pixel_y

    self.width = 20
    self.height = tile_height*0.8
 
    self.rect = Rect(self.pixel_x, self.pixel_y,self.width,self.height)

    self.color = (0,150,0)

    self.door = door