def cree_tableau_de_la_map(file:str):
    """
    Cree une list de list pour moteur,
    à partir du nom du fichier txt, 
    et renvoie la list de list

    Caractère possible dans le txt : 
        '_' ou '-' -> sol
        'S'  ou 's' -> start
        'E' ou 'e' -> end
        '#' -> ladder
        '\n' ne cree rien, il est ignoré
        Tout autre caractère -> vide
    """
    map = []
    with open(file, "r") as lvl_map:
        for etage in lvl_map:
            niveau = []
            i = 0
            while i < len(etage):
                crt = etage[i]

                if crt == '_':
                    niveau += ["sol"]
                    i += 1
                    
                elif crt == 'S':
                    niveau += ["start"]
                    i += 1
                    
                elif crt == 'E':
                    niveau += ["end"]
                    i += 1
                    
                elif crt == '#':
                    niveau += ["ladder"]
                    i += 1
                    
                elif crt == 'B':
                    if i + 1 < len(etage) and etage[i + 1].isdigit(): #regarde si il y a un numero après la lettre
                        button_id = etage[i + 1]
                        niveau += ["button_"+ str(button_id)]
                        i += 2
                    else:
                        niveau += ["button_0"]  # id par défaut
                        i += 1
                    
                elif crt == 'D':
                    if i + 1 < len(etage) and etage[i + 1].isdigit(): #regarde si il y a un numero après la lettre
                        door_id = etage[i + 1]
                        niveau += ["door_"+ str(door_id)]
                        i += 2
                    else:
                        niveau += ["door_0"]  # id par défaut
                        i += 1
                    
                elif crt == '\n':
                    i += 1 
                    
                else:
                    niveau += ["vide"]
                    i += 1
            
            map += [niveau]
    
    taille_etage = len(map[0])
    for tab in map:
        if taille_etage != len(tab):
            print("Erreur: Toutes les lignes du niveau n'ont pas la même longueur!")
            return [["start"]]
    return map