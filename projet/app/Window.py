import pygame
import pygame._sdl2 as sdl2
from time import sleep

class Window:
    """
    Classe dédiée à l'affichage
    """
    def __init__(self, myGame):
        self.game = myGame
        self.infoObject = pygame.display.Info()
        self.screen = pygame.display.set_mode((self.infoObject.current_w-200,self.infoObject.current_h-200),  pygame.SCALED | pygame.RESIZABLE | sdl2.WINDOWPOS_CENTERED) #Fenêtre du jeu.
        self.isoCoordTable = {} #dictionnaire qui associe les coordonnées 2D des tiles à leurs coordonnées ISO. On l'utilisera pour placer les bobs exactement sur les tiles. (x réel , y réel) -> (x iso , y iso)
        self.offsetx = 0
        self.offsety = 0
        self.zoom = 1
        self.value = 20 #taille de la grille // A RELIER AVEC LES PARAMETRES ## ???!!!
        self.screen.fill((255,255,255))
        self.surfacebob = pygame.Surface((self.infoObject.current_w-200, self.infoObject.current_h-200), pygame.SRCALPHA, 32).convert_alpha()
        self.surfacetile = pygame.Surface((self.infoObject.current_w-200, self.infoObject.current_h-200), pygame.SRCALPHA, 32).convert_alpha()
    
    
    
    def display_menu(self):
        #SI LE JOUEUR CLIQUE SUR START :
        self.display_tiles()

    def display(self):
        pygame.display.update()
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
            if event.type == pygame.QUIT: self.Game.isRunning = False
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