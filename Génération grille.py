import pygame
pygame.init()
screen = pygame.display.set_mode((800,800))
done = False
TILE_SIZE = 16

def iso_coord(x, y):
    return (x-y, (x+y)/2)

def update_window(window):
    window.fill((255,255,255))
    pygame.display.update()


def display_tiles(screen, value):
    screen_x, screen_y = screen.get_size()
    for y in range(-value//2, value//2):
        for x in range(-value//2, value//2):
            new_tile = Tile(screen_x//4 + screen_y//2 + x*TILE_SIZE,screen_y//2 - screen_x//4 + y*TILE_SIZE)
            screen.blit(new_tile.image, iso_coord(new_tile.rect.x, new_tile.rect.y))





class Tile():
    def __init__(self, x, y):
        self.image = pygame.image.load("Tile32x32.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        


update_window(screen)
display_tiles(screen,20)
pygame.display.update()


while not done:
    for event in  pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
