# src/systems/interaction_manager.py

from src.core.constants import *

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
    
class InteractionManagerPortal:
    def __init__(self):
        self.active_pairs = [] # [ ((x1, y1), (x2, y2)), ((x3, y3), (x4, y4)) ] 
        self.pending_portal = None  # Stocke temporairement les coordonnées du 1er portail du duo en cours de construction

    def try_place_portal(self, grid_x: int, grid_y: int, level: list):
        '''
        Tente de placer un portail.
        Retourne True si le duo est complété (l'item doit être consommé), False sinon.
        '''
        tile = level[grid_y][grid_x]
        item_consumed = False

        if self.pending_portal is None:
            self.pending_portal = (grid_x, grid_y)
            
            if "portal_pending" not in tile.effects:
                tile.effects.append("portal_pending")
            
            print(f"Portail A (attente) posé en {grid_x}, {grid_y}")
            item_consumed = False
        
        else:
            if (grid_x, grid_y) != self.pending_portal:
                portal_A = self.pending_portal
                portal_B = (grid_x, grid_y)
                
                self.active_pairs.append((portal_A, portal_B))
                
                tile_A = level[portal_A[1]][portal_A[0]]
                if "portal_pending" in tile_A.effects:
                    tile_A.effects.remove("portal_pending")
                if "portal_active" not in tile_A.effects:
                    tile_A.effects.append("portal_active")
                
                if "portal_active" not in tile.effects:
                    tile.effects.append("portal_active")

                self.pending_portal = None
                
                print(f"Portail B posé en {grid_x}, {grid_y}. Liaison créée !")
                item_consumed = True
            
        return item_consumed

    def check_and_teleport_entity(self, entity, level):
        '''
        Vérifie si une entité est sur un portail actif de n'importe quel duo.
        Si oui, téléporte et détruit CE duo spécifique.
        '''
        entity_pos = (entity.grid_x, entity.grid_y)
        
        pair_to_remove = None
        target_pos = None

        for pair in self.active_pairs:
            if pair_to_remove is None:
                p1, p2 = pair
                
                if entity_pos == p1:
                    target_pos = p2
                    pair_to_remove = pair
                elif entity_pos == p2:
                    target_pos = p1
                    pair_to_remove = pair

        if pair_to_remove is not None and target_pos is not None:
            self._teleport_entity(entity, target_pos)

            self.active_pairs.remove(pair_to_remove)
            
            self._remove_visuals(level, pair_to_remove[0])
            self._remove_visuals(level, pair_to_remove[1])

            print(f"Téléportation effectuée ! Duo détruit.")

    def _teleport_entity(self, entity, target_pos):
        dest_x, dest_y = target_pos
        entity.grid_x = dest_x
        entity.grid_y = dest_y
        
        entity.pixel_x = dest_x * TILE_SIZE + (TILE_SIZE - entity.width) // 2
        entity.pixel_y = dest_y * TILE_SIZE + int(TILE_SIZE*0.8) - entity.height
        entity.rect.topleft = (entity.pixel_x, entity.pixel_y)
        entity.target_x = entity.pixel_x
        entity.target_y = entity.pixel_y

    def _remove_visuals(self, level, pos):
        x, y = pos
        tile = level[y][x]
        if "portal_active" in tile.effects:
            tile.effects.remove("portal_active")
        # Par sécurité
        if "portal_pending" in tile.effects:
            tile.effects.remove("portal_pending")