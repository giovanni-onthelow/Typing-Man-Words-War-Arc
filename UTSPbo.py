import copy
import pygame
import random
import math
#import nltk

pygame.init()
# Menggunakan NLTK
from nltk.corpus import words

wordlist = words.words()
len_indexes = []
length = 1

wordlist.sort(key=len)
for i in range(len(wordlist)):
    if len(wordlist[i]) > length:
        length += 1
        len_indexes.append(i)
len_indexes.append(len(wordlist))

#Inisialisasi
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Typing Man : Words War Arc')
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
timer = pygame.time.Clock()
fps = 60
score = 0
pz = True
new_level = True
submit = ''
active_string = ''
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
           'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
# letters 2, 3, 4, 5, 6, 7, 8
choices = [False, True, False, False, False, False, False]

# Load font
header_font = pygame.font.Font('asset/undertale-deltarune-extended-fixed.otf', 30)
pause_font = pygame.font.Font('asset/1up.ttf', 38)
banner_font = pygame.font.Font('asset/1up.ttf', 28)
font = pygame.font.Font('asset/undertale-deltarune-extended-fixed.otf', 28)

# Load image
img_player = pygame.image.load('asset/karakter.png')
img_player = pygame.transform.scale(img_player, (300, 300))
img_background = pygame.image.load('asset/background.png')
img_background = pygame.transform.scale(img_background, (800, 600))

# music and sounds
pygame.mixer.init()

