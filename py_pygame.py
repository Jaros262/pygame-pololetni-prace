# Import the pygame module
import pygame

# Import random for random numbers
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650

pictureArray = ["GameObj/Wiz-up1", "GameObj/Wiz-up2"]
# Define the Player object extending pygame.sprite.Sprite
# The surface we draw on the screen is now a property of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        #self.surf = pygame.Surface((50, 50))
        #self.surf.fill((255, 255, 100))
        self.surf = pygame.image.load("GameObj/Wiz2-stop.png").convert()
        self.rect = self.surf.get_rect()

    # Move the sprite based on keypresses
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
# Define the enemy object extending pygame.sprite.Sprite
# The surface we draw on the screen is now a property of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("GameObj/rock-rect.png").convert()
        self.score = 0

        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(50, SCREEN_HEIGHT-50),
            )
        )
        self.speed = random.randint(1, 5)

    # Move the sprite based on speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 75:
            self.kill()
            self.score =+ 1
            print(self.score)


# Initialize pygame
pygame.init()
pygame.font.init()
font = pygame.font.Font('Fonts/Pixelfy.ttf', 32)
text = font.render('Score:')
# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = pygame.image.load("GameObj/borders-800x650.png")

# Create a custom event for adding a new enemy.
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 750)


# Create our 'player'
player = Player()

# Create groups to hold enemy sprites, and every sprite
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Variable to keep our main loop running
running = True
gameframe = 0
fpsclock = pygame.time.Clock()
# Our main loop
while running:
    # Look at every event in the queue
    fpsclock.tick(60)
    gameframe+=1
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop
        elif event.type == QUIT:
            running = False

        # Should we add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy, and add it to our sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # Update the position of our enemies
    enemies.update()

    # Fill the screen with black
    screen.fill((0, 0, 0))
    screen.blit(background, (0,0))
    text.fill(0,0,0)

    # Draw all our sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, remove the player and stop the loop
        player.kill()
        running = False

    # Flip everything to the display
    pygame.display.flip()
