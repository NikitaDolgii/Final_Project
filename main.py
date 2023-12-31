import pygame
from math import *
import sys
import random


# Инициализация библиотеки
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

# Размеры экрана
W, H = 1024, 768
screen = pygame.display.set_mode((W, H))

# Цвета для игры
c_1 = (78, 205, 196)
c_2 = (26, 83, 92)
c_3 = (247, 255, 247)
c_4 = (255, 107, 107)
c_5 = (255, 230, 109)


# ФПС и часы для отсчёта времени
fps = 60
clock = pygame.time.Clock()


# Класс танка (игрока)
class Tank:

    def __init__(self, x, y, a):

        # Местоположение и угол поворота
        self.x = x
        self.y = y
        self.a = a

        # Местоположение реального центра танка
        self.rx = 0
        self.ry = 0
        self.w = 0
        self.h = 0

        # Линейная и угловая скорость
        self.v = 2
        self.av = 2

        # Кол-во жизней, патронов, монет, очков
        self.lives = 3
        self.missiles = 6
        self.coins = 0
        self.points = 0

        # Объект типа mask, который совпадает с изображением танка в данный момент
        self.mask = pygame.mask.from_surface(green_tank)

        # Индикатор независимого времени самого танка
        self.time = 0

        # Скорость перезарядки, макс. кол-во снарядов и индикаторы "прокачки"
        self.reload_speed = 1
        self.max_missiles = 6
        self.sp = 0
        self.rotsp = 0
        self.misl = 0
        self.reld = 0

        self.img = green_tank
        self.fire_mode = 1
        self.shield = 0
        self.defence = 0
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    # Движение танка вперёд
    def move_forward(self):
        if self.lives > 0:
            if 32 < self.x < 992:
                self.x += self.v * cos(self.a/57.3)
            elif self.x < 32:
                self.x += self.v
            elif self.x > 992:
                self.x -= self.v
            if 32 < self.y < 736:
                self.y -= self.v*sin(self.a/57.3)
            elif self.y < 32:
                self.y += self.v
            elif self.y > 736:
                self.y -= self.v

    # Движение танка назад
    def move_back(self):
        if self.lives > 0:
            if 32 < self.x < 992:
                self.x -= self.v * cos(self.a/57.3)
            elif self.x < 32:
                self.x += self.v
            elif self.x > 992:
                self.x -= self.v
            if 32 < self.y < 736:
                self.y += self.v * sin(self.a/57.3)
            elif self.y < 32:
                self.y += self.v
            elif self.y > 736:
                self.y -= self.v

    # Поворот танка в пространстве
    def rotate_r(self):
        if self.lives > 0:
            self.a -= self.av

    def rotate_l(self):
        if self.lives > 0:
            self.a += self.av

    # Перезарядка патронов
    def reload(self):
        self.time += 1
        if self.time % (240 - self.reld*15) == 0 and self.missiles < self.max_missiles:
            self.missiles += 1
        if self.time % 400 == 0 and self.defence == 1 and self.shield < 3:
            self.shield += 1
        if self.time == 3600:
            self.time = 0

    # Отображение картинки танка на экране
    def render(self):
        if self.lives > 0:
            rotated_img = pygame.transform.rotate(self.img, self.a)
            self.w = rotated_img.get_width() // 2
            self.h = rotated_img.get_height() // 2
            self.rx = self.x - self.w
            self.ry = self.y - self.h
            self.mask = pygame.mask.from_surface(rotated_img)
            screen.blit(rotated_img, (self.rx, self.ry))
            if self.shield == 1:
                rotated_shield = pygame.transform.rotate(shield_1, self.a)
                screen.blit(rotated_shield, (self.rx - self.w, self.ry - self.h))
            if self.shield == 2:
                rotated_shield = pygame.transform.rotate(shield_2, self.a)
                screen.blit(rotated_shield, (self.rx - self.w, self.ry - self.h))
            if self.shield == 3:
                rotated_shield = pygame.transform.rotate(shield_3, self.a)
                screen.blit(rotated_shield, (self.rx - self.w, self.ry - self.h))

    # Отображение кол-ва монет и значка монетки на экране в одиночном режиме (координата x зависит от кол-ва монет)
    def render_coins(self):
        if self.coins < 10:
            screen.blit(coin_image, (30, 90))
        if 10 <= self.coins < 100:
            screen.blit(coin_image, (55, 90))
        if 100 <= self.coins < 1000:
            screen.blit(coin_image, (80, 90))
        if 1000 <= self.coins < 10000:
            screen.blit(coin_image, (105, 90))
        draw_text(str(self.coins), font, c_2, screen, 8, 88)

        draw_text('10', font, c_2, screen, 905, 268)

    # Отображение на экране кол-ва патронов 1-го и 2-го танков (Так как патроны должны отображаться в определённых
    # частях экрана, эти методы разбиты на отдельные для каждого танка)
    def render_missiles_tank_1(self):
        if self.lives > 0:
            for i in range(self.missiles):
                screen.blit(missil_image, (i*32, 50))

    def render_missiles_tank_2(self):
        if self.lives > 0:
            for i in range(self.missiles):
                screen.blit(missil_image, (830 + i*32, 50))

    # Аналогично, отображение на экране кол-ва жизней каждого танка
    def render_hearts_tank_1(self):
        for i in range(self.lives):
            screen.blit(heart_image, (5 + i*32, 10))

    def render_shield(self):
        for i in range(self.shield):
            screen.blit(shield_image, (101 + i*32, 10))

    def render_hearts_tank_2(self):
        for i in range(self.lives):
            screen.blit(heart_image, (930 + i*32, 10))

    # Стрельба (создание и добавление в список нового патрона)
    def fire(self):
        if self.lives > 0:
            if self.fire_mode == 1:
                if self.missiles != 0:
                    self.missiles -= 1
                    bullet = Bullet(self.x, self.y, self.a)
                    return bullet
            if self.fire_mode == 3:
                if self.missiles != 0:
                    self.missiles -= 1
                    b1, b2, b3 = (Bullet(self.x, self.y, self.a-3),
                                  Bullet(self.x, self.y, self.a+3),
                                  Bullet(self.x, self.y, self.a))
                    return b1, b2, b3

    # Проверка на столкновение с объектом
    def hittest(self, obj):
        if self.mask.overlap(obj.mask, (obj.rx - self.rx, obj.ry - self.ry)):
            self.lives, obj.lives = 0, 0

    # Отображение кол-ва очков в одиночном режиме
    def render_points(self):
        draw_text(str(self.points), font, c_2, screen, 900, 20)

    def set_zero(self, x, y, a):
        self.x = x
        self.y = y
        self.a = a
        self.rx = 0
        self.ry = 0
        self.v = 2
        self.av = 2
        self.lives = 3
        self.missiles = 6
        self.coins = 0
        self.points = 0
        self.mask = pygame.mask.from_surface(green_tank)
        self.time = 0
        self.reload_speed = 1
        self.max_missiles = 6
        self.sp = 0
        self.rotsp = 0
        self.misl = 0
        self.reld = 0
        self.img = green_tank
        self.fire_mode = 1
        self.shield = 0
        self.defence = 0
        bullets.clear()
        money.clear()
        enemies.clear()


