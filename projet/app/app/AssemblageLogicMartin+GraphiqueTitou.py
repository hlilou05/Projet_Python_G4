
# PYTHON PROJECT - STI - INSA CVL 2023/2024
# Titouan GODARD 

from random import *
from time import *
from threading import Thread
import pygame
import sys



"""*******************************************"""
# ******************************************** #
""" ************ PARTIE LOGIQUE **************"""
# ******************************************** #
"""*******************************************"""



################ PARAMETRES ######################

### Affichage du jeu ###
GAMEPRINTS = False #Autoriser l'affichage des détails sur le terminal.
TICKPRINTS = True #Autoriser l'affichage des détails des ticks sur le terminal.
TICKSHOWBOBS = False #Autoriser l'affichage du nombre de bobs à chaque ticks sous forme de bâtons.
AFFICHAGE = True
TICKTIME = 5


### Grille ###
gridSizeX = 50 #Taille de la grille sur l'axe X.
gridSizeY = 50 #Taille de la grille sur l'axe Y. 

### Ticks and game ###
ticksPerDay = 100 #Nombre de Ticks par jour
bobsQty = 50 #quantité initiale de Bobs.
foodQty = 50 #quantité d'items Food générés par jours
NbDay = 50 #Nombre de jour à jouer


### Fonction Activated ###
Parthenogenesis = True
Eat = True
Hunt = True
Perception = True
Memory = True
Reproduction = True


import pygame
import os
assets = {
    "arriere_plan" : pygame.image.load(os.path.abspath("src/arrière_plan.jfif")),
    "bob" : pygame.image.load(os.path.abspath("src/bob.png")),
    "bob.blue" : pygame.image.load(os.path.abspath("src/bob.blue.png")),
    "bob.red" : pygame.image.load(os.path.abspath("src/bob.rouge.png")),
    "food" : pygame.image.load(os.path.abspath("src/nourriture.png")),
    "fond_ecran" : pygame.image.load(os.path.abspath("src/Photo.png")),
    "tile" : pygame.image.load(os.path.abspath("src/Tile32x32.png")),
}



### Bob's parameters ###
#Bob's energy
energyInitLevel = 100 #Niveau d'énergie initial des Bobs.
maxEnergy = 200 #Energie max d'un Bob.
#Bob's perception
InitPerception = 1
minPerception = 0
maxPerception = 10
#Bob's velocity
InitVelocity = 1
minVelocity = 0
maxVelocity = 10
#Bob's memory
InitMemory = 1
minMemory = 0
maxMemory = 10
#Bob's mass
InitMass = 1
minMass = 1
maxMass = 30

### Taux de mutation ###
TauxMutationMass = 0.2
TauxMutationVelocity = 0.2
TauxMutationMemory = 0.2
TauxMutationPerception = 0.2

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
tickPerceptionPenalty = 0.2 # Pourcentage des points de perceptions pour conso d'energie
tickMemoryPenalty = 0.2 # Pourcentage des points de perceptions pour conso d'energie

SeuilPredator = 2/3 # Seuil du quotient de masse pour distinguer predateur/proie



################ CLASS BOB ######################

