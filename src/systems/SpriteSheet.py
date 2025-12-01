import pygame
# Walk.png, dimension : 1536x128, 12 animations -> 128x128 par animation
# Idle.png, dimension : 896x128, 7 animations -> 128x128 par animation

class SpriteSheet():
    def __init__(self, image, number_of_animation):
        self.sheet = image
        self.nbr_animation = number_of_animation
        self.dimension = self.sheet.get_size()
        self.frame_width = self.dimension[0] // number_of_animation
        self.frame_height = self.dimension[1]

    def get_image(self, frame, scale, asset_manager):
        image = asset_manager.getTransparentImage(self.frame_width, self.frame_height)
        rect = pygame.Rect(frame * self.frame_width, 0, self.frame_width, self.frame_height)
        image.blit(self.sheet, (0, 0), rect)
        if scale != 1:
            image = pygame.transform.scale(image, (self.frame_width * scale, self.frame_height * scale))
        return image

    def draw(self, screen, player, frame_nbr, asset_manager, scale=1, facing_left=False):
        image = self.get_image(frame_nbr, scale, asset_manager)
        if facing_left:
            image = pygame.transform.flip(image, True, False)
        image = pygame.transform.scale(image, (player.rect.width, player.rect.height))
        screen.blit(image, player.rect.topleft)