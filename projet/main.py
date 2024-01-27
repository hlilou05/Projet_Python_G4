import pygame
from app.World import *
from app.Window import *

def main():
    pygame.init()
    game = World()
    game.run_game()

if __name__ == "__main__":
    main()

