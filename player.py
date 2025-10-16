import pygame
class Player:
    def __init__ (self, grid_x:int, grid_y:int,tile_size:int):

        self.height = 70
        self.width = 50

        self.grid_x = grid_x
        self.grid_y = grid_y

        self.pixel_x = self.grid_x * tile_size + (tile_size - self.width) // 2
        self.pixel_y = self.grid_y * tile_size + int(tile_size*0.8) - self.height

        self.target_x = self.pixel_x
        self.target_y = self.pixel_y

        self.speed_x = 300  
        self.speed_y = 300  

        self.speed_gravity_y = 0
        self.gravity = 600
        self.on_ground = True

        self.moves = []

        self.moving_horizontal = False
        self.moving_vertical = False

        self.frame_dans_air = 0
        


 
    def detection_key(self,grid_width,grid_height,tile_size,past_self,level):
        '''
        Fonction qui détecte une pression des touches et agit en conséquence
        entrées: 
            grid_width : int
            grid_height : int
            tile_size : int
            past_self : Past_self
            level : list
        sorties: none
        '''
        if self.pixel_x == self.target_x and self.pixel_y == self.target_y and not self.moving_horizontal and not self.moving_vertical and not past_self.moving_vertical:
            self.moving_horizontal=True
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                self.try_move_horizontal(-1,grid_width,tile_size,past_self)
            elif keys[pygame.K_d]:
                self.try_move_horizontal(1,grid_width,tile_size,past_self)
            elif keys[pygame.K_z]:
                if level[self.grid_y][self.grid_x].tile_type == "ladder":
                    self.try_move_vertical(-1,grid_height,tile_size,past_self)
  
    def try_move_horizontal(self,dx:int,grid_width,tile_size,past_self):
        '''
        Fonction qui vérifie si le déplacement est possible
        si faisable : update target x pour déplacement et animation
        si pas faisable : ne fait rien
        entrées: 
            dx : int  
            grid_width : int
            tile_size : int
            past_self : Past_self
        sorties: none
        '''
        new_x = self.grid_x + dx
        if 0 <= new_x and new_x < grid_width:
            self.grid_x = new_x
            self.target_x = new_x * tile_size + (tile_size - self.width) // 2


            self.update_moves()
            past_self.moves = self.moves
            past_self.detection_key(tile_size)

    def try_move_vertical(self,dy:int,grid_height,tile_size,past_self):
        '''
        Fonction qui vérifie si le déplacement est possible
        si faisable : update target y pour déplacement et animation
        si pas faisable : ne fait rien
        entrées: 
            dy : int  
            grid_height : int
            tile_size : int
            past_self : Past_self
        sorties: none
        '''
        new_y = self.grid_y + dy
        if 0 <= new_y and new_y < grid_height:
            self.grid_y = new_y
            self.target_y = new_y * tile_size + int(tile_size*0.8) - self.height


            self.update_moves()
            past_self.moves = self.moves
            past_self.detection_key(tile_size)



    def update(self, dt:float, level:list, tile_size:int):
        '''
        fonction qui actualise différents élements relatifs au joueur (à chaque frame)
        entrées: 
            dt : float
            level : list of list
            tile_size : int
        sorties: none
        '''


        # Chute veticale
        if  (level[min(len(level),self.grid_y-1)][self.grid_x].tile_type == "vide" or level[self.grid_y][self.grid_x].tile_type == "vide"):
            self.gestion_gravite(dt,level)


        # Deplacement horizontal
        self.deplacement_horizontal(dt)
        
        if level[self.grid_y][self.grid_x].tile_type == "ladder" or (self.grid_y + 1 < len(level) and level[self.grid_y + 1][self.grid_x].tile_type == "ladder"):
            self.deplacement_vertical(dt)

        
        self.grid_x = int(self.pixel_x // tile_size) # nécessaire pour y à cause de la gravité, x et update par securité
        self.grid_y = int(self.pixel_y // tile_size)




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
                self.moving_horizontal = False


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
                self.moving_vertical = True
            self.frame_dans_air +=1
        else:
            self.speed_gravity_y = 0
            self.frame_dans_air = 0
            self.moving_vertical = False

        self.pixel_y += self.speed_gravity_y * dt

        player_rect = pygame.Rect(self.pixel_x,self.pixel_y,self.width,self.height)

        # Détection structure
        self.on_ground = False
        for i_col in range(max(0, self.grid_x-1), min(len(level[0]), self.grid_x+1)): # on check que les tiles à droite et à gauche pour verifier le sol
            tile = level[self.grid_y][i_col]
            for structure in tile.structures:
                if structure.type == "ground":
                    if player_rect.colliderect(structure.rect):
                        if self.speed_gravity_y >= 0:
                            self.pixel_y = structure.rect.top - self.height
                            self.on_ground = True

        self.target_y = self.pixel_y
        

    def show(self,screen):
        '''
        Fonction qui dessine le joueur en fonction de ses attributs
        entrée: 
            screen : pygames
        sorties: none
        '''
        pygame.draw.rect(screen, "red", (self.pixel_x, self.pixel_y, self.width, self.height ))

    def update_moves (self):
        '''
        Fonction qui ajoute chaque nouvelles coordonnées que prends joueur à un tableau sous forme de tuple (x,y)
        '''
        self.moves.append((self.grid_x,self.grid_y))

    def on_finish(self,level):
        '''
        Fonction qui verifie si le joueur est sur la case de l'arivée
        entrée: 
            level : list of list
        sorties: bool
        '''
        if level[self.grid_y][self.grid_x].tile_type == "end":
            return True
        return False
