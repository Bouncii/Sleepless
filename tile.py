from player import *
class Tile:
    def __init__ (self, grid_x:int, grid_y:int, width:int, height:int, tile_type:str, tile_size):
        self.grid_x = grid_x
        self.grid_y = grid_y

        self.pixel_x = self.grid_x*tile_size
        self.pixel_y = self.grid_y*tile_size

        self.width = width
        self.height = height

        self.tile_type = tile_type # type de la tile (exemple : "sol", "échelle", "bouton", "vide")

        self.background = self.find_color()

        self.structures = self.structures_builder() #Tab contenant l'ensemble des structures (sous forme d'objet rect pygames) présentent dans la tile


    def find_color(self):
        '''
        Fonction qui choisit la couleur en fonction du type de la tile
        sorties: la couleur en rgb
        '''
        if self.tile_type == "sol" or self.tile_type == "vide":
            return (100,100,150)
        elif self.tile_type == "start":
            return (000,250,50)
        elif self.tile_type == "end":
            return (000,50,250)
    def draw(self,screen):
        '''
        Fonction qui dessine la tile puis les structures qu'elle conttient
        entrées: screen
        sorties: none
        '''
        pygame.draw.rect(screen,self.background,(self.pixel_x, self.pixel_y, self.width, self.height))
        for structure in self.structures:
            pygame.draw.rect(screen,structure["color"],structure["rect"])

    def build_sol(self)->pygame.Rect:
        '''
        Fonction qui construit une structure de type sol
        entrées: 
            self
        sorties: 
            un dictionnaire contenant un rect pygame (la fome geometrique) et la couleur en rvb
        '''
        return {"rect":pygame.Rect(self.pixel_x, self.pixel_y+(0.8*self.height),self.width,self.height*0.2),"color":(100,100,0)}

    def structures_builder(self) -> list:
        '''
        Fonction qui construit un tableau avec toute les structures de la tile en fonction de son type
        entrées: 
            self
        sorties: 
            la liste contenant les structures
        '''
        res= []
        if self.tile_type == "sol" or self.tile_type == "start" or self.tile_type=="end":
            res.append(self.build_sol())
        
        
        return res