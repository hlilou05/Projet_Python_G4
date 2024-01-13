

def use_memory(self):
    bob_co = (0,0)
    for coord in GameWorld.gridBob.keys():
        if self == GameWorld.gridBob[coord]:
            bob_co = coord
            break
    if GameWorld.gridFood(bob_co):
        self.path.append([bob_co,GameWorld.gridFood(bob_co)])
    else:
        self.path.append([bob_co, 0])
    if len(self.path) > 2 * (self.memory-self.remembering_food):
        del self.path[0] 
    for food in self.perception["food"].items():
        if food[1] > self.possiblefood[1]:
            self.possiblefood = food
    if self.possiblefood not in self.perception["food"].items():
        self.remembering_food = 1
    else:
        self.remembering_food = 0 

def deplace_perception(self, coord):
    diff = self.perception*2
    maxfood = 0
    for food in self.perception["food"].items():
        if diff > abs(food[0][0]-coord[0])+abs(food[0][1]-coord[1]):
            if maxfood <= food[1]:
                diff = abs(food[0][0]-coord[0])+abs(food[0][1]-coord[1])
                self.currenttarget = food[0]
                maxfood = food[1]
    if self.currenttarget != None:
        reach_target(self,coord)
        self.currenttarget = None
    else:
        maxfood = self.energy
        for bob in self.perception["bob-"].items():
            if diff > abs(bob[0][0]-coord[0])+abs(bob[0][1]-coord[1]):
                if maxfood >= bob[1]:
                    diff = abs(bob[0][0]-coord[0])+abs(bob[0][1]-coord[1])
                    self.currenttarget = bob[0]
                    maxfood = bob[1]
        if self.currenttarget != None:
            reach_target(self,coord)
            self.currenttarget = None
            

    def reach_target(self,coord):
        (x,y) = coord
        if self.currenttarget[0] == coord[0]:
            if self.currenttarget[1] > coord[1]:
                y +=1
            else:
                y -= 1
        elif self.currenttarget[1] == coord[1]:
            if self.currenttarget[0] > coord[0]:
                x += 1
            else:
                x -= 1
        elif self.currenttarget[0] < coord[0] & self.currenttarget[1] < coord[1]:
            if randint(0,1):
                x -= 1
            else:
                y -= 1
        elif self.currenttarget[0] > coord[0] & self.currenttarget[1] < coord[1]:
            if randint(0,1):
                x += 1
            else:
                y -= 1
        elif self.currenttarget[0] < coord[0] & self.currenttarget[1] > coord[1]:
            if randint(0,1):
                x -= 1
            else:
                y += 1