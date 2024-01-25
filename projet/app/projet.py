import random

# REPRO is an option to toggle on and off the reproduction
if REPRO == TRUE :
        def reproduction(Bob a, key):
                if self.energy <= 150 and a.energy <= 150 :
                        if key not in gridNextBob : gridNextBob[key] = []
                        gridNextBob[key].append(Bob())
                        l = len(gridNextBob[key] - 1)
                        gridNextBob[key][l].energy = repro_birth_energy
                        gridNextBob[key][l].size = avrg(self.size, a.size)
                        gridNextBob[key][l].speed = avrg(self.speed, a.speed)
                        gridNextBob[key][l].memory = avrg(self.memory, a.memory)
                        gridNextBob[key][l].perception = avrg(self.perception, a.perception)
                        self.energy -= 100
                        a.energy -= 100 
else :
        def reproduction(Bob a, key) : print("Reproduction is off.")


def avrg(a, b):
        return mutation((a+b)/2) 

def mutation(a):
        mut = a*MUT
        return (random.uniform(a-mut, a+mut))



#######################

# Mutation ? All the functions impacted ?
# Parcour random des bobs ?