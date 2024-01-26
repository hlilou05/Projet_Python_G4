#  Version Rana
# Par rapport au précédent : j'ai ajouté pause pendant le jeu

from random import *
from time import *
from threading import Thread
import pygame
import sys





"""*******************************************"""
# ******************************************** #
""" ************ PARTIE LOGIQUE **************"""
# ******************************************** #
"""*******************************************"""


################ PARAMETRES ######################

### Affichage du jeu ###
GAMEPRINTS = False #Autoriser l'affichage des détails sur le terminal.
TICKPRINTS = True #Autoriser l'affichage des détails des ticks sur le terminal.
TICKSHOWBOBS = False #Autoriser l'affichage du nombre de bobs à chaque ticks sous forme de bâtons.

### Grille ###
gridSizeX = 100 #Taille de la grille sur l'axe X.
gridSizeY = 100 #Taille de la grille sur l'axe Y. 

### Ticks and game ###
ticksPerDay = 100 #Nombre de Ticks par jour
bobsQty = 100 #quantité initiale de Bobs.
foodQty = 100 #quantité d'items Food générés par jours

### Bob's parameters ###
#Bob's energy
energyInitLevel = 100 #Niveau d'énergie initial des Bobs.
maxEnergy = 200 #Energie max d'un Bob.
#Bob's perception
minPerception = 0
maxPerception = 10
#Bob's velocity
minVelocity = 0
maxVelocity = 10
#Bob's memory
minMemory = 0
maxMemory = 10
#Bob's mass
minMass = 1
maxMass = 30

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



################ CLASS BOB ######################

