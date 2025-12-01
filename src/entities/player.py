import pygame
from src.core.constants import *
from src.core.game_misc_functions import *

class Player(pygame.sprite.Sprite):
    def __init__ (self, grid_x:int,grid_y:int,level:list):
        pygame.sprite.Sprite.__init__(self)

        self.height = 0.5*TILE_SIZE
        self.width = 0.3*TILE_SIZE

        self.grid_x = grid_x
        self.grid_y = grid_y

        self.pixel_x = self.grid_x * TILE_SIZE + (TILE_SIZE - self.width) // 2
        self.pixel_y = self.grid_y * TILE_SIZE + int(TILE_SIZE*0.8) - self.height

        self.rect = pygame.Rect(self.pixel_x,self.pixel_y,self.width,self.height)

        self.target_x = self.pixel_x
        self.target_y = self.pixel_y
        self.nbr_pxel_animation = 0
        self.start_animation = self.pixel_x
        self.duree_pixel_animation = 0
        self.idle_time = 0

        self.speed_x = 300  
        self.speed_y = 300  

        self.speed_gravity_y = 0
        self.gravity = 600
        self.on_ground = True

        self.moves = []

        self.moving_horizontal = False
        self.moving_vertical = False
        self.moving_gravite = False
        self.moving = False

        self.frame_dans_air = 0

        self.current_tile = level[self.grid_y][self.grid_x]
        self.tile_below = level[self.grid_y+1][self.grid_x] if self.grid_y+1 < len(level) else None
        self.tile_above = level[self.grid_y-1][self.grid_x] if self.grid_y-1 >= 0 else None
        self.tile_left = level[self.grid_y][self.grid_x-1] if self.grid_x-1 >= 0 else None
        self.tile_right = level[self.grid_y][self.grid_x+1] if self.grid_x+1 < len(level[0]) else None

        self.last_move_time = 0
        self.move_delay = 750
        


 
    def detection_key(self, grid_width, grid_height, past_self_tab):
        '''
        Fonction qui détecte une pression des touches et agit en conséquence
        '''
        if not self.moving_horizontal and not self.moving_vertical and not self.moving_gravite and are_all_past_self_idle(past_self_tab):
            current_time = pygame.time.get_ticks()
            if current_time - self.last_move_time >= self.move_delay:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_q]:
                    self.moving_horizontal = True
                    self.try_move_horizontal(-1, grid_width, grid_height, past_self_tab)
                    self.last_move_time = current_time
                elif keys[pygame.K_d]:
                    self.moving_horizontal = True
                    self.try_move_horizontal(1, grid_width, grid_height, past_self_tab)
                    self.last_move_time = current_time
                elif keys[pygame.K_z]:
                    if self.current_tile.tile_type == "ladder":
                        self.moving_vertical = True
                        self.try_move_vertical(-1, grid_width, grid_height, past_self_tab)
                        self.last_move_time = current_time
                elif keys[pygame.K_s]:
                    if self.tile_below and self.tile_below.tile_type == "ladder":
                        self.moving_vertical = True
                        self.try_move_vertical(1, grid_width, grid_height, past_self_tab)
                        self.last_move_time = current_time


  
    def try_move_horizontal(self, dx:int, grid_width, grid_height, past_self_tab):
        '''
        Fonction qui vérifie si le déplacement est possible
        si faisable : update target x pour déplacement et animation
        si pas faisable : ne fait rien
        entrées: 
            dx : int  
            grid_width : int
            grid_height : int
            past_self_tab : list of Past_self
        sorties: none
        '''
        new_x = self.grid_x + dx
        if 0 <= new_x and new_x < grid_width and self.target_is_door_and_open(dx):
            self.grid_x = new_x
            self.target_x = new_x * TILE_SIZE + (TILE_SIZE - self.width) // 2
            self.nbr_pxel_animation = self.target_x - self.pixel_x
            self.start_animation = self.pixel_x
            self.duree_pixel_animation = self.nbr_pxel_animation // Frames.WALKFRAMES

            if dx == -1:
                direction = "left"
            elif dx == 1:
                direction = "right"
            self.update_moves(direction)
            for past_self in past_self_tab:
                past_self.moves = self.moves
                past_self.detection_key(grid_width,grid_height)

    def try_move_vertical(self,dy:int, grid_width, grid_height, past_self_tab):
        '''
        Fonction qui vérifie si le déplacement est possible
        si faisable : update target y pour déplacement et animation
        si pas faisable : ne fait rien
        entrées: 
            dy : int  
            grid_width : int
            grid_height : int
            past_self_tab : list of Past_self
        sorties: none
        '''
        new_y = self.grid_y + dy
        if 0 <= new_y and new_y < grid_height:
            self.grid_y = new_y
            self.target_y = new_y * TILE_SIZE + int(TILE_SIZE*0.8) - self.height

            if dy == -1:
                direction = "up"
            elif dy == 1:
                direction = "down"
            self.update_moves(direction)
            for past_self in past_self_tab:
                past_self.moves = self.moves
                past_self.detection_key(grid_width,grid_height)



    def update(self, dt:float, level:list,inventory):
        '''
        fonction qui actualise différents élements relatifs au joueur (à chaque frame)
        entrées: 
            dt : float
            level : list of list
        sorties: none
        '''
        self.current_tile = level[self.grid_y][self.grid_x]
        self.tile_below = level[self.grid_y+1][self.grid_x] if self.grid_y+1 < len(level) else None
        self.tile_above = level[self.grid_y-1][self.grid_x] if self.grid_y-1 >= 0 else None
        self.tile_left = level[self.grid_y][self.grid_x-1] if self.grid_x-1 >= 0 else None
        self.tile_right = level[self.grid_y][self.grid_x+1] if self.grid_x+1 < len(level[0]) else None

        self.rect = pygame.Rect(self.pixel_x,self.pixel_y,self.width,self.height)

        self.checkCollisionObject(inventory)

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
            if self.frame_dans_air > 4 : #Au bout de 4 frame de on_ground à l'etat faux on considère que le player tombe, sinon il est toujour sur le sol
                self.moving_gravite = True
            self.frame_dans_air +=1
        else:
            self.speed_gravity_y = 0
            self.frame_dans_air = 0
            self.moving_gravite = False

        self.pixel_y += self.speed_gravity_y * dt   

        self.rect = pygame.Rect(self.pixel_x,self.pixel_y,self.width,self.height)

        # Détection structure
        self.on_ground = False
        for i_col in range(max(0, self.grid_x-1), min(len(level[0]), self.grid_x+1)): # on check que les tiles à droite et à gauche pour verifier le sol
            tile = level[self.grid_y][i_col]
            if "ground" in tile.structures:
                if self.rect.colliderect(tile.structures["ground"].rect):
                    if self.speed_gravity_y >= 0:
                        self.pixel_y = tile.structures["ground"].rect.top - self.height
                        self.on_ground = True

        self.target_y = self.pixel_y

    def draw(self,screen,asset_manager):
        '''
        Fonction qui dessine le joueur en fonction de ses attributs
        entrée: 
            screen : pygames
        sorties: none
        '''
        pygame.draw.rect(screen, "red", (self.pixel_x, self.pixel_y, self.width, self.height ))

    def update_moves (self,direction):
        '''
        Fonction qui ajoute chaque nouvelles coordonnées que prends joueur à un tableau sous forme de tuple (x,y)
        '''
        self.moves.append(direction)

    def on_finish(self):
        '''
        Fonction qui verifie si le joueur est sur la case de l'arivée
        entrée: 
        sorties: bool
        '''
        if self.current_tile.tile_type == "end":
            return True
        return False
    
    def target_is_door_and_open(self,dx):
        '''
        Fonction qui vérifie si la tile sur laquelle le player va aller et une porte ouverte
        entrées:
            dx: -1 ou 1 pour savoir si on va à droite au à gauche
            level : la grille du level
        sortie: bool
        '''
        res = True
        
        if dx == 1 and self.tile_right.tile_type == "door_left": 
            res = self.tile_right.structures["door_left"].is_open
        elif dx == -1 and self.tile_left.tile_type == "door_right":
            res = self.tile_left.structures["door_right"].is_open
        elif dx == -1 and self.current_tile.tile_type == "door_left": 
            res = self.current_tile.structures["door_left"].is_open
        elif dx == 1 and self.current_tile.tile_type == "door_right":
            res = self.current_tile.structures["door_right"].is_open
        return res
    
    def checkCollisionObject(self,inventory):
        '''
        Fonction qui vérifie si le joueur touche un objet
        entrée : 
            level: list
            inventaire : Inventaire
        sortie : None
        '''
        for i in range(len(self.current_tile.items)):
            if self.rect.colliderect(self.current_tile.items[i]) and not inventory.isTypeUsable(self.current_tile.items[i].type):
                item = self.current_tile.items.pop(i)
                inventory.MakeTypeUsable(item.type)

    def update_dt(self, dt):
        if not self.moving:
            self.idle_time += dt * 1000  # dt en secondes → convertir en ms si nécessaire
        else:
            self.idle_time = 0
                        

            


