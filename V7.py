
# PYTHON PROJECT - STI - INSA CVL 2023/2024
# Titouan GODARD

from random import *
from time import *
from threading import Thread
import keyboard

################ VARIABLES ######################

### Grille ###
gridSizeX = 10 #Taille de la grille sur l'axe X.
gridSizeY = 10 #Taille de la grille sur l'axe Y. 

### Ticks and game ###
ticksPerDay = 100 #Nombre de Ticks par jour
bobsQty = 100 #quantité initiale de Bobs.
foodQty = 100 #quantité d'items Food générés par jours

### Energy ###
#Bob's energy
energyInitLevel = 100 #Niveau d'énergie initial des Bobs.
maxEnergy = 200 #Energie max d'un Bob.
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
    def __init__(self) :
        self.mass = randint(10, 30)
        self.speed = 1
        self.energy = energyInitLevel
        self.memory = 0
        self.path = []
        self.perception = 0
        self.actionDone = False

    #FONCTIONS DU BOB : hunt, eat, partheno, fuck, randomMove.
    #parametre recu pour chaque fonction : La case dans laquelle se trouve le bob.

    def partheno(self, key):
        print("Partheno")
        if self.energy==maxEnergy:
            self.energy -= parthenoMotherEnergy
            if key not in GameWorld.gridNextBob : GameWorld.gridNextBob[key]=[]
            GameWorld.gridNextBob[key].append(Bob())
            l=len(GameWorld.gridNextBob[key])
            GameWorld.gridNextBob[key][l-1].energy = birthParthenoEnergy
            GameWorld.gridNextBob[key][l-1].actionDone = True
            GameWorld.bobcount+=1
            print("birth from partheno")
    
    def consumeEnergy(self, key, score):
        """
        Fonction qui retire l'énergie consommée par le bob et vérifie qu'il soit toujours vivant.
        Return True si le bob est dead.
        Return False si le bob est toujours vivant après la consommation d'énergie.
        """
        print("Consume Energy")
        self.energy-= score
        if self.energy<=0: #Verifier si le bob a toujours de l'energie. Sinon il meurt.
            GameWorld.gridBob[key].remove(self) #suppression du bob du tableau. La clé et le dictionnaire ne sont pas supprimés.
            GameWorld.modifiedKeys.append(key)
            print("A Bob starved to death...")
            GameWorld.bobcount-=1
            return True #le bob is dead
        return False #le bob is alive

    def hunt(self, key):
        print("Hunt")
        for i in range (len(GameWorld.gridBob[key])):
            if GameWorld.gridBob[key][i].mass < 2/3*self.mass:
                if self.consumeEnergy(key, tickStaticEnergy): return True #le bob is dead
                #EAT THE BOB
                energyToEat = 1/2 * GameWorld.gridBob[key][i].energy * (1-GameWorld.gridBob[key][i].mass/self.mass)
                if self.energy+energyToEat <= maxEnergy :
                    self.energy+=energyToEat
                else :
                    self.energy = maxEnergy
                    #On ne laisse pas de reste d'énergie dans la case.
                del GameWorld.gridBob[key][i] #Je peux supprimer ce bob car la taille du dictionnaire ne sera pas modifiée.
                #attention, je ne supprime pas la clé du dictionnaire mais seulement le bob qui est contenu dans le tableau qui est associé à la clé.
                GameWorld.modifiedKeys.append(key)
                GameWorld.bobcount-=1
                print("1 bob murdered")
                self.actionDone = True
                return True
        return False

    def fuck(self, key):
        print("Fuck")
        for i in range (len(GameWorld.gridBob[key])):
            if GameWorld.gridBob[key][i].mass >= 2/3*self.mass and GameWorld.gridBob[key][i]!=self and self.mass and self.energy >= parentEnergyRequired and GameWorld.gridBob[key][i].energy >= parentEnergyRequired and GameWorld.gridBob[key][i].actionDone == False and self.actionDone == False:
                GameWorld.gridBob[key][i].actionDone=True
                GameWorld.gridBob[key].append(Bob()) #ici on n'utilise pas de dictionnaire gridNextBob car la case est déja existante dans gridBob. Ainsi on ne modifie pas la taille du dictionnaire gridBob.
                GameWorld.bobcount+=1
                l=len(GameWorld.gridBob[key])
                GameWorld.gridBob[key][l-1].energy = birthSexEnergy
                GameWorld.gridBob[key][l-1].actionDone = True
                GameWorld.gridBob[key][i].consumeEnergy(key, sexEnergy+tickStaticEnergy)
                self.consumeEnergy(key, sexEnergy+tickStaticEnergy)
                print("birth from sex")
                self.actionDone = True
                return True
        return False

    def eat(self, key):
        print("Eat")
        if key not in GameWorld.gridFood or self.energy==maxEnergy : return False
        if self.consumeEnergy(key, tickStaticEnergy): return True #le bob is dead
        if self.energy + GameWorld.gridFood[key] <= maxEnergy :
            energyToEat = GameWorld.gridFood[key]
            del GameWorld.gridFood[key]
        else : 
            energyToEat = maxEnergy-self.energy
            GameWorld.gridFood[key]-=energyToEat
        print("Eat food grrrr")
        self.energy += energyToEat
        self.partheno(key)
        self.actionDone = True
        return True

    def randomMove(self, key):
        print("Move")
        if self.consumeEnergy(key, tickMobileEnergy): return #le bob is dead
        moved=False
        mvcount = 0
        while moved==False : #tant qu'on a pas effectué un déplacement, on cherche un déplacement valide.
            if mvcount > 10 : return False #Au bout de 10 tentatives on abandonne et on considère que le déplacement est impossible. 
            mvcount+=1
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
        GameWorld.modifiedKeys.append(key)
        self.actionDone = True
        print("I move fast hihi")
        return True


