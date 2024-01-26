import pygame


class Window:
    """
    Classe dédiée à l'affichage
    """
    def __init__(self, myGame):
        self.Game = myGame
        self.GBob = GraphicBob()
        self.GFood = GraphicFood()
        self.GTile = Tile()
        self.infoObject = pygame.display.Info()
        self.screen = pygame.display.set_mode((self.infoObject.current_w-200,self.infoObject.current_h-200)) #Fenêtre du jeu.
        self.isoCoordTable = {} #dictionnaire qui associe les coordonnées 2D des tiles à leurs coordonnées ISO. On l'utilisera pour placer les bobs exactement sur les tiles. (x réel , y réel) -> (x iso , y iso)
        self.bobArray = [] #Tableau de bobs à afficher
        self.foodArray = [] #Tableau de food à afficher
        self.zoom = 1
        self.offsetx = 0
        self.offsety = 0
        self.value = 20 #taille de la grille // A RELIER AVEC LES PARAMETRES
        self.screen.fill("WHITE")
        self.update_tiles()
        self.Display()
        #self.display_menu()

    def display_menu(self):
        #SI LE JOUEUR CLIQUE SUR START :
        self.display_tiles()

    def Display(self):
        """
        Fonction qui actualise la grille avec le zoom et maintient l'affichage pendant toute la durée de l'execution.
        """
        self.Actualise_UserInput()
        self.screen.fill("WHITE")
        self.update_tiles()
        self.update_bobs()
        self.update_food()
        pygame.display.update()
    
    def iso_coord(self, x, y):
        """
        Génération de coordonnées isométriques à partir de coordonnées 2D.
        """
        return [x-y, (x+y)/2]

    def update_tiles(self):
        """
        Construction de la grille sur la fenêtre.
        """
        TILE_SIZE = 16*self.zoom
        screen_x, screen_y = self.screen.get_size()
        for y in range(gridSizeY):
            for x in range(gridSizeX):
                #création d'une new Tile
                self.GTile.set_center(screen_x//4 + screen_y//2 + (x-gridSizeX//2)*TILE_SIZE , screen_y//2 - screen_x//4 + (y-gridSizeY//2)*TILE_SIZE)
                #On sauvegarde la coordonnée isométrique de la case pour pouvoir replacer des bobs facilement dedans.
                #Dictionnaire (x réel , y réel) -> (x iso , y iso)
                self.isoCoordTable[(x, y)]  =  [self.iso_coord(self.GTile.rect.center[0], self.GTile.rect.center[1])[0]+self.offsetx*TILE_SIZE  ,  self.iso_coord(self.GTile.rect.center[0], self.GTile.rect.center[1])[1]+self.offsety*TILE_SIZE]
                self.screen.blit(pygame.transform.scale_by(self.GTile.image,self.zoom), self.isoCoordTable[(x,y)])


    def update_bobs(self):
        TILE_SIZE = 16*self.zoom
        BOB_SIZE = 10*self.zoom
        for key in self.Game.gridBob:
            for bob in self.Game.gridBob[key]:
                (x,y)=self.isoCoordTable[key] #coordonnées Top Left de la case
                x+=TILE_SIZE/2 #coordonnée centre de la case
                x+=BOB_SIZE/4 #Coordonnée top left du bob
                y+=TILE_SIZE/5 #coordonnée de la hauteur du bob.
                self.screen.blit(pygame.transform.scale_by(self.GBob.image,self.zoom), (x,y))


    def update_food(self):
        TILE_SIZE = 16*self.zoom
        FOOD_SIZE = 13*self.zoom
        for key in self.Game.gridFood:
            (x,y)=self.isoCoordTable[key] #coordonnées Top Left de la case
            x+=TILE_SIZE/2 #coordonnée centre de la case
            x+=FOOD_SIZE/4 #Coordonnée top left de la food
            y+=TILE_SIZE/5 #coordonnée de la hauteur de la food.
            self.screen.blit(pygame.transform.scale_by(self.GFood.image,self.zoom), (x,y))


    def Actualise_UserInput(self):
        """
        Actualise the zoom from keyboard input or mousewheel.
        Quit if the window is being shut down by the user"""
        for event in pygame.event.get():
            #Exit
            if event.type == pygame.QUIT: self.Game.isRunning = False
            #zoom souris
            if event.type == pygame.MOUSEWHEEL:
                if event.y == 1 :
                    if self.zoom >= 3 : break
                    else : self.zoom+=0.15
                else :
                    if self.zoom <= 0.5 : break
                    else : self.zoom-=0.15
                self.screen.fill("WHITE")
                self.update_tiles()
                self.update_bobs()
            #Appui clavier
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i: #touche i -> zoom in
                        if self.zoom >= 3 : break
                        else : self.zoom+=0.15
                    elif event.key == pygame.K_o: #touche o -> zoom out
                        if self.zoom <= 0.5 : break
                        else : self.zoom -= 0.15
                    elif event.key == pygame.K_DOWN: #touche flèche down
                        self.offsety -= 1
                    elif event.key == pygame.K_UP: #touche flèche up
                        self.offsety += 1
                    elif event.key == pygame.K_RIGHT: #touche flèche droite
                        self.offsetx -= 1
                    elif event.key == pygame.K_LEFT: #touche flèche gauche
                        self.offsetx += 1 
                    elif event.key == pygame.K_SPACE: #touche espace
                        self.Game.isPaused = not self.Game.isPaused
                    self.screen.fill("WHITE")
                    self.update_tiles()
                    self.update_bobs()
        return