class Bob:
    """
    Define the class Bob
    Define size, speed, energy...
    Define functions...
    """

    def __init__(self, game, ID, coord) :
        self.game = game
        self.ID = ID
        self.mass = InitMass
        self.velocity = InitVelocity
        self.energy = energyInitLevel
        self.memory = InitMemory
        self.path = []
        self.remembered_food = [(0, 0), 0]
        self.remembering_food = False
        self.possiblefood = [(0, 0), 0]
        self.perceptionScore = InitPerception
        self.coord = coord
        self.seen = {}
        self.isDead = False
        self.fuite = False
        self.bufvelo = 0.00
        self.game.lastID += 1
        self.action = ""

    #FONCTIONS DU BOB : hunt, eat, partheno, fuck, Move.
        

    def choose_image(self):
        
        self.image = assets["bob"]

        if self.velocity >= 1.2 and self.velocity < 1.6:
            self.image = assets["bob.blue"]
        elif self.velocity > 2 :
            self.image = assets["bob.rouge"]

    def add_bob_to_grid(self):
        if self.coord not in self.game.gridBob:
            self.game.gridBob[self.coord] = []
        self.game.gridBob[self.coord].append(self)
        self.game.bobcount += 1
        
    def Val_Mutation(self, TauxMut, Val):
        return (random.uniform(Val*(1-TauxMut), Val*(1+TauxMut)))

    def partheno(self):
        if not Parthenogenesis : return False
        """
        Fonction de reproduction d'un bob individuellement lorsqu'il a atteint l'énergie maximale.
        """
        if self.energy==maxEnergy:
            babyBob = Bob(self.game, self.game.lastID+1, self.coord)
            
            babyBob.energy = birthParthenoEnergy
            babyBob.mass = int(self.Val_Mutation(TauxMutationMass, self.mass))
            babyBob.velocity = self.Val_Mutation(TauxMutationVelocity, self.velocity)
            babyBob.memory = int(self.Val_Mutation(TauxMutationMemory, self.memory))
            babyBob.perceptionScore = int(self.Val_Mutation(TauxMutationPerception, self.perceptionScore))
            babyBob.add_bob_to_grid
            self.consumeEnergy(parthenoMotherEnergy)
            return True
    
    def consumeEnergy(self, score):
        """
        Fonction qui retire l'énergie consommée par le bob et vérifie qu'il soit toujours vivant.
        Return True si le bob est dead.
        Return False si le bob est toujours vivant après la consommation d'énergie.
        """
        self.energy -= score
        if self.energy<=0: #Verifier si le bob a toujours de l'energie. Sinon il meurt.
            self.die()
            return True #le bob is dead...
        return False #le bob is alive !
    
    def die(self):
        """
        Fonction utilisée pour supprimer correctement un bob décédé.
        """
        self.game.gridBob[self.coord].remove(self) #suppression du bob du tableau associé à ses coordonnées dans le dictionnaire gridBob.
        if self in self.game.bobArray : self.game.bobArray.remove(self) #Retirer le bob du tableau bobArray qui contient les bobs qui doivent jouer leur coup au tick présent. 
        if len(self.game.gridBob[self.coord])==0: del(self.game.gridBob[self.coord]) #Si le tableau est vide, alors on supprime la case du dictionnaire.
        self.game.bobcount -= 1
        self.isDead = True
        return

    def hunt(self):
        if not Hunt : return False
        if self.isDead : return False 
        """
        Fonction qui représente l'action d'un bob qui mange un autre bob.
        """
        for prey in self.game.gridBob[self.coord]:
            if prey != self and prey.mass / self.mass <= SeuilPredator :
                #On a trouvé un bob que l'on peut manger !
                #EAT THE BOB
                energyToEat = 1/2 * prey.energy * (1-prey.mass/self.mass)
                if self.energy+energyToEat <= maxEnergy : self.energy+=energyToEat
                else : self.energy = maxEnergy
                prey.die() #Le bob mangé meurt...
                self.action = "hunt"
                return True
        return False

    def fuck(self):
        if not Reproduction : return False
        if self.isDead : return False
        """
        Fonction de reproduction sexuelle entre 2 bobs.
        """
        for myLover in self.game.gridBob[self.coord] :
            if myLover != self and myLover.mass >= SeuilPredator*self.mass and self.energy >= parentEnergyRequired and myLover.energy >= parentEnergyRequired and myLover in self.game.bobArray :
            #SI le rapport des masses est bon & si l'énergie des deux bobs est supérieur au seuil nécessaire pour la reproduction sexuelle et si le partenaire n'a pas déja effectué une action pendant ce tick.    
                babyBob=Bob(self.game, self.game.lastID+1, self.coord)
                babyBob.energy=birthSexEnergy

                babyBob.mass = int(self.Val_Mutation(TauxMutationMass, (self.mass + myLover.mass)/2))
                babyBob.velocity = self.Val_Mutation(TauxMutationVelocity, (self.velocity + myLover.velocity)/2)
                babyBob.memory = int(self.Val_Mutation(TauxMutationMemory, (self.memory + myLover.memory)/2))
                babyBob.perception = int(self.Val_Mutation(TauxMutationPerception, (self.perceptionScore + myLover.perceptionScore)/2))

                babyBob.add_bob_to_grid()
                self.game.bobArray.remove(myLover)
                myLover.consumeEnergy(sexEnergy)
                self.consumeEnergy(sexEnergy)
                self.action = "fuck"
                return True
        return False

    def eat(self):
        if self.isDead : return False
        if not Eat : return False
        """
        Fonction qui effectue l'action pour un bob de manger un item de Food présent sur la grille à la même position
        """
        if (self.coord not in self.game.gridFood) or self.energy == maxEnergy : return False
        if self.energy + self.game.gridFood[self.coord] <= maxEnergy :
            self.energy += self.game.gridFood.pop(self.coord)
        else :
            energyToEat = maxEnergy-self.energy
            self.game.gridFood[self.coord] -= energyToEat
            self.energy += energyToEat
            self.partheno()
        if self.coord == self.remembered_food[0] :
            self.remembering_food == False
        self.consumeEnergy(tickStaticEnergy) #le bob is dead
        self.action = "eat"
        return True


    def distance(self, x, y, i, j):
        dist = abs(i - x) + abs(j - y)
        return dist

    def escape(self):
        # Evaluate best place to go #
        scores = {}
        score = 0
        (a, b) = self.coord
        velocity = int(self.velocity) + int(self.bufvelo)
        for i in range(-velocity + a, velocity + 1 + a):
            for j in range(velocity - abs(i) + b, velocity - abs(i) + 1 + b):
                if(i >= 0 and i < gridSizeX and j >= 0 and j < gridSizeY):
                    for (x, y) in self.seen["Bob+"].keys():
                        score += self.distance(i, j, x, y)    
                    scores[(i,j)] = score
                    score = 0
        self.action += "escape"
        return max(scores, keys=scores.get)


    def move_towards_coord(self, coord):
        (i, j) = self.coord
        (x, y) = coord
        velocity = int(self.velocity) + int(self.bufvelo)
        distance_to_coord = self.distance(i, j, x, y)
            
        if distance_to_coord <= velocity:
            return (x, y)
            
        else:

            dir_x = (x - i) / distance_to_coord
            dir_y = (y - j) / distance_to_coord

            if random.randint(0,1):
                mov_x = round(dir_x*velocity)
                mov_y = round(dir_y*(velocity - abs(mov_x)))
            else :
                mov_y = round(dir_y*velocity)
                mov_x = round(dir_x*(velocity - abs(mov_y)))
        self.action += "towards"
        return (i, j)


    def random_move(self):

        # Random move using memory and velocity #
        # Bob will move v tiles and won't go back #
        velocity = int(self.velocity) + int(self.bufvelo)
        (x, y) = self.coord
        MoveOk = False
        while not MoveOk:
            if randint(0,1):
                move_x = randint(max(0, x - velocity), min(gridSizeX - 1, x + velocity))
                move_y = randint(max(0, y - (velocity - abs(move_x - x))), min(gridSizeY - 1, y + (velocity - abs(move_x - x))))
            else:
                move_y = randint(max(0, y - velocity), min(gridSizeY - 1, y + velocity))
                move_x = randint(max(0, x - (velocity - abs(move_y - y))), min(gridSizeX - 1, x + (velocity  - abs(move_y - y))))
            if (move_x, move_y) not in self.path :
                MoveOk = True
            if not Memory : MoveOk = True
            if (move_x, move_y) == self.coord : MoveOk = False
        self.action += "random"
        return (move_x, move_y)

    #Function perception to get all elements around
    def perception(self):
        if not Perception : return
        (x, y) = self.coord
        self.seen = {"Bob+": {}, "Bob-": {}, "Food": {}}
        for i in range(-self.perceptionScore, self.perceptionScore  + 1):
            for j in range(- (self.perceptionScore - abs(i)) ,self.perceptionScore - abs(i) + 1):
                if((x + i, y + j) in self.game.gridFood.keys()):
                    self.seen["Food"][(x + i, y + j)] = self.game.gridFood[(x + i, y + j)]
                elif((x + i, y + j) in self.game.gridBob.keys()):
                    for bob in self.game.gridBob[x + i, y+j] :
                        if bob == self : continue    
                        if(self.mass / bob.mass <= SeuilPredator ):
                            self.seen["Bob+"][(x + i, y + j)] = bob
                            self.fuite = True
                        elif(self.mass / bob.mass >= 1 - SeuilPredator):
                            self.seen["Bob-"][(x + i, y + j)] = bob
        self.seen["Food"] = dict(sorted(self.seen["Food"].items(), key=lambda x:x[1], reverse = True))
        self.consumeEnergy(self.perceptionScore*tickPerceptionPenalty)
        return


    def move(self) :
        if self.isDead : return False
        self.bufvelo += self.velocity - int(self.velocity)
        key = self.coord
        (x, y) = (-1, -1)
        self.action = "Move"
        ## Fuite ##
        if self.fuite == 1 :
            (x,y) = self.escape()
        else:
            if Perception :
                (x,y) = self.deplace_perception()
            if (x,y) == (-1, -1):
                if self.remembering_food and Memory:
                    (x,y) = self.move_towards_coord(self.remembered_food[0])
                else:
                    (x, y) = self.random_move()
        if (x,y) not in self.game.gridBob : self.game.gridBob[(x,y)]=[]
        self.game.gridBob[(x,y)].append(self) #On ajoute le bob dans le dictionnaire à sa nouvelle position.
        self.game.gridBob[key].remove(self) #on retire le bob de son ancienne position.
    
        self.bufvelo -= int(self.bufvelo)
        self.coord = (x,y)
        self.consumeEnergy(self.mass*(self.velocity**2))
        print(f"{x, y}")
        return 0
    
    def use_memory(self):
        if not Memory : return
        # if there is some food on the bob's coordinates, save its amount
        self.path.append(self.coord)
        if self.possiblefood not in self.seen["Food"].items() and self.possiblefood[1] > 0:
            self.remembered_food = self.possiblefood
        #if the coordinates of the remembered food contain a different amount of food (food eaten or food that respawned)
        if (self.remembered_food[0]) in self.seen["Food"].keys():
            self.remembering_food = False
            if self.seen["Food"][self.remembered_food[0]] != self.remembered_food[1]:
                self.remembered_food = (self.remembered_food[0], 0)
        # find the biggest food in the bob's perception
        if len(self.seen["Food"].keys()) != 0: 
            if next(iter(self.seen["Food"].items()))[1] > self.remembered_food[1]:
                self.possiblefood = next(iter(self.seen["Food"].items()))
            else:
                self.possiblefood = [(0,0), 0]
        #determines whether the bob needs to remember the food.
        if (self.remembered_food not in self.seen["Food"].items()) and self.remembered_food[1] > 0:
            self.remembering_food = True
        else:
            self.remembering_food = False
        # if the bob already remembers at its maximum capacity, remove the last remembered tiles
        while len(self.path) > 2 * (self.memory-self.remembering_food):
            del self.path[0]
        self.consumeEnergy(self.memory*tickMemoryPenalty)
        return
    

    #function to find the best food to hunt in the bob's perception
    #self.currenttarget : variable which will contain the best food to hunt
    def deplace_perception(self):
        currenttarget = None
        #initializing the variable that will be compared with the Manhattan distance between bob's coordinates and the static foods' coordinates
        diff = self.perceptionScore*2
        maxfood = 0
        #determines nearest static food with the biggest energy
        for food in self.seen["Food"].items():
            if diff >= abs(food[0][0]-self.coord[0])+abs(food[0][1]-self.coord[1]):
                if maxfood <= food[1]:
                    diff = abs(food[0][0]-self.coord[0])+abs(food[0][1]-self.coord[1])
                    currenttarget = food[0]
                    maxfood = food[1]
        if currenttarget != None:
            self.action += "perception 1"
            return self.move_towards_coord(currenttarget)
        else:
            maxfood = self.energy
            #determines the nearest bob with the lowest energy
            for bob in self.seen["Bob-"].items():
                if diff >= abs(bob[0][0]-self.coord[0])+abs(bob[0][1]-self.coord[1]):
                    if maxfood >= bob[1].energy:
                        diff = abs(bob[0][0]-self.coord[0])+abs(bob[0][1]-self.coord[1])
                        currenttarget = bob[0]
                        maxfood = bob[1].energy
        
        if currenttarget != None :
            self.action += "perception 2"
            return self.move_towards_coord(currenttarget)
        else :
            return (-1, -1)

