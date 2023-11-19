import pygame

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
        self.image = pygame.image.load("Tile32x32.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Bob(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.velocity = 25
        self.size = 100
        self.energy = 100
        self.maxenergy = 200
        self.perception = 1
        self.mass= 1
        self.image = pygame.image.load("bob.png")
        self.image_blue = pygame.image.load("bob.blue.png")
        self.image_rouge = pygame.image.load("bob.rouge.png")
        self.image = pygame.transform.scale(self.image, (16, 16)) 
        self.image_blue = pygame.transform.scale(self.image_blue, (16, 16))
        self.image_rouge = pygame.transform.scale(self.image_rouge, (16, 16))
        

        self.image = self.image_blue if self.velocity > 20 else self.image_rouge
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 400
    def move_right(self):
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
            # Plus rapide, plus bleu
            self.image = self.image_blue
        else:
            # Plus lent, plus rouge
            self.image = self.image_rouge

class Game : 
    def __init__(self):
        self.bob=Bob()
        #self.pressed = {
           # "flèche_droite " :  True ,
           # "flèche_gauche " :  False ,
        #}

# Charger notre bob
update_window(screen)
display_tiles(screen, 20)
pygame.display.update()
# Charger le jeu 
game = Game()
while not done:
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            done = True
            print("Fermeture du jeu")
        #detecter si un joueur lache une touche
        elif event.type ==pygame.KEYDOWN:
            if event.key ==pygame.K_RIGHT:
                game.bob.move_right()
            elif event.key ==pygame.K_LEFT:
                game.bob.move_left()
            elif event.key ==pygame.K_UP:
                game.bob.move_up()
            elif event.key ==pygame.K_DOWN:
                game.bob.move_down()
        #elif event.type ==pygame.KEYUP:
            #game.pressed [event.key] = False

    #if game.pressed[pygame.K_RIGHT]:
       # game.bob.move_right()
    #if game.pressed[pygame.K_LEFT]:
        #game.bob.move_left()
    # Mise à jour de la position de Bob (pour le déplacer, par exemple)
    # Exemple : bob.rect.x += bob.velocity

    # Effacer l'écran
    #update_window(screen)

    # Afficher les tuiles du sol
    # display_tiles(screen, 20)

    # Afficher l'image de Bob
    screen.blit(game.bob.image, game.bob.rect)
    pygame.display.update()

pygame.quit()
