#cost of perception -> flat penalty (Ratio on perception's point) => Bc = BmBv²+(Cost)*Bp
# Bp = 0 initially
# Even value -> +- 1
# d(A,B) = |xb - xa| + |yb - ya|

##### CHANGES TO DO #####
#
# Add in Class Bob an attriute -> Nested Dictionnary for the perception
# It will contain 3 dictionnaries of the informations in sight, Bob+ for the predators, Bob- for the prey and Food
# It will be drop at every start of tick so when the game is saved, you have access to the infos insight before mouvement
# Named "Seen" in the function.
#########################
def perception(self, key):
    (x, y) = key
    for i in range(-self.Bp, self.Bp  + 1):
        for j in range(- (self.Bp - abs(i)) ,self.Bp - abs(i) + 1):
            if((x + i, y + j) in GameWorld.gridFood.key()):
                self.Seen["Food"].append((x + i, y + j), GameWorld.gridFood[(x + i, y + j)])
            elif((x + i, y + j) in GameWorld.gridBob.key()):

            








# Survive FIRST, Hunt SECOND
# if  big bob is detected -> maximize distance
# if several lager bobs are detected -> maximize distance with the closest one and even the distance with the other
# Bobs can run away
# Detects while moving and goes to the closest/biggest one if food and the smallest for bobs
# Mouvement -> As soon as you're not there, reduce either your x or y-distance, with same probability.


