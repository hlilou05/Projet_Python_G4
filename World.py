from random import *
from time import *
import pickle
import pygame
import os


from Bob import *
from Constant import *
from Window import *
from Tile import *

clock = pygame.time.Clock()

class World():
    def __init__(self) :
        self.isRunning = True
        self.isoCoordTable = {}
        self.window = Window(self)
        self.tile = Tile(self)
        self.guis = [] # Tableau des GUI
        self.options = option
        self.lastID = -1 #identifiant unique pour chaque bob créé.
        self.pause = False #pour mettre sur pause le jeu.
        self.affichage = AFFICHAGE # Affichage On/Off
        self.gridBob = {} #Dictionnaire de bobs.
        self.gridFood = {} #Dictionnaire d'élements Foods
        self.bobArray=[] #Tableau de bob utilisé à chaque tour pour parcourir l'esemble des bobs de façon aléatoire.
        self.bobcount= 0 #Compteur du nombre de bobs en vie.
        self.dayCounter=0 #Compteur du nombre de jour.
        self.tickCounter=0 #Compteur du nombre de tick
        self.tile.generate_tiles()
        self.window.blit_surfacetile_screen()
        self.bobSpawn() #Générer les bobs à l'initialisation du jeu.
        self.imageFood = assets["food"]
        #statistiques de la forme (min, max, moyenne)
        self.statEnergy = [None, None, None] #statistique d'énergie
        self.statMass = [None, None, None] #statistique de masse
        self.statVelocity = [None, None, None] #statistique de vitesse
        self.statPerception = [None, None, None] #statistique de perception
        self.statMemory = [None, None, None] #statistique de mémoire
        
    
    def bobSpawn(self):
        """
        Fait apparaitre bobsQty bobs aléatoirement répartis sur la map.
        """
        for _ in range(bobsQty):
            x = randint(0, gridSizeX-1)
            y = randint(0, gridSizeY-1)
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
    

    def run_game(self):
        self.day()

    def statistics(self):
        """
        Fonction qui fait des statiqtiques sur les bobs encore en vie.
        """
        self.statEnergy = [maxEnergy, 0, 0]
        self.statMass = [0, 0, 0] #statistique de masse
        self.statVelocity = [0, 0, 0] #statistique de vitesse
        self.statPerception = [0, 0, 0] #statistique de perception
        self.statMemory = [0, 0, 0] #statistique de mémoire
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
                    self.statPerception[0] = bob.perceptionScore
                    self.statPerception[1] = bob.perceptionScore
                    self.statPerception[2] += bob.perceptionScore
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

    def makeBobArray(self):
        """
        A chaque tick, les bobs sont listés dans le tableau bobArray avant d'être appelés pour jouer leur coup dans la fonction tick.
        Cette fonction permet de construire ce tableau.
        """
        self.bobArray.clear()
        for key in self.gridBob:
            for bob in self.gridBob[key]:
                self.bobArray.append(bob)
        return

    def tick(self):
        """
        Fonction qui sollicite tous les bobs pour leur donner une action à réaliser.
        Actions possibles par ordre de priorité : eat, hunt, fuck, randomMove.
        Cette fonction prend un bob aléatoirement dans le tableau bobArray, lui fait jouer son coup puis le supprime du tableauavant de recommencer l'opération pour un autre bob aléatoirement... jusqu'à ce que le tableau soit vide, c-a-d que tous les bobs aient joué leur coup lors du tick actuel.
        """
        #sleep(tickTime)
        self.makeBobArray() #A chaque tick on créé le tableau bobArray de tous les bobs encore en vie.#printGridBob()
        self.tickCounter += 1
        while len(self.bobArray)!=0 :
            if self.pause : continue
            bob = choice(self.bobArray)
            self.bobArray.remove(bob)
            assert bob in self.gridBob[bob.coord]
           # self.update_guis()
            if not bob.isDead : bob.perception()
            #if not bob.isDead : bob.use_memory()
            #Choix d'une action :
            if not bob.hunt(): #Eat food
                if not bob.eat(): #Hunt other bobs
                    if not bob.fuck(): #Fuck
                        bob.move() #Move randomly
        self.window.display()
        clock.tick(tickTime)
        return


    def day(self):
        self.dayCounter += 1
        self.tickCounter = 0
        # self.statistics()
        if self.bobcount!=0 :
            self.foodSpawn()
            for _ in range (ticksPerDay):
                #self.auto_save()
                if self.bobcount == 0 : self.isRunning = False
                self.tick()
        else : self.isRunning = False

    def play(self, NbDay):
        for _ in range (NbDay) :
            self.day()

    def sauvegarde(self, file):
        file = os.path.abspath("__pycache__/" + file + ".pyc")
        with open(file, 'wb') as f:
            pickle.dump(self, f, 3)
            f.close()
        return
    
    def auto_save(self):
        with open(os.path.abspath("__pycache__/autosave"), 'wb') as f:
            pickle.dump(self, f, 3)
            f.close()
        return
    
    def load_sauvegarde(self, file):
        file = os.path.abspath("__pycache__/" + file + ".pyc")
        with open(file, "rd") as f:
            saved = pickle.load(f)
            f.close()
        self = saved
        return
    
    def iso_coord(self, x, y):
        """
        Génération de coordonnées isométriques à partir de coordonnées 2D.
        """
        return (x-y, (x+y)/2)
    
                
    def update_bobs(self):
        for key in self.gridBob:
            for bob in self.gridBob[key]:
                bob.update_bob()

    def update_food(self):
        TILE_SIZE = 16*self.window.zoom
        FOOD_SIZE = 13*self.window.zoom
        for key in self.gridFood:
            (x,y)=self.isoCoordTable[key] #coordonnées Top Left de la case
            x+=TILE_SIZE/2 #coordonnée centre de la case
            x+=FOOD_SIZE/4 #Coordonnée top left de la food
            y+=TILE_SIZE/5 #coordonnée de la hauteur de la food.
            self.window.surfacebob.blit(pygame.transform.scale(self.imageFood, (int(self.imageFood.get_width() * self.window.zoom), int(self.imageFood.get_height() * self.window.zoom))), (x,y))
    
    def add_gui_to_list(self, gui):
        self.guis.append(gui)

    def remove_gui_from_list(self, gui):
        if gui in self.guis :
            self.guis.remove(gui)

    def update_guis(self):
        for gui in self.guis :
            gui.update()