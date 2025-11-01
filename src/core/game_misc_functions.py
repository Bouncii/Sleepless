# src/core/game_misc_functions.py

def are_all_past_self_idle(past_self_tab):
    '''
    Vérifie si les past self ont terminés leurs déplacement
    '''
    res = True
    for past_self in past_self_tab:
        res = res and not past_self.moving
    return res


def are_all_entities_idle(player,past_self_tab):
    '''
    Vérifie si toutes les entités ont terminé leurs déplacements
    '''
    entities_idle = not player.moving and are_all_past_self_idle(past_self_tab)
    return entities_idle