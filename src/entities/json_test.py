import json
FILE = "assets\levels\levels_settings.json"

with open(FILE, "r") as file:
    data = json.load(file)

#print(data["level0"])

def get_settings(map_number:int):
    """ La fonction renvoie un dictionnaire de tous les settings correspondant au numéro du niveau passé en paramètre :
    Entrée : int
    Sortie : dict
    """
    with open(FILE, "r") as file:
        data = json.load(file)
    return data["level" + str(map_number)]