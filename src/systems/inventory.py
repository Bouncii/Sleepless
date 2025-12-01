# src/systems/inventory.py

import pygame
from src.entities.objects import Item
from src.core import ItemTypes

    
class Inventory():
    def __init__(self):
        self.slots = [{"type":ItemTypes.PORTALMAKER,"usable":False},
                      {"type":ItemTypes.STUNMAKER,"usable":False}]
        self.selected_slot = 0
        self.SlotSize = 100
        self.width = self.SlotSize * len(self.slots)
        self.height = self.SlotSize
        self.LastSelectionTime = pygame.time.get_ticks()

    def SelectedIsUsable(self):
        return self.slots[self.selected_slot]["usable"]
    
    def UpdateSelected(self,dx):
        current_time = pygame.time.get_ticks()
        if current_time - self.LastSelectionTime > 200:

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
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.UpdateSelected(1)
        elif keys[pygame.K_LEFT]:
            self.UpdateSelected(-1)
        elif keys[pygame.K_RETURN]:
            self.tryActionItem()

    def tryActionItem(self):
        if self.SelectedIsUsable():
            self.MakeSelectedUnusable()

    
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

        screen.blit(image, (screen_width - self.width, 0))
