from .Constant import *
import pygame
from .Window import *

class Tile():

    """
    Classe dédiée aux Tiles. 
    Une Tile est un petit carreau de la grille
    On définit ici sa taille et l'image qui la représentera.
    """
    def __init__(self, myGame):
        self.game = myGame
        self.image = assets["tile"]
        self.rect = self.image.get_rect()
        self.offsetx = self.game.window.offsetx
        self.offsety = self.game.window.offsety


    def set_center(self, x, y):
        self.rect.center=(x,y)

    def generate_tiles(self):
        """
        Construction de la grille sur la fenêtre.
        """
        TILE_SIZE = 16*self.game.window.zoom
        screen_x, screen_y = self.game.window.screen.get_size()
        for y in range(gridSizeY):
            for x in range(gridSizeX):
                #création d'une new Tile
                self.set_center(screen_x//4 + screen_y//2 + (x-gridSizeX//2)*TILE_SIZE , screen_y//2 - screen_x//4 + (y-gridSizeY//2)*TILE_SIZE)
                #On sauvegarde la coordonnée isométrique de la case pour pouvoir replacer des bobs facilement dedans.
                #Dictionnaire (x réel , y réel) -> (x iso , y iso)
                self.game.isoCoordTable[(x, y)]  =  [self.game.iso_coord(self.rect.center[0], self.rect.center[1])[0]+self.offsetx*TILE_SIZE  ,  self.game.iso_coord(self.rect.center[0], self.rect.center[1])[1]+self.offsety*TILE_SIZE]
                self.game.window.surfacetile.blit(pygame.transform.scale(self.image, (int(self.image.get_width() * self.game.window.zoom), int(self.image.get_height() * self.game.window.zoom))), self.game.isoCoordTable[(x,y)])
