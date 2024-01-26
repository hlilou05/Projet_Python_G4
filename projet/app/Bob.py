from random import *
from Constant import *
from GUI import *


class GraphicBob(GUI):
    def __init__(self, game, bob):
        super().__init__(game)
        self.bob = bob

        # setup UI elements
        self.frame = Frame(self, 0, 0, 250, 300, (64, 64, 64))
        self.entity = Text(self, 10, 10, text="Bob")

        self.energy = Text(self, 10, 50, text="Energy: 100", fontSize=20)
        self.velocity = Text(self, 10, 80, text="Velocity: 1.6", fontSize=20)
        self.mass = Text(self, 10, 110, text="Mass: 10", fontSize=20)
        self.perception = Text(self, 10, 140, text="Perception: 3", fontSize=20)

        self.visible = False

    def update(self):
        if self.visible:
            if self.game.affichage:
                self.visible = False
        mx, my = pygame.mouse.get_pos()
        if not pygame.Rect(mx-50, my-50, 100, 10).colliderect(self.bob.rect):
            self.visible = False

        self.set_position(self.bob.get_position()[0], self.bob.get_position()[1])

        self.draw_element(self.frame)
        self.draw_element(self.entity)

        self.energy.set_text(f"Energy: {int(self.bob.energy)}/{self.bob.maxEnergy}")
        self.velocity.set_text(f"Velocity: {self.bob.velocity}")
        self.mass.set_text(f"Mass: {self.bob.mass}")
        self.perception.set_text(f"Perception: {self.bob.perception}")
        self.draw_element(self.velocity)
        self.draw_element(self.mass)
        self.draw_element(self.energy)
        self.draw_element(self.perception)




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
        self.perception = InitPerception
        self.coord = coord
        self.seen = {}
        self.fuite = False
        self.bufvelo = 0.00
        self.image = assets["bob"]
        self.gui = GraphicBob(self.game, self)
        self.game.add_gui(self.gui)

    #FONCTIONS DU BOB : hunt, eat, partheno, fuck, Move.
        

    def choose_image(self):
        
        self.image = assets["bob"]

        if self.velocity >= 1.2 and self.velocity < 1.6:
            self.image = assets["bob.blue"]
        elif self.velocity > 2 :
            self.image = assets["bob.rouge"]



        
    def Val_Mutation(TauxMut, Val):
        return (random.uniform(Val*(1-TauxMut), Val*(1+TauxMut)))

    def partheno(self):
        if not Parthenogenesis : return False
        """
        Fonction de reproduction d'un bob individuellement lorsqu'il a atteint l'énergie maximale.
        """
        if self.energy==maxEnergy:
            babyBob = Bob(self.jeu, self.lastID+1, self.coord)
            
            babyBob.energy = birthParthenoEnergy
            babyBob.mass = self.Val_Mutation(TauxMutationMass, self.mass)
            babyBob.velocity = self.Val_Mutation(TauxMutationVelocity, self.velocity)
            babyBob.memory = self.Val_Mutation(TauxMutationMemory, self.memory)
            babyBob.perception = self.Val_Mutation(TauxMutationPerception, self.perception)

            self.jeu.gridBob[self.coord].append(babyBob)
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
        return

    def hunt(self):
        if not Hunt : return False
        """
        Fonction qui représente l'action d'un bob qui mange un autre bob.
        """
        for prey in self.gridBob[self.coord]:
            if prey.mass / self.mass <= SeuilPredator :
                #On a trouvé un bob que l'on peut manger !
                #EAT THE BOB
                energyToEat = 1/2 * prey.energy * (1-prey.mass/self.mass)
                if self.energy+energyToEat <= maxEnergy : self.energy+=energyToEat
                else : self.energy = maxEnergy
                prey.die() #Le bob mangé meurt...
                return True
        return False

    def fuck(self):
        if not Reproduction : return False
        """
        Fonction de reproduction sexuelle entre 2 bobs.
        """
        for myLover in self.gridBob[self.coord] :
            if myLover.mass >= SeuilPredator*self.mass and self.energy >= parentEnergyRequired and myLover.energy >= parentEnergyRequired and myLover in self.bobArray :
            #SI le rapport des masses est bon & si l'énergie des deux bobs est supérieur au seuil nécessaire pour la reproduction sexuelle et si le partenaire n'a pas déja effectué une action pendant ce tick.    
                babyBob=Bob(self.jeu, self.lastID+1, self.coord)
                babyBob.energy=birthSexEnergy

                babyBob.mass = self.Val_Mutation(TauxMutationMass, (self.mass + myLover.mass)/2)
                babyBob.velocity = self.Val_Mutation(TauxMutationVelocity, (self.velocity + myLover.velocity)/2)
                babyBob.memory = self.Val_Mutation(TauxMutationMemory, (self.memory + myLover.memory)/2)
                babyBob.perception = self.Val_Mutation(TauxMutationPerception, (self.perception + myLover.perception)/2)

                self.gridBob[self.coord].append(babyBob)
                self.bobArray.remove(myLover)
                myLover.consumeEnergy(sexEnergy)
                self.consumeEnergy(sexEnergy)
                return True
        return False

    def eat(self):
        if not Eat : return False
        """
        Fonction qui effectue l'action pour un bob de manger un item de Food présent sur la grille à la même position
        """
        if (self.coord not in self.gridFood) or self.energy == maxEnergy : return False
        if self.energy + self.gridFood[self.coord] <= maxEnergy :
            energyToEat = self.gridFood[self.coord]
            del self.gridFood[self.coord]
        else :
            energyToEat = maxEnergy-self.energy
            self.gridFood[self.coord] -= energyToEat
            self.energy += energyToEat
            self.partheno()
        self.consumeEnergy(tickStaticEnergy) #le bob is dead
        return True


    def distance(x, y, i, j):
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
                if(i > 0 and i < gridSizeX and j > 0 and j < gridSizeY):
                    for (x, y) in self.seen["Bob+"].keys():
                        score += self.distance(i, j, x, y)    
                    scores[(i,j)] = score
                    score = 0
        return max(scores, keys=scores.get)


    def move_towards_coord(self, coord):
        (i, j) = self.coord
        (x, y) = coord
        velocity = int(self.velocity) + int(self.bufvelo)
        if (x,y):
            distance_to_coord = self.distance(i, j, x, y)
            
            if distance_to_coord < velocity:
                return (x, y)
            
            else:

                dir_x = (x - i) / distance_to_coord
                dir_y = (y - j) / distance_to_coord

                if randint(0,1):
                    mov_x = round(dir_x*velocity)
                    mov_y = round(dir_y*(velocity - mov_x))
                else :
                    mov_y = round(dir_y*velocity)
                    mov_x = round(dir_x*(velocity - mov_y))

                i += mov_x
                j += mov_y

        return (i, j)


    def random_move(self):

        # Random move using memory and velocity #
        # Bob will move v tiles and won't go back #
        velocity = int(self.velocity) + int(self.bufvelo)
        (x, y) = self.coord
        MoveOk = False
        while not MoveOk:
            if randint(0,1):
                move_x = randint(max(0, x - velocity), min(gridSizeX, x - int(velocity)))
                move_y = randint(max(0, y - (velocity - abs(move_x - x)), min(gridSizeY, y - (velocity - abs(move_x - x)))))
            else:
                move_y = randint(max(0, y - velocity, min(gridSizeY, y - velocity)))
                move_x = randint(max(0, x - (velocity - abs(move_y - y))), min(gridSizeX, x - (velocity  - abs(move_y - y))))
            if (move_x, move_y) not in self.path :
                MoveOk = True

        return (move_x, move_y)

    #Function perception to get all elements around
    def perception(self):
        if not Perception : return
        (x, y) = self.coord
        self.seen = {"Bob+": {}, "Bob-": {}, "Food": {}}
        for i in range(-self.perception, self.perception  + 1):
            for j in range(- (self.perception - abs(i)) ,self.perception - abs(i) + 1):
                if((x + i, y + j) in self.jeu.gridFood.key()):
                    self.seen["Food"].append((x + i, y + j), self.jeu.gridFood[(x + i, y + j)])
                elif((x + i, y + j) in self.jeu.gridBob.key()):
                    if(self.mass / self.jeu.gridBob.key[x + i, y + j].mass <= SeuilPredator ):
                        self.seen["Bob+"].append((x + i, y + j), self.jeu.gridFood[(x + i, y + j)])
                        self.fuite = True
                    elif(self.mass / self.jeu.gridBob.key[x + i, y + j].mass >= 1 - SeuilPredator):
                        self.seen["Bob-"].append((x + i, y + j), self.jeu.gridFood[(x + i, y + j)])
        self.seen["Food"] = dict(sorted(self.seen["Food"].items(), key=lambda x:x[1], reverse = True))
        self.consumeEnergy(self.perception*tickPerceptionPenalty)
        return


    def move(self) :

        self.bufvelo += self.velocity - int(self.velocity)
        key = self.coord

        ## Fuite ##
        if self.fuite == 1 :
            (x,y) = self.escape(self)
        else:
            (x,y) = self.deplace_perception(self)
            if (x,y) == (None,None):
                if self.remembering_food :
                    (x,y) = self.move_towards_coord(self, self.remembered_food[0])
                else:
                    (x, y) = self.random_move(self)
        
        if (x,y) not in self.jeu.gridBob : self.jeu.gridBob[(x,y)]=[]
        self.jeu.gridBob[(x,y)].append(self) #On ajoute le bob dans le dictionnaire à sa nouvelle position.
        self.jeu.gridBob[key].remove(self) #on retire le bob de son ancienne position.
        self.coord = (x,y)
    
        self.bufvelo -= int(self.bufvelo)
        self.consumeEnergy(self.mass*(self.velocity**2))
        return 0
    
    def use_memory(self):
        if not Memory : return
        # if there is some food on the bob's coordinates, save its amount
        self.path.append(self.coord)
        if self.possiblefood not in self.seen["Food"].items() & self.possiblefood[1] > 0:
            self.remembered_food = self.possiblefood
        #if the coordinates of the remembered food contain a different amount of food (food eaten or food that respawned)
        if self.seen["Food"].has_key(self.remembered_food[0]):
            self.remembering_food = False
            if self.seen["Food"][self.remembered_food[0]] != self.remembered_food[1]:
                self.remembered_food = (self.remembered_food[0], 0)
        # find the biggest food in the bob's perception
        if self.seen["Food"][1] > self.remembered_food[1]:
            self.possiblefood = self.seen["Food"]
        else:
            self.possiblefood = [(0,0), 0]
        #determines whether the bob needs to remember the food.
        if self.remembered_food not in self.seen["Food"].items() & self.remembered_food[1] > 0:
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
        if not Perception : return
        currenttarget = None
        #initializing the variable that will be compared with the Manhattan distance between bob's coordinates and the static foods' coordinates
        diff = self.perception*2
        maxfood = 0
        #determines nearest static food with the biggest energy
        for food in self.seen["Food"].items():
            if diff >= abs(food[0][0]-self.coord[0])+abs(food[0][1]-self.coord[1]):
                if maxfood <= food[1]:
                    diff = abs(food[0][0]-self.coord[0])+abs(food[0][1]-self.coord[1])
                    currenttarget = food[0]
                    maxfood = food[1]
        if currenttarget != None:
            return self.move_towards_coord(currenttarget)
        else:
            maxfood = self.energy
            #determines the nearest bob with the lowest energy
            for bob in self.perception["bob-"].items():
                if diff >= abs(bob[0][0]-self.coord[0])+abs(bob[0][1]-self.coord[1]):
                    if maxfood >= bob[1]:
                        diff = abs(bob[0][0]-self.coord[0])+abs(bob[0][1]-self.coord[1])
                        currenttarget = bob[0]
                        maxfood = bob[1]
            if currenttarget != None:
                return self.move_towards_coord(currenttarget)
            
    def update_bobs(self):
        TILE_SIZE = 16*self.game.zoom
        BOB_SIZE = 10*self.game.zoom
        for key in self.game.gridBob:
            for bob in self.game.gridBob[key]:
                (x,y)=self.game.isoCoordTable[key] #coordonnées Top Left de la case
                x+=TILE_SIZE/2 #coordonnée centre de la case
                x+=BOB_SIZE/4 #Coordonnée top left du bob
                y+=TILE_SIZE/5 #coordonnée de la hauteur du bob.
                self.screen.surface_bob.blit(pygame.transform.scale_by(self.image,self.game.zoom), (x,y))
                