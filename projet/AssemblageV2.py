
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

### Grille ###
gridSizeX = 100 #Taille de la grille sur l'axe X.
gridSizeY = 100 #Taille de la grille sur l'axe Y. 

### Ticks and game ###
ticksPerDay = 100 #Nombre de Ticks par jour
bobsQty = 1000 #quantité initiale de Bobs.
foodQty = 1000 #quantité d'items Food générés par jours

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
    Classe dédiée aux Bobs, ces petits personnages qui habitent notre monde et animent notre jeu.
    On définira ici toutes les caractéristiques des Bobs (les actions qu'ils peuvent réaliser, leurs attributs etc).
    
    Les Fonctions qui correspondent à des actions macroscopiques des bobs retournent True si le bob a réalisé
    l'action en question et False si les conditions pour réaliser l'action ne sont pas réunies,
    auquel cas le bob devra essayer une autre action.
    """
    def __init__(self, ID, coord) :
        self.ID = ID
        self.mass = randint(10, 30)
        self.velocity = 1
        self.energy = energyInitLevel
        self.memory = 0
        self.path = []
        self.perception = 0
        self.coord = coord #de la forme (x,y)

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
        Fonction utilisée pour supprimer correctement un bob décédé.
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
                if x < gridSizeX and x >= 0:
                    moved = True
            else :
                y += randint(1,2)*2-3 #aléatoirement +1 ou -1 à la coordonnée y
                if y < gridSizeY and y >= 0:
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
        if self.bobcount == 0 : self.isRunning=False
        if not self.isRunning : return
        print()
        print("DAY", self.dayCounter)
        self.foodSpawn()
        for _ in range (ticksPerDay):
            while self.isPaused == True : #Pause
                sleep(0.1)
                #afficher menu pause
                    #si reprise du jeu : afficher
            self.tick()
            self.gameView.Display()
            #sleep(0.1)


    def run_game(self):
        while self.isRunning :
            self.day()
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
        self.image = pygame.image.load("src/Tile32x32.png")
        self.rect = self.image.get_rect()
    def set_center(self, x, y):
        self.rect.center=(x,y)

class GraphicBob():
    def __init__(self):
        self.image = pygame.image.load("src/bob.png")
        self.image_blue = pygame.image.load("src/bob.blue.png")
        self.image_red = pygame.image.load("src/bob.rouge.png")
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.image_blue = pygame.transform.scale(self.image_blue, (10, 10))
        self.image_red = pygame.transform.scale(self.image_red, (10, 10))
    def image_scale(self, scale):
        self.image = pygame.transform.scale(self.image, (scale, scale))
        self.image_blue = pygame.transform.scale(self.image_blue, (scale, scale))
        self.image_red = pygame.transform.scale(self.image_red, (scale, scale))


class GraphicFood():
    def __init__(self):
        self.image = pygame.image.load("src/nourriture.png")
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
                self.screen.blit(pygame.transform.scale(self.GTile.image,self.zoom), self.isoCoordTable[(x,y)])


    def update_bobs(self):
        TILE_SIZE = 16*self.zoom
        BOB_SIZE = 10*self.zoom
        for key in self.Game.gridBob:
            for bob in self.Game.gridBob[key]:
                (x,y)=self.isoCoordTable[key] #coordonnées Top Left de la case
                x+=TILE_SIZE/2 #coordonnée centre de la case
                x+=BOB_SIZE/4 #Coordonnée top left du bob
                y+=TILE_SIZE/5 #coordonnée de la hauteur du bob.
                self.screen.blit(pygame.transform.scale_by(bob.image,self.zoom), (x,y))


    def update_food(self):
        TILE_SIZE = 16*self.zoom
        FOOD_SIZE = 13*self.zoom
        for key in self.Game.gridFood:
            (x,y)=self.isoCoordTable[key] #coordonnées Top Left de la case
            x+=TILE_SIZE/2 #coordonnée centre de la case
            x+=FOOD_SIZE/4 #Coordonnée top left de la food
            y+=TILE_SIZE/5 #coordonnée de la hauteur de la food.
            self.screen.blit(pygame.transform.scale_by(self.GFood.image,self.zoom), (x,y))


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
                self.screen.fill("WHITE")
                self.update_tiles()
                self.update_bobs()
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
