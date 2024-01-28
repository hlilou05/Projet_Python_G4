import pygame
import pygame._sdl2 as sdl2
from time import sleep
from pygame.locals import *
from threading import Thread
import sys
from .Tile import *
from .Constant import *




largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("PROJET_PYTHON_2024")

bleu = (0, 0, 250)
noir = (0, 0, 0)
rouge = (250, 0, 0)
vert = (0, 250, 0)
blanc = (250, 250, 250)
marron = (139, 69, 19)
gridSize = 10
pygame.font.init()  
police = pygame.font.Font(None, 36)
champs = [pygame.Rect(300, 50 + i * 70, 300, 50) for i in range(8)]
couleur_active = pygame.Color('dodgerblue2')
couleur_inactive = pygame.Color('lightskyblue3')
couleur = couleur_inactive
textes = [''] * 8
actif_champ = None

champs = [pygame.Rect(300, 50 + i * 70, 300, 50) for i in range(8)]
couleur_active = pygame.Color('dodgerblue2')
couleur_inactive = pygame.Color('lightskyblue3')
couleur = couleur_inactive
textes = [''] * 8
actif_champ = None



class Window:
    """
    Classe dédiée à l'affichage
    """
    def __init__(self, myGame):
        self.game = myGame
        self.infoObject = pygame.display.Info()
        
        
        self.screen = pygame.display.set_mode((self.infoObject.current_w, self.infoObject.current_h),  pygame.SCALED | pygame.RESIZABLE | sdl2.WINDOWPOS_CENTERED)
        self.surfacebob = pygame.Surface((self.infoObject.current_w, self.infoObject.current_h )).convert_alpha()
        self.surfacetile = pygame.Surface((self.infoObject.current_w, self.infoObject.current_h)).convert_alpha()
        self.isoCoordTable = {} #dictionnaire qui associe les coordonnées 2D des tiles à leurs coordonnées ISO. On l'utilisera pour placer les bobs exactement sur les tiles. (x réel , y réel) -> (x iso , y iso)
        self.offsetx = 0
        self.offsety = 0
        self.zoom = 1
        self.value = 20 #taille de la grille // A RELIER AVEC LES PARAMETRES ## ???!!!
        self.screen.fill((255,255,255))
        self.pages = []
        self.menu_active = True
        self.game_active = False  # Ajout d'une variable pour indiquer si le jeu est actif
        self.suivant_pressed = False
        self.pages.append(self.display_menu)
        self.pages.append(self.affiche_formulaire)
        self.pages.append(self.affiche_deuxieme_page)
        self.current_page = 0
    
    def afficher_texte(self,texte, x, y):
        texte_surface = police.render(texte, True, blanc)
        texte_rect = texte_surface.get_rect()
        texte_rect.center = (x, y)
        fenetre.blit(texte_surface, texte_rect)
    
    def display_menu(self):
        #music_song = pygame.mixer.Sound("music_pygame.mp3")
        #music_song.play()
        while self.menu_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 300 <= x <= 500:
                        if 200 <= y <= 250:
                            print("Start")
                            self.menu_active = False
                            self.game_active = True
                            self.run_game()
                        elif 300 <= y <= 350:
                            print("Options")
                            variables = ['gridSizeX', 'gridSizeY', 'ticksPerDay', 'bobsQty', 'foodQty', 'NbDay', 'maxEnergy', 'energyInitLevel']
                            self.affiche_formulaire(variables)
                        elif 400 <= y <= 450:
                            pygame.quit()
                            sys.exit()

            background = assets["fond_ecran"]
            background = pygame.transform.scale(background, (self.screen.get_width(), self.screen.get_height()))
            self.screen.blit(background, (0, 0))

            self.afficher_texte("GAME OF LIFE", self.screen.get_width() // 2, 100)
            pygame.draw.ellipse(self.screen, marron, (300, 200, 200, 50))
            self.afficher_texte("START", self.screen.get_width() // 2, 225)
            pygame.draw.ellipse(self.screen, marron, (300, 300, 200, 50))
            self.afficher_texte("OPTIONS", self.screen.get_width() // 2, 325)
            pygame.draw.ellipse(self.screen, marron, (300, 400, 200, 50))
            self.afficher_texte("QUIT", self.screen.get_width() // 2, 425)

            pygame.display.update()

    def display(self):
        pygame.display.update()
        self.screen.fill((255,255,255))
        self.surfacebob.fill((0,0,0,0))
        self.game.update_bobs()
        self.game.update_food()
        self.surfacebob.set_alpha(255)
        self.blit_surfacetile_screen()
        self.blit_surfacebob_screen()


    def blit_surfacebob_screen(self):
        self.screen.blit(self.surfacebob, (0, 0))

    def blit_surfacetile_screen(self):
        self.screen.blit(self.surfacetile, (0, 0))

    def Actualise_UserInput(self):
        """
        Actualise the zoom from keyboard input or mousewheel.
        Quit if the window is being shut down by the user"""
        for event in pygame.event.get():
            #Exit
            if event.type == pygame.QUIT: self.game.isRunning = False
            #zoom souris
            if event.type == pygame.MOUSEWHEEL:
                if event.y == 1 :
                    if self.zoom >= 3 : break
                    else : self.zoom+=0.15
                else :
                    if self.zoom <= 0.5 : break
                    else : self.zoom-=0.15
            #Appui clavier
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i: #touche i -> zoom in
                        if self.zoom >= 3 : break
                        else : self.zoom+=0.15
                    elif event.key == pygame.K_o: #touche o -> zoom out
                        if self.zoom <= 0.5 : break
                        else : self.zoom -= 0.15
                    elif event.key == pygame.K_DOWN: #touche flèche down
                        self.offsety -= 1
                    elif event.key == pygame.K_UP: #touche flèche up
                        self.offsety += 1
                    elif event.key == pygame.K_RIGHT: #touche flèche droite
                        self.offsetx -= 1
                    elif event.key == pygame.K_LEFT: #touche flèche gauche
                        self.offsetx += 1 
                    elif event.key == pygame.K_SPACE: #touche espace
                        self.game.pause = not self.game.pause
        return
    
    def run_game(self):
        while self.game_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_active = False
                    self.menu_active = True
                    self.display_menu()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Pause the game and display the pause menu
                        self.game.pause = True
                        self.affiche_pause_menu()
            
            # The rest of your game loop logic goes here
            self.game.run_game()
            self.display()  # This method should update and render your game

            pygame.display.flip()


    def affiche_pause_menu(self):
        self.pause_menu_active = True
        while self.pause_menu_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 300 <= x <= 500 and 200 <= y <= 250:
                        print("Resume")
                        self.pause_menu_active = False
                    elif 300 <= x <= 500 and 300 <= y <= 350:
                        print("Quit to Menu")
                        self.pause_menu_active = False
                        self.game_active = False
                        self.menu_active = True
                        self.display_menu()

            # Affichage de la page de pause
            self.screen.fill("WHITE")
            self.afficher_texte("PAUSE", self.screen.get_width() // 2, 100)
            pygame.draw.ellipse(self.screen, marron, (300, 200, 200, 50))
            self.afficher_texte("Resume", self.screen.get_width() // 2, 225)
            pygame.draw.ellipse(self.screen, marron, (300, 300, 200, 50))
            self.afficher_texte("Quit to Menu", self.screen.get_width() // 2, 325)

            pygame.display.update()
 
    
    def affiche_deuxieme_page(self):
        global couleur_inactive
        global actif_champ
        global textes
        global couleur_page2

        # Charger l'image de fond
        background = assets["arriere_plan"]
        background = pygame.transform.scale(background, (fenetre.get_width(), fenetre.get_height()))
        fenetre.blit(background, (0, 0))

        variables_page2 = ['InitVelocity', 'InitMemory', 'InitMass', 'TauxMutationMass', 'TauxMutationVelocity',
                        'TauxMutationMemory', 'TauxMutationPerception']
        champs_page2 = [pygame.Rect(345, 50 + i * 70, 300, 50) for i in range(len(variables_page2))]
        textes_page2 = [''] * len(variables_page2)
        couleur_page2 = couleur_inactive
        actif_champ_page2 = None

        # Ajouter le bouton "Retour"
        retour_button = pygame.Rect(largeur - 150, hauteur - 100, 100, 50)
        pygame.draw.rect(fenetre, rouge, retour_button)
        self.afficher_texte("Retour", largeur - 100, hauteur - 75)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if retour_button.collidepoint(x, y):
                        self.suivant_pressed = False  # Assurez-vous que suivant_pressed est réinitialisé
                        return  # Quitter la fonction pour revenir à la page précédente

                    for i, champ in enumerate(champs_page2):
                        if champ.collidepoint(event.pos):
                            actif_champ_page2 = i
                            couleur_page2 = pygame.Color('dodgerblue2')
                        else:
                            couleur_page2 = pygame.Color('lightskyblue3')

                if event.type == pygame.KEYDOWN:
                    if actif_champ_page2 is not None:
                        if event.key == pygame.K_RETURN:
                            print("Variable {}: {}".format(actif_champ_page2 + 1, textes_page2[actif_champ_page2]))
                            textes_page2[actif_champ_page2] = ''
                        elif event.key == pygame.K_BACKSPACE:
                            textes_page2[actif_champ_page2] = textes_page2[actif_champ_page2][:-1]
                        else:
                            textes_page2[actif_champ_page2] += event.unicode

            for i, (variable, champ) in enumerate(zip(variables_page2, champs_page2)):
                var_surface = police.render(variable, True, noir)
                fenetre.blit(var_surface, (50, 50 + i * 70))

                pygame.draw.rect(fenetre, couleur_page2, champ, 2)
                texte_surface = police.render(textes_page2[i], True, noir)
                largeur_texte = max(200, texte_surface.get_width() + 10)
                champ.w = largeur_texte
                fenetre.blit(texte_surface, (champ.x + 5, champ.y + 5))

            pygame.display.update()

    def affiche_formulaire(self, variables):
        global couleur
        global actif_champ

        background = assets["arriere_plan"]
        background = pygame.transform.scale(background, (fenetre.get_width(), fenetre.get_height()))
        fenetre.blit(background, (0, 0))

        for i, (variable, champ) in enumerate(zip(variables, champs)):
            var_surface = police.render(variable, True, noir)
            fenetre.blit(var_surface, (50, 50 + i * 70))

            pygame.draw.rect(fenetre, couleur, champ, 0)  # Ajustez la largeur de la bordure à 0 pour éviter la division en 2
            texte_surface = police.render(textes[i], True, noir)
            largeur_texte = max(200, texte_surface.get_width() + 10)
            champ.w = largeur_texte
            fenetre.blit(texte_surface, (champ.x + 5, champ.y + 5))

        retour_button = pygame.Rect(largeur - 150, hauteur - 100, 100, 50)
        pygame.draw.rect(fenetre, rouge, retour_button)
        self.afficher_texte("Retour", largeur - 100, hauteur - 75)
        suivant_button = pygame.Rect(largeur - 150, hauteur - 175, 100, 50)
        pygame.draw.rect(fenetre, vert, suivant_button)
        self.afficher_texte("Suivant", largeur - 100, hauteur - 150)
        pygame.display.flip()

        while not self.suivant_pressed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, champ in enumerate(champs):
                        if champ.collidepoint(event.pos):
                            actif_champ = i
                            couleur = pygame.Color('dodgerblue2')
                        else:
                            couleur = pygame.Color('lightskyblue3')
                    if retour_button.collidepoint(event.pos):
                        return
                    if suivant_button.collidepoint(event.pos):
                        self.suivant_pressed = True  # Définir suivant_pressed à True et quitter la boucle

                if event.type == pygame.KEYDOWN:
                    if actif_champ is not None:
                        if event.key == pygame.K_RETURN:
                            print("Variable {}: {}".format(actif_champ + 1, textes[actif_champ]))
                            textes[actif_champ] = ''
                        elif event.key == pygame.K_BACKSPACE:
                            textes[actif_champ] = textes[actif_champ][:-1]
                        else:
                            textes[actif_champ] += event.unicode

            # Afficher le texte entré dans chaque champ
            for i, (variable, champ) in enumerate(zip(variables, champs)):
                var_surface = police.render(variable, True, noir)
                fenetre.blit(var_surface, (50, 50 + i * 70))

                pygame.draw.rect(fenetre, couleur, champ, 0)
                texte_surface = police.render(textes[i], True, noir)
                largeur_texte = max(200, texte_surface.get_width() + 10)
                champ.w = largeur_texte
                fenetre.blit(texte_surface, (champ.x + 5, champ.y + 5))

            pygame.display.update()

        self.affiche_deuxieme_page()  # Appeler la méthode pour afficher la deuxième page
    
