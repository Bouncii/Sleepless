import pygame
import pygame_gui
import random

class Menu:
    def __init__(self):
        self.window_width, self.window_height = pygame.display.get_surface().get_size()
        self.manager = pygame_gui.UIManager((self.window_width, self.window_height), 'theme.json')
        self.elements = []
        self.build_ui()
        
    def build_ui(self):
        # Supprimer les anciens éléments
        for e in self.elements:
            e.kill()
        self.elements = []


        # Ajoute un titre
        self.title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, self.window_height//3 - 100), (self.window_width, 100)),
            text='SleepLess',
            manager=self.manager
        )
        self.elements.append(self.title)

        # Ajoute un boutton pour jouer
        self.play_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_width//2 - 50, self.window_height//2), (100, 50)),
            text='Play',
            manager=self.manager
        )
        self.play_button.state = "menu"
        self.elements.append(self.play_button)

    # Fonction pour rebuild l'UI qui rappelle build_ui
    def rebuild_ui(self):
        self.manager.set_window_resolution((self.window_width, self.window_height))
        self.build_ui()

    # Update la classe
    def update(self, delta):
        self.manager.update(delta)

    # Dessine les elements
    def draw(self, screen):
        self.manager.draw_ui(screen)

class Fin:
    def __init__(self, message=None):
        self.window_width, self.window_height = pygame.display.get_surface().get_size()
        self.manager = pygame_gui.UIManager((self.window_width, self.window_height), 'theme.json')
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


        # Ajoute un titre
        self.title_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, self.window_height//3 - 50), (self.window_width, 50)),
            text=self.message,
            manager=self.manager
        )
        self.elements.append(self.title_label)

         # Ajoute un boutton pour rejouer
        self.replay_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_width//2.5 - 100, self.window_height//1.5 - 25), (200, 50)),
            text='Replay this level ?',
            manager=self.manager
        )
        self.replay_button.state = "win"
        self.elements.append(self.replay_button)

        # Ajoute un boutton pour changer de niveau
        self.next_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_width//1.5 - 100, self.window_height//1.5 - 25), (200, 50)),
            text='Next Level',
            manager=self.manager
        )
        self.next_button.state = "win"
        self.elements.append(self.next_button)

    # Fonction pour rebuild l'UI qui rappelle build_ui
    def rebuild_ui(self,message=None):
        if message:
            self.message = message
        self.manager.set_window_resolution((self.window_width, self.window_height))
        self.build_ui()

    # Update la classe
    def update(self, delta):
        self.manager.update(delta)

    # Dessine les elements
    def draw(self, screen):
        self.manager.draw_ui(screen)

class Pause:
    def __init__(self):
        self.window_width, self.window_height = pygame.display.get_surface().get_size()
        self.manager = pygame_gui.UIManager((self.window_width, self.window_height), 'theme.json')
        self.elements = []
        self.build_ui()
        
    def build_ui(self):
        # Supprimer les anciens éléments
        for e in self.elements:
            e.kill()
        self.elements = []

        # Ajoute un titre
        self.title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, self.window_height//3 - 100), (self.window_width, 100)),
            text='Menu Pause',
            manager=self.manager
        )
        self.elements.append(self.title)

         # Ajoute un boutton pour rejouer
        self.continue_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_width//2.5 - 100, self.window_height//1.5 - 25), (200, 50)),
            text='Continue this level ?',
            manager=self.manager
        )
        self.continue_button.state = "pause"
        self.elements.append(self.continue_button)

        # Ajoute un boutton pour changer de niveau
        self.controls_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_width//1.5 - 100, self.window_height//1.5 - 25), (200, 50)),
            text='Show game controls',
            manager=self.manager
        )
        self.controls_button.state = "pause"
        self.elements.append(self.controls_button)

    # Fonction pour rebuild l'UI qui rappelle build_ui
    def rebuild_ui(self,message=None):
        if message:
            self.message = message
        self.manager.set_window_resolution((self.window_width, self.window_height))
        self.build_ui()

    # Update la classe
    def update(self, delta):
        self.manager.update(delta)

    # Dessine les elements
    def draw(self, screen):
        self.manager.draw_ui(screen)