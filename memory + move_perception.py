#saves the path taken by the bob in self.path 
# bob_co : bob's coordinates
#self.path : list of lists containing at index 0 the coordinates of a tile and at index 1 the amount of food in it.
# self.remembering_food : a boolean, true if the bob is currently remembering a food not in his perception, false if not
#self.possiblefood : variable equals to the food currently remembered

def use_memory(self,bob_co):
    # if there is some food on the bob's coordinates, save its amount
        self.path.append(bob_co)
    # Coordinates where the bob mustn't go
        self.forbidden_co = bob_co
        no food on bob's coordinates, amount of food = 0
    #if the coordinates of the remembered food contain a different amount of food (food eaten or food that respawned)
    if self.perception["food"].has_key(self.possiblefood[0]):
        if self.perception["food"][1] != self.possiblefood[1]:
            self.possiblefood = (self.possiblefood[0], 0)
    # find the biggest food in the bob's perception
    for food in self.perception["food"].items():
        if food[1] > self.possiblefood[1]:
            self.possiblefood = food
    #determines whether the bob needs to remember the food.
    if self.possiblefood not in self.perception["food"].items() & self.possiblefood[1] > 0:
        self.remembering_food = 1
    else:
        self.remembering_food = 0 
    # if the bob already remembers at its maximum capacity, remove the last remembered tiles
    while len(self.path) > 2 * (self.memory-self.remembering_food):
        del self.path[0] 

#function to find the best food to hunt in the bob's perception
#self.currenttarget : variable which will contain the best food to hunt
def deplace_perception(self, coord):
    (x,y) = (0,0)
    #initializing the variable that will be compared with the Manhattan distance between bob's coordinates and the static foods' coordinates
    diff = self.Bp*2
    maxfood = 0
    #determines nearest static food with the biggest energy
    for food in self.perception["food"].items():
        if diff >= abs(food[0][0]-coord[0])+abs(food[0][1]-coord[1]):
            if maxfood <= food[1]:
                diff = abs(food[0][0]-coord[0])+abs(food[0][1]-coord[1])
                self.currenttarget = food[0]
                maxfood = food[1]
    if self.currenttarget != None:
       (x,y) = reach_target(self,coord)
        if (x,y) not in GameWorld.gridBob : 
            GameWorld.gridBob[(x,y)]=[]
        GameWorld.gridBob[(x,y)].append(self)
        GameWorld.gridBob[Key].remove(self)
        self.currenttarget = None
    else:
        maxfood = self.energy
        #determines the nearest bob with the lowest energy
        for bob in self.perception["bob-"].items():
            if diff >= abs(bob[0][0]-coord[0])+abs(bob[0][1]-coord[1]):
                if maxfood >= bob[1]:
                    diff = abs(bob[0][0]-coord[0])+abs(bob[0][1]-coord[1])
                    self.currenttarget = bob[0]
                    maxfood = bob[1]
        if self.currenttarget != None:
            (x,y) = reach_target(self,coord)
            if (x,y) not in GameWorld.gridBob : 
                GameWorld.gridBob[(x,y)]=[]
            GameWorld.gridBob[(x,y)].append(self)
            GameWorld.gridBob[Key].remove(self)
            self.currenttarget = None
            
    #function to randomly decrease the distance between the bob and its hunted food.
    def reach_target(self,coord):
        (x,y) = coord
        if self.currenttarget[0] == coord[0]:
            if self.currenttarget[1] > coord[1]:
                y += int(self.velocity)
            else:
                y -= int(self.velocity)
        elif self.currenttarget[1] == coord[1]:
            if self.currenttarget[0] > coord[0]:
                x += int(self.velocity)
            else:
                x -= int(self.velocity)
        elif self.currenttarget[0] < coord[0] & self.currenttarget[1] < coord[1]:
            if randint(0,1):
                x -= int(self.velocity)
            else:
                y -= int(self.velocity)
        elif self.currenttarget[0] > coord[0] & self.currenttarget[1] < coord[1]:
            if randint(0,1):
                x += int(self.velocity)
            else:
                y -= int(self.velocity)
        elif self.currenttarget[0] < coord[0] & self.currenttarget[1] > coord[1]:
            if randint(0,1):
                x -= int(self.velocity)
            else:
                y += int(self.velocity)
        return (x,y)
