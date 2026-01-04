import pygame
import pygame_gui
import random
import os

DARK_TEAL = (15, 30, 38) 

class Menu:
    def __init__(self):
        self.window_width, self.window_height = pygame.display.get_surface().get_size()
        
        self.manager = pygame_gui.UIManager((self.window_width, self.window_height), 'theme.json')

        self.background = None

        if os.path.exists("background.png"):
            self.background = pygame.image.load("background.png").convert()
            self.background = pygame.transform.scale(self.background, (self.window_width, self.window_height))
        
        self.elements = []
        self.build_ui()
        
    def build_ui(self):
        # Supprimer les anciens éléments
        for e in self.elements:
            e.kill()
        self.elements = []


        # Ajoute un titre
        self.title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, self.window_height//4), (self.window_width, 150)),
            text='SLEEPLESS',
            manager=self.manager,
            object_id='#main_title'
        )
        self.elements.append(self.title)

        # Ajoute un boutton pour jouer
        btn_width = 220
        btn_height = 65
        self.play_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.window_width//2 - btn_width//2, self.window_height//1.8), 
                (btn_width, btn_height)
            ),
            text='Start the Dream',
            manager=self.manager
        )
        self.play_button.state = "menu"
        self.elements.append(self.play_button)

    # Fonction pour rebuild l'UI qui rappelle build_ui
    def rebuild_ui(self):
        self.window_width, self.window_height = pygame.display.get_surface().get_size()
        self.manager.set_window_resolution((self.window_width, self.window_height))
        if self.background:
             self.background = pygame.transform.scale(self.background, (self.window_width, self.window_height))
        self.build_ui()
    # Update la classe
    def update(self, delta):
        self.manager.update(delta)
    # Dessine les elements
    def draw(self, screen):
        if self.background:
            screen.blit(self.background, (0,0))
        else:
            screen.fill(DARK_TEAL)
        self.manager.draw_ui(screen)

class Fin:
    def __init__(self, message=None):
        self.window_width, self.window_height = pygame.display.get_surface().get_size()
        self.manager = pygame_gui.UIManager((self.window_width, self.window_height), 'theme.json')
        self.elements = []
        self.level_messages = [
            "The nightmare fades away...",
            "A glimmer of hope...",
            "Level purified.",
            "The dream continues..."
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
            relative_rect=pygame.Rect((0, self.window_height//4), (self.window_width, 100)),
            text=self.message,
            manager=self.manager,
            object_id='#main_title'
        )
        self.elements.append(self.title_label)

        # Ajoute un boutton pour rejouer
        btn_width = 220
        self.replay_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_width//2 - btn_width - 20, self.window_height//1.8), (btn_width, 50)),
            text='Replay Level',
            manager=self.manager
        )
        self.replay_button.state = "win"
        self.elements.append(self.replay_button)

        # Ajoute un boutton pour changer de niveau
        self.next_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_width//2 + 20, self.window_height//1.8), (btn_width, 50)),
            text='Next Dream',
            manager=self.manager
        )
        self.next_button.state = "win"
        self.elements.append(self.next_button)

    def rebuild_ui(self, message=None):
        if message: self.message = message
        self.window_width, self.window_height = pygame.display.get_surface().get_size()
        self.manager.set_window_resolution((self.window_width, self.window_height))
        self.build_ui()

    def update(self, delta):
        self.manager.update(delta)

    def draw(self, screen):
        overlay = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)) 
        screen.blit(overlay, (0,0))
        self.manager.draw_ui(screen)

class Pause:
    def __init__(self):
        self.window_width, self.window_height = pygame.display.get_surface().get_size()
        self.manager = pygame_gui.UIManager((self.window_width, self.window_height), 'theme.json')
        self.elements = []
        self.build_ui()
        
    def build_ui(self):
        for e in self.elements:
            e.kill()
        self.elements = []

        self.title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, self.window_height//5), (self.window_width, 100)),
            text='Pause',
            manager=self.manager,
            object_id='#main_title'
        )
        self.elements.append(self.title)

        center_x = self.window_width // 2 - 125 
        start_y = self.window_height // 2.2
        gap = 60

        self.continue_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((center_x, start_y), (250, 50)),
            text='Resume',
            manager=self.manager
        )
        self.continue_button.state = "pause"
        self.elements.append(self.continue_button)

        # Ajoute un boutton pour voir la liste de contrôles
        self.controls_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((center_x, start_y + gap), (250, 50)),
            text='Controls',
            manager=self.manager
        )
        self.controls_button.state = "pause"
        self.elements.append(self.controls_button)

        self.leave_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((center_x, start_y + gap*2), (250, 50)),
            text='Quit Game',
            manager=self.manager
        )
        self.leave_button.state = "pause"
        self.elements.append(self.leave_button)

    def rebuild_ui(self, message=None):
        self.window_width, self.window_height = pygame.display.get_surface().get_size()
        self.manager.set_window_resolution((self.window_width, self.window_height))
        self.build_ui()

    # Update la classe
    def update(self, delta):
        self.manager.update(delta)

    # Dessine les elements
    def draw(self, screen):
        # Overlay Bleu Nuit transparent au lieu de violet
        overlay = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
        overlay.fill((10, 20, 25, 200)) 
        screen.blit(overlay, (0,0))
        self.manager.draw_ui(screen)

class Controls:
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

        # Titre
        self.title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 30), (self.window_width, 80)),
            text='Controls',
            manager=self.manager,
            object_id='#main_title'
        )
        self.elements.append(self.title)

        controls_text = (
            "<font color='#4db6ac' size=5><b>MOVEMENT</b></font><br>"
            "Move Left / Right : <b>Q / D</b><br>"
            "Climb Up / Down : <b>Z / S</b><br><br>"
            
            "<font color='#4db6ac' size=5><b>ACTIONS</b></font><br>"
            "Switch Item : <b><-  -></b><br>"
            "Use Item : <b>Enter</b><br><br>"
            "Select Tile : <b>Left Click</b><br><br>"
            
            "<font color='#4db6ac' size=5><b>SYSTEM</b></font><br>"
            "Pause : <b>Esc</b><br>"
            "Restart : <b>R</b>"
        )

        self.controls_label = pygame_gui.elements.UITextBox(
            html_text=controls_text,
            relative_rect=pygame.Rect(
                (self.window_width//2 - 300, self.window_height//4 + 20),
                (600, 400)
            ),
            manager=self.manager
        )
        self.elements.append(self.controls_label)

        # Bouton retour
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.window_width//2 - 100, self.window_height - 100),
                (200, 50)
            ),
            text='Back',
            manager=self.manager
        )
        self.back_button.state = "controls"
        self.elements.append(self.back_button)

    def rebuild_ui(self, message=None):
        self.window_width, self.window_height = pygame.display.get_surface().get_size()
        self.manager.set_window_resolution((self.window_width, self.window_height))
        self.build_ui()

    def update(self, delta):
        self.manager.update(delta)

    def draw(self, screen):
        screen.fill(DARK_TEAL)
        self.manager.draw_ui(screen)