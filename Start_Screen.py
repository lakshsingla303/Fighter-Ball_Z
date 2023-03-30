import os
import pygame
import random
from pygame import mixer

# Initialization of pygame and Basic variables
pygame.init()
pygame.display.set_caption("Fighter Ball Z")
size = width, height = 1280, 720
state = 1

# Loading textures
logo = pygame.image.load("Textures/DBFZ Logo.png")
marker = pygame.image.load("Textures/DB4.png")

# Background music
mixer.music.load("Music/Faulconer, Bruce - Perfect Cell Theme.flac")
mixer.music.play(-1)
selection = pygame.mixer.Sound("Music/Menu Selection Click.wav")
mixer.music.set_volume(0.6)


class Text:
    # Location of text on screen
    start_x = 530
    start_y = 310
    options_x = 480
    options_y = 410
    exit_x = 560
    exit_y = 510
    marker_x = 0
    marker_y = 0
    global state

    @classmethod  # Text Displayer
    def display_text(cls, screen, text, x_pos, y_pos, font, font_size=70, colour=(255, 255, 255)):
        screen_font = pygame.font.Font(font, font_size)
        home_screen_start = screen_font.render(str(text), True, colour)
        screen.blit(home_screen_start, (x_pos, y_pos))

    @classmethod  # State change definer
    def screen_state(cls, screen):
        if state == 1:
            cls.display_text(screen, "START", cls.start_x, cls.start_y, "freesansbold.ttf", colour=(0, 0, 0))
            cls.display_text(screen, "OPTIONS", cls.options_x, cls.options_y, "freesansbold.ttf")
            cls.display_text(screen, "EXIT", cls.exit_x, cls.exit_y, "freesansbold.ttf")
            cls.marker_x = cls.start_x - 80
            cls.marker_y = cls.start_y
        elif state == 2:
            cls.display_text(screen, "START", cls.start_x, cls.start_y, "freesansbold.ttf")
            cls.display_text(screen, "OPTIONS", cls.options_x, cls.options_y, "freesansbold.ttf", colour=(0, 0, 0))
            cls.display_text(screen, "EXIT", cls.exit_x, cls.exit_y, "freesansbold.ttf")
            cls.marker_x = cls.options_x - 80
            cls.marker_y = cls.options_y
        else:
            cls.display_text(screen, "START", cls.start_x, cls.start_y, "freesansbold.ttf")
            cls.display_text(screen, "OPTIONS", cls.options_x, cls.options_y, "freesansbold.ttf")
            cls.display_text(screen, "EXIT", cls.exit_x, cls.exit_y, "freesansbold.ttf", colour=(0, 0, 0))
            cls.marker_x = cls.exit_x - 80
            cls.marker_y = cls.exit_y


class LinearMovement:
    def __init__(self, image, length, breadth, initial_x=0, initial_y=0, dx=float(0), dy=float(0), angle=float(0)):
        self.initial_x = initial_x
        self.initial_y = initial_y
        self.image = image
        self.length = length
        self.breadth = breadth
        self.dx = dx
        self.dy = dy
        self.angle = angle

        self.rotation = 0
        self.surface = pygame.Surface((self.length, self.breadth), pygame.SRCALPHA, 32)
        self.rect = self.surface.get_rect(center=(self.initial_x, self.initial_y))

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.rotation += self.angle

    def re_spawn(self):
        if self.rect.bottom >= height:
            self.rect.y -= random.randint(1000, 10000)

    def draw(self):
        self.surface = pygame.Surface((self.length, self.breadth), pygame.SRCALPHA, 32)
        self.surface.blit(pygame.transform.rotate(self.image, self.rotation), (0, 0))
        screen.blit(self.surface, self.rect)

    def loop(self, respawning=0):
        self.move()
        if respawning == 1:
            self.re_spawn()
        self.draw()

    def check_bounded(self):
        if self.rect.x <= 0 or self.rect.x >= width:
            self.dx *= -1


sprite_sheet = []
ANIMATION_DELAY = 3
animation_count = 1
for i in [1, 2, 3, 4, 5]:
    sprite_sheet.append(pygame.image.load(f"Textures/t{i}.png"))


def animate(screen):
    global animation_count, running
    sprite_index = (animation_count // ANIMATION_DELAY) % len(sprite_sheet)
    sprite = sprite_sheet[sprite_index]
    animation_count += 1
    screen.blit(sprite, (0, 0))
    if sprite_index == len(sprite_sheet) - 1:
        running = False


# Dragon Ball variables
db_list = ["DB1.png", "DB2.png", "DB3.png", "DB4.png", "DB5.png", "DB6.png", "DB7.png"]
number_of_balls = 49
dragon_ball_list = []

# List maker for Dragon Balls
for i in range(number_of_balls):
    random_ball = random.choice(db_list)
    if random.randint(1, 10) <= 6:
        random_ball = pygame.transform.scale(pygame.image.load(fr"Textures/{random_ball}"), (40, 40))
    elif random.randint(1, 2) % 2 == 0:
        random_ball = pygame.image.load(fr"Textures/{random_ball}")
    else:
        random_ball = pygame.transform.scale(pygame.image.load(fr"Textures/{random_ball}"), (30, 30))
    dragon_ball = LinearMovement(random_ball, 60, 60, random.randint(0, 1280), random.randint(-10000, -1000),
                                 dy=random.randint(1000, 5000) / 1000, angle=0.5)
    dragon_ball_list.append(dragon_ball)

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

animation = False
running = True

bg_frames = []
for frame in os.listdir(path=fr"Textures/Shenron"):
    bg_frames.append(pygame.transform.scale(pygame.image.load(fr"Textures/Shenron/{frame}"), size))
animation_count_ex = 0

while running:
    sprite_index_ex = (animation_count_ex // 4) % len(bg_frames)
    animation_count_ex += 1
    background = bg_frames[sprite_index_ex]

    screen.blit(background, (0, 0))
    # QUIT PROGRAM LOOP
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if state != 3:
                    state = state + 1
                    selection.play()
            if event.key == pygame.K_UP:
                if state != 1:
                    state = state - 1
                    selection.play()
            if event.key == pygame.K_RETURN:
                animation = True

    screen.blit(background, (0, 0))

    for ball in dragon_ball_list:
        ball.loop(1)

    screen.blit(logo, (390, 30))
    screen.blit(marker, (Text.marker_x, Text.marker_y))
    Text.screen_state(screen)
    if animation:
        animate(screen)

    clock.tick(60)
    pygame.display.flip()
