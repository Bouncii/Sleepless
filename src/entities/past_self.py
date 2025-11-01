import pygame
from src.core.constants import *

class Past_self:
    def __init__ (self, grid_x:int, grid_y:int):

        self.height = 0.5*TILE_SIZE
        self.width = 0.3*TILE_SIZE

        self.grid_x = grid_x
        self.grid_y = grid_y

        self.pixel_x = self.grid_x * TILE_SIZE + (TILE_SIZE - self.width) // 2
        self.pixel_y = self.grid_y * TILE_SIZE + int(TILE_SIZE*0.8) - self.height

        self.target_x = self.pixel_x
        self.target_y = self.pixel_y

        self.speed_x = 300  
        self.speed_y = 300  

        self.speed_gravity_y = 0
        self.gravity = 600
        self.on_ground = True

        self.moving_horizontal = False
        self.moving_vertical = False
        self.moving_gravite = False
        self.moving = False

        self.moves = []
        self.tour = 0

        self.timer_spawn = 4
        


    def detection_key(self):
        '''
        Fonction qui détecte une pression des touches et agit en conséquence (on bouge si le délai de spawn est écoulé ou alors on décrémente celui-ci)
        entrées: none
        sorties: none
        '''


        if self.timer_spawn == 0:
            self.move()
        else:
            self.timer_spawn -= 1

            

    def move_horizontal(self,new_x:int):
        '''
        Fonction qui déplace horizontalement past self a partir de new_x
        entrées: 
            new_x : int
        sorties: none
        '''

        self.grid_x = new_x
        self.target_x = new_x * TILE_SIZE + (TILE_SIZE - self.width) // 2


    def move_vertical(self,new_y:int):
        '''
        Fonction qui déplace verticalement past self a partir de new_y
        entrées: 
            new_y : int
        sorties: none
        '''

        self.grid_y = new_y
        self.target_y = new_y * TILE_SIZE + int(TILE_SIZE*0.8) - self.height



    def move(self):
        '''
        Fonction qui assigne la cible du deplacement du past self en fonction de la liste des moves et incrémente self.tour(indice dans moves)
        entrées: none
        sorties: none
        '''


        next_move = self.moves[self.tour]
        
        if self.grid_x != next_move[0]:
            self.move_horizontal(next_move[0])
            self.moving_horizontal = True
        elif self.grid_y != next_move[1]:
            self.move_vertical(next_move[1])
            self.moving_vertical = True
        self.tour += 1

            

            

    def update(self, dt:float, level:list):
        '''
        fonction qui actualise différents élements relatifs au past_self (à chaque frame)
        entrées: 
            dt : float
            level : list of list
        sorties: none
        '''

        # Chute veticale
        if not self.moving_vertical:
            self.gestion_gravite(dt,level)


        # Deplacement horizontal
        self.deplacement_horizontal(dt)
        
        if self.moving_vertical:
            self.deplacement_vertical(dt)

        
        

        self.grid_x = int(self.pixel_x // TILE_SIZE) # nécessaire pour y à cause de la gravité, x et update par securité
        self.grid_y = int(self.pixel_y // TILE_SIZE)

        self.moving = self.moving_horizontal or self.moving_vertical or self.moving_gravite



    def deplacement_horizontal(self,dt:float):
        '''
        Fonction qui actualise le déplacement/animation horizontal :
        vérifie si x target ne est pas atteinte, si pas atteinte alors on additionne/soustrait la co avec speed
        entrée : 
            dt : float
        '''
        if self.pixel_x < self.target_x:
            self.pixel_x += self.speed_x * dt
            if self.pixel_x > self.target_x:
                self.pixel_x = self.target_x
        elif self.pixel_x > self.target_x:
            self.pixel_x -= self.speed_x * dt
            if self.pixel_x < self.target_x:
                self.pixel_x = self.target_x
        else:
                self.moving_horizontal = False



    def deplacement_vertical(self,dt:float):
            '''
            Fonction qui actualise le déplacement/animation vertical :
            vérifie si y target ne est pas atteinte, si pas atteinte alors on additionne/soustrait la co avec speed
            entrée : 
                dt : float
            '''
            if self.pixel_y < self.target_y:
                self.pixel_y += self.speed_y * dt
                if self.pixel_y > self.target_y:
                    self.pixel_y = self.target_y

            elif self.pixel_y > self.target_y:
                self.pixel_y -= self.speed_y * dt
                if self.pixel_y < self.target_y:
                    self.pixel_y = self.target_y
            else:
                self.moving_vertical = False




    def gestion_gravite(self,dt,level):
        '''
        Fonction qui gère le déplacement/animation lié à la gravité : 
        incremente les coordonnées par la vitesse verticale (dont on additionne aussi la valeur avec gravité) quand on ne touche pas le sol
        entrées: 
            dt : float
            level : list of list
        sorties: none
        '''
        if not self.on_ground:
            self.speed_gravity_y += self.gravity * dt
            if self.debug > 4 :
                self.moving_gravite = True
            self.debug +=1
        else:
            self.speed_gravity_y = 0
            self.debug = 0
            self.moving_gravite = False

        self.pixel_y += self.speed_gravity_y * dt

        player_rect = pygame.Rect(self.pixel_x,self.pixel_y,self.width,self.height)

        # Détection structure
        self.on_ground = False
        for i_col in range(max(0, self.grid_x-1), min(len(level[0]), self.grid_x+2)): # on check que les tiles à droite et à gauche pour verifier le sol
            tile = level[self.grid_y][i_col]
            if "ground" in tile.structures:
                    if player_rect.colliderect(tile.structures["ground"].rect):
                        if self.speed_gravity_y >= 0:
                            self.pixel_y = tile.structures["ground"].rect.top - self.height
                            self.on_ground = True

        self.target_y = self.pixel_y

    def show(self,screen):
        '''
        Fonction qui dessine le past self en fonction de ses attributs
        entrées: 
            screen: pygames
        sorties: none
        '''
        pygame.draw.rect(screen, "orange", (self.pixel_x, self.pixel_y, self.width, self.height ))
