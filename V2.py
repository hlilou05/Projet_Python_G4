
# PYTHON PROJECT - STI - INSA CVL 2023
# Titouan GODARD

from random import *

################ VARIABLES ######################

bobsQty = 20 #quantité initiale de Bobs.
foodQty = 5 #quantité d'items Food sur la map générés au départ et par jour de jeu.
foodEnergy = 20 #quantité d'énergie d'un item de food généré sur la map.
energyInitLevel = 100 #Niveau d'énergie initial des Bobs.
gridSize = 10 #Taille de la grille carrée.
maxEnergy = 200 #Energie max d'un Bob.
ticksPerDay = 100 #Nombre de Ticks par jour


################ CLASS BOB ######################

class Bob:
    """
    Define the class Bob
    Define size, speed, energy...
    Define functions...
    """
    def __init__(self) :
        self.type = "Bob"
        self.size = 1
        self.speed = 1
        self.energy = energyInitLevel
        self.memory = 0
        self.path = []
        self.perception = 0
        self.actionDone = False

    #FONCTIONS DU BOB : hunt, eat, partheno, fuck, randomMove.
    #parametre recu pour chaque fonction : La case dans laquelle se trouve le bob.

    """def hunt(self, mycase):
        if len(mycase.bobs)>1 :
            if 2/3*self.size>mycase.bobs[1].size:

        return False"""


############### CLASS CASE ######################

class Case:
    """
    Définit une case de la grille.
    Une case contient un tableau de Bobs et un niveau de Food.
    """
    def __init__(self):
        self.bobs=[]
        self.foodLevel=0


################### Grille ######################

# Dictionnaire Grille. Clé -> (x,y), contient un élément de type class Case.
#grid est une variable globale. PAS BESOIN DE LA PASSER EN PARAMETRE.
grid = {}


################## Fonctions ####################

def printGrid():
    """
    Affichage rapide du contenu du dictionnaire.
    Pas dans l'ordre... !
    """
    for cle, val in grid.items():
        print("Coord :",cle, "\t Nb Bobs :", len(val.bobs), "\tFood Level :", val.foodLevel)

def bobSpawn():
    """
    Fait apparaitre bobsQty bobs aléatoirement répartis sur la map.
    """
    for i in range(bobsQty):
        a = randint(0, gridSize-1)
        b = randint(0, gridSize-1)
        if (a,b) not in grid : grid[(a,b)]=Case()
        grid[(a,b)].bobs.append(Bob())

def foodSpawn():
    """
    Fait apparaitre FoodQty elements de Food aléatoirement répartis sur la map.
    """
    for j in range(foodQty):
        a = randint(0, gridSize-1)
        b = randint(0, gridSize-1)
        if (a,b) not in grid : grid[(a,b)]=Case()
        grid[(a,b)].foodLevel+=foodEnergy

def initialisation():
    """
    Sequence d'initialisation du jeu.
    """
    bobSpawn()
    foodSpawn()

def tick():
    """
    Fonction qui sollicite tous les bobs pour leur donner une action à réaliser
    Actions possibles par ordre de priorité : hunt, eat, fuck, randomMove.
    """
    bobcount = 0
    for key in grid:
        for i in range (len(grid[key].bobs)):
            bobcount +=1
            """
            #Choix d'une action :
            if grid[key].bobs[i].actionDone :
                continue #Passer au bob suivant.

            if not grid[key].bobs[i].hunt(grid[key]): #Hunt other bobs
                if not grid[key].bobs[i].eat(grid[key]): #Eat food
                    if not grid[key].bobs[i].fuck(grid[key]): #Fuck
                        if not grid[key].bobs[i].randomMove(grid[key]): #Move randomly
                            print("ERREUR : UN BOB N A PAS EFFECTUE SON ACTION !")
    return bobcount"""
    

############## Déroulement du jeu ###############
"""
initialisation()
for t in range (ticksPerDay):
    foodSpawn()
    bobcount = tick()
printGrid()
print("Il reste", bobcount, "Bobs en vie.")
"""

a=1
b=3
grid[(a,b)]=Case()
grid[(a,b)].bobs.append(Bob())
print(grid[(a,b)].bobs[0].energy)