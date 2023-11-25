import pygame
from math import *

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

W, H = 1024, 768
screen = pygame.display.set_mode((W, H))

fps = 30
clock = pygame.time.Clock()


class Tank:
    def __init__(self):
        self.x = 150
        self.y = 150
        self.a = 90
        self.v = 7

    def move_forward(self):
        self.x += self.v * cos(self.a/57.3)
        self.y -= self.v*sin(self.a/57.3)

    def move_back(self):
        self.x -= self.v * cos(self.a/57.3)
        self.y += self.v * sin(self.a/57.3)

    def rotate_r(self):
        self.a -= 4

    def rotate_l(self):
        self.a += 4

    def render(self, images, spread=3):
        for i, img in enumerate(images):
            rotated_img = pygame.transform.rotate(img, self.a)
            screen.blit(rotated_img, (self.x - rotated_img.get_width() // 2, self.y - rotated_img.get_height() // 2 - i * spread))

    def fire(self):
        bullet = Bullet(self.x, self.y, self.a)
        return bullet


class Bullet:
    def __init__(self, x, y, a):
        self.x = x
        self.y = y
        self.v = 20
        self.a = a
        self.vx = self.v * cos(self.a/57.3)
        self.vy = self.v * sin(self.a/57.3)
        self.r = 3
        self.rect = pygame.Rect(self.x, self.y, self.r, self.r)

    def render(self):
        pygame.draw.circle(screen, 'Black', (self.x, self.y - 27), self.r)
        self.rect = pygame.Rect(self.x, self.y - 27, self.r, self.r)
        if (self.x**2 + self.y**2) > 1000000:
            self.r = 0

    def move(self):
        self.x += self.vx
        self.y -= self.vy
        self.a = 1


class Zombie:
    def __init__(self):
        self.x = 500
        self.y = 500
        self.v = 1
        self.rect = pygame.Rect(self.x, self.y, 50, 50)
        self.a = 1
        self.vx = self.v * cos(self.a/57.3)
        self.vy = self.v * sin(self.a/57.3)

    def targetting(self):
        if tank.x > self.x:
            self.a = atan(-(tank.y - self.y) / (tank.x - self.x))*57.3 + 90
        elif tank.x < self.x:
            self.a = atan(-(tank.y - self.y) / (tank.x - self.x))*57.3 + 270
        else:
            self.a = atan((tank.y - self.y) / (tank.x - self.x + 0.00001))*57.3 + 270

    def render(self, images, spread=1):
        for i, img in enumerate(images):
            rotated_img = pygame.transform.rotate(img, self.a)
            screen.blit(rotated_img, (self.x - rotated_img.get_width() // 2, self.y - rotated_img.get_height() // 2 - i * spread))


    def hittest(self, obj):
        if self.rect.colliderect(obj):
            return True

    def move(self):
        self.vx = self.v * sin(self.a/57.3)
        self.vy = self.v * cos(self.a/57.3)
        self.x += self.vx
        self.y += self.vy









s = pygame.mixer.Sound("sfx/shot.wav")
d = pygame.mixer.Sound("sfx/zombie_die.wav")
tank = Tank()
zombie = Zombie()
bullets = []
background = pygame.image.load('images/background.png')
green_tank_spritesheet = pygame.image.load('images/green_tank.png').convert_alpha()
zombie_1_spritesheet = pygame.image.load('images/zombie_1.png').convert_alpha()


def get_image(sheet, images, layers, width, height, scale):
    n = 0
    while n <= layers:
        image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        image.blit(sheet, (0, 0), (0, (layers - 1 - n)*height, width, height))
        image = pygame.transform.scale(image, (scale*width, scale*height))
        images.append(image)
        images.append(image)
        n += 1


green_tank_images = []
zombie_1_images = []

get_image(green_tank_spritesheet, green_tank_images, 10, 15, 10, 5)
get_image(zombie_1_spritesheet, zombie_1_images, 64, 15, 9, 3)

# игровой цикл

running = True

while running:

    clock.tick(fps)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                s.play()
                bullet = tank.fire()
                bullets.append(bullet)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        tank.rotate_r()
    if keys[pygame.K_a]:
        tank.rotate_l()
    if keys[pygame.K_w]:
        tank.move_forward()
    if keys[pygame.K_s]:
        tank.move_back()

    screen.blit(background, (0, 0))
    screen.fill('White')
    for b in bullets:
        if zombie.hittest(b):
            d.play()
        b.move()
        b.render()
    tank.render(green_tank_images)
    zombie.targetting()
    zombie.move()
    zombie.render(zombie_1_images)
    pygame.display.update()