# Класс врагов, атакующих игрока в одиночном режиме
class Enemy:
    def __init__(self, img):
        self.x, self.y = random.choice(
            [(-50, random.randint(0, H)),
                (W + 50, random.randint(0, H)),
                (random.randint(0, W), -50),
                (random.randint(0, W), H + 50)]
        )
        self.a = 1
        self.v = 2
        self.vx = self.v * cos(self.a / 57.3)
        self.vy = self.v * sin(self.a / 57.3)
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def render(self):
        self.mask = pygame.mask.from_surface(self.img)
        screen.blit(self.img, (self.x, self.y))

    def targetting(self):
        if tank_1.rx > self.x:
            self.a = atan(-(tank_1.ry - self.y) / (tank_1.rx - self.x)) * 57.3 + 90
        elif tank_1.rx < self.x:
            self.a = atan(-(tank_1.ry - self.y) / (tank_1.rx - self.x)) * 57.3 + 270
        else:
            self.a = atan((tank_1.ry - self.y) / (tank_1.rx - self.x + 0.00001)) * 57.3 + 270

    def move(self):
        self.vx = self.v * sin(self.a / 57.3)
        self.vy = self.v * cos(self.a / 57.3)
        self.x += self.vx
        self.y += self.vy

    def hittest(self):
        if tank_1.shield > 0:
            if self.mask.overlap(shield_mask, (tank_1.rx - tank_1.w - self.x, tank_1.ry - tank_1.h - self.y)):
                tank_1.shield -= 1
                return True
        elif self.mask.overlap(tank_1.mask, (tank_1.rx - self.x, tank_1.ry - self.y)):
            tank_1.lives -= 1
            return True



class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mask = pygame.mask.from_surface(coin_drop)
        self.life = 1

    def render(self):
        if self.life:
            screen.blit(coin_drop, (self.x, self.y))

    def hittest(self, obj):
        if self.life:
            if self.mask.overlap(obj, (tank_1.rx - self.x, tank_1.ry - self.y)):
                coin_sound.play()
                tank_1.coins += 5
                self.life = 0