class Bob:
    """
    Classe dédiée aux Bobs, ces petits personnages qui habitent notre monde et animent notre jeu.
    On définira ici toutes les caractéristiques des Bobs (les actions qu'ils peuvent réaliser, leurs attributs etc).
    
    Les Fonctions qui correspondent à des actions macroscopiques des bobs retournent True si le bob a réalisé
    l'action en question et False si les conditions pour réaliser l'action ne sont pas réunies,
    auquel cas le bob devra essayer une autre action.
    """
    def __init__(self, ID, coord) :
        self.ID = ID
        self.mass = randint(10, 30)
        self.velocity = 1
        self.energy = energyInitLevel
        self.memory = 0
        self.path = []
        self.perception = 0
        self.coord = coord

    #FONCTIONS DU BOB : hunt, eat, partheno, fuck, randomMove.
    #parametre recu pour chaque fonction : La case dans laquelle se trouve le bob.

    def partheno(self):
        """
        Fonction de reproduction d'un bob individuellement lorsqu'il a atteint l'énergie maximale.
        """
        GameWorld.gamePrint("Function : Partheno")
        if self.energy==maxEnergy:
            self.consumeEnergy(parthenoMotherEnergy)
            babyBob = Bob(GameWorld.lastID+1, self.coord)
            babyBob.energy = birthParthenoEnergy
            GameWorld.gridBob[self.coord].append(babyBob)
            GameWorld.gamePrint("birth from partheno. End of the function")
    
    def consumeEnergy(self, score):
        """
        Fonction qui retire l'énergie consommée par le bob et vérifie qu'il soit toujours vivant.
        Return True si le bob est dead.
        Return False si le bob est toujours vivant après la consommation d'énergie.
        """
        GameWorld.gamePrint("\tFunction : ConsumeEnergy")
        self.energy -= score
        if self.energy<=0: #Verifier si le bob a toujours de l'energie. Sinon il meurt.
            self.die()
            return True #le bob is dead...
        return False #le bob is alive !
    
    def die(self):
        """
        Fonction utilisée pour supprimer correctement un bob décédé.
        """
        GameWorld.gridBob[self.coord].remove(self) #suppression du bob du tableau associé à ses coordonnées dans le dictionnaire gridBob.
        if self in GameWorld.bobArray : GameWorld.bobArray.remove(self) #Retirer le bob du tableau bobArray qui contient les bobs qui doivent jouer leur coup au tick présent. 
        if len(GameWorld.gridBob[self.coord])==0: del(GameWorld.gridBob[self.coord]) #Si le tableau est vide, alors on supprime la case du dictionnaire.
        return

    def hunt(self):
        """
        Fonction qui représente l'action d'un bob qui mange un autre bob.
        """
        GameWorld.gamePrint("Function : Hunt")
        for prey in GameWorld.gridBob[self.coord]:
            if prey.mass < 2/3*self.mass:
                #On a trouvé un bob que l'on peut manger !
                if self.consumeEnergy(tickStaticEnergy): return True #le bob is dead
                #EAT THE BOB
                energyToEat = 1/2 * prey.energy * (1-prey.mass/self.mass)
                if self.energy+energyToEat <= maxEnergy : self.energy+=energyToEat
                else : self.energy = maxEnergy # A VERIFIER DANS LES REGLES !!!!!!!!!!!!!!!!
                prey.die() #Le bob mangé meurt...
                GameWorld.gamePrint("A bob was murdered. End of the function.")
                return True
        return False

    def fuck(self):
        """
        Fonction de reproduction sexuelle entre 2 bobs.
        """
        GameWorld.gamePrint("Function : Fuck")
        for myLover in GameWorld.gridBob[self.coord] :
            if myLover.mass >= 2/3*self.mass and self.energy >= parentEnergyRequired and myLover.energy >= parentEnergyRequired and myLover in GameWorld.bobArray :
            #SI le rapport des masses est bon & si l'énergie des deux bobs est supérieur au seuil nécessaire pour la reproduction sexuelle et si le partenaire n'a pas déja effectué une action pendant ce tick.    
                babyBob=Bob(GameWorld.lastID+1, self.coord)
                babyBob.energy=birthSexEnergy
                GameWorld.gridBob[self.coord].append(babyBob)
                GameWorld.bobArray.remove(myLover)
                myLover.consumeEnergy(sexEnergy+tickStaticEnergy)
                self.consumeEnergy(sexEnergy+tickStaticEnergy)
                GameWorld.gamePrint("birth from sex")
                return True
        return False

    def eat(self):
        """
        Fonction qui effectue l'action pour un bob de manger un item de Food présent sur la grille à la même position
        """
        GameWorld.gamePrint("Function : Eat")
        if self.coord not in GameWorld.gridFood or self.energy == maxEnergy : return False
        if self.consumeEnergy(tickStaticEnergy): return True #le bob is dead
        if self.energy + GameWorld.gridFood[self.coord] <= maxEnergy :
            energyToEat = GameWorld.gridFood[self.coord]
            del GameWorld.gridFood[self.coord]
        else : 
            energyToEat = maxEnergy-self.energy
            GameWorld.gridFood[self.coord] -= energyToEat
        self.energy += energyToEat
        self.partheno()
        GameWorld.gamePrint("grrrr... End of the function.")
        return True

    def randomMove(self):
        """
        Fonction de déplacement aléaroire sur une case adjacente.
        """
        GameWorld.gamePrint("Function : RandomMove")
        previousKey = self.coord
        if self.consumeEnergy(tickMobileEnergy): return #le bob is dead
        moved = False
        mvcount = 0
        while moved == False : #tant qu'on a pas effectué un déplacement, on cherche un déplacement valide.
            if mvcount > 10 : return False #Au bout de 10 tentatives on abandonne et on considère que le déplacement est impossible. 
            mvcount += 1
            (x,y) = self.coord
            if randint(0,1) : #choix random vertical ou horizontal.
                x += randint(1,2)*2-3 #aléatoirement +1 ou -1 à la coordonnée x
                if x <= gridSizeX-1 and x >= 0:
                    moved = True
            else :
                y += randint(1,2)*2-3 #aléatoirement +1 ou -1 à la coordonnée y
                if y <= gridSizeY-1 and y >= 0:
                    moved = True
        #on applique le déplacement valide trouvé auparavant.
        if (x,y) not in GameWorld.gridBob : GameWorld.gridBob[(x,y)]=[]
        GameWorld.gridBob[(x,y)].append(self) #On ajoute le bob dans le dictionnaire à sa nouvelle position.
        GameWorld.gridBob[previousKey].remove(self) #on retire le bob de son ancienne position.
        self.coord = (x,y)
        if len(GameWorld.gridBob[previousKey])==0: del(GameWorld.gridBob[previousKey])
        GameWorld.gamePrint("Bob moved, end of the function.")
        return True


################### Grille ######################

