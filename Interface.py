# PYTHON PROJECT - STI - INSA CVL 2023/2024
# version Rana
import pygame
from random import randint

gridSize = 10 

pygame.init()
screen = pygame.display.set_mode((800, 800))
done = False
TILE_SIZE = 16


def iso_coord(x, y):
   return (x - y, (x + y) / 2)


def update_window(window):
   window.fill((255, 255, 255))
   pygame.display.update()


def display_tiles(screen, value):
   screen_x, screen_y = screen.get_size()
   for y in range(-value//2, value//2):
       for x in range(-value//2, value//2):
           new_tile = Tile(screen_x // 4 + screen_y // 2 + x * TILE_SIZE, screen_y // 2 - screen_x // 4 + y * TILE_SIZE)
           screen.blit(new_tile.image, iso_coord(new_tile.rect.x, new_tile.rect.y))


class Tile:
    def __init__(self, x, y):
        self.bob = None
        self.food = None
        self.image = pygame.image.load("Tile32x32.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Bob(pygame.sprite.Sprite):
   def __init__(self):
       super().__init__()
       self.velocity = 15
       self.size = randint(10, 20)
       self.energy = 100
       self.maxenergy = 200
       self.perception = 0
       self.mass= 1
       self.image = pygame.image.load("bob.png")
       self.image_blue = pygame.image.load("bob.blue.png")
       self.image_rouge = pygame.image.load("bob.rouge.png")
       self.image = pygame.transform.scale(self.image, (16, 16))
       self.image_blue = pygame.transform.scale(self.image_blue, (16, 16))
       self.image_rouge = pygame.transform.scale(self.image_rouge, (16, 16))
       self.rect = self.image.get_rect()
       self.rect.x = 300
       self.rect.y = 400
   def move_right(self): 
       if self.rect.x + self.velocity < screen.get_width() - self.rect.width:
            self.rect.x += 1
            screen.fill((255, 255, 255))
            self.rect.x+=self.velocity
            display_tiles(screen, 20)
   def move_left(self):
       self.rect.x-= self.velocity
       display_tiles(screen, 20)
   def move_up(self):
       screen.fill((255, 255, 255))
       self.rect.y -= self.velocity
       display_tiles(screen, 20)
   def move_down(self):
       screen.fill((255, 255, 255))
       self.rect.y += self.velocity
       display_tiles(screen, 20)
   
   def update_color(self):
       if self.velocity > 20:
           self.image = self.image_blue
       if self.mass >10:
           self.image = self.image_rouge


class Game:
    def __init__(self):
        self.grid = [[Tile(x, y) for x in range(gridSize)] for y in range(gridSize)]
        self.bob = Bob()
        self.all_food = pygame.sprite.Group()
        self.foodSpawn(10)

    def foodSpawn(self, quantity):
        for _ in range(quantity):
            a = randint(0, gridSize - 1)
            b = randint(0, gridSize - 1)
            if not self.grid[a][b].food:
                self.grid[a][b].food = Food(a, b)
                self.all_food.add(self.grid[a][b].food)
                # ... position the food on the grid ...

    def update_bob_position(self, x, y):
        if self.bob.rect.x != x or self.bob.rect.y != y:
            self.grid[x][y].bob = self.bob
            if self.bob.rect.x is not None and self.bob.rect.y is not None:
                self.grid[self.bob.rect.x][self.bob.rect.y].bob = None
            self.bob.rect.x, self.bob.rect.y = x, y





class Food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.energy = 100
        self.image = pygame.image.load("nourriture.png")
        self.image = pygame.transform.scale(self.image, (24, 24))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 310, 400

# Charger notre bob
update_window(screen)
display_tiles(screen, 20)
pygame.display.update()
# Charger le jeu
game = Game()


for food in game.all_food:
        screen.blit(food.image, food.rect)

while not done:
    
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           done = True
           print("Fermeture du jeu")
       elif event.type ==pygame.KEYDOWN:
           if event.key ==pygame.K_RIGHT:
               game.bob.move_right()
           elif event.key ==pygame.K_LEFT:
               game.bob.move_left()
           elif event.key ==pygame.K_UP:
               game.bob.move_up()
           elif event.key ==pygame.K_DOWN:
               game.bob.move_down()
      
   for food in game.all_food:
        screen.blit(food.image, food.rect)

   # Effacer l'écran
   #update_window(screen)


   # Afficher les tuiles du sol
   # display_tiles(screen, 20)


   # Afficher l'image de Bob
   screen.blit(game.bob.image, game.bob.rect)
   pygame.display.update()


pygame.quit()








