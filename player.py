import pygame
import pygame.mask
import pygame.gfxdraw
from pygame import mixer
import random
import os

pygame.init()


class Player(pygame.sprite.Sprite):
    keys1 = [pygame.K_e, pygame.K_q, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_LSHIFT, pygame.K_LCTRL,
             pygame.K_f]
    keys2 = [pygame.K_KP8, pygame.K_KP7, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN,
             pygame.K_RCTRL, pygame.K_KP9]

    goku_hit = pygame.mixer.Sound("Music/Goku Hit.ogg")
    goku_attack = pygame.mixer.Sound("Music/Goku Attack.ogg")
    vegeta_hit = pygame.mixer.Sound("Music/Vegeta Hit.ogg")
    vegeta_attack = pygame.mixer.Sound("Music/Vegeta Attack.ogg")
    goku_kamehameha = pygame.mixer.Sound("Music/Goku Kamehameha.ogg")
    vegeta_final_flash = pygame.mixer.Sound("Music/Vegeta Final Flash.ogg")

    goku_attack_voices = [goku_attack, goku_kamehameha]
    vegeta_attack_voices = [vegeta_attack, vegeta_final_flash]

    @classmethod
    def target_setter(cls, a, b):
        a.target = b
        b.target = a

    @classmethod
    def check_hit(cls, a, b):
        if a.mask.overlap(b.mask, (b.rect.x - a.rect.x, b.rect.y - a.rect.y)):
            if a.state == "Attack" and b.state == "Attack":
                a.health -= 1
                a.move(50 * a.flip, 0)
                b.health -= 1
                b.move(50 * b.flip, 0)
                a.hit = True
                b.hit = True
            elif a.state == "Attack" and b.hit is False and b.state != "Block":
                b.health -= a.damage
                b.move(50 * b.flip, 0)
                b.hit = True
                b.hit_sound.play()
            elif b.state == "Attack" and a.hit is False and a.state != "Block":
                a.health -= b.damage
                a.move(50 * a.flip, 0)
                a.hit = True
                a.hit_sound.play()

    def __init__(self, image, length, breadth, x, y, keys, hit_sound, attack_sound):
        super().__init__()
        self.target = None
        self.flip = None
        self.damage = 0
        self.animation_change = 1
        self.teleport_count = 0
        self.hit_sound = hit_sound
        self.attack_sound = attack_sound
        self.ki = True

        self.image = image
        self.sprite_dict = {}
        for sprite in os.listdir(path=fr"Characters\{self.image}"):
            frame_list = os.listdir(path=fr"Characters\{self.image}\{sprite}")
            frames = []
            for frame in frame_list:
                frames.append(
                    pygame.transform.scale_by(pygame.image.load(fr"Characters\{self.image}\{sprite}\{frame}"), 1.8))
            self.sprite_dict[f"{sprite}"] = frames

        self.keys = keys
        self.length = length
        self.breadth = breadth
        self.surface = pygame.Surface((length, breadth), 32)
        self.sprite_state = "Idle"
        self.character = self.sprite_dict[self.sprite_state][0]
        self.rect = self.surface.get_rect(bottomleft=(x, y))
        self.mask = pygame.mask.from_surface(self.surface)

        self.vel_y = 0
        self.health = 100
        self.ki_level = 100
        self.animation_count = 1
        self.sprite_index = 1
        self.state = "Idle"
        self.attack_state = False
        self.jump_state = False
        self.key_shift = False
        self.key_ctrl = False
        self.key_e = False
        self.key_q = False
        self.key_w = False
        self.key_s = False
        self.key_f = False
        self.hit = False
        self.locked = False
        self.animation_completed = False
        self.ki_blast_list = []

    def move(self, dx, dy):
        initial_x = 0
        gravity = 1.2

        self.vel_y += gravity
        initial_x += self.vel_y
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            dy = screen_height - 110 - self.rect.bottom
            self.jump_state = False

        self.rect.x += dx
        self.rect.y += dy

    def move_and_keys(self):
        key = pygame.key.get_pressed()
        if self.locked is False:
            if key[self.keys[0]]:
                self.key_e = True
            else:
                self.key_e = False
            if key[self.keys[1]]:
                self.key_q = True
            else:
                self.key_q = False
            if key[self.keys[2]]:
                self.key_w = True
            else:
                self.key_w = False
            if key[self.keys[3]]:
                self.key_s = True
            else:
                self.key_s = False
            if key[self.keys[4]]:
                if self.state != "Attack":
                    self.move(-5, 0)
                if self.jump_state is False:
                    self.sprite_state = "Walk_Back"
            if key[self.keys[5]]:
                if self.state != "Attack":
                    self.move(5, 0)
                if self.jump_state is False:
                    self.sprite_state = "Walk"
            if key[self.keys[6]]:
                self.key_shift = True
            else:
                self.key_shift = False
            if key[self.keys[7]]:
                self.key_ctrl = True
            else:
                self.key_ctrl = False
            if key[self.keys[8]]:
                self.key_f = True
            else:
                self.key_f = False

            if self.key_w and self.jump_state is False:
                self.animation_count = 0
                self.vel_y = -30
                self.jump_state = True
                self.state = "Jump"
                self.sprite_state = "Jump"
                self.teleport_count = 1
            self.move(0, self.vel_y)

    def attacks(self, target):
        if self.hit is True:
            self.state = "Hit"
            self.sprite_state = "Hit_Recover"

        if self.hit is False:
            if self.key_e is True:
                if self.key_shift is True:
                    if self.rect.x <= target:
                        self.move(20, 0)
                    else:
                        self.move(-20, 0)
                    self.state = "Attack"
                    self.sprite_state = "Dash_Punch"
                    self.damage = 1
                elif self.key_w is True and self.jump_state is False:
                    self.jump_state = True
                    self.state = "Attack"
                    self.sprite_state = "Up_Punch"
                    self.damage = 1
                elif self.key_s is True:
                    self.state = "Attack"
                    self.sprite_state = "Low_Punch"
                    self.damage = 1
                elif self.key_ctrl is True:
                    self.state = "Attack_Ki_Blast"
                    self.sprite_state = "Ki_Blast"
                    self.damage = 5
                else:
                    self.state = "Attack"
                    self.sprite_state = "Punch"
                    self.damage = 1

            if self.key_shift is True:
                if self.key_e is True:
                    if self.rect.x <= target:
                        self.move(20, 0)
                    else:
                        self.move(-20, 0)
                    self.state = "Attack"
                    self.sprite_state = "Dash_Punch"
                    self.damage = 1
                elif self.key_q is True:
                    if self.rect.x <= target:
                        self.move(20, 0)
                    else:
                        self.move(-20, 0)
                    self.state = "Attack"
                    self.sprite_state = "Dash_Elbow"
                    self.damage = 2

            if self.key_q is True:
                if self.key_shift is True:
                    if self.rect.x <= target:
                        self.move(20, 0)
                    else:
                        self.move(-20, 0)
                    self.state = "Attack"
                    self.sprite_state = "Dash_Elbow"
                    self.damage = 2
                elif self.key_w is True:
                    self.state = "Attack"
                    self.sprite_state = "Up_Kick"
                    self.damage = 2
                elif self.key_s is True:
                    self.state = "Attack"
                    self.sprite_state = "Low_Kick"
                    self.damage = 2
                elif self.key_ctrl is True:
                    self.state = "Attack_Ki_Blast"
                    self.sprite_state = "Ki_Blast_Short"
                    self.damage = 3
                else:
                    self.state = "Attack"
                    self.sprite_state = "Kick"
                    self.damage = 2

            if self.key_s is True:
                if self.key_e is True:
                    self.sprite_state = "Low_Punch"
                    self.state = "Attack"
                    self.damage = 1
                elif self.key_q is True:
                    self.sprite_state = "Low_Kick"
                    self.state = "Attack"
                    self.damage = 2
                else:
                    self.sprite_state = "Up_Block"
                    self.state = "Block"
                    self.damage = 0

            if self.state != "Jump" and self.key_f is True and self.key_shift is True and self.teleport_count == 1:
                self.teleport_count -= 1
                self.rect.x = self.target.rect.x - 50 * self.flip

            elif self.state != "Jump" and self.key_f is True and self.ki_level >= 50:
                self.sprite_state = "Special"
                self.state = "Attack_Ki_Blast"
                self.damage = 20

            if self.state == "Idle" or "Attack":
                if self.key_e is True and self.key_q is True:
                    self.sprite_state = "Ki_Charge"
                    self.ki_level += 0.05
                    if self.ki_level >= 100:
                        self.ki_level = 100
                    elif self.ki_level <= 0:
                        self.ki_level = 0

    def drawer(self):
        self.surface = pygame.Surface((self.length, self.breadth), pygame.SRCALPHA, 32)
        _, _, width, height = self.character.get_rect()
        self.surface.blit(self.character, ((self.length - width) / 2, self.breadth - height))
        screen.blit(self.turn(self.surface), self.rect)

    def animate(self):
        animation_delay = 7
        if self.sprite_index >= len(self.sprite_dict[self.sprite_state]) - 1:
            self.animation_count = 0
            self.animation_completed = True
            # self.sprite_state = "Idle"

        self.sprite_index = (self.animation_count // animation_delay) % len(self.sprite_dict[self.sprite_state])
        self.animation_count += self.animation_change
        if self.sprite_state == "Ki_Charge" or self.sprite_state == "Special":
            screen.blit(self.sprite_dict["Ki_Charge_Aura"][random.randint(0, 2)],
                        (self.rect.left - 50, self.rect.bottom - 380))
        self.character = self.sprite_dict[self.sprite_state][self.sprite_index]
        self.mask = pygame.mask.from_surface(self.surface)

    def reset(self):
        self.sprite_index = 0
        self.animation_count = 0
        if self.state == "Attack":
            if self.key_q is True or self.key_e is True:
                self.state = "Attack"
                self.attack_sound[0].play()
            else:
                self.state = "Idle"

        if self.state == "Attack_Ki_Blast":
            self.ki = True
            self.locked = False
            self.state = "Idle"

        if self.state == "Block":
            self.state = "Idle"

        if self.state == "Jump":
            if self.rect.y <= 600:
                self.state = "Idle"

        if self.state == "Hit":
            self.state = "Idle"
            self.hit = False

        if self.state == "Idle" and self.sprite_state != "Walk":
            self.sprite_state = "Idle"
        elif self.state == "Idle":
            self.sprite_state = "Idle"

    def turn(self, sprite):
        if self.target.rect.centerx < self.rect.centerx:
            self.flip = 1
            return sprite
        else:
            self.flip = -1
            return pygame.transform.flip(sprite, True, False)

    def blast(self, form="", speed=12):
        if self.ki_level >= 20:
            if self.state == "Attack_Ki_Blast" and self.sprite_state != "Ki_Charge":
                self.ki_blast_list.append(KiBlast(self, form, x_speed=speed))
                self.ki = False
                self.damage = 3
                if form == "Short_":
                    self.ki_level -= 5
                else:
                    self.ki_level -= 10

    def loop(self, target=0):
        self.move_and_keys()
        self.attacks(target)
        self.animate()
        if self.state == "Attack_Ki_Blast" and self.sprite_index >= min(5, len(
                self.sprite_dict[self.sprite_state]) // 3) and self.ki is True:
            if self.key_q is True:
                self.state = "Attack_Ki_Blast"
                self.blast("Short_")
                self.attack_sound[0].play()
            elif self.key_e is True:
                self.state = "Attack_Ki_Blast"
                self.blast()
                self.attack_sound[0].play()
            elif self.key_f is True:
                self.state = "Attack_Ki_Blast"
                self.blast("Special_", speed=7)
                self.locked = True
                self.attack_sound[1].play()

        if self.ki_blast_list:
            for ki in self.ki_blast_list:
                ki.loop()
                if ki.form != "Special_":
                    if ki.rect.x <= 0 or ki.rect.x >= screen_width:
                        self.ki_blast_list.remove(ki)
                else:
                    if self.animation_completed:
                        self.ki_blast_list.remove(ki)
        if self.animation_completed is True:
            self.reset()
            self.attacks(target)
            self.animation_completed = False
        self.drawer()


class KiBlast:
    def __init__(self, character, form="", start=False, x_speed=12):
        self.character = character
        self.ki_blast_sprites = character.sprite_dict[f"Ki_Blast_{form}Animation"]
        self.form = form
        self.start = start
        self.x_speed = x_speed
        self.surface = pygame.Surface((300, 300), pygame.SRCALPHA, 32)
        self.x = 100
        self.y = 90
        self.rect_setter()
        self.index = 0
        self.animation_count = 0
        self.mask = pygame.mask.from_surface(self.ki_blast_sprites[self.index])

    def rect_setter(self):
        if self.form == "":
            self.rect = self.ki_blast_sprites[0].get_rect(center=(
                self.character.rect.centerx - 0.375 * self.character.breadth * self.character.flip,
                self.character.rect.centery - 0.2 * self.character.length))
        elif self.form == "Short_":
            self.rect = self.ki_blast_sprites[0].get_rect(center=(
                self.character.rect.centerx - 0.375 * self.character.breadth * self.character.flip,
                self.character.rect.centery - 0.05 * self.character.length))
        elif self.form == "Special_":
            self.rect = self.ki_blast_sprites[0].get_rect(center=(
                self.character.rect.centerx - 0.6 * self.character.breadth * self.character.flip,
                self.character.rect.centery - 0.001 * self.character.length))

    def move(self):
        if self.start:
            pass
        else:
            self.rect.x += self.character.flip * -self.x_speed

    def drawer(self):
        self.surface = pygame.Surface((300, 300), pygame.SRCALPHA, 32)
        if self.character.flip == 1:
            self.surface.blit(pygame.transform.flip(self.ki_blast_sprites[self.index], True, False), (0, 0))
        else:
            self.surface.blit(self.ki_blast_sprites[self.index], (0, 0))
        screen.blit(self.surface, self.rect)

    def special(self):
        self.surface_2 = pygame.Surface((self.x, self.y), pygame.SRCALPHA, 32)
        self.surface_2.blit(
            pygame.transform.scale(self.character.sprite_dict["Ki_Blast_Special_Animation"][1], (self.x, self.y)),
            (0, 0))
        if self.character.flip == 1:
            screen.blit(self.surface_2, (self.rect.x, self.rect.y))
            screen.blit((self.character.sprite_dict["Ki_Blast_Special_Animation"][0]),
                        self.ki_blast_sprites[0].get_rect(center=(
                            self.character.rect.centerx + 0.6 * self.character.breadth * -self.character.flip,
                            self.character.rect.centery + 0.001 * self.character.length)))
        else:
            screen.blit(self.surface_2, (self.rect.x - self.x + 100, self.rect.y))
            screen.blit(pygame.transform.flip(self.character.sprite_dict["Ki_Blast_Special_Animation"][0], True, False),
                        self.ki_blast_sprites[0].get_rect(center=(
                            self.character.rect.centerx + max(0.6 * self.character.breadth * -self.character.flip, -80),
                            self.character.rect.centery)))

    def collision(self):
        if self.mask.overlap(self.character.target.mask,
                             (self.character.target.rect.x - self.rect.x, self.character.target.rect.y - self.rect.y)):
            self.character.target.hit = True
            if self.form == "Special_":
                self.character.damage = 0.3
            self.character.target.health -= self.character.damage
            if self.form != "Special_":
                self.character.ki_blast_list.remove(self)
            self.character.target.move(100 * self.character.target.flip, 0)
            if self.character.target.state == "Block" and self.form == "Short_":
                self.character.target.health += self.character.damage
                self.character.target.hit = False
                self.character.target.move(-50 * self.character.target.flip, 0)

    def loop(self):
        self.move()
        if self.form == "Special_":
            self.special()
            self.x += self.x_speed
        self.drawer()
        self.collision()


def background_animator():
    bg_list = os.listdir(path=fr"Backgrounds")
    if random.randint(1, 3) % 3 == 0:
        bg_name = "Dragon"
        bg_frame_list = os.listdir(path=fr"Backgrounds/{bg_name}")
    else:
        bg_name = random.choice(bg_list)
        bg_frame_list = os.listdir(path=fr"Backgrounds/{bg_name}")
    bg_frames = []
    for frame in bg_frame_list:
        bg_frames.append(pygame.transform.scale(pygame.image.load(fr"Backgrounds/{bg_name}/{frame}"),
                                                (screen_width, screen_height)))
    return bg_frames


pygame.init()
pygame.display.set_caption("Fighter Ball Z")
size = screen_width, screen_height = 1280, 720
background_frames = background_animator()
hp_bar = pygame.image.load("Textures/DataBar.png")
ki_bar = pygame.transform.scale(pygame.image.load("Textures/DataBar.png"), (260, 28))
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

# Load and Play music 1 once and then music 2 endlessly
mixer.music.load("Music/Unwinnable Battle.mp3")
mixer.music.play()
mixer.music.queue("Music/Ultra Instinct Theme.mp3", loops=-1)
mixer.music.set_volume(0.8)

goku = "Goku"
vegeta = "Vegeta"

player1 = Player(vegeta, 260, 260, 20, 610, Player.keys1, Player.vegeta_hit, Player.vegeta_attack_voices)
player2 = Player(goku, 320, 320, 1000, 610, Player.keys2, Player.goku_hit, Player.goku_attack_voices)

player1_bg = pygame.transform.scale(player1.sprite_dict["Start_Screen"][0], (1280, 355))
player2_bg = pygame.transform.scale(player2.sprite_dict["Start_Screen"][0], (1280, 355))
versus_bg = pygame.image.load("Textures/VS.png")
running = True


def main():
    global running
    Player.target_setter(player1, player2)
    animation_count_ex = 0
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        sprite_index_ex = (animation_count_ex // 7) % len(background_frames)
        animation_count_ex += 1
        background = background_frames[sprite_index_ex]

        screen.blit(background, (0, 0))

        pygame.gfxdraw.filled_polygon(screen, [(61, 53), (61 + 420 * player1.health / 100, 53),
                                               (43 + 420 * player1.health / 100, 91), (43, 91)], (253, 126, 11))
        pygame.gfxdraw.filled_polygon(screen, [(801 + 420 * (100 - player2.health) / 100, 53), (1221, 53),
                                               (1239, 91), (819 + 420 * (100 - player2.health) / 100, 91)], (253, 126, 11))

        pygame.gfxdraw.filled_polygon(screen, [(40, 92), (40 + 197 * player1.ki_level / 100, 92),
                                               (30 + 197 * player1.ki_level / 100, 113), (30, 113)], (255, 255, 0))
        pygame.gfxdraw.filled_polygon(screen, [(1044 + 197 * (100 - player2.ki_level) / 100, 92), (1241, 92),
                                               (1251, 113), (1054 + 197 * (100 - player2.ki_level) / 100, 113)],
                                      (255, 255, 0))

        screen.blit(hp_bar, (25, 52))
        screen.blit(pygame.transform.flip(hp_bar, True, False), (795, 52))

        player1.loop(player1.rect.x)
        player2.loop(player2.rect.x)
        Player.check_hit(player1, player2)

        if pygame.time.get_ticks() <= 3001:
            screen.blit(player1_bg, (0, 0))
            screen.blit(pygame.transform.flip(player2_bg, True, False), (0, 365))
            pygame.draw.rect(screen, (0, 0, 0), (0, 355, 1280, 10))
            screen.blit(versus_bg, (452, 0))

        # print(f"{player1.image} is {player1.state}")
        # print(f"{player2.image} is {player2.state}")
        if player1.health <= 0:
            print("Player 2 WON")
            running = False
        elif player2.health <= 0:
            print("Player 1 WON")
            running = False
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
