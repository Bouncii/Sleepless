import pygame
import pygame_gui
import random

class Menu:
    def __init__(self, GRID_WIDTH, TILE_SIZE, GRID_HEIGHT):
        self.GRID_WIDTH = GRID_WIDTH
        self.GRID_HEIGHT = GRID_HEIGHT
        self.TILE_SIZE = TILE_SIZE
        self.manager = pygame_gui.UIManager((GRID_WIDTH*TILE_SIZE, GRID_HEIGHT*TILE_SIZE), 'theme.json')
        self.elements = []
        self.build_ui()

    def build_ui(self):
        # Supprimer les anciens éléments
        for e in self.elements:
            e.kill()
        self.elements = []

        width_window = self.GRID_WIDTH * self.TILE_SIZE
        height_window = self.GRID_HEIGHT * self.TILE_SIZE

        self.title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, height_window//3 - 50), (width_window, 50)),
            text='SleepLess',
            manager=self.manager
        )
        self.elements.append(self.title)

        self.play_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((width_window//2 - 50, height_window//2), (100, 50)),
            text='Play',
            manager=self.manager
        )
        self.elements.append(self.play_button)

    def rebuild_ui(self, GRID_WIDTH, TILE_SIZE, GRID_HEIGHT):
        self.GRID_WIDTH = GRID_WIDTH
        self.GRID_HEIGHT = GRID_HEIGHT
        self.TILE_SIZE = TILE_SIZE
        self.manager.set_window_resolution((GRID_WIDTH*TILE_SIZE, GRID_HEIGHT*TILE_SIZE))
        self.build_ui()

    def update(self, delta):
        self.manager.update(delta)

    def draw(self, screen):
        self.manager.draw_ui(screen)

class Fin:
    def __init__(self, GRID_WIDTH, TILE_SIZE, GRID_HEIGHT, message=None):
        self.GRID_WIDTH = GRID_WIDTH
        self.GRID_HEIGHT = GRID_HEIGHT
        self.TILE_SIZE = TILE_SIZE
        self.manager = pygame_gui.UIManager((GRID_WIDTH*TILE_SIZE, GRID_HEIGHT*TILE_SIZE), 'theme.json')
        self.elements = []
        self.level_messages = [
            "Congratulations! You've cleared this level!",
            "Well done! You've completed this level!",
            "Great job! Level cleared!",
            "Level complete! Fantastic work!",
            "You did it! This level is cleared!"
        ]
        self.message = message or random.choice(self.level_messages)
        self.build_ui()

    def build_ui(self):
        # Supprimer les anciens éléments
        for e in self.elements:
            e.kill()
        self.elements = []

        width_window = self.GRID_WIDTH * self.TILE_SIZE
        height_window = self.GRID_HEIGHT * self.TILE_SIZE

        self.title_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, height_window//3 - 50), (width_window, 50)),
            text=self.message,
            manager=self.manager
        )
        self.elements.append(self.title_label)

        self.replay_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((width_window//2.5 - 100, height_window//1.5 - 25), (200, 50)),
            text='Replay this level ?',
            manager=self.manager
        )
        self.elements.append(self.replay_button)

        self.next_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((width_window//1.5 - 100, height_window//1.5 - 25), (200, 50)),
            text='Next Level',
            manager=self.manager
        )
        self.elements.append(self.next_button)

    def rebuild_ui(self, GRID_WIDTH, TILE_SIZE, GRID_HEIGHT, message=None):
        self.GRID_WIDTH = GRID_WIDTH
        self.GRID_HEIGHT = GRID_HEIGHT
        self.TILE_SIZE = TILE_SIZE
        if message:
            self.message = message
        self.manager.set_window_resolution((GRID_WIDTH*TILE_SIZE, GRID_HEIGHT*TILE_SIZE))
        self.build_ui()

    def update(self, delta):
        self.manager.update(delta)

    def draw(self, screen):
        self.manager.draw_ui(screen)