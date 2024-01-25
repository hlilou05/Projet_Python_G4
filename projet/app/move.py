from math import sqrt
from random import randint

X = 100
Y = 100

def move(self) :
    # Condition and verification #

    ####### REPRENDRE POUR ENLEVER LES CODES MULTIPLES ########
    key = self.coord
    ## Fuite ##
    if self.fuite == 1 :
        (x,y) = escape(self, key)
        if (x,y) not in GameWorld.gridBob : GameWorld.gridBob[(x,y)]=[]
        GameWorld.gridBob[(x,y)].append(self) #On ajoute le bob dans le dictionnaire à sa nouvelle position.
        GameWorld.gridBob[Key].remove(self) #on retire le bob de son ancienne position.
        self.coord = (x,y)
        if len(GameWorld.gridBob[Key])==0: del(GameWorld.gridBob[Key])
        return 0
    ## Eat ##
        ### Vision ###
            #### food ####
            #### bob- ####
        ### Mémoire ###
            #### Tout droit ####
    if self.remembering_food :
        (x, y) = move_towards_food(self, key)
        if (x,y) not in GameWorld.gridBob : GameWorld.gridBob[(x,y)]=[]
        GameWorld.gridBob[(x,y)].append(self) #On ajoute le bob dans le dictionnaire à sa nouvelle position.
        GameWorld.gridBob[Key].remove(self) #on retire le bob de son ancienne position.        self.coord = (x,y)
        if len(GameWorld.gridBob[Key])==0: del(GameWorld.gridBob[Key])
        return 0
    ## Random move ##
    (x, y) = random_move(self, key)
    self.coord = (x, y)
    
    return 0

# for i in range(-self.Bp, self.Bp  + 1):
#        for j in range(- (self.Bp - abs(i)) ,self.Bp - abs(i) + 1):

def escape(self, key):
    # Evaluate best place to go #
    scores = {}
    score = 0
    (a, b) = key
    for i in range(-int(self.velocity) + a, int(self.velocity) + 1 + a):
        for j in range(-int(self.velocity) - abs(i) + b, int(self.velocity) - abs(i) + 1 + b):
            if(i > 0 and i < X and j > 0 and j < Y):
                for (x, y) in self.Seen["Bob+"].keys():
                    score += distance(i, j, x, y)    
                scores.update({(i,j): score})
                score = 0
    return max(scores, keys=scores.get)

def distance(x, y, i, j):
    dist = abs(i - x) + abs(j - y)
    return dist

def move_towards_food(self, key):
    (i, j) = key
    (x, y) = self.remembered_food[0]
    if (x,y):
        distance_to_food = distance(i, j, x, y)
        
        if distance_to_food < int(self.velocity):
            return (x, y)
        
        else:
            dir_x = (x - i) / distance_to_food
            dir_y = (y - j) / distance_to_food

            i += int(dir_x * self.velocity)
            j += int(dir_y * self.velocity)
    return (i, j)


def random_move(self, key):

    # Random move using memory and velocity #
    # Bob will move v tiles and won't go back #
    
    (x, y) = key
    MoveOk = False
    while not MoveOk:
        if randint(0,1):
            move_x = randint(max(0, x - int(self.velocity)), min(X, x - int(self.velocity)))
            move_y = randint(max(0, y - (int(self.velocity) - abs(move_x - x)), min(Y, y - (int(self.velocity) - abs(move_x - x)))))
        else:
            move_y = randint(max(0, y - int(self.velocity), min(Y, y - int(self.velocity))))
            move_x = randint(max(0, x - (int(self.velocity)  - abs(move_y - y))), min(X, x - (int(self.velocity)  - abs(move_y - y))))
            if (move_x, move_y) not in self.path :
                MoveOk = True

    return (move_x, move_y)