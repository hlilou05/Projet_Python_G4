
# PYTHON PROJECT - STI - INSA CVL 2023/2024
# Titouan GODARD

from random import *

################ VARIABLES ######################

bobsQty = 50 #quantité initiale de Bobs.
foodQty = 5 #quantité d'items Food sur la map générés au départ et par jour de jeu.
foodEnergy = 20 #quantité d'énergie d'un item de food généré sur la map.
energyInitLevel = 100 #Niveau d'énergie initial des Bobs.
gridSize = 10 #Taille de la grille carrée.
maxEnergy = 200 #Energie max d'un Bob.
birthEnergy = 50
motherEnergy = 150
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
        self.size = randint(10, 20)
        self.speed = 1
        self.energy = energyInitLevel
        self.memory = 0
        self.path = []
        self.perception = 0
        self.actionDone = False

    #FONCTIONS DU BOB : hunt, eat, partheno, fuck, randomMove.
    #parametre recu pour chaque fonction : La case dans laquelle se trouve le bob.

    def partheno(self, key):
        if self.energy>maxEnergy:
            self.energy -= motherEnergy
            if key not in gridNextBob : gridNextBob[key]=[]
            gridNextBob[key].append(Bob())
            l=len(gridNextBob[key])
            gridNextBob[key][l-1].energy = birthEnergy
            print("birth")


    def hunt(self, key): #OK !
        if len(gridBob[key])>1:
            for i in range (len(gridBob[key])):
                if gridBob[key][i].size<2/3*self.size:
                    #EAT THE BOB
                    self.energy += gridBob[key][i].energy
                    del gridBob[key][i] #Je peux supprimer ce bob car la taille du dictionnaire ne sera pas modifiée.
                    self.partheno(key)
                    return True
        return False


    def fuck(self, key): #MARTIN
        return False


    def eat(self, key): #MARTIN
        return False


    def randomMove(self, key): #TITOUAN
        moved=False
        while moved==False:
            (x,y)=key
            if randint(0,1) : #choix random vertical ou horizontal.
                x+=randint(1,2)*2-3 #aléatoirement +1 ou -1 à la coordonnée x
                if x<=gridSize-1 and x>=0:
                    moved = True
            else :
                y+=randint(1,2)*2-3 #aléatoirement +1 ou -1 à la coordonnée y
                if y<=gridSize-1 and y>=0:
                    moved = True

        if (x,y) not in gridNextBob : gridNextBob[(x,y)]=[]
        gridNextBob[(x,y)].append(self)
        gridBob[key].remove(self)
        return True



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

gridBob = {}
gridNextBob = {}
gridFood = {}


################## Fonctions ####################

def printGridBob():
    """
    Affichage rapide du contenu des dictionnaires.
    Pas dans l'ordre... !
    """
    for cle, val in gridBob.items():
        print("Coord :",cle, "\t Nb Bobs :", len(val))


def printGridFood():
    """
    Affichage rapide du contenu des dictionnaires.
    Pas dans l'ordre... !
    """
    for cle, val in gridFood.items():
        print("Coord :",cle, "\tFood Level :", val)
    

def bobSpawn():
    """
    Fait apparaitre bobsQty bobs aléatoirement répartis sur la map.
    """
    for i in range(bobsQty):
        a = randint(0, gridSize-1)
        b = randint(0, gridSize-1)
        if (a,b) not in gridBob : gridBob[(a,b)]=[]
        gridBob[(a,b)].append(Bob())


def foodSpawn():
    """
    Fait apparaitre FoodQty elements de Food aléatoirement répartis sur la map.
    """
    for j in range(foodQty):
        a = randint(0, gridSize-1)
        b = randint(0, gridSize-1)
        if (a,b) not in gridFood : gridFood[(a,b)]=0
        gridFood[(a,b)]+=foodEnergy


def initialisation():
    """
    Sequence d'initialisation du jeu.
    """
    bobSpawn()
    foodSpawn()
    printGridBob()
    printGridFood()


def removeDeadBoddies():
    keysToRemove = []
    for key, bobs in gridBob.items():
        if len(bobs)==0 : keysToRemove.append(key)
    for key in keysToRemove :
        del gridBob[key]



def mergeGrids():
    for key in gridNextBob:
        if key not in gridBob : gridBob[key]=[]
        gridBob[key]=gridNextBob[key]


def tick():
    """
    Fonction qui sollicite tous les bobs pour leur donner une action à réaliser
    Actions possibles par ordre de priorité : eat, hunt, fuck, randomMove.
    """
    bobcount = 0
    for key in gridBob:
        for bob in gridBob[key]:
            bobcount +=1
            
            #Choix d'une action :
            if bob.actionDone :
                continue #Passer au bob suivant.

            if not bob.eat(key): #Eat food
                if not bob.hunt(key): #Hunt other bobs
                    if not bob.fuck(key): #Fuck
                        if not bob.randomMove(key): #Move randomly
                            print("ERREUR : UN BOB N A PAS EFFECTUE SON ACTION !")
    removeDeadBoddies()
    mergeGrids()
    gridNextBob.clear()
    return bobcount
    

############## Déroulement du jeu ###############

initialisation()
foodSpawn()
for i in range (1) :
    foodSpawn()
    for t in range (ticksPerDay):
        print("TICK")
        bobcount = tick()
        printGridBob()

#printGridBob()
#printGridFood()
print("Il reste", bobcount, "Bobs en vie.")