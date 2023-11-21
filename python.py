# import pygame
# import sys

# pygame.init()

# largeur, hauteur = 800, 600
# fenetre = pygame.display.set_mode((largeur, hauteur))
# pygame.display.set_caption("PROJET_PYTHON_2024")

# bleu = (0, 0, 250)
# noir = (0, 0, 0)
# rouge = (250, 0, 0)
# vert = (0, 250, 0)

# music_song = pygame.mixer.Sound("music_pygame.mp3")
# music_song.play()

# police = pygame.font.Font(None, 36)

# def afficher_texte(texte, x, y):
#     texte_surface = police.render(texte, True, noir)
#     texte_rect = texte_surface.get_rect()
#     texte_rect.center = (x, y)
#     fenetre.blit(texte_surface, texte_rect)

# def main_menu():
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 x, y = pygame.mouse.get_pos()
#                 if 300 <= x <= 500:
#                     if 200 <= y <= 250:
#                         print("Start")
#                         interface_jeu()
#                     elif 300 <= y <= 350:
#                         print("Options")
#                     elif 400 <= y <= 450:
#                         pygame.quit()
#                         sys.exit()

#         background = pygame.image.load("image_path.jpg")
#         background = pygame.transform.scale(background, (fenetre.get_width(), fenetre.get_height()))
#         fenetre.blit(background, (0, 0))

#         afficher_texte("GAME", largeur // 2, 100)
#         pygame.draw.rect(fenetre, rouge, (300, 200, 200, 50))
#         afficher_texte("START", largeur // 2, 225)
#         pygame.draw.rect(fenetre, rouge, (300, 300, 200, 50))
#         afficher_texte("OPTIONS", largeur // 2, 325)
#         pygame.draw.rect(fenetre, rouge, (300, 400, 200, 50))
#         afficher_texte("QUIT", largeur // 2, 425)

#         pygame.display.update()
# TILE_SIZE = 16
# class Tile():
#     def __init__(self, x, y):
#         self.image = pygame.image.load("Tile32x32.png")
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y


# def iso_coord(x, y):
#     return (x - y, (x + y) / 2)

# def update_window(fenetre):
#     background = pygame.image.load("arrière_plan.jfif")
#     background = pygame.transform.scale(background, (fenetre.get_width(), fenetre.get_height()))
#     fenetre.blit(background, (0, 0))
    

# def display_tiles(screen, value):
#     screen_x, screen_y = screen.get_size()
#     for y in range(-value // 2, value // 2):
#         for x in range(-value // 2, value // 2):
#             new_tile = Tile(screen_x // 4 + screen_y // 2 + x * TILE_SIZE,
#                             screen_y // 2 - screen_x // 4 + y * TILE_SIZE)
#             screen.blit(new_tile.image, iso_coord(new_tile.rect.x, new_tile.rect.y))

# def interface_jeu():
#     jeu_en_cours = True
#     while jeu_en_cours:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
        
#         done = False
        
        
#         update_window(fenetre)
#         display_tiles(fenetre, 20)
#         pygame.display.update()
        


# # Point d'entrée du programme
# if __name__ == "__main__":
#     main_menu()

# import pygame
# import sys

# pygame.init()

# # Couleurs
# BLANC = (255, 255, 255)
# NOIR = (0, 0, 0)
# GRIS = (200, 200, 200)

# # Initialisation de Pygame
# largeur, hauteur = 600, 300
# fenetre = pygame.display.set_mode((largeur, hauteur))
# pygame.display.set_caption("Affichage avec champ de saisie")

# # Police
# police = pygame.font.Font(None, 36)

# # Champ de texte
# champ_texte = pygame.Rect(300, 100, 300, 50)
# couleur_active = pygame.Color('dodgerblue2')
# couleur_inactive = pygame.Color('lightskyblue3')
# couleur = couleur_inactive
# texte = ''
# actif = False

# def affiche(var):
#     fenetre.fill(BLANC)

