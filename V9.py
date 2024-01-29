
# PYTHON PROJECT - STI - INSA CVL 2023/2024
# Titouan GODARD

from random import *
from time import *
from threading import Thread
import keyboard

################ PARAMETRES ######################

### Affichage du jeu ###
GAMEPRINTS = False #Autoriser l'affichage des détails sur le terminal.
TICKPRINTS = True #Autoriser l'affichage des détails des ticks sur le terminal.
TICKSHOWBOBS = False #Autoriser l'affichage du nombre de bobs à chaque ticks sous forme de bâtons.

### Grille ###
gridSizeX = 100 #Taille de la grille sur l'axe X.
gridSizeY = 100 #Taille de la grille sur l'axe Y. 

### Ticks and game ###
ticksPerDay = 100 #Nombre de Ticks par jour
bobsQty = 100 #quantité initiale de Bobs.
foodQty = 100 #quantité d'items Food générés par jours

### Bob's parameters ###
#Bob's energy
energyInitLevel = 100 #Niveau d'énergie initial des Bobs.
maxEnergy = 200 #Energie max d'un Bob.
#Bob's perception
minPerception = 0
maxPerception = 10
#Bob's velocity
minVelocity = 0
maxVelocity = 10
#Bob's memory
minMemory = 0
maxMemory = 10
#Bob's mass
minMass = 1
maxMass = 30

### Energy ###
#Food Items
foodEnergy = 100 #quantité d'énergie d'un item de food généré sur la map.
#Energy for Partheno
parthenoMotherEnergy = 150 #Energie consommée pour produire un bob par partheno
birthParthenoEnergy = 50 #Energie d'un nouveau bob né par partheno
#Energy for Sexual reproduction
parentEnergyRequired = 150 #Energie nécessaire pour commencer la reproduction sexuelle.
birthSexEnergy = 100 #Energie d'un bob né par reproduction sexuelle
sexEnergy = 100 #energie consommée pour produire un bob par reproduction sexuelle
#Energy for each Tick
tickStaticEnergy = 0.5 #energie consommée par tick en restant static
tickMobileEnergy = 1 #energie consommée par tick en étant mobile



################ CLASS BOB ######################

