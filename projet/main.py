from app.World import *

def main():
    GameWorld = World()
    GAME = Thread(target=GameWorld.play, args=[NbDay])
    #PAUSE = Thread(target=GameWorld.pauseGame, args=[]) 

    GAME.start()
    #PAUSE.start()

    #sleep(1)
    GameWorld.pause=False
    GAME.join()

    GameWorld.printStatistics()

if __name__ == "__main__":
    main()