from queue import Queue
class Bob:
    def __init__(self,c) :
        self.em=300
        self.c=c
        self.size= 1 #(randint(5, 10) + randint(5, 10))/2
        self.speed=1
        self.energy=100
        self.memory=0
        self.path= Queue(maxsize = self.memory)
        self.perception=0
    def eat(self,e):
        self.energy+=e
    def move(self,newMovement):
        if  self.path.full():
            self.path.get()
        self.path.put(newMovement)
    def partheno(self,x,y):
        if self.size>self.em:
            Bob(self.c)
            
                 

