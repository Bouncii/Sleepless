# src/systems/item_effect_manager.py
from src.core.constants import ItemTypes

class ItemEffectManager:
    def __init__(self, interaction_manager_portal=None):
        self.portal_manager = interaction_manager_portal

    def apply_effect(self, item_type: str, tile, level=None):
        '''
        Applique l'effet correspondant à l'item sur la tuile donnée.
        Retourne True si l'item doit être consommé (désactivé dans l'inventaire).
        '''
        
        if item_type == ItemTypes.STUNMAKER:
            if "stun" not in tile.effects:
                tile.effects.append("stun")
                print(f"Piège STUN posé en {tile.grid_x}, {tile.grid_y}")
                return True
        
        elif item_type == ItemTypes.PORTALMAKER:
            if self.portal_manager and level is not None:
                consumed = self.portal_manager.try_place_portal(tile.grid_x, tile.grid_y, level)
                return consumed
                
        return False