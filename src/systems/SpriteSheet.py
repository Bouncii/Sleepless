import pygame
# Walk.png, dimension : 1536x128, 12 animations -> 128x128 par animation
# Idle.png, dimension : 896x128, 7 animations

# TODO
# - une fonction qui recupère en splitant l'image à la xème etape de l'animation avec un modulo, plus ou moins get_image avec modification
# - une fonction qui applique au personnage l'image

class SpriteSheet():
    def __init__(self,image,number_of_animation):
        self.sheet = image
        self.nbr_animation = number_of_animation
        self.dimension = (1,1)
        self.frame_dimension = (1,1)
    
    def get_image(self,frame,width,height,scale):
        image = pygame.Surface((width,height)).convert_alpha()
        image.blit(self.sheet,(0,0),((frame*width),0,width,height))
        image = pygame.transform.scale(image,(width*scale,height*scale))
        return image
    
