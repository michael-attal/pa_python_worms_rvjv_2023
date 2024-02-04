import sys
import pygame
from Entities import physicsobject
from Environment import platform

# Setup game window
pygame.init()
screen_size = screen_width, screen_height = 600, 400
pygame.display.set_caption("Game Window")
screen = pygame.display.set_mode(screen_size)

# Set FPS here
fps_limit = 60

clock = pygame.time.Clock()

# Setup game
worm = physicsobject.Worm(clock, screen_width / 2, 10)
worm_sprites = pygame.sprite.Group()
worm_sprites.add(worm)

platform = platform.Platform(0, screen_height - 10, screen_width, 5)
platform_sprites = pygame.sprite.Group()
platform_sprites.add(platform)

game_loop_running = True
while game_loop_running:
    # Event handler
    for event in pygame.event.get():
        # System event for window closing (X button on the window)
        if event.type == pygame.QUIT:
            game_loop_running = False

    worm_sprites.update()
    for sprite in platform_sprites.sprites():
        collided = pygame.sprite.spritecollide(sprite, worm_sprites, False)
        for collidedWorm in collided:
            collidedWorm.handleCollision(sprite)

    # Rendering (Base: White screen)
    screen.fill((255, 255, 255))
    platform_sprites.draw(screen)
    worm_sprites.draw(screen)

    # Update game window
    pygame.display.flip()

    # Ticking game logic (I think? Not quite sure how this works yet)
    clock.tick(fps_limit)

pygame.quit()
sys.exit()