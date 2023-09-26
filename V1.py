# PYTHON PROJECT - STI - INSA CVL 2023
# Titouan GODARD

from random import *

bobsQty = 10 #quantité initiale de Bobs.
foodQty = 5 #quantité d'items Food sur la map générés à chaque tour.
energyInitLevel = 100 #Niveau d'énergie initial des Bobs.
gridSize = 10 #Taille de la grille carrée.
maxEnergy = 200

################ CLASS BOB ######################

class Bob:
    """Define the class Bob
    Define size, speed, energy...
    Define functions eat(), move(), hunt()
    The Bob position will be stored directly in the grid[][]"""
    def __init__(self) :
        self.type="Bob"
        self.size= 1 #(randint(5, 10) + randint(5, 10))/2
        self.speed=1
        self.energy=energyInitLevel
        self.memory=0
        self.path=[]
        self.perception=0
            

############### CLASS CASE #######################

class Case:
    """Define the class Grid"""
    def __init__(self):
        self.bobs=[]
        self.foodLevel=0
    #def hunt()
    #def sex()
    #def partheno()

############### CLASS GRID #######################

class Grid:
    """Define the class Grid"""
    def __init__(self):
        self.grid = [[Case()] * gridSize] * gridSize
        for i in range(bobsQty):
            self.grid[randint(0, gridSize-1)][randint(0, gridSize-1)].bobs.append(Bob())
        for j in range(foodQty):
            self.grid[randint(0, gridSize-1)][randint(0, gridSize-1)].foodLevel+=100

############## FUNCTIONS ########################

def gridInit():
    """Initialise the Grid with bobs and foods items randomly placed"""
    gameGrid=Grid()
    return gameGrid

"""
def printGrid(gameGrid):
    for raw in range(gridSize):
        print (gameGrid.grid[raw])
"""

def printGrid():
    for raw in range (gridSize):
        t=[]
        for col in range (gridSize):
            x=0
            for bob in (gameGrid.grid[raw][col].bobs):
                x=x+1
            t.append(x)
        print(t)


gameGrid = gridInit()
printGrid()

"""
def main():
    #initialisation
    while #test si il y a toujours des bobs en vie :
        
        
"""

def eatAndHunt():
    """If a bob is at the same place as a food item, it eats the food.
    If two bobs are at the same place, the bigger eats the smaller."""
    for raw in range(gridSize):
        for col in range(gridSize):
            for x in grid[raw][col]:
                for y in grid[raw][col]: #pour toute paire d'élément dans la cellule
                    if (x.type=="Bob" and y.type=="Food"): #cas où il y a un Bob et un Food
                        """Bob eat the Food"""
                        x.energy = x.energy + y.energy
                        del y
                    elif (x.type=="Bob" and y.type=="Bob" and x.size>=1.5*y.size): #cas où il y a deux Bobs
                        """Bob eat the other Bob"""
                        x.energy = x.energy + y.energy
                        del y






"""

def bobsSizeRepartition():
    (cat5,cat6,cat7,cat8,cat9) = (0,0,0,0,0)
    for i in range(100000):
        b=Bob()
        if (b.size<6): cat5=cat5+1
        elif (b.size<7): cat6=cat6+1
        elif (b.size<8): cat7=cat7+1
        elif (b.size<9): cat8=cat8+1
        else : cat9=cat9+1
    print ("cat5 :", cat5/bobsQty)
    print ("cat6 :", cat6/bobsQty)
    print ("cat7 :", cat7/bobsQty)
    print ("cat8 :", cat8/bobsQty)
    print ("cat9 :", cat9/bobsQty)
    print ("cat10 :", cat10/bobsQty)


    """