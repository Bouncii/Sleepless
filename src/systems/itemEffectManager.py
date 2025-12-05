# src/systems/item_effect_manager.py
from src.core.constants import ItemTypes

class ItemEffectManager:
    def apply_effect(self, item_type: str, tile):
        '''
        Applique l'effet correspondant à l'item sur la tuile donnée.
        '''
        if item_type == ItemTypes.STUNMAKER:
            if "stun" not in tile.effects:
                tile.effects.append("stun")
                print(f"Piège STUN posé en {tile.grid_x}, {tile.grid_y}")
                return True
        return False