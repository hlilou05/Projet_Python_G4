# Will mutates values of different fonction before spawning the bob
import random

MUT = 0.10

def MutatedAvrg(a, b):
        avrg = (a + b)/2
        return random.uniform(avrg*(1 - MUT),avrg*(1 + MUT))