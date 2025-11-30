# src/systems/interaction_manager.py
class InteractionManagerButtonsDoors:
    def __init__(self):
        self.connections = {}  # {button_id: [door_id1, door_id2, ...]}
        self.pressed_buttons = []
        self.doors = {}  # {door_id: objet door}
        self.buttons = {}  # {button_id: objet button}
    
    def register_door(self, door_id, door_object):
        '''
        Fonction qui enregistre une porte dans le manager
        entrées :
          door_id : int
          door_object : Door
        sortie : None
        '''
        self.doors[door_id] = door_object
        #Ferme la porte par défaut
        door_object.close()  
    
    def register_button(self, button_id, button_object):
        '''
        Fonction qui enregistre un bouton dans le manager
        entrées :
          button_id : int
          button_object : Button
        sortie : None
        '''
        self.buttons[button_id] = button_object
    
    def add_connection(self, button_id, door_id):
        '''
        Fonction qui établit une connexion entre un bouton et une porte
        entrées :
          button_id : int
          door_id : int
        sortie : None
        '''
        if button_id not in self.connections:
            self.connections[button_id] = []
        self.connections[button_id].append(door_id)
    
    def button_pressed(self, button_id):
        '''
        Fonction qui est appelé quand un bouton est pressé
        entrées :
          button_id : int
        sortie : none
        '''
        self.pressed_buttons.append(button_id)
        if button_id in self.buttons:
            self.buttons[button_id].press()
        self.update_doors()
    
    def button_released(self, button_id):
        '''
        Fonction qui est appelé quand un bouton est relâché
        entrées :
          button_id : int
        sortie : none
        '''
        if button_id in self.pressed_buttons:
            self.pressed_buttons.remove(button_id)
        if button_id in self.buttons:
            self.buttons[button_id].release()
        self.update_doors()
    
    def update_doors(self):
        '''Fonction qui met à jour l'état de toutes les portes'''
        # Récupère toutes les portes concernées par les boutons pressés
        affected_doors = []
        for button_id in self.pressed_buttons:
            if button_id in self.connections:
                affected_doors += self.connections[button_id]
        # Ouvre/ferme les portes
        for door_id, door_obj in self.doors.items():
            if door_id in affected_doors:
                door_obj.open()
            else:
                door_obj.close()
    
    def is_door_open(self, door_id):
        '''
        Fonction qui vérifie si une porte est ouverte
        entrées :
          door_id : int
        sortie : none
        '''
        return door_id in self.doors and self.doors[door_id].is_open
    
class InteractionInventoryLevel:
    pass