# src\build\map_settings_functions.py
import json
from src.core import Paths
from src.entities import objects

def get_settings_by_level_number(level_num:int):
    """ La fonction renvoie un dictionnaire de tous les settings correspondant au numéro du niveau passé en paramètre :
    Entrée : int
    Sortie : dict
    """
    with open(Paths.SETTINGS, "r") as file:
        data = json.load(file)
    return data["level" + str(level_num)]
    

def get_number_of_level():
    with open(Paths.SETTINGS, "r") as file:
        data = json.load(file)
    return data["number_of_level"]

# Exemple : get_settings_by_level_number(1) -> {'past_selfs': [{'past_self_timer_spawn': 2}, {'past_self_timer_spawn': 7}], 'items': [{'eclair': [2, 2]}, {'teleporteur': [1, 3]}]}

def add_item_to_tiles(items:list, level:list):
    for elt in items:
        for cle,val in elt.items():
                    if cle == "portal":
                        level[val[1]][val[0]].items.append(objects.Item(val[0],val[1],objects.ItemTypes.PORTALMAKER))
                    elif cle == "stun":
                        level[val[1]][val[0]].items.append(objects.Item(val[0],val[1],objects.ItemTypes.STUNMAKER))

# Exemple : recuperer les items : get_settings_by_level_number(1)["items"] -> [{'stun': [2, 2]}, {'teleporteur': [1, 3]}]