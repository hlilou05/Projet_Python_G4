GameWorld = World()

NbDay = 50
GAME = Thread(target=GameWorld.play, args=[NbDay])
#PAUSE = Thread(target=GameWorld.pauseGame, args=[]) 

GAME.start()
#PAUSE.start()

#sleep(1)
GameWorld.pause=False
GAME.join()

GameWorld.printStatistics()