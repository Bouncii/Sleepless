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

        self.speed_x = 300 
        self.speed_y = 0

        self.gravity = 600
        self.on_ground = False

        self.moves = []
        


 
    def detection_key(self,grid_width,tile_size,past_self):
        '''
        Fonction qui détecte une pression des touches et agit en conséquence
        entrées: 
        tile_size : int
        grid_width : int
        sorties: none
        '''
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.try_move(-1,grid_width,tile_size,past_self)
        elif keys[pygame.K_d]:
            self.try_move(1,grid_width,tile_size,past_self)
  
    def try_move(self,dx:int,grid_width,tile_size,past_self):
        '''
        Fonction qui vérifie si le déplacement est possible
        si faisable : update target x et y pour déplacement et animation
        si pas faisable : ne fait rien
        entrées: 
        dx : int  
        tile_size : int
        grid_width : int
        sorties: none
        '''
        new_x = self.grid_x + dx
        if 0 <= new_x and new_x < grid_width:
            self.grid_x = new_x
            self.target_x = new_x * tile_size + (tile_size - self.width) // 2


            self.update_moves()
            past_self.moves = self.moves
            past_self.detection_key(tile_size)


    def update(self, dt:float, level:list, tile_size:int, grid_width:int):
        '''
        fonction qui actualise différents élements relatifs au joueur
        entrées: 
        dt : float
        level : list of list
        tile_size : int
        grid_width : int
        sorties: none
        '''


        # Chute veticale
        self.gestion_gravite(dt,level)


        # Deplacement horizontal
        self.deplacement_horizontal(dt)

        
        self.grid_x = int(self.pixel_x // tile_size) # nécessaire pour y à cause de la gravité, x est update par securité
        self.grid_y = int(self.pixel_y // tile_size)

        #Affichage tile à chaque changement -----DEBEUGUAGE-----
        previous_coord = (self.grid_x,self.grid_y)
        if previous_coord != (self.grid_x,self.grid_y):
            print(self.grid_x,self.grid_y)



    def deplacement_horizontal(self,dt:float):
        '''
        Fonction qui actualise le déplacement/animation horizontal :
        vérifie si x target ne est pas atteinte, si pas atteinte alors on additionne/soustrait la co avec speed
        entrée : dt
        '''
        if self.pixel_x < self.target_x:
            self.pixel_x += self.speed_x * dt
            if self.pixel_x > self.target_x:
                self.pixel_x = self.target_x
        if self.pixel_x > self.target_x:
            self.pixel_x -= self.speed_x * dt
            if self.pixel_x < self.target_x:
                self.pixel_x = self.target_x



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
            self.speed_y += self.gravity * dt
        else:
            self.speed_y = 0

        self.pixel_y += self.speed_y * dt

        player_rect = pygame.Rect(self.pixel_x,self.pixel_y,self.width,self.height)

        # Détection structure
        self.on_ground = False
        for i_col in range(max(0, self.grid_x-1), min(len(level[0]), self.grid_x+2)): # on check que les tiles à droite et à gauche pour verifier le sol
            tile = level[self.grid_y][i_col]
            for structure in tile.structures:
                if player_rect.colliderect(structure["rect"]):
                    if self.speed_y >= 0:
                        self.pixel_y = structure["rect"].top - self.height
                        self.on_ground = True

    def show(self,screen):
        '''
        Fonction qui dessine le joueur en fonction de ses attributs
        entrées: screen
        sorties: none
        '''
        pygame.draw.rect(screen, "red", (self.pixel_x, self.pixel_y, self.width, self.height ))

    def update_moves (self):
        '''
        Fonction qui ajoute chaque nouvelles coordonnées que prends joueur à un tableau sous forme de tuple (x,y)
        '''
        self.moves.append((self.grid_x,self.grid_y))