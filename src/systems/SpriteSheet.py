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
        img = pygame.image.load(image)
        self.dimension = img.get_size()
        self.frame_dimension = (self.dimension[0]//number_of_animation, self.dimension[1])
    
    def get_image(self,frame,scale):
        image = pygame.Surface((self.dimension[0],self.dimension[1])).convert_alpha()
        image.blit(self.sheet,(0,0),((frame*self.dimension[0]),0,self.dimension[0],self.dimension[1]))
        image = pygame.transform.scale(image,(self.dimension[0]*scale,self.dimension[1]*scale))
        return image

    def draw(self, screen, player, frame_nbr):
            image = self.get_image(frame_nbr,1)
            screen.blit(image, player.rect.topleft)