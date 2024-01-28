import pygame
from .Constant import *


# Class interface graphique
class GUI:
    def __init__(self, game):
        self.game = game
        self.x = 0
        self.y = 0

        self.visible = True

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def draw_element(self, element):
        if not self.visible : return
        element.update

# Class parente des éléments GUI
class GUI_Element:
    def __init__(self, gui, x=0, y=0, width=0, height=0, color=(255, 255, 255), mom = None):
        self.gui = gui # L'interface dans lequelle l'élément sera affiché
        self.x = x # Position x dans l'interface
        self.y = y # Position y dans l'interface
        self.width = width # Largeur du rectangle representant l'élément
        self.height = height # Hauteur du rectangle representant l'élément
        self.mom = mom # Element mère en cas de dépendance des éléments (example un bouton dans un interface, si on bouge l'interface on bouge le bouton)
        self.screenPos = [0, 0] # Position de l'écran
        self.game = self.gui.game # Le jeu associé à l'interface. (class World)
        self.mouseOn = False # La souris est sur l'élément ?
        self.actif = True # L'élément est activé ?
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    
    def update_rect(self):
        x = self.x + self.gui.x
        y = self.y + self.gui.y

        if self.mom is not None :
            x += self.mom.rect.x
            y += self.mom.rect.y

        x = (self.screenPos[0] * gridSizeX) + x
        y = (self.screenPos[1] * gridSizeY) + y

        self.rect = pygame.Rect(x, y, self.width, self.height)

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_size(self, width, height):
        self.width = width
        self.height = height

    def set_parent(self, parent):
        self.parent = parent

    def update(self):
        self.update_rect()

        if self.parent is not None:
            self.active = self.parent.active

        cursor_x, cursor_y = pygame.mouse.get_pos()
        if pygame.Rect(cursor_x - 3, cursor_y - 3, 5, 5).colliderect(self.rect): # Is the cursor on the element ?
            self.mouseOn = True
        else:
            self.mouseOn = False

class Frame(GUI_Element):
    def __init__(self, gui, x=0, y=0, w=0, h=0, color=(255, 255, 255), mom=None):
        super().__init__(gui, x, y, w, h, mom)
        self.color = color

    def set_color(self, color):
        self.color = color

    def draw(self):
        pygame.draw.rect(self.game.screen, self.color, self.rect)

    def update(self):
        if not self.active: return
        super().update()
        self.draw()

class Text(GUI_Element):
    def __init__(self, gui, x=0, y=0, color=(255, 255, 255), fontSize=28, text="Text", mom=None):
        super().__init__(gui, x, y, 0, 0, mom)
        self.color = color
        self.fontSize = fontSize
        self.text = text

        self.update_font()

        # state
        self.mouseOn = False

    # update the font (updating it every second will lag)
    def update_font(self):
        self.font = pygame.font.SysFont("Arial", self.fontSize)

    def set_color(self, color):
        self.color = color

    def get_width(self):
        return self.font.size(self.text)[0]

    def get_height(self):
        return self.font.size(self.text)[1]

    def set_font_size(self, size):
        self.fontSize = size
        self.update_font()

    def set_text(self, text):
        self.text = text

    def draw(self):
        surface = self.font.render(self.text, False, self.color)

        self.gui.game.screen.blit(surface, (self.rect.x, self.rect.y))

    def update(self):
        super().update()
        if not self.active: return
        self.draw()