#     # Affichage de la chaîne de caractères
#     var_surface = police.render(var, True, NOIR)
#     fenetre.blit(var_surface, (50, 100))

#     # Champ de texte
#     pygame.draw.rect(fenetre, couleur, champ_texte, 2)
#     texte_surface = police.render(texte, True, NOIR)
#     largeur_texte = max(200, texte_surface.get_width()+10)
#     champ_texte.w = largeur_texte
#     fenetre.blit(texte_surface, (champ_texte.x+5, champ_texte.y+5))

#     pygame.display.flip()

# # Boucle principale
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if champ_texte.collidepoint(event.pos):
#                 actif = not actif
#             else:
#                 actif = False
#             couleur = couleur_active if actif else couleur_inactive
#         if event.type == pygame.KEYDOWN:
#             if actif:
#                 if event.key == pygame.K_RETURN:
#                     print(texte)
#                     texte = ''
#                 elif event.key == pygame.K_BACKSPACE:
#                     texte = texte[:-1]
#                 else:
#                     texte += event.unicode

#     affiche("Variable")

















import pygame
import sys

pygame.init()

largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("PROJET_PYTHON_2024")

bleu = (0, 0, 250)
noir = (0, 0, 0)
rouge = (250, 0, 0)
vert = (0, 250, 0)

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

def interface_jeu():
    jeu_en_cours = True
    while jeu_en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        done = False
        update_window(fenetre)
        display_tiles(fenetre, 20)
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

        


# # Point d'entrée du programme
# if __name__ == "__main__":
#     main_menu()



# import pygame
# import sys

# pygame.init()

# # Couleurs
# BLANC = (255, 255, 255)
# NOIR = (0, 0, 0)
# GRIS = (200, 200, 200)

# # Initialisation de Pygame
# largeur, hauteur = 800, 600
# fenetre = pygame.display.set_mode((largeur, hauteur))
# pygame.display.set_caption("Formulaire avec champs de saisie")

# # Police
# police = pygame.font.Font(None, 36)

# # Champs de texte
# champs = [pygame.Rect(200, 50 + i * 70, 300, 50) for i in range(8)]

# couleur_active = pygame.Color('dodgerblue2')
# couleur_inactive = pygame.Color('lightskyblue3')
# couleur = couleur_inactive
# textes = [''] * 8
# actif_champ = None

# def affiche_formulaire(variables):
#     fenetre.fill(BLANC)

#     for i, (variable, champ) in enumerate(zip(variables, champs)):
#         # Affichage de la variable
#         var_surface = police.render(variable, True, NOIR)
#         fenetre.blit(var_surface, (50, 50 + i * 70))

#         # Champ de saisie
#         pygame.draw.rect(fenetre, couleur, champ, 2)
#         texte_surface = police.render(textes[i], True, NOIR)
#         largeur_texte = max(200, texte_surface.get_width() + 10)
#         champ.w = largeur_texte
#         fenetre.blit(texte_surface, (champ.x + 5, champ.y + 5))

#     pygame.display.flip()

# # Liste de variables
# variables = ['G.S.Larg', 'G.S.long', 'Energy', 'Velocity', 'Min energy', 'The mass', 'score Bp', 'memory']

# # Boucle principale
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             for i, champ in enumerate(champs):
#                 if champ.collidepoint(event.pos):
#                     actif_champ = i
#                     couleur = couleur_active
#                 else:
#                     couleur = couleur_inactive
#         if event.type == pygame.KEYDOWN:
#             if actif_champ is not None:
#                 if event.key == pygame.K_RETURN:
#                     print("Variable {}: {}".format(actif_champ + 1, textes[actif_champ]))
#                     textes[actif_champ] = ''
#                 elif event.key == pygame.K_BACKSPACE:
#                     textes[actif_champ] = textes[actif_champ][:-1]
#                 else:
#                     textes[actif_champ] += event.unicode

#     affiche_formulaire(variables)


