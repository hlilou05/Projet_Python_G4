
# PYTHON PROJECT - STI - INSA CVL 2023/2024
# Titouan GODARD

from random import *
from time import *

################ VARIABLES ######################

bobsQty = 100 #quantité initiale de Bobs.
foodQty = 100 #quantité d'items Food sur la map générés au départ et par jour de jeu.
foodEnergy = 20 #quantité d'énergie d'un item de food généré sur la map.
energyInitLevel = 100 #Niveau d'énergie initial des Bobs.
gridSizeX = 100 #Taille de la grille sur l'axe X.
gridSizeY = 100 #Taille de la grille sur l'axe Y.
maxEnergy = 200 #Energie max d'un Bob.
birthParthenoEnergy = 50 #Energie d'un nouveau bob né par partheno
motherEnergy = 150 #Energie consommée pour produire un bob par partheno
parentEnergyRequired = 150 #Energie nécessaire pour commencer la reproduction sexuelle.
birthSexEnergy = 100 #Energie d'un bob né par reproduction sexuelle
SexEnergy = 100 #energie consommée pour produire un bob par reproduction sexuelle
ticksPerDay = 100 #Nombre de Ticks par jour
tickStaticEnergy = 0.5 #energie consommée par tick en restant static
tickMobileEnergy = 1 #energie consommée par tick en étant mobile



################ CLASS BOB ######################

class Bob:
    """
    Define the class Bob
    Define size, speed, energy...
    Define functions...
    """
    def __init__(self) :
        self.type = "Bob"
        self.mass = 10#randint(10, 20)
        self.speed = 1
        self.energy = energyInitLevel
        self.memory = 0
        self.path = []
        self.perception = 0
        self.actionDone = False

    #FONCTIONS DU BOB : hunt, eat, partheno, fuck, randomMove.
    #parametre recu pour chaque fonction : La case dans laquelle se trouve le bob.

    def partheno(self, key):
        if self.energy==maxEnergy:
            self.energy -= motherEnergy
            if key not in GameWorld.gridNextBob : GameWorld.gridNextBob[key]=[]
            GameWorld.gridNextBob[key].append(Bob())
            l=len(GameWorld.gridNextBob[key])
            GameWorld.gridNextBob[key][l-1].energy = birthParthenoEnergy
            print("birth from partheno")

    def energyControl(self, key): #if the bob can eat more than his max energy, he leaves some food on the ground and bottoms out at the max lever of energy.
        if self.energy>maxEnergy: #on regarde si le bob a atteint son niveau d'énergie max. Si il a trop mangé, il recrache le supplément et reste au niveau maximal. Le supplément revient dans la case ou se situe le bob.
            if key not in GameWorld.gridFood : GameWorld.gridFood[key]=0
            GameWorld.gridFood[key]+=self.energy-maxEnergy
            self.energy=maxEnergy
            print("A bob has reach his max level of energy")
            self.partheno(key)
        elif key in GameWorld.gridFood : #si l'énergie ne dépasse pas le max et qu'il existe de l'énergie (égale à 0 si tout fonctionne) dans la case de coordonnée key, on supprime la case key du dictionnaire gridFood.
            del GameWorld.gridFood[key]
    
    def consumeEnergy(self, key, score):
        """
        Fonction qui retire l'énergie consommée par le bob et vérifie qu'il soit toujours vivant.
        Return True si le bob est dead.
        Return False si le bob est toujours vivant après la consommation d'énergie.
        """
        self.energy-= score
        if self.energy<=0: #Verifier si le bob a toujours de l'energie. Sinon il meurt.
            GameWorld.gridBob[key].remove(self)
            print("A Bob starved to death...")
            return True
        return False


    def hunt(self, key): #TITOUAN
        if self.consumeEnergy(key, tickStaticEnergy): return True
        for i in range (len(GameWorld.gridBob[key])):
            if GameWorld.gridBob[key][i].mass < 2/3*self.mass:
                #EAT THE BOB
                self.energy += 1/2 * GameWorld.gridBob[key][i].energy * (1-GameWorld.gridBob[key][i].mass/self.mass)
                self.energyControl(key)
                del GameWorld.gridBob[key][i] #Je peux supprimer ce bob car la taille du dictionnaire ne sera pas modifiée.
                print("1 bob murdered")
                return True
        return False


    def fuck(self, key): #TITOUAN
        for i in range (len(GameWorld.gridBob[key])):
            if GameWorld.gridBob[key][i].mass >= 2/3*self.mass and GameWorld.gridBob[key][i]!=self and self.mass and self.energy >= parentEnergyRequired and GameWorld.gridBob[key][i].energy >= parentEnergyRequired and GameWorld.gridBob[key][i].actionDone == False and self.actionDone == False:
                GameWorld.gridBob[key][i].actionDone=True
                self.actionDone=True
                GameWorld.gridBob[key].append(Bob()) #ici on n'utilise pas de dictionnaire gridNextBob car la case est déja existante dans gridBob. Ainsi on ne modifie pas la taille du dictionnaire gridBob.
                l=len(GameWorld.gridBob[key])
                GameWorld.gridBob[key][l-1].energy = birthSexEnergy
                GameWorld.gridBob[key][i].consumeEnergy(key, SexEnergy+tickStaticEnergy)
                self.consumeEnergy(key, SexEnergy+tickStaticEnergy)
                print("birth from sex")
                return True
        return False


    def eat(self, key): #TITOUAN
        if self.consumeEnergy(key, tickStaticEnergy): return True
        if key not in GameWorld.gridFood or self.energy==maxEnergy : return False
        self.energy += GameWorld.gridFood[key]
        self.energyControl(key)
        print("Eat food grrrr")
        return True



    def randomMove(self, key): #TITOUAN
        if self.consumeEnergy(key, tickMobileEnergy): return

        moved=False
        while moved==False: #tant qu'on a pas effectué un déplacement, on cherche un déplacement valide.
            (x,y)=key
            if randint(0,1) : #choix random vertical ou horizontal.
                x+=randint(1,2)*2-3 #aléatoirement +1 ou -1 à la coordonnée x
                if x<=gridSizeX-1 and x>=0:
                    moved = True
            else :
                y+=randint(1,2)*2-3 #aléatoirement +1 ou -1 à la coordonnée y
                if y<=gridSizeY-1 and y>=0:
                    moved = True

        #on applique le déplacement valide trouvé auparavant.
        # ici on utilise un deuxième dictionnaire gridNextBob car on ne peut pas rallonger le dictionnaire gridBob pendant qu'on le parcours dans la fonction tick().
        if (x,y) not in GameWorld.gridNextBob : GameWorld.gridNextBob[(x,y)]=[]
        GameWorld.gridNextBob[(x,y)].append(self)
        GameWorld.gridBob[key].remove(self)
        return


