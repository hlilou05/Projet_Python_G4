from app.World import *


def main():
    pygame.init()
    game = World()
    game.window.display_menu()
    # while game.isRunning:
    #     game.run_game()
    pygame.quit()

if __name__ == "__main__":
    main()