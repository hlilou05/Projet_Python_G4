from Constant import *
import pygame


image_tile = pygame.image.load("Tile32x32.png")
screen = pygame.display.set_mode((600, 600))


class Tile():

    """
    Classe dédiée aux Tiles. 
    Une Tile est un petit carreau de la grille
    On définit ici sa taille et l'image qui la représentera.
    """
    def __init__(self, myGame):
        self.Game = myGame
        self.rect = image_tile.get_rect()


    def set_center(self, x, y):
        self.rect.center=(x,y)

    def generate_tiles(self):
        """
        Construction de la grille sur la fenêtre.
        """
        TILE_SIZE = 16*self.zoom
        screen_x, screen_y = screen.get_size()
        for y in range(gridSize):
            for x in range(gridSize):
                #création d'une new Tile
                self.set_center(screen_x//4 + screen_y//2 + (x-gridSize//2)*TILE_SIZE , screen_y//2 - screen_x//4 + (y-gridSize//2)*TILE_SIZE)
                #On sauvegarde la coordonnée isométrique de la case pour pouvoir replacer des bobs facilement dedans.
                #Dictionnaire (x réel , y réel) -> (x iso , y iso)
                self.isoCoordTable[(x, y)]  =  [self.iso_coord(self.rect.center[0], self.rect.center[1])[0]+self.offsetx*TILE_SIZE  ,  self.iso_coord(self.rect.center[0], self.rect.center[1])[1]+self.offsety*TILE_SIZE]
                self.myGame.surfacetile.blit(pygame.transform.scale_by(image_tile,self.zoom), self.isoCoordTable[(x,y)])


