# Example file showing a circle moving on screen
import pygame

#################################### game initialization ####################################

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

TILE_SIZE = 128   
GRID_WIDTH = 7    
GRID_HEIGHT = 3

level_str = [["sol" for j in range (7)] for i in range (3)]

#################################### Player ####################################




class Player:
  def __init__ (self, grid_x:int, grid_y:int):

    self.grid_x = grid_x
    self.grid_y = grid_y

    self.pixel_x = self.grid_x*TILE_SIZE
    self.pixel_y = self.grid_y*TILE_SIZE

    self.target_x = self.pixel_x
    self.target_y = self.pixel_y

    self.speed = 300 
    self.height = 70
    self.width = 50
 

  def move(self):
    '''
    Fonction qui détecte une pression des touches et agit en conséquence
    entrées: none
    sorties: none
    '''
    if self.pixel_x == self.target_x and self.pixel_y == self.target_y:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            self.try_move(0,-1)
        elif keys[pygame.K_s]:
            self.try_move(0,1)
        elif keys[pygame.K_q]:
            self.try_move(-1,0)
        elif keys[pygame.K_d]:
            self.try_move(1,0)
  
  def try_move(self,dx:int,dy:int):
      '''
      Fonction qui vérifie si le déplacement est possible
      si faisable : update target x et y pour déplacement et animation
      si pas faisable : ne fait rien
      entrées: 
        dx : int  
        dy : int  
      sorties: none
      '''
      new_x = self.grid_x + dx
      new_y = self.grid_y + dy
      if 0 <= new_x and new_x < GRID_WIDTH and 0 <= new_y and new_y < GRID_HEIGHT:
          self.grid_x = new_x
          self.grid_y = new_y
          self.target_x = self.grid_x * TILE_SIZE
          self.target_y = self.grid_y * TILE_SIZE

  def update(self, dt):
    '''
    Fonction qui actualise le déplacement/animation
    vérifie si x et y target ne sont pas atteints, si pas atteints alors on incrémente la co avec speed
    entrées: 
    dt : float
    sorties: none
    '''
    if self.pixel_x < self.target_x:
        self.pixel_x += self.speed * dt
        if self.pixel_x > self.target_x:
            self.pixel_x = self.target_x
    if self.pixel_x > self.target_x:
        self.pixel_x -= self.speed * dt
        if self.pixel_x < self.target_x:
            self.pixel_x = self.target_x

    if self.pixel_y < self.target_y:
        self.pixel_y += self.speed * dt
        if self.pixel_y > self.target_y:
            self.pixel_y = self.target_y
    if self.pixel_y > self.target_y:
        self.pixel_y -= self.speed * dt
        if self.pixel_y < self.target_y:
            self.pixel_y = self.target_y

  def show(self,tile_size:int):
      '''
      Fonction qui dessine le joueur en fonction de ses attributs
      entrées: 
        tile_size :int
      sorties: none
      '''
      pygame.draw.rect(screen, "red", (self.pixel_x, self.pixel_y, self.width, self.height ))


#################################### Map ####################################

def build_sol(pos_tile_pixel:tuple, tile_dimension:tuple)->pygame.Rect:
    '''
    Fonction qui construit une structure de type sol
    entrées: 
        pos_tile_pixel : tuple des coordonnées de la tile en pixel
        tile_dimension : tuple  des dimension de la tile
    sorties: 
        un dictionnaire contenant un rect pygame (la fome geometrique) et la couleur en rvb
    '''
    return {"rect":pygame.Rect(pos_tile_pixel[0], pos_tile_pixel[1]+(0.8*tile_dimension[1]),tile_dimension[0],tile_dimension[1]*0.2),"color":(100,100,0)}

def structures_builder(tile_type:str,pos_tile_pixel:tuple,tile_dimension:tuple) -> list:
    '''
    Fonction qui construit un tableau avec toute les structures de la tile en fonction de son type
    entrées: 
        tile_type : str  
        pos_tile_pixel : tuple  
        tile_dimension : tuple  
    sorties: 
        la liste contenant les structures
    '''
    res= []
    if tile_type == "sol":
        res.append(build_sol(pos_tile_pixel,tile_dimension))
    return res
    


class Tile:
    def __init__ (self, grid_x:int, grid_y:int, width:int, height:int, tile_type:str):
        self.grid_x = grid_x
        self.grid_y = grid_y

        self.pixel_x = self.grid_x*TILE_SIZE
        self.pixel_y = self.grid_y*TILE_SIZE

        self.width = width
        self.height = height

        self.background = (100,100,150)

        self.tile_type = tile_type # type de la tile (exemple : "sol", "échelle", "bouton", "vide")

        self.structures = structures_builder(self.tile_type,(self.pixel_x,self.pixel_y),(self.width,self.height)) #Tab contenant l'ensemble des structures (sous forme d'objet rect pygames) présentent dans la tile


    def draw(self):
        '''
        Fonction qui dessine la tile puis les structures qu'elle conttient
        entrées: none
        sorties: none
        '''
        pygame.draw.rect(screen,self.background,(self.pixel_x, self.pixel_y, self.width, self.height))
        for structure in self.structures:
            pygame.draw.rect(screen,structure["color"],structure["rect"])








def level_builder(grid_width:int,grid_height:int,tile_size:int,level_str:str) -> list:
    '''
    Fonction qui construit le niveau sous forme de tableau 2 dimension d'objet Tile 
    entrées: 
        grid_height : int  
        grid_width : int  
        tile_size : int  
        level_str : str  
    sorties: 
        res : list
    '''
    res=[]
    for row in range(grid_height):
        tab_row = []
        for col in range(grid_width):
            type = level_str[row][col]
            tile = Tile(col,row,tile_size,tile_size,type)
            tab_row.append(tile)
        res.append(tab_row)
    return res


#################################### game ####################################
         
level = level_builder(GRID_WIDTH,GRID_HEIGHT,TILE_SIZE,level_str)

player = Player(0,0)

# def grid_builder(grid_height:int,grid_width:int,tile_size:int):
#     for row in range(grid_height):
#         for col in range(grid_width):
#             tile_type = level[row][col]
#             x = col * tile_size
#             y = row * tile_size

#             if tile_type == 0:
#                 pygame.draw.rect(screen, (100,0,255), (x, y, TILE_SIZE, TILE_SIZE))
#             elif tile_type == 1:
#                 pygame.draw.rect(screen, (100,100,100), (x, y, TILE_SIZE, TILE_SIZE))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0,0,0))

    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            level[row][col].draw()

    player.move()
    player.update(dt)
    player.show(TILE_SIZE)

    

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()

#######################################################
# TODO : Draw implementation des classes dans le jeu
#######################################################