################### Grille ######################

# Dictionnaire Grille. Clé -> (x,y), contient un élément de type class Case.
#grid est une variable globale. PAS BESOIN DE LA PASSER EN PARAMETRE.

class World():
    """
    Classe dédiée au fonctionnement du jeu : faire spawn les bobs, stocker les bobs et toute entité sur la grille,
    exécuter les tics, faire appel aux fonctions d'affichage de la partie graphique à la fin des tics, etc.
    """
    def __init__(self) :
        self.lastID = -1 #identifiant unique pour chaque bob créé.
        self.isRunning = True
        self.isPaused = False #pour mettre sur pause le jeu.
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
        self.gameView = View(self) #classe de l'affichage
        
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
            mybob=Bob(self, self.lastID+1, (x,y))
            mybob.add_bob_to_grid()
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
                self.statPerception[0] = min(self.statPerception[0], bob.perceptionScore)
                self.statPerception[1] = max(self.statPerception[1], bob.perceptionScore)
                self.statPerception[2] += bob.perceptionScore
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
        self.tickCounter += 1
        if TICKPRINTS : print("tick", self.tickCounter, " : ", self.bobcount, "Bobs alive.")
        while len(self.bobArray)!=0 :
            bob = choice(self.bobArray)
            self.bobArray.remove(bob)
            assert bob in self.gridBob[bob.coord]
            #Choix d'une action :
            if not bob.eat(): #Eat food
                if not bob.hunt(): #Hunt other bobs
                    if not bob.fuck(): #Fuck
                        bob.random_move() #Move randomly
        #sleep(0.5)
        if TICKSHOWBOBS :
            for _ in range(self.bobcount): print("|", end = "")
            print()
        return
    

    def day(self, renderMode):
        """
        Fonction qui lance la simulation d'un "Day"
        Permet de mettre sur pause le jeu à tout moment entre deux ticks.
        Met a jour les statistiques à chaque début de jour"""
        self.dayCounter += 1
        self.tickCounter = 0
        self.statistics()
        print()
        print("DAY", self.dayCounter)
        self.foodSpawn()
        for _ in range (ticksPerDay):
            if self.bobcount == 0 : self.isRunning=False #quitter si tous les bobs sont morts
            if not self.isRunning : return #quitter si l'attribut isRunning est False.
            while self.isPaused == True : #Pause
                if not self.isRunning : return #quitter si l'attribut isRunning est False.
                sleep(0.1)
                if not renderMode : self.gameView.Display()
                #afficher menu pause
                    #si reprise du jeu : afficher
            self.tick()
            if not renderMode : self.gameView.Display()
            sleep(0.1)


    def run_game(self):
        while self.isRunning :
            self.day(False) #renderMode=False
        pygame.quit()

    def run_main_menu(self):
        return

    def run_pause_menu(self):
        return