class Bob:
    """
    Define the class Bob
    Define size, speed, energy...
    Define functions...
    """
    def __init__(self, ID, coord) :
        self.ID = ID
        self.mass = randint(10, 30)
        self.velocity = 1
        self.energy = energyInitLevel
        self.memory = 0
        self.path = []
        self.perception = 0
        self.coord = coord

    #FONCTIONS DU BOB : hunt, eat, partheno, fuck, randomMove.
    #parametre recu pour chaque fonction : La case dans laquelle se trouve le bob.

    def partheno(self):
        """
        Fonction de reproduction d'un bob individuellement lorsqu'il a atteint l'énergie maximale.
        """
        GameWorld.gamePrint("Function : Partheno")
        if self.energy==maxEnergy:
            self.consumeEnergy(parthenoMotherEnergy)
            babyBob = Bob(GameWorld.lastID+1, self.coord)
            babyBob.energy = birthParthenoEnergy
            GameWorld.gridBob[self.coord].append(babyBob)
            GameWorld.gamePrint("birth from partheno. End of the function")
    
    def consumeEnergy(self, score):
        """
        Fonction qui retire l'énergie consommée par le bob et vérifie qu'il soit toujours vivant.
        Return True si le bob est dead.
        Return False si le bob est toujours vivant après la consommation d'énergie.
        """
        GameWorld.gamePrint("\tFunction : ConsumeEnergy")
        self.energy -= score
        if self.energy<=0: #Verifier si le bob a toujours de l'energie. Sinon il meurt.
            self.die()
            return True #le bob is dead...
        return False #le bob is alive !
    
    def die(self):
        """
        Fonction utilisée pour supprimer correctement un bob dcédé.
        """
        GameWorld.gridBob[self.coord].remove(self) #suppression du bob du tableau associé à ses coordonnées dans le dictionnaire gridBob.
        if self in GameWorld.bobArray : GameWorld.bobArray.remove(self) #Retirer le bob du tableau bobArray qui contient les bobs qui doivent jouer leur coup au tick présent. 
        if len(GameWorld.gridBob[self.coord])==0: del(GameWorld.gridBob[self.coord]) #Si le tableau est vide, alors on supprime la case du dictionnaire.
        return

    def hunt(self):
        """
        Fonction qui représente l'action d'un bob qui mange un autre bob.
        """
        GameWorld.gamePrint("Function : Hunt")
        for prey in GameWorld.gridBob[self.coord]:
            if prey.mass < 2/3*self.mass:
                #On a trouvé un bob que l'on peut manger !
                if self.consumeEnergy(tickStaticEnergy): return True #le bob is dead
                #EAT THE BOB
                energyToEat = 1/2 * prey.energy * (1-prey.mass/self.mass)
                if self.energy+energyToEat <= maxEnergy : self.energy+=energyToEat
                else : self.energy = maxEnergy # A VERIFIER DANS LES REGLES !!!!!!!!!!!!!!!!
                prey.die() #Le bob mangé meurt...
                GameWorld.gamePrint("A bob was murdered. End of the function.")
                return True
        return False

    def fuck(self):
        """
        Fonction de reproduction sexuelle entre 2 bobs.
        """
        GameWorld.gamePrint("Function : Fuck")
        for myLover in GameWorld.gridBob[self.coord] :
            if myLover.mass >= 2/3*self.mass and self.energy >= parentEnergyRequired and myLover.energy >= parentEnergyRequired and myLover in GameWorld.bobArray :
            #SI le rapport des masses est bon & si l'énergie des deux bobs est supérieur au seuil nécessaire pour la reproduction sexuelle et si le partenaire n'a pas déja effectué une action pendant ce tick.    
                babyBob=Bob(GameWorld.lastID+1, self.coord)
                babyBob.energy=birthSexEnergy
                GameWorld.gridBob[self.coord].append(babyBob)
                GameWorld.bobArray.remove(myLover)
                myLover.consumeEnergy(sexEnergy+tickStaticEnergy)
                self.consumeEnergy(sexEnergy+tickStaticEnergy)
                GameWorld.gamePrint("birth from sex")
                return True
        return False

    def eat(self):
        """
        Fonction qui effectue l'action pour un bob de manger un item de Food présent sur la grille à la même position
        """
        GameWorld.gamePrint("Function : Eat")
        if self.coord not in GameWorld.gridFood or self.energy == maxEnergy : return False
        if self.consumeEnergy(tickStaticEnergy): return True #le bob is dead
        if self.energy + GameWorld.gridFood[self.coord] <= maxEnergy :
            energyToEat = GameWorld.gridFood[self.coord]
            del GameWorld.gridFood[self.coord]
        else : 
            energyToEat = maxEnergy-self.energy
            GameWorld.gridFood[self.coord] -= energyToEat
        self.energy += energyToEat
        self.partheno()
        GameWorld.gamePrint("grrrr... End of the function.")
        return True

    def randomMove(self):
        """
        Fonction de déplacement aléaroire sur une case adjacente.
        """
        GameWorld.gamePrint("Function : RandomMove")
        previousKey = self.coord
        if self.consumeEnergy(tickMobileEnergy): return #le bob is dead
        moved = False
        mvcount = 0
        while moved == False : #tant qu'on a pas effectué un déplacement, on cherche un déplacement valide.
            if mvcount > 10 : return False #Au bout de 10 tentatives on abandonne et on considère que le déplacement est impossible. 
            mvcount += 1
            (x,y) = self.coord
            if randint(0,1) : #choix random vertical ou horizontal.
                x += randint(1,2)*2-3 #aléatoirement +1 ou -1 à la coordonnée x
                if x <= gridSizeX-1 and x >= 0:
                    moved = True
            else :
                y += randint(1,2)*2-3 #aléatoirement +1 ou -1 à la coordonnée y
                if y <= gridSizeY-1 and y >= 0:
                    moved = True
        #on applique le déplacement valide trouvé auparavant.
        if (x,y) not in GameWorld.gridBob : GameWorld.gridBob[(x,y)]=[]
        GameWorld.gridBob[(x,y)].append(self) #On ajoute le bob dans le dictionnaire à sa nouvelle position.
        GameWorld.gridBob[previousKey].remove(self) #on retire le bob de son ancienne position.
        self.coord = (x,y)
        if len(GameWorld.gridBob[previousKey])==0: del(GameWorld.gridBob[previousKey])
        GameWorld.gamePrint("Bob moved, end of the function.")
        return True


