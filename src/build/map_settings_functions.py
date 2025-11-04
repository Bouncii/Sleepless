# src\build\map_settings_functions.py
import json
PATH = "assets\\levels\\levels_settings.json"

def get_settings_by_level_number(level_num:int):
    """ La fonction renvoie un dictionnaire de tous les settings correspondant au numéro du niveau passé en paramètre :
    Entrée : int
    Sortie : dict
    """
    with open(PATH, "r") as file:
        data = json.load(file)
    return data["level" + str(level_num)]

def get_number_of_level():
    with open(PATH, "r") as file:
        data = json.load(file)
    return data["number_of_level"]

# Exemple : get_settings_by_level_number(1) -> {'past_selfs': [{'past_self_timer_spawn': 8}, {'past_self_timer_spawn': 2}]}