# Dictionnaire Grille. Clé -> (x,y), contient un élément de type class Case.
#grid est une variable globale. PAS BESOIN DE LA PASSER EN PARAMETRE.

class World():
    """
    Classe dédiée au fonctionnement du jeu : faire spawn les bobs, stocker les bobs et toute entité sur la grille, exécuter les tics, faire appel aux fonctions d'affichage de la partie graphique à la fin des tics, etc.
    """
    def __init__(self) :
        self.lastID = -1 #identifiant unique pour chaque bob créé.
        self.isPaused = False #pour mettre sur pause le jeu.
        self.gridBob = {} #Dictionnaire de bobs.
        self.gridFood = {} #Dictionnaire d'élements Foods
        self.bobArray=[] #Tableau de bob utilisé à chaque tour pour parcourir l'esemble des bobs de façon aléatoire.
        self.bobcount=bobsQty #Compteur du nombre de bobs en vie.
        self.dayCounter=0 #Compteur du nombre de jour.
        self.tickCounter=0 #Compteur du nombre de ticks.
        self.bobSpawn() #Générer les bobs à l'initialisation du jeu.
        #statistiques de la forme (min, max, moyenne)
        self.statEnergy = [None, None, None] #statistique d'énergie
        self.statMass = [None, None, None] #statistique de masse
        self.statVelocity = [None, None, None] #statistique de vitesse
        self.statPerception = [None, None, None] #statistique de perception
        self.statMemory = [None, None, None] #statistique de mémoire
        
    def gamePrint(self, msg):
        if GAMEPRINTS : print(msg)
        return

    def printGridBob(self):
        """
        Affichage rapide du contenu des dictionnaires.
        Pas dans l'ordre... !
        """
        for cle, val in self.gridBob.items():
            print("Coord :",cle, "\t Nb Bobs :", len(val))
        return

    def printGridFood(self):
        """
        Affichage rapide du contenu des dictionnaires.
        Pas dans l'ordre... !
        """
        for cle, val in self.gridFood.items():
            print("Coord :",cle, "\tFood Level :", val)
        return
    
    def bobSpawn(self):
        """
        Fait apparaitre bobsQty bobs aléatoirement répartis sur la map.
        """
        for _ in range(bobsQty):
            x = randint(0, gridSizeX-1)
            y = randint(0, gridSizeY-1)
            if (x, y) not in self.gridBob : self.gridBob[(x, y)]=[]
            mybob=Bob(self.lastID+1, (x,y))
            self.gridBob[(x, y)].append(mybob)
        return

    def foodSpawn(self):
        """
        Fait apparaitre FoodQty elements de Food aléatoirement répartis sur la map.
        """
        for _ in range(foodQty):
            x = randint(0, gridSizeX-1)
            y = randint(0, gridSizeY-1)
            if (x, y) not in self.gridFood : self.gridFood[(x, y)]=0
            self.gridFood[(x, y)]+=foodEnergy
        return
    
    def statistics(self):
        """
        Fonction qui fait des statiqtiques sur les bobs encore en vie.
        """
        self.statEnergy = [maxEnergy, 0, 0]
        self.statMass = [maxMass, minMass, 0] #statistique de masse
        self.statVelocity = [maxVelocity, minVelocity, 0] #statistique de vitesse
        self.statPerception = [maxPerception, minPerception, 0] #statistique de perception
        self.statMemory = [maxMemory, minMemory, 0] #statistique de mémoire
        self.bobcount = 0
        for key in self.gridBob:
            for bob in self.gridBob[key]:
                self.bobcount += 1
                self.statMass[0] = min(self.statMass[0], bob.mass)
                self.statMass[1] = max(self.statMass[1], bob.mass)
                self.statMass[2] += bob.mass
                self.statEnergy[0] = min(self.statEnergy[0], bob.energy)
                self.statEnergy[1] = max(self.statMass[1], bob.energy)
                self.statEnergy[2] += bob.energy
                self.statVelocity[0] = min(self.statVelocity[0], bob.velocity)
                self.statVelocity[1] = max(self.statVelocity[1], bob.velocity)
                self.statVelocity[2] += bob.velocity
                self.statPerception[0] = min(self.statPerception[0], bob.perception)
                self.statPerception[1] = max(self.statPerception[1], bob.perception)
                self.statPerception[2] += bob.perception
                self.statMemory[0] = min(self.statMemory[0], bob.memory)
                self.statMemory[1] = max(self.statMemory[1], bob.memory)
                self.statMemory[2] += bob.memory

        if self.bobcount == 0 :
            self.statEnergy = [0, 0, 0]
            self.statMass = [0, 0, 0]
            self.statVelocity = [0, 0, 0]
            self.statPerception = [0, 0, 0]
            self.statMemory = [0, 0, 0]
        else : 
            self.statMass[2] /= self.bobcount
            self.statEnergy[2] /= self.bobcount
            self.statVelocity[2] /= self.bobcount
            self.statPerception[2] /= self.bobcount
            self.statMemory[2] /= self.bobcount
            self.statMass[2] = round(self.statMass[2], 2)
            self.statEnergy[2] = round(self.statEnergy[2], 2)
            self.statVelocity[2] = round(self.statVelocity[2], 2)
            self.statPerception[2] = round(self.statPerception[2], 2)
            self.statMemory[2] = round(self.statMemory[2], 2)
        return
    
    def printStatistics(self):
        """
        Fonction qui affiche les statistiques du jeu.
        """
        print("Statistiques du jeu :")
        print("\t Nombre de bobs :", self.bobcount)
        print("\t vitesse :", self.statVelocity)
        print("\t mass :", self.statMass)
        print("\t energy :", self.statEnergy)
        print("\t perception :", self.statPerception)
        print("\t memory :", self.statMemory)
        return
    
    def saveTheGame(self): #enregistre le jeu actuel dans le document jeu.data
        return


    def makeBobArray(self):
        """
        A chaque tick, les bobs sont listés dans le tableau bobArray avant d'être appelés pour jouer leur coup dans la fonction tick.
        Cette fonction permet de construire ce tableau.
        """
        self.bobArray.clear()
        for key in self.gridBob:
            for bob in self.gridBob[key]:
                self.bobArray.append(bob)
                bob.coord=key
        self.bobcount=len(self.bobArray)
        return


    def tick(self):
        """
        Fonction qui sollicite tous les bobs pour leur donner une action à réaliser.
        Actions possibles par ordre de priorité : eat, hunt, fuck, randomMove.
        Cette fonction prend un bob aléatoirement dans le tableau bobArray, lui fait jouer son coup puis le supprime du tableauavant de recommencer l'opération pour un autre bob aléatoirement... jusqu'à ce que le tableau soit vide, c-a-d que tous les bobs aient joué leur coup lors du tick actuel.
        """
        self.makeBobArray() #A chaque tick on créé le tableau bobArray de tous les bobs encore en vie.#printGridBob()
        self.tickCounter += 1
        if TICKPRINTS : print("tick", self.tickCounter, " : ", self.bobcount, "Bobs alive.")
        while len(self.bobArray)!=0 :
            bob = choice(self.bobArray)
            self.bobArray.remove(bob)
            assert bob in self.gridBob[bob.coord]
            #Choix d'une action :
            if not bob.eat(): #Eat food
                if not bob.hunt(): #Hunt other bobs
                    if not bob.fuck(): #Fuck
                        bob.randomMove() #Move randomly
        #sleep(0.5)
        if TICKSHOWBOBS :
            for _ in range(self.bobcount): print("|", end = "")
            print()
        return
    
    def day(self):
        """
        Fonction qui lance la simulation d'un "Day"
        Permet de mettre sur pause le jeu à tout moment entre deux ticks.
        Met a jour les statistiques à chaque début de jour"""
        self.dayCounter += 1
        self.tickCounter = 0
        self.statistics()
        if self.bobcount!=0 :
            print()
            print("DAY", self.dayCounter)
            self.foodSpawn()
            for _ in range (ticksPerDay):
                while self.isPaused == False : sleep(0.5) #pour mettre sur pause.
                self.tick()
                #printGridBob()

    def play(self, NbDay):
        for _ in range (NbDay) :
            self.day()

    #def pauseGame(self):
     #   while GAME.is_alive():
      #      if keyboard.is_pressed("p"):
       #         print("pause")
        #        if self.pause == True : self.pause = False
         #       else : self.pause=True
          #      break







