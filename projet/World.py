from random import *
from time import *
from threading import Thread
import pickle
import pygame
import sys
from Constant import *


import Bob



class World():
    def __init__(self) :
        self.window = Window(self)
        self.lastID = -1 #identifiant unique pour chaque bob créé.
        self.pause = False #pour mettre sur pause le jeu.
        self.affichage = AFFICHAGE
        self.gridBob = {} #Dictionnaire de bobs.
        self.gridFood = {} #Dictionnaire d'élements Foods
        self.bobArray=[] #Tableau de bob utilisé à chaque tour pour parcourir l'esemble des bobs de façon aléatoire.
        self.bobcount=bobsQty #Compteur du nombre de bobs en vie.
        self.dayCounter=0 #Compteur du nombre de jour.
        self.tickCounter=0 #Compteur du nombre de ticks.
        self.bobSpawn() #Générer les bobs à l'initialisation du jeu.
        self.guis = [] # Tableau des GUI
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
            mybob=Bob(self, self.lastID+1, (x,y))
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
        self.statMass = [0, 0, 0] #statistique de masse
        self.statVelocity = [0, 0, 0] #statistique de vitesse
        self.statPerception = [0, 0, 0] #statistique de perception
        self.statMemory = [0, 0, 0] #statistique de mémoire
        self.bobcount = 0
        for key in self.gridBob:
            for bob in self.gridBob[key]:
                if(self.bobcount == 0) :
                    self.statMass[0] = bob.mass
                    self.statMass[1] = bob.mass
                    self.statMass[2] += bob.mass
                    self.statEnergy[0] = bob.energy
                    self.statEnergy[1] = bob.energy
                    self.statEnergy[2] += bob.energy
                    self.statVelocity[0] = bob.velocity
                    self.statVelocity[1] = bob.velocity
                    self.statVelocity[2] += bob.velocity
                    self.statPerception[0] = bob.perception
                    self.statPerception[1] = bob.perception
                    self.statPerception[2] += bob.perception
                    self.statMemory[0] = bob.memory
                    self.statMemory[1] = bob.memory
                    self.statMemory[2] += bob.memory
                else :
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
            bob.perception()
            bob.memory()
            #Choix d'une action :
            if not bob.hunt(): #Eat food
                if not bob.eat(): #Hunt other bobs
                    if not bob.fuck(): #Fuck
                        bob.move() #Move randomly

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
        if self.bobcount!=0 :
            print()
            self.foodSpawn()
            for _ in range (ticksPerDay):
                self.auto_save()
                while self.pause == True : continue # pour mettre sur pause.
                self.tick()

    def play(self, NbDay):
        for _ in range (NbDay) :
            self.day()

    def sauvegarde(self, file):
        file = "../__pycache__/" + file + ".pyc"
        with open(file, 'wb') as f:
            pickle.dump(self, f, 3)
            f.close()
        return
    
    def auto_save(self):
        with open("../__pycache__/autosave", 'wb') as f:
            pickle.dump(self, f, 3)
            f.close()
        return
    
    def load_sauvegarde(self, file):
        file = "../__pycache__/" + file + ".pyc"
        with open(file, "rd") as f:
            saved = pickle.load(f)
            f.close()
        self = saved
        return
    