import pygame
pygame.init()
screen = pygame.display.set_mode((600,600))
done = False
TILE_SIZE = 16

def iso_coord(x, y):
    return (x-y, (x+y)/2)

def update_window(window):
    window.fill((255,255,255))
    pygame.display.update()

def loadLVL(lvl):
    f = open(lvl, "r")
    data = f.readlines()
    t = []
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == "0":
                t.append(Tile(x,y))
    return t

def render(object, screen):
    screen.blit(object.image, iso_coord(object.rect.x, object.rect.y))
    pygame.display.update()

class Tile():
    def __init__(self, x, y):
        self.image = pygame.image.load("Real Tile.png")
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE


update_window(screen)
tiles = loadLVL("lvl.txt")
for tile in tiles:
    render(tile, screen)

while done == False:
    for event in  pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