"""*******************************************"""
# ********************************************* #
""" ********** PARTIE GRAPHIQUE EN 2D *********"""
# ********************************************* #
"""*******************************************"""
import pygame
from pygame.locals import *
from threading import Thread
from time import sleep
import sys

pygame.init()
largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("PROJET_PYTHON_2024")
done = False

bleu = (0, 0, 250)
noir = (0, 0, 0)
rouge = (250, 0, 0)
vert = (0, 250, 0)
blanc = (250, 250, 250)
marron = (139, 69, 19)
gridSize = 10
police = pygame.font.Font(None, 36)

def afficher_texte(texte, x, y):
    texte_surface = police.render(texte, True, blanc)
    texte_rect = texte_surface.get_rect()
    texte_rect.center = (x, y)
    fenetre.blit(texte_surface, texte_rect)

champs = [pygame.Rect(300, 50 + i * 70, 300, 50) for i in range(8)]
couleur_active = pygame.Color('dodgerblue2')
couleur_inactive = pygame.Color('lightskyblue3')
couleur = couleur_inactive
textes = [''] * 8
actif_champ = None

class Tile:
    def __init__(self, x, y):
        self.image = pygame.image.load("Tile32x32.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class View:
    def __init__(self):
        self.infoObject = pygame.display.Info()
        self.screen = pygame.display.set_mode((self.infoObject.current_w - 600, self.infoObject.current_h - 600))
        self.running = True
        self.zoom = 1
        self.offsetx = 0
        self.offsety = 0
        self.value = 20
        self.screen.fill("WHITE")
        self.current_page = 0  # Ajout d'une variable pour suivre la page actuelle
        self.menu_active = True
        self.game_active = False  # Ajout d'une variable pour indiquer si le jeu est actif
        self.suivant_pressed = False
        self.pages = []
        # Initialiser les pages
        self.pages.append(self.display_menu)
        self.pages.append(self.affiche_formulaire)
        self.pages.append(self.affiche_deuxieme_page)
        # Choisir la première page à afficher
        self.current_page = 0
        self.run()
        self.display_menu()

    def display_menu(self):
        music_song = pygame.mixer.Sound("music_pygame.mp3")
        music_song.play()
        while self.menu_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 300 <= x <= 500:
                        if 200 <= y <= 250:
                            print("Start")
                            self.menu_active = False
                            self.game_active = True
                            self.run_game()
                        elif 300 <= y <= 350:
                            print("Options")
                            variables = ['GridSizeX', 'GridSizeY', 'TicksPerDay', 'BobsQty', 'FoodQty', 'EnergyInitLevel', 'MaxEnergy', 'InitPerception']
                            self.affiche_formulaire(variables)
                        elif 400 <= y <= 450:
                            pygame.quit()
                            sys.exit()

            background = pygame.image.load("Photo.png")
            background = pygame.transform.scale(background, (self.screen.get_width(), self.screen.get_height()))
            self.screen.blit(background, (0, 0))

            afficher_texte("GAME OF LIFE", self.screen.get_width() // 2, 100)
            pygame.draw.ellipse(self.screen, marron, (300, 200, 200, 50))
            afficher_texte("START", self.screen.get_width() // 2, 225)
            pygame.draw.ellipse(self.screen, marron, (300, 300, 200, 50))
            afficher_texte("OPTIONS", self.screen.get_width() // 2, 325)
            pygame.draw.ellipse(self.screen, marron, (300, 400, 200, 50))
            afficher_texte("QUIT", self.screen.get_width() // 2, 425)

            pygame.display.update()

    def run_game(self):
        while self.game_active:
            self.actualise_user_input()
            self.screen.fill("WHITE")
            self.display_tiles()
            pygame.display.update()
            sleep(0.01)
    def run(self):
        while self.running:
            # Exécuter la page actuelle
            self.pages[self.current_page]()


    def continuous_display(self):
        ThreadDisplay = Thread(target=self.continuous_display_thread)
        ThreadDisplay.start()

    def continuous_display_thread(self):
        while self.running:
            self.actualise_user_input()
            pygame.display.update()
            sleep(0.01)

    def iso_coord(self, x, y):
        return [x - y, (x + y) / 2]

    def display_tiles(self):
        pause_button = pygame.Rect(self.screen.get_width() - 200, 50, 150, 50)
        pygame.draw.rect(self.screen, marron, pause_button)
        afficher_texte("Pause", self.screen.get_width() - 125, 75)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pause_button.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(self.screen, rouge, pause_button, 2)

        if pygame.mouse.get_pressed()[0] and pause_button.collidepoint(mouse_x, mouse_y):
            self.affiche_pause_menu()
        TILE_SIZE = 16 * self.zoom
        screen_x, screen_y = self.screen.get_size()
        for y in range(-self.value // 2, self.value // 2):
            for x in range(-self.value // 2, self.value // 2):
                new_tile = Tile(screen_x // 4 + screen_y // 2 + x * TILE_SIZE,
                                screen_y // 2 - screen_x // 4 + y * TILE_SIZE)
                self.screen.blit(pygame.transform.scale(new_tile.image, (int(32 * self.zoom), int(32 * self.zoom))),
                                 (self.iso_coord(new_tile.rect.x, new_tile.rect.y)[0] + self.offsetx * TILE_SIZE,
                                  self.iso_coord(new_tile.rect.x, new_tile.rect.y)[1] + self.offsety * TILE_SIZE))
    def affiche_pause_menu(self):
        self.pause_menu_active = True
        while self.pause_menu_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 300 <= x <= 500 and 200 <= y <= 250:
                        print("Resume")
                        self.pause_menu_active = False
                    elif 300 <= x <= 500 and 300 <= y <= 350:
                        print("options")
                        self.pause_menu_active = False
                        variables = ['GridSizeX', 'GridSizeY', 'TicksPerDay', 'BobsQty', 'FoodQty', 'EnergyInitLevel', 'MaxEnergy', 'InitPerception']
                        self.affiche_formulaire(variables)
                    elif 300 <= x <= 500 and 400 <= y <= 450:
                        print("Quit to Menu")
                        self.pause_menu_active = False
                        self.game_active = False
                        self.menu_active = True
                        self.display_menu()
                    
                        

            # Affichage de la page de pause
            self.screen.fill("WHITE")
            afficher_texte("PAUSE", self.screen.get_width() // 2, 100)
            pygame.draw.ellipse(self.screen, marron, (300, 200, 200, 50))
            afficher_texte("Resume", self.screen.get_width() // 2, 225)
            pygame.draw.ellipse(self.screen, marron, (300, 300, 200, 50))
            afficher_texte("Options", self.screen.get_width() // 2, 325)
            pygame.draw.ellipse(self.screen, marron, (300, 400, 200, 50))
            afficher_texte("Quit to Menu", self.screen.get_width() // 2, 425)

            pygame.display.update()
 
    def actualise_user_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.menu_active = False
                self.game_active = False
            if event.type == pygame.MOUSEWHEEL:
                if event.y == 1:
                    if self.zoom >= 3:
                        break
                    else:
                        self.zoom += 0.15
                else:
                    if self.zoom <= 0.5:
                        break
                    else:
                        self.zoom -= 0.15
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    if self.zoom >= 3:
                        break
                    else:
                        self.zoom += 0.15
                elif event.key == pygame.K_o:
                    if self.zoom <= 0.5:
                        break
                    else:
                        self.zoom -= 0.15
                elif event.key == pygame.K_UP:
                    self.offsety -= 1
                elif event.key == pygame.K_DOWN:
                    self.offsety += 1
                elif event.key == pygame.K_LEFT:
                    self.offsetx -= 1
                elif event.key == pygame.K_RIGHT:
                    self.offsetx += 1
    def affiche_deuxieme_page(self):
        global couleur_inactive
        global actif_champ
        global textes
        global couleur_page2

        # Charger l'image de fond
        background = pygame.image.load("arrière_plan.jfif")
        background = pygame.transform.scale(background, (fenetre.get_width(), fenetre.get_height()))
        fenetre.blit(background, (0, 0))

        variables_page2 = ['InitVelocity', 'InitMemory', 'InitMass', 'TauxMutationMass', 'TauxMutationVelocity',
                        'TauxMutationMemory', 'TauxMutationPerception']
        champs_page2 = [pygame.Rect(50, 50 + i * 70, 300, 50) for i in range(len(variables_page2))]
        textes_page2 = [''] * len(variables_page2)
        couleur_page2 = couleur_inactive
        actif_champ_page2 = None

        # Ajouter le bouton "Retour"
        retour_button = pygame.Rect(largeur - 150, hauteur - 100, 100, 50)
        pygame.draw.rect(fenetre, rouge, retour_button)
        afficher_texte("Retour", largeur - 100, hauteur - 75)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if retour_button.collidepoint(x, y):
                        self.current_page -= 1  # Revenir à la page précédente
                        return

                    for i, champ in enumerate(champs_page2):
                        if champ.collidepoint(event.pos):
                            actif_champ_page2 = i
                            couleur_page2 = pygame.Color('dodgerblue2')
                        else:
                            couleur_page2 = pygame.Color('lightskyblue3')

                if event.type == pygame.KEYDOWN:
                    if actif_champ_page2 is not None:
                        if event.key == pygame.K_RETURN:
                            print("Variable {}: {}".format(actif_champ_page2 + 1, textes_page2[actif_champ_page2]))
                            textes_page2[actif_champ_page2] = ''
                        elif event.key == pygame.K_BACKSPACE:
                            textes_page2[actif_champ_page2] = textes_page2[actif_champ_page2][:-1]
                        else:
                            textes_page2[actif_champ_page2] += event.unicode

            for i, (variable, champ) in enumerate(zip(variables_page2, champs_page2)):
                var_surface = police.render(variable, True, noir)
                fenetre.blit(var_surface, (50, 50 + i * 70))

                pygame.draw.rect(fenetre, couleur_page2, champ, 2)
                texte_surface = police.render(textes_page2[i], True, noir)
                largeur_texte = max(200, texte_surface.get_width() + 10)
                champ.w = largeur_texte
                fenetre.blit(texte_surface, (champ.x + 5, champ.y + 5))

            pygame.display.update()


    def affiche_formulaire(self, variables):
        global couleur
        global actif_champ

        background = pygame.image.load("arrière_plan.jfif")
        background = pygame.transform.scale(background, (fenetre.get_width(), fenetre.get_height()))
        fenetre.blit(background, (0, 0))

        for i, (variable, champ) in enumerate(zip(variables, champs)):
            var_surface = police.render(variable, True, noir)
            fenetre.blit(var_surface, (50, 50 + i * 70))

            pygame.draw.rect(fenetre, couleur, champ, 2)
            texte_surface = police.render(textes[i], True, noir)
            largeur_texte = max(200, texte_surface.get_width() + 10)
            champ.w = largeur_texte
            fenetre.blit(texte_surface, (champ.x + 5, champ.y + 5))

        retour_button = pygame.Rect(largeur - 150, hauteur - 100, 100, 50)
        pygame.draw.rect(fenetre, rouge, retour_button)
        afficher_texte("Retour", largeur - 100, hauteur - 75)
        suivant_button = pygame.Rect(largeur - 150, hauteur - 175, 100, 50)
        pygame.draw.rect(fenetre, vert, suivant_button)
        afficher_texte("Suivant", largeur - 100, hauteur - 150)
        pygame.display.flip()

        while not self.suivant_pressed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, champ in enumerate(champs):
                        if champ.collidepoint(event.pos):
                            actif_champ = i
                            couleur = pygame.Color('dodgerblue2')
                        else:
                            couleur = pygame.Color('lightskyblue3')
                    if retour_button.collidepoint(event.pos):
                        return
                    if suivant_button.collidepoint(event.pos):
                        self.suivant_pressed = True  # Définir suivant_pressed à True et quitter la boucle

                    if event.type == pygame.KEYDOWN:
                        if actif_champ is not None:
                            if event.key == pygame.K_RETURN:
                                print("Variable {}: {}".format(actif_champ + 1, textes[actif_champ]))
                                textes[actif_champ] = ''
                            elif event.key == pygame.K_BACKSPACE:
                                textes[actif_champ] = textes[actif_champ][:-1]
                            else:
                                textes[actif_champ] += event.unicode

            pygame.display.update()

        self.affiche_deuxieme_page()  # Appeler la méthode pour afficher la deuxième page


   

# Initialiser et lancer la boucle principale
# affichage = View()
# affichage.display_menu()



"""********************************************"""
# ********************************************** #
""" ************DEROULEMENT DU JEU**************"""
# ********************************************** #
"""********************************************"""

import pygame
pygame.init()

        
GameWorld = World()
NbDay = 50

affichage = View()