################### Grille ######################

# Dictionnaire Grille. Clé -> (x,y), contient un élément de type class Case.
#grid est une variable globale. PAS BESOIN DE LA PASSER EN PARAMETRE.

class World():
    def __init__(self) :
        self.pause = True #pour mettre sur pause le jeu
        self.gridBob = {}
        self.gridNextBob = {}
        self.gridFood = {}
        self.bobSpawn()
        self.printGridBob()
        self.printGridFood()
        self.bobcount=bobsQty
        self.modifiedKeys=[] #keys that might not contain any bob at the end of a tick.

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
        for key in self.modifiedKeys :
            if len(self.gridBob[key])==0: del self.gridBob[key]
        self.modifiedKeys.clear()
        return

    def mergeGrids(self): #fusionne le dictionnaire gridNextBob (qui représente les bobs qui viennent de se déplacer) dans le dictionnaire gridBobs
        for key in self.gridNextBob:
            if key not in self.gridBob : self.gridBob[key]=[]
            for bob in self.gridNextBob[key] : self.gridBob[key].append(bob)
        self.gridNextBob.clear()
        return
    
    def save(self): #enregistre le jeu actuel dans le document jeu.data
        parameters=str()


    def tick(self):
        """
        Fonction qui sollicite tous les bobs pour leur donner une action à réaliser
        Actions possibles par ordre de priorité : eat, hunt, fuck, randomMove.
        """
        for key in self.gridBob:
            for bob in self.gridBob[key]:
                print("***********BOB************")
                #Choix d'une action :
                #sleep(0.1)
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
        #sleep(0.5)
        return
    
    def day(self):
        if GameWorld.bobcount!=0 :
            print("\n**********************************\n\t******** DAY ********\n**********************************\n")
            GameWorld.foodSpawn()
            for t in range (ticksPerDay):
                while GameWorld.pause == True : sleep(0.1)
                print("****************************\n\t\ttick !\n****************************\n")
                GameWorld.tick()
                #printGridBob()

    def play(self, NbDay):
        for i in range (NbDay) :
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

NbDay = 10
GAME = Thread(target=GameWorld.play, args=[NbDay])
#PAUSE = Thread(target=GameWorld.pauseGame, args=[]) 

GAME.start()
#PAUSE.start()

#sleep(1)
GameWorld.pause=False
GAME.join()

#PAUSE.run()

#while GAME.is_alive():
#    sleep(0.1)
#print("done")

#printGridBob()
#printGridFood()
print("Il reste", GameWorld.bobcount, "Bobs en vie.")
#printGridFood()