"""*******************************************"""
# ********************************************* #
""" ********** PARTIE GRAPHIQUE EN 3D *********"""
# ********************************************* #
"""*******************************************"""




class Tile():
    """
    Classe dédiée aux Tiles. 
    Une Tile est un petit carreau de la grille
    On définit ici sa taille et l'image qui la représentera.
    """
    def __init__(self):
        self.image = assets["tile"]
        self.rect = self.image.get_rect()
    def set_center(self, x, y):
        self.rect.center=(x,y)

class GraphicBob():
    def __init__(self):
        self.image = assets["bob"]
        self.image_blue = assets["bob.blue"]
        self.image_red = assets["bob.red"]
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.image_blue = pygame.transform.scale(self.image_blue, (10, 10))
        self.image_red = pygame.transform.scale(self.image_red, (10, 10))
    def image_scale(self, scale):
        self.image = pygame.transform.scale(self.image, (scale, scale))
        self.image_blue = pygame.transform.scale(self.image_blue, (scale, scale))
        self.image_red = pygame.transform.scale(self.image_red, (scale, scale))


class GraphicFood():
    def __init__(self):
        self.image = assets["food"]
        self.image = pygame.transform.scale(self.image, (13, 13))


class View:
    """
    Classe dédiée à l'affichage
    """
    def __init__(self, myGame):
        self.Game = myGame
        self.GBob = GraphicBob()
        self.GFood = GraphicFood()
        self.GTile = Tile()
        self.infoObject = pygame.display.Info()
        self.screen = pygame.display.set_mode((self.infoObject.current_w-200,self.infoObject.current_h-200)) #Fenêtre du jeu.
        self.isoCoordTable = {} #dictionnaire qui associe les coordonnées 2D des tiles à leurs coordonnées ISO. On l'utilisera pour placer les bobs exactement sur les tiles. (x réel , y réel) -> (x iso , y iso)
        self.bobArray = [] #Tableau de bobs à afficher
        self.foodArray = [] #Tableau de food à afficher
        self.zoom = 1
        self.offsetx = 0
        self.offsety = 0
        self.value = 20 #taille de la grille // A RELIER AVEC LES PARAMETRES
        self.screen.fill("WHITE")
        self.update_tiles()
        self.Display()
        #self.display_menu()

    def display_menu(self):
        #SI LE JOUEUR CLIQUE SUR START :
        self.display_tiles()

    def Display(self):
        """
        Fonction qui actualise la grille avec le zoom et maintient l'affichage pendant toute la durée de l'execution.
        """
        self.Actualise_UserInput()
        self.screen.fill("WHITE")
        self.update_tiles()
        self.update_bobs()
        self.update_food()
        pygame.display.update()
    
    def iso_coord(self, x, y):
        """
        Génération de coordonnées isométriques à partir de coordonnées 2D.
        """
        return [x-y, (x+y)/2]

    def update_tiles(self):
        """
        Construction de la grille sur la fenêtre.
        """
        TILE_SIZE = 16*self.zoom
        screen_x, screen_y = self.screen.get_size()
        for y in range(gridSizeY):
            for x in range(gridSizeX):
                #création d'une new Tile
                self.GTile.set_center(screen_x//4 + screen_y//2 + (x-gridSizeX//2)*TILE_SIZE , screen_y//2 - screen_x//4 + (y-gridSizeY//2)*TILE_SIZE)
                #On sauvegarde la coordonnée isométrique de la case pour pouvoir replacer des bobs facilement dedans.
                #Dictionnaire (x réel , y réel) -> (x iso , y iso)
                self.isoCoordTable[(x, y)]  =  [self.iso_coord(self.GTile.rect.center[0], self.GTile.rect.center[1])[0]+self.offsetx*TILE_SIZE  ,  self.iso_coord(self.GTile.rect.center[0], self.GTile.rect.center[1])[1]+self.offsety*TILE_SIZE]
                scaled_width = int(self.GTile.image.get_width() * self.zoom)
                scaled_height = int(self.GTile.image.get_height() * self.zoom)
                scaled_image = pygame.transform.scale(self.GTile.image, (scaled_width, scaled_height))
                iso_x, iso_y = self.isoCoordTable[(x, y)]
                self.screen.blit(scaled_image, (iso_x, iso_y))



    def update_bobs(self):
        TILE_SIZE = 16*self.zoom
        BOB_SIZE = 10*self.zoom
        for key in self.Game.gridBob:
            for bob in self.Game.gridBob[key]:
                (x,y)=self.isoCoordTable[key] #coordonnées Top Left de la case
                x+=TILE_SIZE/2 #coordonnée centre de la case
                x+=BOB_SIZE/4 #Coordonnée top left du bob
                y+=TILE_SIZE/5 #coordonnée de la hauteur du bob.
                scaled_image = pygame.transform.scale(self.GBob.image, (int(self.GBob.image.get_width() * self.zoom), int(self.GBob.image.get_height() * self.zoom)))
                self.screen.blit(scaled_image, (x, y))




    def update_food(self):
        TILE_SIZE = 16*self.zoom
        FOOD_SIZE = 13*self.zoom
        for key in self.Game.gridFood:
            (x,y)=self.isoCoordTable[key] #coordonnées Top Left de la case
            x+=TILE_SIZE/2 #coordonnée centre de la case
            x+=FOOD_SIZE/4 #Coordonnée top left de la food
            y+=TILE_SIZE/5 #coordonnée de la hauteur de la food.
            scaled_width = int(self.GFood.image.get_width() * self.zoom)
            scaled_height = int(self.GFood.image.get_height() * self.zoom)
            scaled_image = pygame.transform.scale(self.GFood.image, (scaled_width, scaled_height))
            self.screen.blit(scaled_image, (x, y))



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
                        self.Game.isPaused = not self.Game.isPaused
        self.screen.fill("WHITE")
        self.update_tiles()
        self.update_bobs()
        return



"""********************************************"""
# ********************************************** #
""" ************DEROULEMENT DU JEU**************"""
# ********************************************** #
"""********************************************"""


import pygame
pygame.init()

        
GameWorld = World()
GameWorld.run_game()


"""
fenetre = View(GameWorld)

while GameWorld.isRunning:
    GameWorld.tick()
    fenetre.Display()
    sleep(0.3)

"""
