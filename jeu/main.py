import pygame
from app.World import World
from app.Window import Window




def main():
    pygame.init()
    game = World()
    screen = Window(game)
    screen.display_menu()
    # while game.isRunning:
    #     game.run_game()
    pygame.quit()

if __name__ == "__main__":
    main()