pygame.mixer.music.load('asset/sound/in the pool.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)
click = pygame.mixer.Sound('asset/sound/click.mp3')
woosh = pygame.mixer.Sound('asset/sound/Swoosh.mp3')
wrong = pygame.mixer.Sound('asset/sound/Instrument Strum.mp3')
click.set_volume(0.3)
woosh.set_volume(0.2)
wrong.set_volume(0.3)

# game variables
level = 1
lives = 5
word_objects = []
bullet_list = []

# High score
file = open('high_score.txt', 'r')
read = file.readlines()
high_score = int(read[0])
file.close()

# Daftar kata khusus untuk kata boss dan kata bomb
boss_word = [
    "apocalypse", "terminator", "destruction", "nightmare",
    "juggernaut", "unstoppable", "catastrophe", "leviathan"
]
bomb_word = [
    "boom", "bang", "pow", "zap", "crash",
    "smash", "blast", "kaboom", "doooom"
]

# CLASS

# PARENT CLASS Word
class Word:
    def __init__(self, text, speed, y_pos, x_pos):
        self.text = text
        self.speed = speed
        self.y_pos = y_pos
        self.x_pos = x_pos
        self.color = 'white'
        self.is_targeted = False

    def draw(self):
        if self.is_targeted:
            screen.blit(font.render(self.text, True, 'gray'), (self.x_pos, self.y_pos))
        else:
            screen.blit(font.render(self.text, True, self.color), (self.x_pos, self.y_pos))

            act_len = len(active_string)
            if active_string == self.text[:act_len]:
                screen.blit(font.render(active_string, True, 'green'), (self.x_pos, self.y_pos))

    def update(self):
        self.x_pos -= self.speed


# CHILD CLASS Word: Kata Boss
class WordBoss(Word):
    def __init__(self, text, speed, y_pos, x_pos):
        super().__init__(text, speed, y_pos, x_pos)
        self.color = 'red'
        self.y_awal = y_pos

    def update(self):
        self.x_pos -= self.speed
        self.y_pos = self.y_awal + math.sin(self.x_pos / 30) * 40


# CHILD CLASS Word: Kata Bom
class WordBomb(Word):
    def __init__(self, text, speed, y_pos, x_pos):
        super().__init__(text, speed, y_pos, x_pos)
        self.color = 'orange'
        self.is_bomb = True

    def update(self):
        self.x_pos -= self.speed
        self.y_pos += random.choice([-2, 0, 2])
        self.x_pos += random.choice([-1, 0, 1])


# CLASS peluru
class Bullet:
    def __init__(self, x, y, target_word):
        self.x = x
        self.y = y
        self.target = target_word
        self.speed = 18

    def update(self):
        dy = (self.target.y_pos + 15) - self.y
        dx = self.target.x_pos - self.x
        distance = math.hypot(dx, dy)

        if distance < self.speed:
            return True
        else:
            if distance != 0:
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
            return False

    def draw(self, surface):
        pygame.draw.circle(surface, 'yellow', (int(self.x), int(self.y)), 6)
        pygame.draw.circle(surface, 'orange', (int(self.x), int(self.y)), 9, 2)


# CLASS: Main Character
class MainCharacter:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = img_player
        self.gun_end_x = x + 20
        self.gun_end_y = y + 5

    def draw(self, surface, target_x=None, target_y=None):
        surface.blit(self.image, (self.x - 120, self.y - 120))

        base_x = self.x + 20
        base_y = self.y + 5

        angle = 0
        if target_x is not None and target_y is not None:
            dy = target_y - base_y
            dx = target_x - base_x
            angle = math.atan2(dy, dx)

        gun = 35
        self.gun_end_x = base_x + math.cos(angle) * gun
        self.gun_end_y = base_y + math.sin(angle) * gun
        pygame.draw.line(surface, (100, 100, 100), (base_x, base_y), (self.gun_end_x, self.gun_end_y), 15)

# CLASS Button
class Button:
    def __init__(self, x_pos, y_pos, text, clicked, surf):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.clicked = clicked
        self.surf = surf

    def draw(self):
        cir = pygame.draw.circle(self.surf, (45, 89, 135), (self.x_pos, self.y_pos), 35)
        if cir.collidepoint(pygame.mouse.get_pos()):
            butts = pygame.mouse.get_pressed()
            if butts[0]:
                pygame.draw.circle(self.surf, (190, 35, 35), (self.x_pos, self.y_pos), 35)
                self.clicked = True
            else:
                pygame.draw.circle(self.surf, (190, 89, 135), (self.x_pos, self.y_pos), 35)
        pygame.draw.circle(self.surf, 'white', (self.x_pos, self.y_pos), 35, 3)
        self.surf.blit(pause_font.render(self.text, True, 'white'), (self.x_pos - 15, self.y_pos - 25))


def draw_screen():
    pygame.draw.rect(screen, (32, 42, 68), [0, HEIGHT - 100, WIDTH, 100], 0)
    pygame.draw.rect(screen, 'white', [0, 0, WIDTH, HEIGHT], 5)
    pygame.draw.line(screen, 'white', (0, HEIGHT - 100), (WIDTH, HEIGHT - 100), 2)
    pygame.draw.line(screen, 'white', (250, HEIGHT - 100), (250, HEIGHT), 2)
    pygame.draw.line(screen, 'white', (700, HEIGHT - 100), (700, HEIGHT), 2)
    pygame.draw.rect(screen, 'black', [0, 0, WIDTH, HEIGHT], 2)
    screen.blit(header_font.render(f'Level: {level}', True, 'white'), (10, HEIGHT - 75))
    screen.blit(header_font.render(f'"{active_string}"', True, 'white'), (270, HEIGHT - 75))
    pause_btn = Button(748, HEIGHT - 52, 'II', False, screen)
    pause_btn.draw()
    screen.blit(banner_font.render(f'Score: {score}', True, 'white'), (250, 10))
    screen.blit(banner_font.render(f'Best: {high_score}', True, 'white'), (540, 10))
    screen.blit(banner_font.render(f'Lives: {lives}', True, 'white'), (10, 10))
    return pause_btn.clicked


def draw_pause():
    choice_commits = copy.deepcopy(choices)
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(surface, (0, 0, 0, 100), [100, 100, 600, 300], 0, 5)
    pygame.draw.rect(surface, (0, 0, 0, 200), [100, 100, 600, 300], 5, 5)
    resume_btn = Button(160, 210, '>', False, surface)
    resume_btn.draw()
    quit_btn = Button(400, 210, 'X', False, surface)
    quit_btn.draw()
    surface.blit(header_font.render('MENU', True, 'white'), (110, 110))
    surface.blit(header_font.render('PLAY!', True, 'white'), (210, 175))
    surface.blit(header_font.render('QUIT', True, 'white'), (450, 175))
    surface.blit(header_font.render('Active Letter Lengths:', True, 'white'), (110, 250))

    for i in range(len(choices)):
        btn = Button(160 + (i * 80), 350, str(i + 2), False, surface)
        btn.draw()
        if btn.clicked:
            if choice_commits[i]:
                choice_commits[i] = False
            else:
                choice_commits[i] = True
        if choices[i]:
            pygame.draw.circle(surface, 'green', (160 + (i * 80), 350), 35, 5)
    screen.blit(surface, (0, 0))
    return resume_btn.clicked, choice_commits, quit_btn.clicked


def generate_level():
    word_objs = []
    include = []
    vertical_spacing = (HEIGHT - 150) // level
    if True not in choices:
        choices[0] = True
    for i in range(len(choices)):
        if choices[i]:
            include.append((len_indexes[i], len_indexes[i + 1]))

    for i in range(level):
        speed = random.randint(1, 3)
        y_pos = random.randint(10 + (i * vertical_spacing), (i + 1) * vertical_spacing)
        x_pos = random.randint(WIDTH, WIDTH + 1000)

        chance = random.random()

        # Jika BOSS (10% peluang)
        if chance <= 0.10:
            text = random.choice(boss_word)
            new_word = WordBoss(text, speed, y_pos, x_pos)

        # Jika BOMB (20% peluang)
        elif chance <= 0.30:
            text = random.choice(bomb_word)
            new_word = WordBomb(text, speed, y_pos, x_pos)

        # Jika Kata NORMAL (70% peluang)
        else:
            ind_sel = random.choice(include)
            index = random.randint(ind_sel[0], ind_sel[1])
            text = wordlist[index].lower()
            new_word = Word(text, speed, y_pos, x_pos)

        word_objs.append(new_word)

    return word_objs

def check_high_score():
    global high_score
    if score > high_score:
        high_score = score
        try:
            file = open('high_score.txt', 'w')
            file.write(str(int(high_score)))
            file.close()
        except Exception:
            pass

# Game Loop Utama
run = True
player = MainCharacter(60, (HEIGHT - 100) // 2)

while run:
    screen.blit(img_background, (0, 0))
    timer.tick(fps)
    target_x, target_y = None, None
    if active_string != '':
        for w in word_objects:
            if w.text.startswith(active_string) and not w.is_targeted and w.x_pos > 0:
                target_x = w.x_pos
                target_y = w.y_pos + 15
                break

    player.draw(screen, target_x, target_y)

    pause_butt = draw_screen()

    if pz:
        resume_butt, changes, quit_butt = draw_pause()
        if resume_butt:
            pz = False
        if quit_butt:
            check_high_score()
            run = False

    if new_level and not pz:
        word_objects = generate_level()
        new_level = False
    else:
        for w in word_objects:
            w.draw()
            if not pz:
                w.update()
            # Jika kata keluar dari layar (terlewat)
            if w.x_pos < -200:
                word_objects.remove(w)

                if not isinstance(w, WordBomb):
                    lives -= 1

    if len(word_objects) <= 0 and not pz:
        level += 1
        new_level = True
    # logika peluru bergerak menghancurkan target
    if not pz:
        for p in bullet_list[:]:
            p.draw(screen)
            hit = p.update()
            if hit:
                bullet_list.remove(p)
                woosh.play()

                wrd = p.target
                if wrd in word_objects:
                    points = wrd.speed * len(wrd.text) * 10 * (len(wrd.text) / 4)
                    score += int(points)

                    # Logika Boss & Bom
                    if isinstance(wrd, WordBoss):
                        lives += 2
                    elif isinstance(wrd, WordBomb):
                        lives -= 2

                        # Hancurkan Kata
                    word_objects.remove(wrd)
    if submit != '':
        match_found = False
        for wrd in word_objects:
            if wrd.text == submit and not wrd.is_targeted and wrd.x_pos > 0:
                wrd.is_targeted = True
                match_found = True

                bullet_new = Bullet(player.gun_end_x, player.gun_end_y, wrd)
                bullet_list.append(bullet_new)

                click.play()
                break

        if not match_found:
            wrong.play()

        submit = ''

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            check_high_score()
            run = False

        if event.type == pygame.KEYDOWN:
            if not pz:
                if event.unicode.lower() in letters:
                    active_string += event.unicode
                    click.play()
                if event.key == pygame.K_BACKSPACE and len(active_string) > 0:
                    active_string = active_string[:-1]
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    submit = active_string
                    active_string = ''
            if event.key == pygame.K_ESCAPE:
                if pz:
                    pz = False
                else:
                    pz = True
        if event.type == pygame.MOUSEBUTTONUP and pz:
            if event.button == 1:
                choices = changes

    if pause_butt:
        pz = True

    if lives < 0:
        pz = True
        level = 1
        lives = 5
        word_objects = []
        bullet_list_ = []
        new_level = True
        check_high_score()
        score = 0

    pygame.display.flip()

pygame.quit()