import pygame
import sys
from random import randint

pygame.init()

largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("PROJET_PYTHON_2024")
done=False

bleu = (0, 0, 250)
noir = (0, 0, 0)
rouge = (250, 0, 0)
vert = (0, 250, 0)
gridSize = 10 

# Utilisez des noms de variables différents, sinon vous écrasez la variable noir
# Déplacez la musique dans la fonction principale pour éviter des problèmes de lecture avant l'initialisation de Pygame
police = pygame.font.Font(None, 36)

def afficher_texte(texte, x, y):
    texte_surface = police.render(texte, True, noir)
    texte_rect = texte_surface.get_rect()
    texte_rect.center = (x, y)
    fenetre.blit(texte_surface, texte_rect)

def main_menu():
    # Déplacez l'initialisation de la musique ici
    music_song = pygame.mixer.Sound("music_pygame.mp3")
    music_song.play()

    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 300 <= x <= 500:
                    if 200 <= y <= 250:
                        print("Start")
                        interface_jeu()
                    elif 300 <= y <= 350:
                        print("Options")
                        # Vous devez définir la liste 'variables' avant d'appeler la fonction
                        variables = ['G.S.Larg', 'G.S.long', 'Energy', 'Velocity', 'Min energy', 'The mass', 'score Bp', 'memory']
                        affiche_formulaire(variables)
                    elif 400 <= y <= 450:
                        pygame.quit()
                        sys.exit()

        background = pygame.image.load("image_path.jpg")
        background = pygame.transform.scale(background, (fenetre.get_width(), fenetre.get_height()))
        fenetre.blit(background, (0, 0))

        afficher_texte("GAME", largeur // 2, 100)
        pygame.draw.rect(fenetre, rouge, (300, 200, 200, 50))
        afficher_texte("START", largeur // 2, 225)
        pygame.draw.rect(fenetre, rouge, (300, 300, 200, 50))
        afficher_texte("OPTIONS", largeur // 2, 325)
        pygame.draw.rect(fenetre, rouge, (300, 400, 200, 50))
        afficher_texte("QUIT", largeur // 2, 425)

        pygame.display.update()

TILE_SIZE = 16
class Tile():
    def __init__(self, x, y):
        self.image = pygame.image.load("Tile32x32.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.bob = None
        self.food = None

def iso_coord(x, y):
    return (x - y, (x + y) / 2)

def update_window(fenetre):
    background = pygame.image.load("arrière_plan.jfif")
    background = pygame.transform.scale(background, (fenetre.get_width(), fenetre.get_height()))
    fenetre.blit(background, (0, 0))

def display_tiles(screen, value):
    screen_x, screen_y = screen.get_size()
    for y in range(-value // 2, value // 2):
        for x in range(-value // 2, value // 2):
            new_tile = Tile(screen_x // 4 + screen_y // 2 + x * TILE_SIZE,
                            screen_y // 2 - screen_x // 4 + y * TILE_SIZE)
            screen.blit(new_tile.image, iso_coord(new_tile.rect.x, new_tile.rect.y))


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
       if self.rect.x + self.velocity < fenetre.get_width() - self.rect.width:
            self.rect.x += 1
            fenetre.fill((255, 255, 255))
            self.rect.x+=self.velocity
            display_tiles(fenetre, 20)
   def move_left(self):
       self.rect.x-= self.velocity
       display_tiles(fenetre, 20)
   def move_up(self):
       fenetre.fill((255, 255, 255))
       self.rect.y -= self.velocity
       display_tiles(fenetre, 20)
   def move_down(self):
       fenetre.fill((255, 255, 255))
       self.rect.y += self.velocity
       display_tiles(fenetre, 20)
   
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

# # Charger notre bob
# update_window(fenetre)
# display_tiles(fenetre, 20)
# pygame.display.update()
# # Charger le jeu
game = Game()


# for food in game.all_food:
#         fenetre.blit(food.image, food.rect)



def interface_jeu():
    jeu_en_cours = True
    done = False

    while jeu_en_cours and not done:
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    game.bob.move_right()
                elif event.key == pygame.K_LEFT:
                    game.bob.move_left()
                elif event.key == pygame.K_UP:
                    game.bob.move_up()
                elif event.key == pygame.K_DOWN:
                    game.bob.move_down()

       
        # Effacer l'écran
        update_window(fenetre)

        # Afficher les tuiles du sol
        display_tiles(fenetre, 20)

        # Afficher l'image de Bob
        fenetre.blit(game.bob.image, game.bob.rect)
        for food in game.all_food:
            fenetre.blit(food.image, food.rect)

        pygame.display.update()




# Champs de texte
champs = [pygame.Rect(200, 50 + i * 70, 300, 50) for i in range(8)]

couleur_active = pygame.Color('dodgerblue2')
couleur_inactive = pygame.Color('lightskyblue3')
couleur = couleur_inactive
textes = [''] * 8
actif_champ = None

def affiche_formulaire(variables):
    # Vous devez initialiser Pygame avant d'utiliser ses fonctionnalités
    pygame.init()
    global couleur
    global actif_champ

    background = pygame.image.load("arrière_plan.jfif")
    background = pygame.transform.scale(background, (fenetre.get_width(), fenetre.get_height()))
    fenetre.blit(background, (0, 0))

    for i, (variable, champ) in enumerate(zip(variables, champs)):
        # Affichage de la variable
        var_surface = police.render(variable, True, noir)
        fenetre.blit(var_surface, (50, 50 + i * 70))

        # Champ de saisie
        pygame.draw.rect(fenetre, couleur, champ, 2)
        texte_surface = police.render(textes[i], True, noir)
        largeur_texte = max(200, texte_surface.get_width() + 10)
        champ.w = largeur_texte
        fenetre.blit(texte_surface, (champ.x + 5, champ.y + 5))

    pygame.display.flip()
    # Liste de variables
    variables = ['G.S.Larg', 'G.S.long', 'Energy', 'Velocity', 'Min energy', 'The mass', 'score Bp', 'memory']

    # Boucle principale
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, champ in enumerate(champs):
                    if champ.collidepoint(event.pos):
                        actif_champ = i
                        couleur = couleur_active
                    else:
                        couleur = couleur_inactive
            if event.type == pygame.KEYDOWN:
                if actif_champ is not None:
                    if event.key == pygame.K_RETURN:
                        print("Variable {}: {}".format(actif_champ + 1, textes[actif_champ]))
                        textes[actif_champ] = ''
                    elif event.key == pygame.K_BACKSPACE:
                        textes[actif_champ] = textes[actif_champ][:-1]
                    else:
                        textes[actif_champ] += event.unicode

            affiche_formulaire(variables)

# Appeler la fonction principale
if __name__ == "__main__":
    main_menu()





















