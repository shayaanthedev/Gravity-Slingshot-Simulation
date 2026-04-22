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

class Planet:
    def __init__(self, x ,y, mass):
        self.x=x
        self.y=y
        self.mass=mass
    
    def draw(self):
        win.blit(PLANET, (self.x - planet_size, self.y-planet_size))


class Spacecraft:
    def __init__(self, x, y, vel_x, vel_y, mass):
        self.x=x
        self.y=y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass
    
    def move(self, planet=None):
        distance = math.sqrt((self.x - planet.x)**2 + (self.y - planet.y)**2)
        force = (g * self.mass * planet.mass) / distance ** 2
        acceleration = force / self.mass
        angle = math.atan2(planet.y - self.y, planet.x - self.x)

        acceleration_x = acceleration * math.cos(angle)
        acceleration_y = acceleration * math.sin(angle)

        self.vel_x += acceleration_x
        self.vel_y += acceleration_y 

        self.x += self.vel_x
        self.y += self.vel_y

    def draw(self):
        pygame.draw.circle(win, RED, (int(self.x), int(self.y)), obj_size)

def create_ship(Location, mouse):
    t_x, t_y = Location
    m_x, m_y = mouse
    vel_x = (m_x - t_x)/vel_scale
    vel_y = (m_y - t_y)/vel_scale
    obj = Spacecraft(t_x, t_y, vel_x, vel_y, ship_mass)
    return obj


def main():
    running = True
    clock = pygame.time.Clock()

    planet=Planet(WIDTH//2,HEIGHT//2,planet_mass)
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
                    obj = create_ship(temp_obj_pos, mouse_pos)
                    objects.append(obj)
                    temp_obj_pos = None
                else:
                    temp_obj_pos = mouse_pos


        win.blit(BG, (0,0))

        if temp_obj_pos:
            pygame.draw.line(win, WHITE, temp_obj_pos, mouse_pos, 2)
            pygame.draw.circle(win, RED, temp_obj_pos, obj_size)


        for obj in objects[:]:
            obj.draw()
            obj.move(planet)
            offscreen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
            collided = math.sqrt((obj.x - planet.x)**2 + (obj.y - planet.y)**2) <= planet_size
            if offscreen or collided:
                objects.remove(obj)

        planet.draw()


        pygame.display.update()


    pygame.quit()

if __name__=="__main__":
    main()