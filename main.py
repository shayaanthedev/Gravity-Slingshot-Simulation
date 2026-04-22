import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800,600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Slingshot Simulator")
pygame.display.set_icon(pygame.image.load("jpterpng.jpg"))


planet_mass = 100
ship_mass = 5
g = 5
fps = 60
planet_size = 50
obj_size = 5
vel_scale = 100

BG = pygame.transform.scale(pygame.image.load("spacebg.jpg"), (WIDTH, HEIGHT))
PLANET = pygame.transform.scale(pygame.image.load("jpterpng.jpg"), (planet_size*2, planet_size*2))

WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
BLACK = (0,0,0)

class Spacecraft:
    def __init__(self, x, y, vel_x, vel_y, mass):
        self.x=x
        self.y=y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass
    
    def move(self, planet=None):
        self.x == self.vel_x
        self.y == self.vel_y
    def draw(self):
        pygame.draw.circle(win, RED, (int(self.x), int(self.y), obj_size))

def main():
    running = True
    clock = pygame.time.Clock()

    objects = []
    temp_obj_pos = None

    while running:
        clock.tick(fps)

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if temp_obj_pos:
                    t_x, t_y = temp_obj_pos
                    obj = Spacecraft(t_x, t_y, 0, 0, ship_mass)
                    objects.append(obj)
                    temp_obj_pos = None
                else:
                    temp_obj_pos = mouse_pos


        win.blit(BG, (0,0))

        if temp_obj_pos:
            pygame.draw.circle(win, RED, temp_obj_pos, obj_size)
            pygame.draw.line(win, WHITE, temp_obj_pos, mouse_pos, 2)

        for obj in objects:
            obj.draw()
        pygame.display.update()


    pygame.quit()

if __name__=="__main__":
    main()