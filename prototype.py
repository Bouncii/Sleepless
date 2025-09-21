# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

TILE_SIZE = 128
GRID_WIDTH = 7
GRID_HEIGHT = 3

level = [
    [0,0,0,1,1,0,0],
    [0,1,0,0,0,0,0],
    [0,1,1,1,0,0,0],
]

class Player:
  def __init__ (self,grid_position:tuple):

      self.grid_x = grid_position[0]
      self.grid_y = grid_position[1]

      self.pixel_x = self.grid_x*TILE_SIZE
      self.pixel_y = self.grid_y*TILE_SIZE

      self.target_x = self.pixel_x
      self.target_y = self.pixel_y

      self.speed = 300 
      self.height = 70
      self.width = 50
 
  
  def move(self):
    if self.pixel_x == self.target_x and self.pixel_y == self.target_y:
      keys = pygame.key.get_pressed()
      if keys[pygame.K_z]:
          self.try_move(0,-1)
      if keys[pygame.K_s]:
          self.try_move(0,1)
      if keys[pygame.K_q]:
          self.try_move(-1,0)
      if keys[pygame.K_d]:
          self.try_move(1,0)
  
  def try_move(self,dx:int,dy:int):
      new_x = self.grid_x + dx
      new_y = self.grid_y + dy
      if 0 <= new_x and new_x < GRID_WIDTH and 0 <= new_y and new_y < GRID_HEIGHT:
          self.grid_x = new_x
          self.grid_y = new_y
          self.target_x = self.grid_x * TILE_SIZE
          self.target_y = self.grid_y * TILE_SIZE

  def update(self, dt):
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

  def show(self,tile_size):
      pygame.draw.rect(screen, "red", (self.pixel_x, self.pixel_y, self.width, self.height ))


def grid_builder(grid_height:int,grid_width:int,tile_size:int):
    for row in range(grid_height):
      for col in range(grid_width):
          tile_type = level[row][col]
          x = col * tile_size
          y = row * tile_size

          if tile_type == 0:
              pygame.draw.rect(screen, (100,0,255), (x, y, TILE_SIZE, TILE_SIZE))
          elif tile_type == 1:
              pygame.draw.rect(screen, (100,100,100), (x, y, TILE_SIZE, TILE_SIZE))

player = Player((0,0))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0,0,0))

    grid_builder(GRID_HEIGHT,GRID_WIDTH,TILE_SIZE)

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