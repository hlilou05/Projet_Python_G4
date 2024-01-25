#saves the path taken by the bob in self.path 
# bob_co : bob's coordinates
#self.path : list of lists containing at index 0 the coordinates of a tile and at index 1 the amount of food in it.
# self.remembering_food : a boolean, true if the bob is currently remembering a food not in his perception, false if not
#self.possiblefood : variable equals to the food that the bob could remember

def use_memory(self):

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
            self.possiblefood = ((0,0), 0)
        #determines whether the bob needs to remember the food.
        if self.remembered_food not in self.seen["Food"].items() & self.remembered_food[1] > 0:
            self.remembering_food = True
        else:
            self.remembering_food = False
        # if the bob already remembers at its maximum capacity, remove the last remembered tiles
        while len(self.path) > 2 * (self.memory-self.remembering_food):
            del self.path[0]

#function to find the best food to hunt in the bob's perception
#self.currenttarget : variable which will contain the best food to hunt
def deplace_perception(self):
    currenttarget = None
    #initializing the variable that will be compared with the Manhattan distance between bob's coordinates and the static foods' coordinates
    diff = self.Bp*2
    maxfood = 0
    #determines nearest static food with the biggest energy
    for food in self.perception["food"].items():
        if diff >= abs(food[0][0]-self.coord[0])+abs(food[0][1]-self.coord[1]):
            if maxfood <= food[1]:
                diff = abs(food[0][0]-self.coord[0])+abs(food[0][1]-self.coord[1])
                currenttarget = food[0]
                maxfood = food[1]
    if currenttarget != None:
        return move_towards_coord(currenttarget)
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
            return move_towards_coord(currenttarget)
            