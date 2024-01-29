import sys
import pygame

from Level import Level

pygame.init()

# Setup game window
screen_size = screen_width, screen_height = 600, 400
pygame.display.set_caption("Game Window")
screen = pygame.display.set_mode(screen_size)

# Set FPS here
fps_limit = 60

clock = pygame.time.Clock()

level = Level(screen)
# Level settings here (If any)

game_loop_running = True
while game_loop_running:
    # Ticking game logic (I think? Not quite sure how this works yet)
    clock.tick(fps_limit)

    # Event handler
    for event in pygame.event.get():
        # System event for window closing (X button on the window)
        if event.type == pygame.QUIT:
            game_loop_running = False

    # Rendering (Base: White screen)
    screen.fill((255, 255, 255))
    level.drawLevelRender()

    # Update game window
    pygame.display.flip()

pygame.quit()
sys.exit()