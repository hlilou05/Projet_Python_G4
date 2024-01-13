from math import sqrt
from random import randint

GridSize = (X = 100, Y = 100)

def move(self, key) :
    # Condition and verification #

    
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
    if self.food_memory[0] :
        (x, y) = move_towards_food(self, key)
        if (x,y) not in GameWorld.gridBob : GameWorld.gridBob[(x,y)]=[]
        GameWorld.gridBob[(x,y)].append(self) #On ajoute le bob dans le dictionnaire à sa nouvelle position.
        GameWorld.gridBob[Key].remove(self) #on retire le bob de son ancienne position.        self.coord = (x,y)
        if len(GameWorld.gridBob[Key])==0: del(GameWorld.gridBob[Key])
        return 0
    ## Random move ##

    return 0

# for i in range(-self.Bp, self.Bp  + 1):
#        for j in range(- (self.Bp - abs(i)) ,self.Bp - abs(i) + 1):

def escape(self, key):
    # Evaluate best place to go #
    scores = {}
    score = 0
    for i in range(-int(self.velocity), int(self.velocity) + 1):
        for j in range(-int(self.velocity) - abs(i), int(self.velocity) - abs(i) + 1):
            if(i > 0 and i < X and j > 0 and j < Y):
                for (x, y) in self.Seen["Bob+"].keys():
                    score += distance(i, j, x, y)    
                scores.update({(i,j): score})
                score = 0
    return max(scores, keys=scores.get)

def distance(x, y, i, j):
    dist = sqrt((i - x)**2 + (j - y)**2)
    return dist

def move_towards_food(self, key):
    (i, j) = key
    (x, y) = self.food_memory[0]
    if (x,y):
        distance_to_food = distance(i, j, x, y)
        
        if int(distance_to_food) < int(velocity):
            return (x, y)
        
        else:
            dir_x = (x - i) / distance_to_food
            dir_y = (y - j) / distance_to_food

            i += int(dir_x * self.velocity)
            j += int(dir_y * self.velocity)
    return (i, j)