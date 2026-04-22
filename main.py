import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravitational Slingshot Effect")
pygame.display.set_icon(pygame.image.load("planet1.png"))

G = 5
FPS = 60
OBJ_SIZE = 5
VEL_SCALE = 100

BG = pygame.transform.scale(pygame.image.load("spacebg.jpg"), (WIDTH, HEIGHT))

EARTH_IMG = pygame.transform.scale(pygame.image.load("planet1.png"), (100, 100))
JUPITER_IMG = pygame.transform.scale(pygame.image.load("planet2.png"), (160, 160))
PLUTO_IMG = pygame.transform.scale(pygame.image.load("planet3.png"), (80, 80))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

GITHUB_TEXT = "GitHub: @shayaanthedev"

PLANET_OPTIONS = {
    "earth": {"mass": 100, "image": EARTH_IMG},
    "jupiter": {"mass": 750, "image": JUPITER_IMG},
    "pluto": {"mass": 40, "image": PLUTO_IMG}
}

PLANET_INFO = {
    "earth": {
        "name": "Earth",
        "mass_text": "5.97 x 10^24 kg",
        "radius": "6,371 km"
    },
    "jupiter": {
        "name": "Jupiter",
        "mass_text": "1.90 x 10^27 kg",
        "radius": "69,911 km"
    },
    "pluto": {
        "name": "Pluto",
        "mass_text": "1.31 x 10^22 kg",
        "radius": "1,188 km"
    }
}

PLANET_SIZES = {
    "earth": 50,
    "jupiter": 80,
    "pluto": 40
}

CURRENT_PLANET_KEY = "earth"
PLANET_SIZE_CURRENT = 50
PLANET = EARTH_IMG
PLANET_MASS = 100

SHIP_MASS = 5


def draw_github():
    font = pygame.font.SysFont(None, 24)
    text = font.render(GITHUB_TEXT, True, (180, 180, 180))
    win.blit(text, (10, HEIGHT - 30))


class Planet:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass

    def draw(self):
        size = PLANET_SIZE_CURRENT
        win.blit(PLANET, (self.x - size, self.y - size))


class Spacecraft:
    def __init__(self, x, y, vel_x, vel_y, mass):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass

    def move(self, planet):
        distance = math.sqrt((self.x - planet.x)**2 + (self.y - planet.y)**2)

        if distance == 0:
            return

        force = (G * self.mass * planet.mass) / distance ** 2
        acceleration = force / self.mass
        angle = math.atan2(planet.y - self.y, planet.x - self.x)

        self.vel_x += acceleration * math.cos(angle)
        self.vel_y += acceleration * math.sin(angle)

        self.x += self.vel_x
        self.y += self.vel_y

    def draw(self):
        pygame.draw.circle(win, RED, (int(self.x), int(self.y)), OBJ_SIZE)


def create_ship(location, mouse):
    t_x, t_y = location
    m_x, m_y = mouse
    vel_x = (m_x - t_x) / VEL_SCALE
    vel_y = (m_y - t_y) / VEL_SCALE
    return Spacecraft(t_x, t_y, vel_x, vel_y, SHIP_MASS)


def draw_info():
    font = pygame.font.SysFont(None, 28)
    info = PLANET_INFO[CURRENT_PLANET_KEY]
    text = f"{info['name']} | Mass: {info['mass_text']} | Radius: {info['radius']}"
    render = font.render(text, True, WHITE)
    win.blit(render, (10, 10))


def menu():
    global PLANET, PLANET_MASS, CURRENT_PLANET_KEY, PLANET_SIZE_CURRENT

    font = pygame.font.SysFont(None, 50)
    running = True

    while running:
        win.fill((0, 0, 0))

        title = font.render("Select Planet", True, WHITE)
        win.blit(title, (WIDTH//2 - 150, 100))

        earth_text = font.render("1. Earth", True, BLUE)
        jupiter_text = font.render("2. Jupiter", True, BLUE)
        pluto_text = font.render("3. Pluto", True, BLUE)

        win.blit(earth_text, (WIDTH//2 - 100, 200))
        win.blit(jupiter_text, (WIDTH//2 - 100, 300))
        win.blit(pluto_text, (WIDTH//2 - 100, 400))

        draw_github()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:
                    PLANET = PLANET_OPTIONS["earth"]["image"]
                    PLANET_MASS = PLANET_OPTIONS["earth"]["mass"]
                    CURRENT_PLANET_KEY = "earth"
                    PLANET_SIZE_CURRENT = PLANET_SIZES["earth"]
                    running = False

                if event.key == pygame.K_2:
                    PLANET = PLANET_OPTIONS["jupiter"]["image"]
                    PLANET_MASS = PLANET_OPTIONS["jupiter"]["mass"]
                    CURRENT_PLANET_KEY = "jupiter"
                    PLANET_SIZE_CURRENT = PLANET_SIZES["jupiter"]
                    running = False

                if event.key == pygame.K_3:
                    PLANET = PLANET_OPTIONS["pluto"]["image"]
                    PLANET_MASS = PLANET_OPTIONS["pluto"]["mass"]
                    CURRENT_PLANET_KEY = "pluto"
                    PLANET_SIZE_CURRENT = PLANET_SIZES["pluto"]
                    running = False


def main():
    menu()

    running = True
    clock = pygame.time.Clock()

    planet = Planet(WIDTH // 2, HEIGHT // 2, PLANET_MASS)
    objects = []
    temp_obj_pos = None

    while running:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main()
                    return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if temp_obj_pos:
                    obj = create_ship(temp_obj_pos, mouse_pos)
                    objects.append(obj)
                    temp_obj_pos = None
                else:
                    temp_obj_pos = mouse_pos

        win.blit(BG, (0, 0))

        draw_info()
        draw_github()

        if temp_obj_pos:
            pygame.draw.line(win, WHITE, temp_obj_pos, mouse_pos, 2)
            pygame.draw.circle(win, RED, temp_obj_pos, OBJ_SIZE)

        for obj in objects[:]:
            obj.draw()
            obj.move(planet)

            off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
            collided = math.sqrt((obj.x - planet.x)**2 + (obj.y - planet.y)**2) <= PLANET_SIZE_CURRENT

            if off_screen or collided:
                objects.remove(obj)

        planet.draw()

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()