class Bullet:
    def __init__(self, x, y, a):
        self.x = x
        self.y = y
        self.v = tank_1.v + 10
        self.a = a
        self.vx = self.v * cos(self.a/57.3)
        self.vy = self.v * sin(self.a/57.3)
        self.mask = pygame.mask.from_surface(bullet_image)
        self.life = 0
        self.rect = pygame.Rect(self.x-4, self.y-4, 8, 8)

    def render(self):
            self.rect = pygame.Rect(self.x, self.y, 3, 3)
            self.mask = pygame.mask.from_surface(bullet_image)
            screen.blit(bullet_image, (self.x, self.y))
            self.life += 1

    def hittest_tank_1(self, obj):
        if self.mask.overlap(obj, (tank_1.rx - self.x, tank_1.ry - self.y)) and self.life > 3:
            self.x, self.y = 10000, 10000
            p.play()
            tank_1.lives -= 1

    def hittest_tank_2(self, obj):
        if self.mask.overlap(obj, (tank_2.rx - self.x, tank_2.ry - self.y)) and self.life > 3:
            self.x, self.y = 10000, 10000
            p.play()
            tank_2.lives -= 1

    def hittest_enemy(self):
        for en in enemies:
            if self.mask.overlap(en.mask, (en.x - self.x, en.y - self.y)):
                p.play()
                coin = Coin(en.x, en.y)
                money.append(coin)
                enemies.remove(en)
                self.life = 150



    def move_1(self):
        self.x += self.vx
        self.y -= self.vy
        self.a = 1

        # АПДЕЙТ 3 Начало
    def move_2(self):
        for i in range(len(wall_vertical_rect)):
            if (wall_vertical_rect[i]).collidepoint(self.rect.center):
                self.vx *= (-1)
        for i in range(len(wall_horizontal_rect)):
            if (wall_horizontal_rect[i]).collidepoint(self.rect.center):
                self.vy *= (-1)
                # Апдейт 3 конец
        self.x += self.vx
        self.y -= self.vy
        self.a = 1


