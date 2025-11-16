# src/systems/inventory.py

from src.entities.objects import Item

class InventorySlot:
    def __init__(self):
        self.item = None
        self.quantity = 0

    def IsEmpty(self):
        return self.item is None
    
    def CanAddItem (self,item):
        return self.item.type == item.type or self.IsEmpty
    
    def AddItem(self,item):
        '''
        Méthode qui permet d'ajouter un item à un slot et renvoie le résultat de l'opération sous forme de booléen
        entrée :
            - item : Item
        sortie :
            - bool
        '''
        if self.CanAddItem(item):
            if self.IsEmpty:
                self.item = item.type
            self.quantity += 1
            item.is_in_inventory = True
            return True
        return False

    def RemoveItem(self,item):
        '''
        Méthode qui permet de supprimer un item  d'un slot et renvoie le résultat de l'opération sous forme de booléen
        entrée :
            - item : Item
        sortie :
            - bool
        '''
        if self.item.type == item.type and not self.IsEmpty:
            self.quantity -= 1
            if self.quantity == 0:
                self.item = None
            return True
        return False
    
class Inventory():
    def __init__(self,size = 2):
        self.slots = [InventorySlot for _ in range(size)]
        self.selected_slot = 0