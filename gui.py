import pygame
import pygame_gui
import random

class Menu:
    def __init__(self, GRID_WIDTH, TILE_SIZE, GRID_HEIGHT):
        self.manager = pygame_gui.UIManager((GRID_WIDTH*TILE_SIZE, GRID_HEIGHT*TILE_SIZE), 'theme.json')
        self.play_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((GRID_WIDTH*TILE_SIZE//2 - 100//2, GRID_HEIGHT*TILE_SIZE//1.5 - 50//2), (100, 50)),
            text='Play',
            manager=self.manager
        )
        self.title_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, GRID_HEIGHT*TILE_SIZE//3 - 100), (GRID_WIDTH*TILE_SIZE, 50)),
            text='SleepLess',
            manager=self.manager,
            object_id=pygame_gui.core.ObjectID(class_id="#menu_titre")
        )

    def update(self, delta):
        self.manager.update(delta)

    def draw(self, screen):
        self.manager.draw_ui(screen)

class Fin:
    def __init__(self, GRID_WIDTH, TILE_SIZE, GRID_HEIGHT):
        level_messages = [
            "Congratulations! You've cleared this level!",
            "Well done! You've completed this level!",
            "Great job! Level cleared!",
            "Level complete! Fantastic work!",
            "You did it! This level is cleared!"
        ]

        self.manager = pygame_gui.UIManager((GRID_WIDTH*TILE_SIZE, GRID_HEIGHT*TILE_SIZE), 'theme.json')
        self.title_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, GRID_HEIGHT*TILE_SIZE//3 - 100), (GRID_WIDTH*TILE_SIZE, 50)),
            text= random.choice(level_messages),
            manager=self.manager,
        )
        self.replay_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((GRID_WIDTH*TILE_SIZE//2 - 100//2, GRID_HEIGHT*TILE_SIZE//1.5 - 50//2), (100, 50)),
            text='Replay ?',
            manager=self.manager
        )

    def update(self, delta):
        self.manager.update(delta)

    def draw(self, screen):
        self.manager.draw_ui(screen)