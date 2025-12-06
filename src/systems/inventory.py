# src/systems/inventory.py

import pygame
from src.core import ItemTypes
from .tileSelection import *
from .itemEffectManager import *

    
class Inventory():
    def __init__(self,level,interaction_manager_portal):
        self.slots = [{"type":ItemTypes.PORTALMAKER,"usable":False},
                      {"type":ItemTypes.STUNMAKER,"usable":False}]
        self.selected_slot = 0
        self.SlotSize = 100
        self.width = self.SlotSize * len(self.slots)
        self.height = self.SlotSize
        self.LastSelectionTime = pygame.time.get_ticks()

        self.tile_selection_manager = TileSelection()
        self.effect_manager = ItemEffectManager(interaction_manager_portal)

    def SelectedIsUsable(self):
        return self.slots[self.selected_slot]["usable"]
    
    def UpdateSelected(self,dx):
        current_time = pygame.time.get_ticks()
        if current_time - self.LastSelectionTime > 200:
            self.tile_selection_manager.active = False
            self.selected_slot += dx
            self.LastSelectionTime = pygame.time.get_ticks()
            if self.selected_slot <0 :
                self.selected_slot = len(self.slots)-1
            elif self.selected_slot >= len(self.slots):
                self.selected_slot = 0
            
    
    def MakeSelectedUsable(self):
        if not self.SelectedIsUsable:
            self.slots[self.selected_slot]["usable"] = True
            return True
        return False
    

    def MakeSelectedUnusable(self):
        if self.SelectedIsUsable:
            self.slots[self.selected_slot]["usable"] = False
            return True
        return False
    
    def getPosItemInv(self,type):
        for i in range(len(self.slots)):
            if self.slots[i]["type"] == type:
                return i
        return None

    
    def MakeTypeUsable(self,type:str):
        pos = self.getPosItemInv(type)
        if pos != None:
            self.slots[pos]["usable"] = True
            return True
        return False
    
    def isTypeUsable(self,type):
        return self.slots[self.getPosItemInv(type)]["usable"]
    
    def update(self,level,player):
        self.tile_selection_manager.update(level)
        self.useItemListener(level)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.UpdateSelected(1)
        elif keys[pygame.K_LEFT]:
            self.UpdateSelected(-1)
        elif keys[pygame.K_RETURN]:
            self.ActivateSelection(player,level)

    def ActivateSelection(self, player, level):
        '''Gère l'activation (touche Entrée)'''
        if self.SelectedIsUsable():
            current_type = self.slots[self.selected_slot]["type"]
            
            if current_type == ItemTypes.PORTALMAKER:
                target_tile = level[player.grid_y][player.grid_x]
                
                success = self.effect_manager.apply_effect(current_type, target_tile, level)
                if success:
                    self.MakeSelectedUnusable()

            elif current_type == ItemTypes.STUNMAKER:
                self.tile_selection_manager.activate()

    def useItemListener(self, level):
        '''Gère l'activation après sélection souris (pour le STUN)'''
        if self.tile_selection_manager.selectedTile and self.SelectedIsUsable():
            current_item_type = self.slots[self.selected_slot]["type"]
            success = self.effect_manager.apply_effect(current_item_type, self.tile_selection_manager.selectedTile, level)
            if success:
                self.MakeSelectedUnusable()
                self.tile_selection_manager.selectedTile = None
    
    def display(self,screen,asset_manager,screen_width):
        image = asset_manager.getTransparentImage(self.SlotSize*len(self.slots), self.SlotSize)
        for i in range(len(self.slots)):
            ItemImage = asset_manager.get_scaled_image(self.slots[i]["type"], self.SlotSize, self.SlotSize)
            if not self.slots[i]["usable"]:
                ItemImage = asset_manager.surface_to_grayscale(ItemImage)
            image.blit(ItemImage, (self.SlotSize*i, 0))
        pygame.draw.line(image,(255,0,0),(self.selected_slot*self.SlotSize,0),(self.selected_slot*self.SlotSize + self.SlotSize,0),10)
        pygame.draw.line(image,(255,0,0),(self.selected_slot*self.SlotSize,0),(self.selected_slot*self.SlotSize,self.SlotSize),10)
        pygame.draw.line(image,(255,0,0),(self.selected_slot*self.SlotSize,self.SlotSize),(self.selected_slot*self.SlotSize + self.SlotSize,self.SlotSize),10)
        pygame.draw.line(image,(255,0,0),(self.selected_slot*self.SlotSize+self.SlotSize,self.SlotSize),(self.selected_slot*self.SlotSize + self.SlotSize,0),10)

        self.tile_selection_manager.display(screen)
        screen.blit(image, (screen_width - self.width, 0))