################### Grille ######################

# Dictionnaire Grille. Clé -> (x,y), contient un élément de type class Case.
#grid est une variable globale. PAS BESOIN DE LA PASSER EN PARAMETRE.

class World():
    def __init__(self) :
        self.gridBob = {}
        self.gridNextBob = {}
        self.gridFood = {}
        self.bobSpawn()
        self.printGridBob()
        self.printGridFood()

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
        for i in range(bobsQty):
            x = randint(0, gridSizeX-1)
            y = randint(0, gridSizeY-1)
            if (x, y) not in self.gridBob : self.gridBob[(x, y)]=[]
            self.gridBob[(x, y)].append(Bob())
        return

    def foodSpawn(self):
        """
        Fait apparaitre FoodQty elements de Food aléatoirement répartis sur la map.
        """
        for j in range(foodQty):
            x = randint(0, gridSizeX-1)
            y = randint(0, gridSizeY-1)
            if (x, y) not in self.gridFood : self.gridFood[(x, y)]=0
            self.gridFood[(x, y)]+=foodEnergy
        return

    def removeDeadBoddies(self): #remove the empty bob arrays in the dictionnary gridBob.
        keysToRemove = []
        for key, bobs in self.gridBob.items():
            if len(bobs)==0 : keysToRemove.append(key)
        for key in keysToRemove :
            del self.gridBob[key]
        return

    def mergeGrids(self): #fusionne le dictionnaire gridNextBob (qui représente les bobs qui viennent de se déplacer) dans le dictionnaire gridBobs
        for key in self.gridNextBob:
            if key not in self.gridBob : self.gridBob[key]=[]
            for bob in self.gridNextBob[key] : self.gridBob[key].append(bob)
        self.gridNextBob.clear()
        return

    def howManyBobs(self):
        """
        Return the number of bobs alive in the game.
        """
        bobcount = 0
        for key, bobs in self.gridBob.items():
            bobcount+=len(bobs)
        return bobcount

    def tick(self):
        """
        Fonction qui sollicite tous les bobs pour leur donner une action à réaliser
        Actions possibles par ordre de priorité : eat, hunt, fuck, randomMove.
        """
        for key in self.gridBob:
            for bob in self.gridBob[key]:
                #Choix d'une action :
                if bob.actionDone :
                    continue #Passer au bob suivant.
                if not bob.eat(key): #Eat food
                    if not bob.hunt(key): #Hunt other bobs
                        if not bob.fuck(key): #Fuck
                            bob.randomMove(key) #Move randomly
        self.removeDeadBoddies()
        self.mergeGrids()
        for key, bobs in self.gridBob.items():
            for bob in bobs:
                bob.actionDone = False
        sleep(0.5)
        return
    
    def day(self):
        if GameWorld.howManyBobs()!=0 :
            print("\n\t******** DAY ********\n")
            GameWorld.foodSpawn()
            for t in range (ticksPerDay):
                print("\t\ttick !")
                GameWorld.tick()
                #printGridBob()



############## Déroulement du jeu ###############

GameWorld = World()
for i in range (1) :
    GameWorld.day()

#printGridBob()
#printGridFood()
print("Il reste", GameWorld.howManyBobs(), "Bobs en vie.")
#printGridFood()