import pygame
from app.World import *
from app.Window import *

def main():

    pygame.init()
    largeur, hauteur = 800, 600
    screen = pygame.display.set_mode((largeur, hauteur))
    pygame.display.set_caption("PROJET_PYTHON_2024")

    game = World()
    window = Window(game)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
             

        if window.menu_active:
            window.display_menu()
        elif window.game_active:
            window.display()
        elif window.pause_menu_active:
            window.affiche_pause_menu()
        elif window.suivant_pressed:
            window.affiche_deuxieme_page()

        
if __name__ == "__main__":
    main()

