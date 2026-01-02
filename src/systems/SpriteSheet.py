import pygame

class SpriteSheet():
    def __init__(self, image, number_of_animation):
        self.sheet = image
        self.nbr_animation = number_of_animation
        self.dimension = self.sheet.get_size()
        
        self.avg_frame_width = self.dimension[0] / number_of_animation
        self.frame_height = self.dimension[1]

    def get_image(self, frame, asset_manager):
        x_start = int(frame * self.avg_frame_width)
        x_end = int((frame + 1) * self.avg_frame_width)
        width = x_end - x_start

        image = asset_manager.getTransparentImage(width, self.frame_height)
        rect = pygame.Rect(x_start, 0, width, self.frame_height)
        image.blit(self.sheet, (0, 0), rect)
        
        return image

    def draw(self, screen, player, frame_nbr, asset_manager, scale=1, facing_left=False):
        image = self.get_image(frame_nbr, asset_manager)
        
        if facing_left:
            image = pygame.transform.flip(image, True, False)
            
        target_height = player.height * scale
        ratio_affichage = target_height / self.frame_height
        fixed_display_width = int(self.avg_frame_width * ratio_affichage)
        
        image = pygame.transform.scale(image, (fixed_display_width, int(target_height)))

        image_rect = image.get_rect()
        
        image_rect.midbottom = player.rect.midbottom
        screen.blit(image, image_rect)