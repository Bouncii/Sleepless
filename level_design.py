def cree_tableau_de_la_map(file:str):
    """
    Cree une list de list pour moteur,
    à partir du nom du fichier txt, 
    et renvoie la list de list

    Caractère possible dans le txt : 
        '_' ou '-' -> sol
        'S'  ou 's' -> start
        'E' ou 'e' -> end
        Tout autre caractère -> vide
    """
    map = []
    with open(file, "r") as lvl_map:
        for etage in lvl_map:
            niveau = []
            for crt in etage:
                if crt == '_' or crt == '-':
                    niveau += ["sol"]
                elif crt == 'S' or crt == 's':
                    niveau += ["start"]
                elif crt == 'E' or crt == 'e':
                    niveau += ["end"]
                elif crt == '\n':
                    pass
                else:
                    niveau += ["vide"]
            map += [niveau]
    
    taille_etage = len(map[0])
    for tab in map:
        if taille_etage != len(tab):
            return [["start"]]
    return map

print(cree_tableau_de_la_map("level.txt"))