# АПДЕЙТ 1 | 28.11.2023. Начало
# Первичное создание контура лабиринта
wall_vertical = pygame.image.load('images/other_imgs/wall_vertical_10x50.png').convert_alpha()
wall_vertical_rect = []
for i in range(H // 50 + 2):
    wall_vertical_rect.append(wall_vertical.get_rect(left=0, top=i * 50 + 90))
    wall_vertical_rect.append(wall_vertical.get_rect(right=W, top=i * 50 + 90))

wall_horizontal = pygame.image.load('images/other_imgs/wall_horizontal_50x10.png').convert_alpha()
wall_horizontal_rect = []
for i in range(W // 50 + 2):
    wall_horizontal_rect.append(wall_horizontal.get_rect(left=i * 50, top=90))
    wall_horizontal_rect.append(wall_horizontal.get_rect(right=i * 50, bottom=H))

# Карта для двоих (настраивается вручную)
for i in range(6):
    wall_horizontal_rect.append(wall_horizontal.get_rect(left=50 * i, top=H - 120))
    wall_horizontal_rect.append(wall_horizontal.get_rect(right=W - 50 * i, top=120 + 90))
for i in range(3):
    wall_vertical_rect.append(wall_vertical.get_rect(left=300, bottom=H - 120 - 50 * i + 10))
    wall_vertical_rect.append(wall_vertical.get_rect(right=W - 300, top=120 + 90 + 50 * i))
for i in range(4):
    wall_vertical_rect.append(wall_vertical.get_rect(left=300, bottom=-250 + H - 120 - 50 * i + 10))
    wall_vertical_rect.append(wall_vertical.get_rect(right=W - 300, top=+250 + 120 + 90 + 50 * i))

for i in range(3):
    wall_horizontal_rect.append(wall_horizontal.get_rect(left=250 - 50 * i, top=H - 120 - 50 * 3 + 10))
    wall_horizontal_rect.append(wall_horizontal.get_rect(left=W - 310 + 50 * i, top=120 + 90 + 150))

for i in range(10):
    wall_vertical_rect.append(wall_vertical.get_rect(left=420, bottom=H - 50 * i + 10))
    wall_vertical_rect.append(wall_vertical.get_rect(right=W - 420, top=120 - 30 + 50 * i))


# АПДЕЙТ 1 | 28.11.2023. Конец


# загрузка звуковых эффектов
s = pygame.mixer.Sound('sfx/shoot.wav')
p = pygame.mixer.Sound('sfx/hit.wav')
b = pygame.mixer.Sound('sfx/button.wav')
coin_sound = pygame.mixer.Sound('sfx/coin_sound.wav')

# загрузка изображений танков
green_tank = pygame.transform.scale(pygame.image.load('images/tank_imgs/green_tank.png'), (64, 64))
green_tank_broken = pygame.transform.scale(pygame.image.load('images/tank_imgs/green_tank_broken.png'), (64, 64))
brown_tank = pygame.transform.scale(pygame.image.load('images/tank_imgs/brown_tank.png'), (64, 64))
brown_tank_broken = pygame.transform.scale(pygame.image.load('images/tank_imgs/brown_tank_broken.png'), (64, 64))
green_tank_3_bullets = pygame.transform.scale(pygame.image.load('images/tank_imgs/green_tank_3_bullets.png'), (64, 64))

# загрузка изображений кнопок главного меню
one_player_up = pygame.transform.scale(pygame.image.load('images/button_images/1_player_up.png'), (384, 96))
one_player_down = pygame.transform.scale(pygame.image.load('images/button_images/1_player_down.png'), (384, 96))
two_players_up = pygame.transform.scale(pygame.image.load('images/button_images/2_players_up.png'), (384, 96))
two_players_down = pygame.transform.scale(pygame.image.load('images/button_images/2_players_down.png'), (384, 96))
quit_up = pygame.transform.scale(pygame.image.load('images/button_images/quit_up.png'), (384, 96))
quit_down = pygame.transform.scale(pygame.image.load('images/button_images/quit_down.png'), (384, 96))

# загрузка изображений кнопок меню смерти/паузы в одиночной игре
retry_up = pygame.transform.scale(pygame.image.load('images/button_images/retry_up.png'), (384, 96))
retry_down = pygame.transform.scale(pygame.image.load('images/button_images/retry_down.png'), (384, 96))
main_menu_up = pygame.transform.scale(pygame.image.load('images/button_images/main_menu_up.png'), (384, 96))
main_menu_down = pygame.transform.scale(pygame.image.load('images/button_images/main_menu_down.png'), (384, 96))
continue_up = pygame.transform.scale(pygame.image.load('images/button_images/continue_up.png'), (384, 96))
continue_down = pygame.transform.scale(pygame.image.load('images/button_images/continue_down.png'), (384, 96))

# загрузка кнопок клавиатуры (для управления игроками)
w_button = pygame.transform.scale(pygame.image.load('images/button_images/w.png'), (96, 96))
a_button = pygame.transform.scale(pygame.image.load('images/button_images/a.png'), (96, 96))
s_button = pygame.transform.scale(pygame.image.load('images/button_images/s.png'), (96, 96))
d_button = pygame.transform.scale(pygame.image.load('images/button_images/d.png'), (96, 96))
space = pygame.transform.scale(pygame.image.load('images/button_images/space.png'), (384, 96))
up_button = pygame.transform.scale(pygame.image.load('images/button_images/up.png'), (96, 96))
down_button = pygame.transform.scale(pygame.image.load('images/button_images/down.png'), (96, 96))
right_button = pygame.transform.scale(pygame.image.load('images/button_images/right.png'), (96, 96))
left_button = pygame.transform.scale(pygame.image.load('images/button_images/left.png'), (96, 96))
q_button = pygame.transform.scale(pygame.image.load('images/button_images/q.png'), (96, 96))
m_button = pygame.transform.scale(pygame.image.load('images/button_images/m.png'), (96, 96))

# загрузка кнопок улучшений и 'эволюции' в одиночной игре
upgrade_up = pygame.transform.scale(pygame.image.load('images/button_images/upgrade_up.png'), (32, 32))
upgrade_down = pygame.transform.scale(pygame.image.load('images/button_images/upgrade_down.png'), (32, 32))
shield_up = pygame.image.load('images/other_imgs/shield_up.png')
shield_down = pygame.image.load('images/other_imgs/shield_down.png')
three_bullets_up = pygame.image.load('images/other_imgs/3_bullets_up.png')
three_bullets_down = pygame.image.load('images/other_imgs/3_bullets_down.png')

# загрузка других изображений
bullet_image = pygame.image.load('images/other_imgs/bullet.png')
heart_image = pygame.transform.scale(pygame.image.load('images/other_imgs/heart.png'), (32, 32))
missil_image = pygame.transform.scale(pygame.image.load('images/other_imgs/missil.png'), (32, 32))
coin_image = pygame.transform.scale(pygame.image.load('images/other_imgs/coin.png'), (32, 32))
enemy_1_image = pygame.transform.scale(pygame.image.load('images/other_imgs/enemy_1.png'), (64, 64))
enemy_2_image = pygame.image.load('images/other_imgs/enemy_2.png')
reload_image = pygame.transform.scale(pygame.image.load('images/other_imgs/reload.png'), (80, 16))
bullets_image = pygame.transform.scale(pygame.image.load('images/other_imgs/bullets.png'), (80, 16))
speed_image = pygame.transform.scale(pygame.image.load('images/other_imgs/speed.png'), (52, 16))
rotation_image = pygame.transform.scale(pygame.image.load('images/other_imgs/rotation.png'), (80, 16))
boss = pygame.image.load('images/other_imgs/boss.png')
coin_drop = pygame.image.load('images/other_imgs/coin_drop.png')
shield_1 = pygame.transform.scale(pygame.image.load('images/other_imgs/shield_1.png'), (128, 128))
shield_2 = pygame.transform.scale(pygame.image.load('images/other_imgs/shield_2.png'), (128, 128))
shield_3 = pygame.transform.scale(pygame.image.load('images/other_imgs/shield_3.png'), (128, 128))
shield_mask = pygame.mask.from_surface(shield_1)
shield_image = pygame.transform.scale(pygame.image.load('images/other_imgs/shield_image.png'), (32, 32))


# некоторые объекты и функции, необходимые для игрового цикла
def create_enemy_1():
    enemy_1 = Enemy(enemy_1_image)
    enemies.append(enemy_1)


def create_enemy_2():
    enemy_2 = Enemy(enemy_2_image)
    enemies.append(enemy_2)


def create_boss_1(t):
    screen.blit(boss, (-400 + t, 34))


tank_1 = Tank(100, 400, 90)
tank_2 = Tank(900, 400, 90)
tank_1.img = green_tank
tank_2.img = brown_tank

bullets = []
enemies = []
money = []


def evolve_menu():
    ind = True
    while ind:
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True


        button_3_bullets = pygame.Rect(120, 150, 384, 384)
        button_shield = pygame.Rect(520, 150, 384, 384)

        mx, my = pygame.mouse.get_pos()
        if button_3_bullets.collidepoint((mx, my)):
            screen.blit(three_bullets_down, button_3_bullets)
            if click:
                b.play()
                tank_1.img = green_tank_3_bullets
                tank_1.fire_mode = 3
                ind = False

        else:
            screen.blit(three_bullets_up, button_3_bullets)
        if button_shield.collidepoint((mx, my)):
            screen.blit(shield_down, button_shield)
            if click:
                b.play()
                tank_1.defence = 1
                tank_1.shield = 3
                ind = False

        else:
            screen.blit(shield_up, button_shield)

        click = False

        clock.tick(fps)
        pygame.display.update()


# игровой цикл для одиночной игры
def game_for_one():

    click = False
    t = 0

    running = True
    while running:

        screen.fill(c_1)

        t += 1

        if t < 600:
            draw_text('Get ready! ' + str((600 - t) // 60) + ' s', font, c_2, screen, 400, 50)

        if 600 < t < 4200:
            draw_text('Wave 1: ' + str((4200 - t) // 60) + ' s', font, c_2, screen, 400, 50)

            if t % 120 == 0:
                tank_1.points += 10

            if t % 300 == 0:
                create_enemy_1()

        if 4200 < t < 5100:
            draw_text('Cooldown: ' + str((5100 - t) // 60) + ' s', font, c_2, screen, 400, 50)

        if 5100 < t < 8700:
            draw_text('Wave 2: ' + str((8700 - t) // 60) + ' s', font, c_2, screen, 400, 50)

            if t % 120 == 0:
                tank_1.points += 10

            if t % 450 == 0:
                create_enemy_1()

            if t % 600 == 0:
                create_enemy_2()

        if 8700 < t < 8880:
            draw_text('Evolution time!', font, c_2, screen, 400, 50)

        if t == 8880:
            evolve_menu()

        if 8880 < t < 9780:
            draw_text('Get ready! ' + str((9780 - t) // 60) + ' s', font, c_2, screen, 400, 50)

        if 9780 < t < 13380:
            draw_text('Wave 3: ' + str((13380 - t) // 60) + ' s', font, c_2, screen, 400, 50)

            if t % 120 == 0:
                tank_1.points += 10

            if t % 200 == 0:
                create_enemy_1()

            if t % 300 == 0:
                create_enemy_2()

        if t > 13380:
            draw_text('Have fun!', font, c_2, screen, 400, 50)

            if t % 100 == 0 or t % 450 == 0:
                create_enemy_1()

            if t % 150 == 0:
                create_enemy_2()




        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    if tank_1.lives > 0 and tank_1.missiles > 0:
                        if tank_1.fire_mode == 1:
                            s.play()
                            bullet = tank_1.fire()
                            bullets.append(bullet)
                        if tank_1.fire_mode == 3:
                            s.play()
                            b1, b2, b3 = tank_1.fire()
                            bullets.append(b1)
                            bullets.append(b2)
                            bullets.append(b3)
                if e.key == pygame.K_ESCAPE:
                    pause_menu_one()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    click = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            tank_1.rotate_r()
        if keys[pygame.K_a]:
            tank_1.rotate_l()
        if keys[pygame.K_w]:
            tank_1.move_forward()
        if keys[pygame.K_s]:
            tank_1.move_back()

        tank_1.reload()
        tank_1.render_coins()
        tank_1.render_shield()

        for m in money:
            m.render()
            m.hittest(tank_1.mask)

        for enemy in enemies:
            if enemy.hittest():
                p.play()
                enemies.remove(enemy)
            enemy.targetting()
            enemy.render()
            enemy.move()


        for bul in bullets:
            if bul.life >= 100:
                bullets.remove(bul)
            bul.hittest_enemy()
            bul.move_1()
            bul.render()
            bul.hittest_tank_1(tank_1.mask)

        tank_1.render_hearts_tank_1()
        tank_1.render_missiles_tank_1()
        tank_1.render_points()
        tank_1.render()


        #########################################################################

        button_upgrade_speed = pygame.Rect(860, 80, 32, 32)
        button_upgrade_rotation_speed = pygame.Rect(860, 130, 32, 32)
        button_upgrade_missiles = pygame.Rect(860, 180, 32, 32)
        button_upgrade_reload = pygame.Rect(860, 230, 32, 32)

        mx, my = pygame.mouse.get_pos()

        screen.blit(
            pygame.transform.scale(pygame.image.load('images/scale_imgs/scale_' + str(tank_1.sp) + '.png'), (96, 32)),
            (900, 80)
        )
        screen.blit(
            pygame.transform.scale(pygame.image.load('images/scale_imgs/scale_' + str(tank_1.rotsp) + '.png'),
                                   (96, 32)),
            (900, 130)
        )
        screen.blit(
            pygame.transform.scale(pygame.image.load('images/scale_imgs/scale_' + str(tank_1.misl) + '.png'), (96, 32)),
            (900, 180)
        )
        screen.blit(
            pygame.transform.scale(pygame.image.load('images/scale_imgs/scale_' + str(tank_1.reld) + '.png'), (96, 32)),
            (900, 230)
        )

        screen.blit(speed_image, pygame.Rect(900, 64, 52, 8))
        screen.blit(rotation_image, pygame.Rect(896, 114, 80, 8))
        screen.blit(bullets_image, pygame.Rect(891, 164, 80, 8))
        screen.blit(reload_image, pygame.Rect(891, 214, 80, 8))
        screen.blit(coin_image, pygame.Rect(950, 270, 32, 32))

        if tank_1.coins >= 10:
            if button_upgrade_speed.collidepoint((mx, my)):
                screen.blit(upgrade_down, button_upgrade_speed)
                if click:
                    if tank_1.sp < 10:
                        b.play()
                        tank_1.v += 0.5
                        tank_1.coins -= 10
                        tank_1.sp += 1
            else:
                screen.blit(upgrade_up, button_upgrade_speed)

        if tank_1.coins >= 10:
            if button_upgrade_rotation_speed.collidepoint((mx, my)):
                screen.blit(upgrade_down, button_upgrade_rotation_speed)
                if click:
                    if tank_1.rotsp < 10:
                        b.play()
                        tank_1.av += 0.2
                        tank_1.coins -= 10
                        tank_1.rotsp += 1
            else:
                screen.blit(upgrade_up, button_upgrade_rotation_speed)

        if tank_1.coins >= 10:
            if button_upgrade_missiles.collidepoint((mx, my)):
                screen.blit(upgrade_down, button_upgrade_missiles)
                if click:
                    if tank_1.misl < 10:
                        b.play()
                        tank_1.max_missiles += 1
                        tank_1.coins -= 10
                        tank_1.misl += 1
            else:
                screen.blit(upgrade_up, button_upgrade_missiles)

            if tank_1.coins >= 10:
                if button_upgrade_reload.collidepoint((mx, my)):
                    screen.blit(upgrade_down, button_upgrade_reload)
                    if click:
                        if tank_1.reld < 10:
                            b.play()
                            tank_1.reload_speed += 0.5
                            tank_1.coins -= 10
                            tank_1.reld += 1
                else:
                    screen.blit(upgrade_up, button_upgrade_reload)

            click = False

        ####################################################################

        if tank_1.lives == 0:
            running = False
            death_menu_one()



        clock.tick(fps)
        pygame.display.update()


# игровой цикл 1 на 1
def game_for_two():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    if tank_1.lives > 0 and tank_1.missiles > 0:
                        s.play()
                        bullet = tank_1.fire()
                        bullets.append(bullet)
                if event.key == pygame.K_m:
                    if tank_2.lives > 0 and tank_2.missiles:
                        s.play()
                        bullet = tank_2.fire()
                        bullets.append(bullet)
                if event.key == pygame.K_ESCAPE:
                    pause_menu_two()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            tank_1.rotate_r()
        if keys[pygame.K_a]:
            tank_1.rotate_l()
        if keys[pygame.K_w]:
            tank_1.move_forward()
        if keys[pygame.K_s]:
            tank_1.move_back()
        if keys[pygame.K_RIGHT]:
            tank_2.rotate_r()
        if keys[pygame.K_LEFT]:
            tank_2.rotate_l()
        if keys[pygame.K_UP]:
            tank_2.move_forward()
        if keys[pygame.K_DOWN]:
            tank_2.move_back()

        screen.fill(c_1)

        # АПДЕЙТ 2 | 28.11.2023. Начало
        # Рисование вертикальных стенок лабиринта

        for i in range(len(wall_vertical_rect)):
            screen.blit(wall_vertical, wall_vertical_rect[i])

        for i in range(len(wall_horizontal_rect)):
            screen.blit(wall_horizontal, wall_horizontal_rect[i])
        # АПДЕЙТ 2 | 28.11.2023. Конец

        for bul in bullets:
            if bul.life >= 100:
                bullets.remove(bul)
            bul.move_2()
            bul.render()
            bul.hittest_tank_1(tank_1.mask)
            bul.hittest_tank_2(tank_2.mask)

        tank_1.render()
        tank_2.render()
        tank_1.reload()
        tank_2.reload()
        tank_1.render_hearts_tank_1()
        tank_2.render_hearts_tank_2()
        tank_1.render_missiles_tank_1()
        tank_2.render_missiles_tank_2()
        tank_1.hittest(tank_2)

        if tank_1.lives == 0:
            running = False
            death_menu_two()
        if tank_2.lives == 0:
            running = False
            death_menu_two()

        clock.tick(fps)
        pygame.display.update()


# шрифт и функция для написания текста на экране
font = pygame.font.SysFont('None', 50)


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


# главное меню
def main_menu():

    while True:
        screen.fill(c_1)
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True


        button_arcade = pygame.Rect(50, 100, 384, 96)
        button_play_two = pygame.Rect(50, 250, 384, 96)
        button_quit = pygame.Rect(50, 400, 384, 96)

        mx, my = pygame.mouse.get_pos()
        if button_arcade.collidepoint((mx, my)):
            screen.blit(one_player_down, button_arcade)
            if click:
                b.play()
                control_menu_one()
        else:
            screen.blit(one_player_up, button_arcade)
        if button_play_two.collidepoint((mx, my)):
            screen.blit(two_players_down, button_play_two)
            if click:
                b.play()
                control_menu_two()
        else:
            screen.blit(two_players_up, button_play_two)
        if button_quit.collidepoint((mx, my)):
            screen.blit(quit_down, button_quit)
            if click:
                b.play()
                pygame.time.delay(100)
                pygame.quit()
                sys.exit()
        else:
            screen.blit(quit_up, button_quit)

        clock.tick(fps)
        pygame.display.update()


def control_menu_one():
    while True:
        screen.fill(c_1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    tank_1.set_zero(500, 400, 90)
                    tank_1.img = green_tank
                    b.play()
                    game_for_one()

        screen.blit(w_button, (250, 200))
        screen.blit(a_button, (100, 350))
        screen.blit(s_button, (250, 350))
        screen.blit(d_button, (400, 350))
        screen.blit(space, (400, 500))

        draw_text('W - move forward', font, c_2, screen, 600, 200)
        draw_text('S - move back', font, c_2, screen, 600, 250)
        draw_text('A, D - rotate', font, c_2, screen, 600, 300)
        draw_text('Space - shoot', font, c_2, screen, 600, 350)
        draw_text('Escape - pause', font, c_2, screen, 600, 400)
        draw_text('Press to start', font, c_2, screen, 470, 620)

        clock.tick(fps)
        pygame.display.update()


def control_menu_two():
    while True:
        screen.fill(c_1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    tank_1.set_zero(50, 700, 90)
                    tank_2.set_zero(900, 150, 270)
                    tank_1.img = green_tank
                    tank_2.img = brown_tank
                    b.play()
                    game_for_two()

        screen.blit(w_button, (190, 100))
        screen.blit(a_button, (40, 250))
        screen.blit(s_button, (190, 250))
        screen.blit(d_button, (340, 250))
        screen.blit(q_button, (190, 400))

        screen.blit(up_button, (750, 100))
        screen.blit(left_button, (600, 250))
        screen.blit(down_button, (750, 250))
        screen.blit(right_button, (900, 250))
        screen.blit(m_button, (750, 400))

        draw_text('1st Player', font, c_2, screen, 150, 50)
        draw_text('2nd Player', font, c_2, screen, 700, 50)
        screen.blit(space, (320, 550))
        draw_text('Press to start', font, c_2, screen, 400, 660)

        clock.tick(fps)
        pygame.display.update()


# меню паузы для одного игрока
def pause_menu_one():
    while True:

        screen.fill(c_1)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        button_retry = pygame.Rect(340, 350, 384, 96)
        button_continue = pygame.Rect(340, 200, 384, 96)
        button_main_menu = pygame.Rect(340, 500, 384, 96)

        mx, my = pygame.mouse.get_pos()
        if button_retry.collidepoint((mx, my)):
            screen.blit(retry_down, button_retry)
            if click:
                tank_1.set_zero(500, 400, 90)
                tank_1.img = green_tank
                b.play()
                game_for_one()
        else:
            screen.blit(retry_up, button_retry)
        if button_continue.collidepoint((mx, my)):
            screen.blit(continue_down, button_continue)
            if click:
                b.play()
                game_for_one()
        else:
            screen.blit(continue_up, button_continue)
        if button_main_menu.collidepoint((mx, my)):
            screen.blit(main_menu_down, button_main_menu)
            if click:
                b.play()
                main_menu()
        else:
            screen.blit(main_menu_up, button_main_menu)

        clock.tick(fps)
        pygame.display.update()


def pause_menu_two():
    while True:

        screen.fill(c_1)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        button_retry = pygame.Rect(340, 350, 384, 96)
        button_continue = pygame.Rect(340, 200, 384, 96)
        button_main_menu = pygame.Rect(340, 500, 384, 96)

        mx, my = pygame.mouse.get_pos()
        if button_retry.collidepoint((mx, my)):
            screen.blit(retry_down, button_retry)
            if click:
                tank_1.set_zero(50, 700, 90)
                tank_2.set_zero(900, 150, 270)
                tank_1.img = green_tank
                tank_2.img = brown_tank
                b.play()
                game_for_two()
        else:
            screen.blit(retry_up, button_retry)
        if button_continue.collidepoint((mx, my)):
            screen.blit(continue_down, button_continue)
            if click:
                b.play()
                game_for_two()
        else:
            screen.blit(continue_up, button_continue)
        if button_main_menu.collidepoint((mx, my)):
            screen.blit(main_menu_down, button_main_menu)
            if click:
                b.play()
                main_menu()
        else:
            screen.blit(main_menu_up, button_main_menu)

        clock.tick(fps)
        pygame.display.update()


# меню смерти для одного игрока
def death_menu_one():
    while True:
        screen.fill(c_5)
        draw_text("You've got " + str(tank_1.points + tank_1.coins) + " points!", font, c_2, screen, 340, 100)
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        button_retry = pygame.Rect(340, 200, 384, 96)
        button_main_menu = pygame.Rect(340, 350, 384, 96)

        mx, my = pygame.mouse.get_pos()
        if button_retry.collidepoint((mx, my)):
            screen.blit(retry_down, button_retry)
            if click:
                tank_1.set_zero(500, 400, 90)
                tank_1.img = green_tank
                b.play()
                game_for_one()
        else:
            screen.blit(retry_up, button_retry)
        if button_main_menu.collidepoint((mx, my)):
            screen.blit(main_menu_down, button_main_menu)
            if click:
                b.play()
                main_menu()
        else:
            screen.blit(main_menu_up, button_main_menu)
        clock.tick(fps)
        pygame.display.update()


# меню смерти для двух игроков
def death_menu_two():
    while True:
        screen.fill(c_5)
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        button_retry = pygame.Rect(340, 200, 384, 96)
        button_main_menu = pygame.Rect(340, 350, 384, 96)

        mx, my = pygame.mouse.get_pos()
        if button_retry.collidepoint((mx, my)):
            screen.blit(retry_down, button_retry)
            if click:
                tank_1.set_zero(50, 700, 90)
                tank_2.set_zero(900, 150, 270)
                tank_1.img = green_tank
                tank_2.img = brown_tank
                b.play()
                game_for_two()
        else:
            screen.blit(retry_up, button_retry)
        if button_main_menu.collidepoint((mx, my)):
            screen.blit(main_menu_down, button_main_menu)
            if click:
                b.play()
                main_menu()
        else:
            screen.blit(main_menu_up, button_main_menu)

        clock.tick(fps)
        pygame.display.update()


main_menu()
