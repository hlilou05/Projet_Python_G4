### Affichage du jeu ###
GAMEPRINTS = False #Autoriser l'affichage des détails sur le terminal.
TICKPRINTS = True #Autoriser l'affichage des détails des ticks sur le terminal.
TICKSHOWBOBS = False #Autoriser l'affichage du nombre de bobs à chaque ticks sous forme de bâtons.
AFFICHAGE = True
TICKTIME = 5


### Grille ###
gridSizeX = 10 #Taille de la grille sur l'axe X.
gridSizeY = 10 #Taille de la grille sur l'axe Y. 

### Ticks and game ###
ticksPerDay = 100 #Nombre de Ticks par jour
bobsQty = 5 #quantité initiale de Bobs.
foodQty = 100 #quantité d'items Food générés par jours
NbDay = 50 #Nombre de jour à jouer


### Fonction Activated ###
Parthenogenesis = True
Eat = True
Hunt = True
Perception = False
Memory = True
Reproduction = True



### Bob's parameters ###
#Bob's energy
energyInitLevel = 100 #Niveau d'énergie initial des Bobs.
maxEnergy = 200 #Energie max d'un Bob.
#Bob's perception
InitPerception = 2
#Bob's velocity
InitVelocity = 1
#Bob's memory
InitMemory = 1
#Bob's mass
InitMass = 1

### Taux de mutation ###
TauxMutationMass = 0.2
TauxMutationVelocity = 0.2
TauxMutationMemory = 0.2
TauxMutationPerception = 0.2

### Energy ###
#Food Items
foodEnergy = 100 #quantité d'énergie d'un item de food généré sur la map.
#Energy for Partheno
parthenoMotherEnergy = 150 #Energie consommée pour produire un bob par partheno
birthParthenoEnergy = 50 #Energie d'un nouveau bob né par partheno
#Energy for Sexual reproduction
parentEnergyRequired = 150 #Energie nécessaire pour commencer la reproduction sexuelle.
birthSexEnergy = 100 #Energie d'un bob né par reproduction sexuelle
sexEnergy = 100 #energie consommée pour produire un bob par reproduction sexuelle
#Energy for each Tick
tickStaticEnergy = 0.5 #energie consommée par tick en restant static
tickMobileEnergy = 1 #energie consommée par tick en étant mobile
tickPerceptionPenalty = 0.2 # Pourcentage des points de perceptions pour conso d'energie
tickMemoryPenalty = 0.2 # Pourcentage des points de perceptions pour conso d'energie

SeuilPredator = 2/3 # Seuil du quotient de masse pour distinguer predateur/proie


### Images ###
import pygame
import os
assets = {
    "arriere_plan" : pygame.image.load(os.path.abspath("src/arrière_plan.jfif")),
    "bob" : pygame.image.load(os.path.abspath("src/bob.png")),
    "bob.blue" : pygame.image.load(os.path.abspath("src/bob.blue.png")),
    "bob.rouge" : pygame.image.load(os.path.abspath("src/bob.rouge.png")),
    "food" : pygame.image.load(os.path.abspath("src/nourriture.png")),
    "fond_ecran" : pygame.image.load(os.path.abspath("src/Photo.png")),
    "tile" : pygame.image.load(os.path.abspath("src/Tile32x32.png")),
}

### Colors ###
bleu = (0, 0, 250)
noir = (0, 0, 0)
rouge = (250, 0, 0)
vert = (0, 250, 0)
blanc = (250, 250, 250)
marron = (139, 69, 19)

### Dictionnaire Options Game ###
options = {"gridSizeX" : gridSizeX, "gridSizeY" : gridSizeY, "ticksPerDay" : ticksPerDay, "bobsQty" : bobsQty,
        "foodQty" : foodQty, "NbDay" : NbDay, "energyInitLevel" : energyInitLevel,
        "InitPerception" : InitPerception, "InitVelocity" : InitVelocity, "InitMass" : InitMass, 
        "InitMemory" : InitMemory, "TauxMutationMass" : TauxMutationMass, "TauxMutationVelocity" : TauxMutationVelocity , "TauxMutationMemory" : TauxMutationMemory, "TauxMutationPerception" : TauxMutationPerception   }