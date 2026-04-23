import pygame
import os
import math

pygame.init()

WIDTH, HEIGHT = 1200, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravitational Slingshot Effect")
pygame.display.set_icon(pygame.image.load(os.path.join("assets", "appicon.png")))

G = 5
FPS = 60
OBJ_SIZE = 5
VEL_SCALE = 100

MIN_ZOOM = 0.5
MAX_ZOOM = 2.5
ZOOM = 1.0

BG = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "spacebg.jpg")),
    (WIDTH, HEIGHT)
)

EARTH_IMG = pygame.image.load(os.path.join("assets", "planet1.png")).convert_alpha()
JUPITER_IMG = pygame.image.load(os.path.join("assets", "planet2.png")).convert_alpha()
PLUTO_IMG = pygame.image.load(os.path.join("assets", "planet3.png")).convert_alpha()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

GITHUB_TEXT = "GitHub: @shayaanthedev"

TRAIL_ENABLED = False

PLANET_OPTIONS = {
    "earth": {"mass": 350, "image": EARTH_IMG},
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


def world_to_screen(x, y):
    sx = (x - WIDTH // 2) * ZOOM + WIDTH // 2
    sy = (y - HEIGHT // 2) * ZOOM + HEIGHT // 2
    return int(sx), int(sy)


def screen_to_world(sx, sy):
    x = (sx - WIDTH // 2) / ZOOM + WIDTH // 2
    y = (sy - HEIGHT // 2) / ZOOM + HEIGHT // 2
    return x, y


def draw_github():
    font = pygame.font.SysFont("consolas", 24)
    text = font.render(GITHUB_TEXT, True, (180, 180, 180))
    win.blit(text, (10, HEIGHT - 30))


class Planet:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass

    def draw(self, image=None, size=None):
        if image is None:
            image = PLANET
        if size is None:
            size = PLANET_SIZE_CURRENT

        sx, sy = world_to_screen(self.x, self.y)
        scaled_size = max(1, int(size * ZOOM))

        scaled_img = pygame.transform.smoothscale(image, (scaled_size * 2, scaled_size * 2))
        win.blit(scaled_img, (sx - scaled_size, sy - scaled_size))


class Spacecraft:
    def __init__(self, x, y, vel_x, vel_y, mass):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass
        self.trail = []

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
        sx, sy = world_to_screen(self.x, self.y)
        scaled_size = max(1, int(OBJ_SIZE * ZOOM))
        pygame.draw.circle(win, RED, (sx, sy), scaled_size)

        if TRAIL_ENABLED:
            self.trail.append((self.x, self.y))

            if len(self.trail) > 200:
                self.trail.pop(0)

            for i in range(1, len(self.trail)):
                fade = int(255 * i / len(self.trail))
                x1, y1 = world_to_screen(*self.trail[i - 1])
                x2, y2 = world_to_screen(*self.trail[i])

                pygame.draw.line(
                    win,
                    (fade, fade, fade),
                    (x1, y1),
                    (x2, y2),
                    max(1, int(2 * ZOOM))
                )
        else:
            self.trail.clear()


def create_ship(location, mouse):
    t_x, t_y = location
    m_x, m_y = mouse
    vel_x = (m_x - t_x) / VEL_SCALE
    vel_y = (m_y - t_y) / VEL_SCALE
    return Spacecraft(t_x, t_y, vel_x, vel_y, SHIP_MASS)


def draw_info():
    font = pygame.font.SysFont("verdana", 28)
    info = PLANET_INFO[CURRENT_PLANET_KEY]
    text = f"{info['name']} | Mass: {info['mass_text']} | Radius: {info['radius']}"
    render = font.render(text, True, WHITE)
    win.blit(render, (10, 10))


def draw_hud():
    font = pygame.font.SysFont("verdana", 22)
    trail_status = font.render(f"Trail [T]: {'ON' if TRAIL_ENABLED else 'OFF'}", True, WHITE)
    zoom_status = font.render(f"Zoom [Scroll]: {ZOOM:.1f}x", True, WHITE)
    win.blit(trail_status, (WIDTH - 250, 10))
    win.blit(zoom_status, (WIDTH - 250, 38))


def draw_centered_text(font, text, y, color=WHITE):
    render = font.render(text, True, color)
    win.blit(render, (WIDTH // 2 - render.get_width() // 2, y))


def menu():
    global PLANET, PLANET_MASS, CURRENT_PLANET_KEY, PLANET_SIZE_CURRENT

    title_font = pygame.font.SysFont("arial", 44, bold=True)
    body_font = pygame.font.SysFont("arial", 24)
    small_font = pygame.font.SysFont("arial", 20)

    running = True

    while running:
        win.fill((0, 0, 0))

        draw_centered_text(title_font, "Gravitational Slingshot Effect", 40)
        pygame.draw.line(win, WHITE, (180, 105), (WIDTH - 180, 105), 2)

        draw_centered_text(body_font, "What is a gravitational slingshot?", 130)
        draw_centered_text(
            small_font,
            "It is when a spacecraft uses a planet's gravity to change speed and direction.",
            165
        )
        draw_centered_text(
            small_font,
            "The planet pulls the spacecraft, and the spacecraft can gain or lose speed from that motion.",
            192
        )

        pygame.draw.line(win, WHITE, (180, 235), (WIDTH - 180, 235), 2)

        draw_centered_text(body_font, "Select a planet", 255)

        draw_centered_text(body_font, "1. Earth", 310)
        draw_centered_text(small_font, "Balanced gravity and a good starting point.", 345)

        draw_centered_text(body_font, "2. Jupiter", 395)
        draw_centered_text(small_font, "Stronger pull, so the spacecraft bends more sharply.", 430)

        draw_centered_text(body_font, "3. Pluto", 480)
        draw_centered_text(small_font, "Weaker gravity, so the motion is softer and slower.", 515)

        pygame.draw.line(win, WHITE, (180, 560), (WIDTH - 180, 560), 2)

        draw_centered_text(body_font, "How to use the program", 580)
        draw_centered_text(small_font, "Press 1, 2, or 3 to choose a planet.", 615)
        draw_centered_text(
            small_font,
            "In the simulation, click once to set the ship start point, then click again to launch it.",
            642
        )
        draw_centered_text(
            small_font,
            "Press T to toggle trails and use the mouse wheel to zoom.",
            669
        )

        draw_centered_text(small_font, "Press the number key to start.", 720)

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
    global TRAIL_ENABLED, ZOOM

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
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # FIXED (no recursion)

                if event.key == pygame.K_t:
                    TRAIL_ENABLED = not TRAIL_ENABLED

            if event.type == pygame.MOUSEWHEEL:
                ZOOM = max(MIN_ZOOM, min(MAX_ZOOM, ZOOM + event.y * 0.1))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if temp_obj_pos:
                        world_start = screen_to_world(*temp_obj_pos)
                        world_mouse = screen_to_world(*mouse_pos)
                        obj = create_ship(world_start, world_mouse)
                        objects.append(obj)
                        temp_obj_pos = None
                    else:
                        temp_obj_pos = mouse_pos

        win.blit(BG, (0, 0))

        draw_info()
        draw_github()
        draw_hud()

        if temp_obj_pos:
            pygame.draw.line(win, WHITE, temp_obj_pos, mouse_pos, 2)
            pygame.draw.circle(win, RED, temp_obj_pos, OBJ_SIZE)

        for obj in objects[:]:
            obj.draw()
            obj.move(planet)

            sx, sy = world_to_screen(obj.x, obj.y)

            margin = int(200 / ZOOM)
            off_screen = sx < -margin or sx > WIDTH + margin or sy < -margin or sy > HEIGHT + margin

            collided = math.sqrt((obj.x - planet.x)**2 + (obj.y - planet.y)**2) <= PLANET_SIZE_CURRENT

            if off_screen or collided:
                objects.remove(obj)

        planet.draw()

        pygame.display.update()


if __name__ == "__main__":
    while True:  
        menu()
        main()
        ZOOM = 1.0