################### Grille ######################

# Dictionnaire Grille. Clé -> (x,y), contient un élément de type class Case.
#grid est une variable globale. PAS BESOIN DE LA PASSER EN PARAMETRE.

class World():
    def __init__(self) :
        self.lastID = -1 #identifiant unique pour chaque bob créé.
        self.pause = True #pour mettre sur pause le jeu.
        self.gridBob = {} #Dictionnaire de bobs.
        self.gridFood = {} #Dictionnaire d'élements Foods
        self.bobArray=[] #Tableau de bob utilisé à chaque tour pour parcourir l'esemble des bobs de façon aléatoire.
        self.bobcount=bobsQty #Compteur du nombre de bobs en vie.
        self.dayCounter=0 #Compteur du nombre de jour.
        self.tickCounter=0 #Compteur du nombre de ticks.
        self.bobSpawn() #Générer les bobs à l'initialisation du jeu.
        #statistiques de la forme (min, max, moyenne)
        self.statEnergy = [None, None, None] #statistique d'énergie
        self.statMass = [None, None, None] #statistique de masse
        self.statVelocity = [None, None, None] #statistique de vitesse
        self.statPerception = [None, None, None] #statistique de perception
        self.statMemory = [None, None, None] #statistique de mémoire
        
    def gamePrint(self, msg):
        if GAMEPRINTS : print(msg)
        return

    def printGridBob(self):
        """
        Affichage rapide du contenu des dictionnaires.
        Pas dans l'ordre... !
        """
        for cle, val in self.gridBob.items():
            print("Coord :",cle, "\t Nb Bobs :", len(val))
        return

    def printGridFood(self):
        """
        Affichage rapide du contenu des dictionnaires.
        Pas dans l'ordre... !
        """
        for cle, val in self.gridFood.items():
            print("Coord :",cle, "\tFood Level :", val)
        return
    
    def bobSpawn(self):
        """
        Fait apparaitre bobsQty bobs aléatoirement répartis sur la map.
        """
        for _ in range(bobsQty):
            x = randint(0, gridSizeX-1)
            y = randint(0, gridSizeY-1)
            if (x, y) not in self.gridBob : self.gridBob[(x, y)]=[]
            mybob=Bob(self.lastID+1, (x,y))
            self.gridBob[(x, y)].append(mybob)
        return

    def foodSpawn(self):
        """
        Fait apparaitre FoodQty elements de Food aléatoirement répartis sur la map.
        """
        for _ in range(foodQty):
            x = randint(0, gridSizeX-1)
            y = randint(0, gridSizeY-1)
            if (x, y) not in self.gridFood : self.gridFood[(x, y)]=0
            self.gridFood[(x, y)]+=foodEnergy
        return
    
    def statistics(self):
        """
        Fonction qui fait des statiqtiques sur les bobs encore en vie.
        """
        self.statEnergy = [maxEnergy, 0, 0]
        self.statMass = [maxMass, minMass, 0] #statistique de masse
        self.statVelocity = [maxVelocity, minVelocity, 0] #statistique de vitesse
        self.statPerception = [maxPerception, minPerception, 0] #statistique de perception
        self.statMemory = [maxMemory, minMemory, 0] #statistique de mémoire
        self.bobcount = 0
        for key in self.gridBob:
            for bob in self.gridBob[key]:
                self.bobcount += 1
                self.statMass[0] = min(self.statMass[0], bob.mass)
                self.statMass[1] = max(self.statMass[1], bob.mass)
                self.statMass[2] += bob.mass
                self.statEnergy[0] = min(self.statEnergy[0], bob.energy)
                self.statEnergy[1] = max(self.statMass[1], bob.energy)
                self.statEnergy[2] += bob.energy
                self.statVelocity[0] = min(self.statVelocity[0], bob.velocity)
                self.statVelocity[1] = max(self.statVelocity[1], bob.velocity)
                self.statVelocity[2] += bob.velocity
                self.statPerception[0] = min(self.statPerception[0], bob.perception)
                self.statPerception[1] = max(self.statPerception[1], bob.perception)
                self.statPerception[2] += bob.perception
                self.statMemory[0] = min(self.statMemory[0], bob.memory)
                self.statMemory[1] = max(self.statMemory[1], bob.memory)
                self.statMemory[2] += bob.memory

        if self.bobcount == 0 :
            self.statEnergy = [0, 0, 0]
            self.statMass = [0, 0, 0]
            self.statVelocity = [0, 0, 0]
            self.statPerception = [0, 0, 0]
            self.statMemory = [0, 0, 0]
        else : 
            self.statMass[2] /= self.bobcount
            self.statEnergy[2] /= self.bobcount
            self.statVelocity[2] /= self.bobcount
            self.statPerception[2] /= self.bobcount
            self.statMemory[2] /= self.bobcount
            self.statMass[2] = round(self.statMass[2], 2)
            self.statEnergy[2] = round(self.statEnergy[2], 2)
            self.statVelocity[2] = round(self.statVelocity[2], 2)
            self.statPerception[2] = round(self.statPerception[2], 2)
            self.statMemory[2] = round(self.statMemory[2], 2)
        return
    
    def printStatistics(self):
        """
        Fonction qui affiche les statistiques du jeu.
        """
        print("Statistiques du jeu :")
        print("\t Nombre de bobs :", self.bobcount)
        print("\t vitesse :", self.statVelocity)
        print("\t mass :", self.statMass)
        print("\t energy :", self.statEnergy)
        print("\t perception :", self.statPerception)
        print("\t memory :", self.statMemory)
        return
    
    def saveTheGame(self): #enregistre le jeu actuel dans le document jeu.data
        return


    def makeBobArray(self):
        """
        A chaque tick, les bobs sont listés dans le tableau bobArray avant d'être appelés pour jouer leur coup dans la fonction tick.
        Cette fonction permet de construire ce tableau.
        """
        self.bobArray.clear()
        for key in self.gridBob:
            for bob in self.gridBob[key]:
                self.bobArray.append(bob)
                bob.coord=key
        self.bobcount=len(self.bobArray)
        return


    def tick(self):
        """
        Fonction qui sollicite tous les bobs pour leur donner une action à réaliser.
        Actions possibles par ordre de priorité : eat, hunt, fuck, randomMove.
        Cette fonction prend un bob aléatoirement dans le tableau bobArray, lui fait jouer son coup puis le supprime du tableauavant de recommencer l'opération pour un autre bob aléatoirement... jusqu'à ce que le tableau soit vide, c-a-d que tous les bobs aient joué leur coup lors du tick actuel.
        """
        self.makeBobArray() #A chaque tick on créé le tableau bobArray de tous les bobs encore en vie.#printGridBob()
        GameWorld.tickCounter += 1
        if TICKPRINTS : print("tick", self.tickCounter, " : ", self.bobcount, "Bobs alive.")
        while len(self.bobArray)!=0 :
            bob = choice(self.bobArray)
            self.bobArray.remove(bob)
            assert bob in GameWorld.gridBob[bob.coord]
            #Choix d'une action :
            if not bob.eat(): #Eat food
                if not bob.hunt(): #Hunt other bobs
                    if not bob.fuck(): #Fuck
                        bob.randomMove() #Move randomly
        #sleep(0.5)
        if TICKSHOWBOBS :
            for _ in range(self.bobcount): print("|", end = "")
            print()
        return
    
    def day(self):
        """
        Fonction qui lance la simulation d'un "Day"
        Permet de mettre sur pause le jeu à tout moment entre deux ticks.
        Met a jour les statistiques à chaque début de jour"""
        self.dayCounter += 1
        self.tickCounter = 0
        self.statistics()
        if GameWorld.bobcount!=0 :
            print()
            print("DAY", self.dayCounter)
            GameWorld.foodSpawn()
            for _ in range (ticksPerDay):
                while GameWorld.pause == True : sleep(0.5) #pour mettre sur pause.
                GameWorld.tick()
                #printGridBob()

    def play(self, NbDay):
        for _ in range (NbDay) :
            self.day()

    #def pauseGame(self):
     #   while GAME.is_alive():
      #      if keyboard.is_pressed("p"):
       #         print("pause")
        #        if self.pause == True : self.pause = False
         #       else : self.pause=True
          #      break

############## Déroulement du jeu ###############

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

#PAUSE.run()

#while GAME.is_alive():
#    sleep(0.1)
#print("done")

#printGridBob()
#printGridFood()
#printGridFood()