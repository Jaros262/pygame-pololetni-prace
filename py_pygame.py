import pygame

import random
import pygame.freetype

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650

pictureArray = ["GameObj/Wiz-up1", "GameObj/Wiz-up2"]

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("GameObj/Wiz2-stop.png").convert()
        self.rect = self.surf.get_rect()
        self.score = 0

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            self.surf = pygame.image.load("GameObj/Wiz2-up.png").convert()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            self.surf = pygame.image.load("GameObj/Wiz2-stop.png").convert()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
            self.surf = pygame.image.load("GameObj/Wiz2-left.png").convert()
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
            self.surf = pygame.image.load("GameObj/Wiz2-right.png").convert()

        # Keep player on the screen
        if self.rect.left < 50:
            self.rect.left = 50
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 50:
            self.rect.top = 50
        elif self.rect.bottom >= SCREEN_HEIGHT-50:
            self.rect.bottom = SCREEN_HEIGHT-50

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("GameObj/rock-rect.png").convert()
        self.score = 0
        self.speed2 = 5
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(65, SCREEN_HEIGHT-65),
            )
        )
        self.speed = random.randint(1, self.speed2)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 75:
            self.kill()
            #player.score =+ 1
            #print(player.score)

pygame.init()
pygame.font.init()
font = pygame.font.Font('Fonts/Pixelfy.ttf', 32)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = pygame.image.load("GameObj/borders-800x650.png")

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 750)


player = Player()
enemy = Enemy()

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

score = 0
running = True
gameframe = 0
fpsclock = pygame.time.Clock()

while running:
    fpsclock.tick(60)
    gameframe+=1
    if gameframe % 750 == 0:
        enemy.speed2 +=1
    for event in pygame.event.get():

        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            if new_enemy.rect.right < 75:
                player.score += 1


    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    text = font.render(f'Score: ', True, [255, 0, 0])
    enemies.update()

    screen.fill((0, 0, 0))
    screen.blit(background, (0,0))
    screen.blit(text, (65, 5))
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    print(player.score)
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False


    pygame.display.flip()