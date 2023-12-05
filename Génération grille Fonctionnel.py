import pygame
pygame.init()
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w-200,infoObject.current_h-200))
done = False
zoom = 1
offsetx = 0
offsety = 0
value = 20



def iso_coord(x, y):
    return [x-y, (x+y)/2]


def display_tiles(offx, offy):
    TILE_SIZE = 16*zoom
    screen_x, screen_y = screen.get_size()
    for y in range(-value//2, value//2):
        for x in range(-value//2, value//2):
            new_tile = Tile(screen_x//4 + screen_y//2 + x*TILE_SIZE,screen_y//2 - screen_x//4 + y*TILE_SIZE)
            screen.blit(pygame.transform.scale_by(new_tile.image,zoom), (iso_coord(new_tile.rect.x, new_tile.rect.y)[0]+offx*TILE_SIZE,iso_coord(new_tile.rect.x, new_tile.rect.y)[1]+offy*TILE_SIZE))


class Tile():
    def __init__(self, x, y):
        self.image = pygame.image.load("Tile32x32.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

screen.fill("WHITE")
display_tiles(0, 0)
pygame.display.update()


while not done:
    for event in  pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEWHEEL:
            if event.y == 1:
                if zoom >= 3:
                    break
                else:
                    zoom+=0.15
            else:
                if zoom <= 0.5:
                    break
                else:
                    zoom-=0.15
            screen.fill("WHITE")
            display_tiles(offsetx, offsety)
            pygame.display.update()
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    if zoom == 3:
                        break
                    else:
                        zoom+=0.15
                elif event.key == pygame.K_o:
                    if zoom == 0.5:
                        break
                    else:
                        zoom -= 0.15
                elif event.key == pygame.K_UP:
                    offsety -= 1
                elif event.key == pygame.K_DOWN:
                    offsety += 1
                elif event.key == pygame.K_LEFT:
                    offsetx -= 1
                elif event.key == pygame.K_RIGHT:
                    offsetx += 1 
                screen.fill("WHITE")
                display_tiles(offsetx, offsety)
                pygame.display.update()


        

        


pygame.quit()