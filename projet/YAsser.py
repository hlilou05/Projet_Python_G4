import pygame
from pygame.locals import *
from threading import Thread
from time import sleep
import sys

pygame.init()
largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("PROJET_PYTHON_2024")
done = False

bleu = (0, 0, 250)
noir = (0, 0, 0)
rouge = (250, 0, 0)
vert = (0, 250, 0)
blanc = (250, 250, 250)
marron = (139, 69, 19)
gridSize = 10
police = pygame.font.Font(None, 36)

def afficher_texte(texte, x, y):
    texte_surface = police.render(texte, True, blanc)
    texte_rect = texte_surface.get_rect()
    texte_rect.center = (x, y)
    fenetre.blit(texte_surface, texte_rect)

champs = [pygame.Rect(300, 50 + i * 70, 300, 50) for i in range(8)]
couleur_active = pygame.Color('dodgerblue2')
couleur_inactive = pygame.Color('lightskyblue3')
couleur = couleur_inactive
textes = [''] * 8
actif_champ = None

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
                        print("options")
                        self.pause_menu_active = False
                        variables = ['GridSizeX', 'GridSizeY', 'TicksPerDay', 'BobsQty', 'FoodQty', 'EnergyInitLevel', 'MaxEnergy', 'InitPerception']
                        self.affiche_formulaire(variables)
                    elif 300 <= x <= 500 and 400 <= y <= 450:
                        print("Quit to Menu")
                        self.pause_menu_active = False
                        self.game_active = False
                        self.menu_active = True
                        self.display_menu()
                    
                        

            # Affichage de la page de pause
            self.screen.fill("WHITE")
            afficher_texte("PAUSE", self.screen.get_width() // 2, 100)
            pygame.draw.ellipse(self.screen, marron, (300, 200, 200, 50))
            afficher_texte("Resume", self.screen.get_width() // 2, 225)
            pygame.draw.ellipse(self.screen, marron, (300, 300, 200, 50))
            afficher_texte("Options", self.screen.get_width() // 2, 325)
            pygame.draw.ellipse(self.screen, marron, (300, 400, 200, 50))
            afficher_texte("Quit to Menu", self.screen.get_width() // 2, 425)

            pygame.display.update()

def affiche_deuxieme_page(self):
        global couleur_inactive
        global actif_champ
        global textes
        global couleur_page2

        # Charger l'image de fond
        background = pygame.image.load("arrière_plan.jfif")
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
        afficher_texte("Retour", largeur - 100, hauteur - 75)

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

        background = pygame.image.load("arrière_plan.jfif")
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
        afficher_texte("Retour", largeur - 100, hauteur - 75)
        suivant_button = pygame.Rect(largeur - 150, hauteur - 175, 100, 50)
        pygame.draw.rect(fenetre, vert, suivant_button)
        afficher_texte("Suivant", largeur - 100, hauteur - 150)
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
                            variables = ['GridSizeX', 'GridSizeY', 'TicksPerDay', 'BobsQty', 'FoodQty', 'EnergyInitLevel', 'MaxEnergy', 'InitPerception']
                            self.affiche_formulaire(variables)
                        elif 400 <= y <= 450:
                            pygame.quit()
                            sys.exit()

            background = pygame.image.load("Photo.png")
            background = pygame.transform.scale(background, (self.screen.get_width(), self.screen.get_height()))
            self.screen.blit(background, (0, 0))

            afficher_texte("GAME OF LIFE", self.screen.get_width() // 2, 100)
            pygame.draw.ellipse(self.screen, marron, (300, 200, 200, 50))
            afficher_texte("START", self.screen.get_width() // 2, 225)
            pygame.draw.ellipse(self.screen, marron, (300, 300, 200, 50))
            afficher_texte("OPTIONS", self.screen.get_width() // 2, 325)
            pygame.draw.ellipse(self.screen, marron, (300, 400, 200, 50))
            afficher_texte("QUIT", self.screen.get_width() // 2, 425)

            pygame.display.update()

def run_game(self):
        while self.game_active:
            self.actualise_user_input()
            self.screen.fill("WHITE")
            self.display_tiles()
            pygame.display.update()
            sleep(0.01)
def run(self):
    while self.running:
        # Exécuter la page actuelle
        self.pages[self.current_page]()