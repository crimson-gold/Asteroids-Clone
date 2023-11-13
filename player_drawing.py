import pygame
import math
from random import randint
# Constants and Configuration
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PLAYER_SIZE = 10
ROTATION_SPEED = 4
ACCELERATION = 0.12
FRICTION = 0.99
FPS = 60

class Player:
    def __init__(self, screen_width, screen_height):
        self.pos = [screen_width // 2, screen_height // 2]
        self.velocity = [0, 0]
        self.angle = randint(0,360)

    def update(self):
        # Update player position based on velocity
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        # Wrap the player around the screen
        self.pos[0] %= SCREEN_WIDTH
        self.pos[1] %= SCREEN_HEIGHT

        # Apply friction to slow down the player
        self.velocity[0] *= FRICTION
        self.velocity[1] *= FRICTION

    def accelerate(self):
        # Calculate acceleration based on the angle
        acceleration_x = ACCELERATION * math.cos(math.radians(self.angle))
        acceleration_y = ACCELERATION * math.sin(math.radians(self.angle))
        
        # Apply acceleration to velocity
        self.velocity[0] += acceleration_x
        self.velocity[1] += acceleration_y

    def draw(self, screen):
        # Draw the player as an isosceles triangle with a smaller base
        points = [
            (self.pos[0] + (PLAYER_SIZE * 2) * math.cos(math.radians(self.angle)),
             self.pos[1] + (PLAYER_SIZE * 2) * math.sin(math.radians(self.angle))),
            (self.pos[0] + (PLAYER_SIZE // 2) * math.cos(math.radians(self.angle - 120)),
             self.pos[1] + (PLAYER_SIZE // 2) * math.sin(math.radians(self.angle - 120))),
            (self.pos[0] + (PLAYER_SIZE // 2) * math.cos(math.radians(self.angle + 120)),
             self.pos[1] + (PLAYER_SIZE // 2) * math.sin(math.radians(self.angle + 120)))
        ]
        pygame.draw.lines(screen, WHITE, True, points)

def handle_input(player):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        player.angle += ROTATION_SPEED
    if keys[pygame.K_a]:
        player.angle -= ROTATION_SPEED
    if keys[pygame.K_SPACE]:
        player.accelerate()

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroid Game")

    player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        handle_input(player)
        player.update()

        screen.fill(BLACK)
        player.draw(screen)

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
if __name__ == "__main__":
    main()