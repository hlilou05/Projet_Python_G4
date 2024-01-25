from random import *
from Constant import *

class Bob:
    """
    Define the class Bob
    Define size, speed, energy...
    Define functions...
    """
    def __init__(self, jeu, ID, coord) :
        self.jeu
        self.ID = ID
        self.mass = randint(10, 30)
        self.velocity = 1
        self.energy = energyInitLevel
        self.memory = 0
        self.path = []
        self.remembering_food = False
        self.perception = 0
        self.coord = coord
        self.seen = {"Bob+": {}, "Bob-": {}, "Food": {}}
        self.fuite = False
        self.bufvelo = 0.00


    #FONCTIONS DU BOB : hunt, eat, partheno, fuck, randomMove.
    #parametre recu pour chaque fonction : La case dans laquelle se trouve le bob.

    def partheno(self):
        """
        Fonction de reproduction d'un bob individuellement lorsqu'il a atteint l'énergie maximale.
        """
        self.gamePrint("Function : Partheno")
        if self.energy==maxEnergy:
            self.consumeEnergy(parthenoMotherEnergy)
            babyBob = Bob(self.lastID+1, self.coord)
            babyBob.energy = birthParthenoEnergy
            self.gridBob[self.coord].append(babyBob)
            self.gamePrint("birth from partheno. End of the function")
    
    def consumeEnergy(self, score):
        """
        Fonction qui retire l'énergie consommée par le bob et vérifie qu'il soit toujours vivant.
        Return True si le bob est dead.
        Return False si le bob est toujours vivant après la consommation d'énergie.
        """
        self.gamePrint("\tFunction : ConsumeEnergy")
        self.energy -= score
        if self.energy<=0: #Verifier si le bob a toujours de l'energie. Sinon il meurt.
            self.die()
            return True #le bob is dead...
        return False #le bob is alive !
    
    def die(self):
        """
        Fonction utilisée pour supprimer correctement un bob dcédé.
        """
        self.jeu.gridBob[self.coord].remove(self) #suppression du bob du tableau associé à ses coordonnées dans le dictionnaire gridBob.
        if self in self.jeu.bobArray : self.jeu.bobArray.remove(self) #Retirer le bob du tableau bobArray qui contient les bobs qui doivent jouer leur coup au tick présent. 
        if len(self.jeu.gridBob[self.coord])==0: del(self.jeu.gridBob[self.coord]) #Si le tableau est vide, alors on supprime la case du dictionnaire.
        return

    def hunt(self):
        """
        Fonction qui représente l'action d'un bob qui mange un autre bob.
        """
        self.gamePrint("Function : Hunt")
        for prey in self.gridBob[self.coord]:
            if prey.mass < 2/3*self.mass:
                #On a trouvé un bob que l'on peut manger !
                if self.consumeEnergy(tickStaticEnergy): return True #le bob is dead
                #EAT THE BOB
                energyToEat = 1/2 * prey.energy * (1-prey.mass/self.mass)
                if self.energy+energyToEat <= maxEnergy : self.energy+=energyToEat
                else : self.energy = maxEnergy # A VERIFIER DANS LES REGLES !!!!!!!!!!!!!!!!
                prey.die() #Le bob mangé meurt...
                self.gamePrint("A bob was murdered. End of the function.")
                return True
        return False

    def fuck(self):
        """
        Fonction de reproduction sexuelle entre 2 bobs.
        """
        self.gamePrint("Function : Fuck")
        for myLover in self.gridBob[self.coord] :
            if myLover.mass >= 2/3*self.mass and self.energy >= parentEnergyRequired and myLover.energy >= parentEnergyRequired and myLover in self.bobArray :
            #SI le rapport des masses est bon & si l'énergie des deux bobs est supérieur au seuil nécessaire pour la reproduction sexuelle et si le partenaire n'a pas déja effectué une action pendant ce tick.    
                babyBob=Bob(self.lastID+1, self.coord)
                babyBob.energy=birthSexEnergy
                self.gridBob[self.coord].append(babyBob)
                self.bobArray.remove(myLover)
                myLover.consumeEnergy(sexEnergy+tickStaticEnergy)
                self.consumeEnergy(sexEnergy+tickStaticEnergy)
                self.gamePrint("birth from sex")
                return True
        return False

    def eat(self):
        """
        Fonction qui effectue l'action pour un bob de manger un item de Food présent sur la grille à la même position
        """
        self.gamePrint("Function : Eat")
        if self.coord not in self.gridFood or self.energy == maxEnergy : return False
        if self.consumeEnergy(tickStaticEnergy): return True #le bob is dead
        if self.energy + self.gridFood[self.coord] <= maxEnergy :
            energyToEat = self.gridFood[self.coord]
            del self.gridFood[self.coord]
        else : 
            energyToEat = maxEnergy-self.energy
            self.gridFood[self.coord] -= energyToEat
            self.energy += energyToEat
            self.partheno()
        self.gamePrint("grrrr... End of the function.")
        return True


    # for i in range(-self.Bp, self.Bp  + 1):
    #        for j in range(- (self.Bp - abs(i)) ,self.Bp - abs(i) + 1):
    def distance(x, y, i, j):
        dist = abs(i - x) + abs(j - y)
        return dist

    def escape(self):
        # Evaluate best place to go #
        scores = {}
        score = 0
        (a, b) = self.coord
        for i in range(-int(self.velocity) + a, int(self.velocity) + 1 + a):
            for j in range(-int(self.velocity) - abs(i) + b, int(self.velocity) - abs(i) + 1 + b):
                if(i > 0 and i < gridSizeX and j > 0 and j < gridSizeY):
                    for (x, y) in self.Seen["Bob+"].keys():
                        score += self.distance(i, j, x, y)    
                    scores.update({(i,j): score})
                    score = 0
        return max(scores, keys=scores.get)


    def move_towards_food(self):
        (i, j) = self.coord
        (x, y) = self.remembered_food[0]
        if (x,y):
            distance_to_food = self.distance(i, j, x, y)
            
            if distance_to_food < int(self.velocity):
                return (x, y)
            
            else:
                dir_x = (x - i) / distance_to_food
                dir_y = (y - j) / distance_to_food

                i += int(dir_x * self.velocity)
                j += int(dir_y * self.velocity)
        return (i, j)


    def random_move(self):

        # Random move using memory and velocity #
        # Bob will move v tiles and won't go back #
        
        (x, y) = self.coord
        MoveOk = False
        while not MoveOk:
            if randint(0,1):
                move_x = randint(max(0, x - int(self.velocity)), min(gridSizeX, x - int(self.velocity)))
                move_y = randint(max(0, y - (int(self.velocity) - abs(move_x - x)), min(gridSizeY, y - (int(self.velocity) - abs(move_x - x)))))
            else:
                move_y = randint(max(0, y - int(self.velocity), min(gridSizeY, y - int(self.velocity))))
                move_x = randint(max(0, x - (int(self.velocity)  - abs(move_y - y))), min(gridSizeX, x - (int(self.velocity)  - abs(move_y - y))))
                if (move_x, move_y) not in self.path :
                    MoveOk = True

        return (move_x, move_y)
        
        #Function perception to get all elements around
    def perception(self):
        (x, y) = self.coord
        self.seen.drop.values()
        for i in range(-self.perception, self.perception  + 1):
            for j in range(- (self.perception - abs(i)) ,self.perception - abs(i) + 1):
                if((x + i, y + j) in self.jeu.gridFood.key()):
                    self.seen["Food"].append((x + i, y + j), self.jeu.gridFood[(x + i, y + j)])
                elif((x + i, y + j) in self.jeu.gridBob.key()):
                    if(self.jeu.gridBob.key[x + i, y + j].mass/self.mass > SeuilPredator ):
                        self.seen["Bob+"].append((x + i, y + j), self.jeu.gridFood[(x + i, y + j)])
                        self.fuite = 1
                    else:
                        self.seen["Bob-"].append((x + i, y + j), self.jeu.gridFood[(x + i, y + j)])
        return
    

    def move(self) :
        # Condition and verification #

        ####### REPRENDRE POUR ENLEVER LES CODES MULTIPLES ########
        ####### AJOUTER BUFFER VELO ########
        key = self.coord
        ## Fuite ##
        if self.fuite == 1 :
            (x,y) = self.escape(self)
            if (x,y) not in self.jeu.gridBob : self.jeu.gridBob[(x,y)]=[]
            self.jeu.gridBob[(x,y)].append(self) #On ajoute le bob dans le dictionnaire à sa nouvelle position.
            self.jeu.gridBob[key].remove(self) #on retire le bob de son ancienne position.
            self.coord = (x,y)
            if len(self.jeu.gridBob[key])==0: del(self.jeu.gridBob[key])
            return 0
        ## Eat ##
            ### Vision ###
                #### food ####
                #### bob- ####
            ### Mémoire ###
                #### Tout droit ####
        if self.remembering_food :
            (x, y) = self.move_towards_food(self, key)
            if (x,y) not in self.jeu.gridBob : self.jeu.gridBob[(x,y)]=[]
            self.jeu.gridBob[(x,y)].append(self) #On ajoute le bob dans le dictionnaire à sa nouvelle position.
            self.jeu.gridBob[key].remove(self) #on retire le bob de son ancienne position.        self.coord = (x,y)
            if len(self.jeu.gridBob[key])==0: del(self.jeu.gridBob[key])
            return 0
        ## Random move ##
        (x, y) = self.random_move(self, key)
        self.coord = (x, y)
        
        return 0