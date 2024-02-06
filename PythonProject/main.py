import sys
import pygame
import gamemanager
from GameObjects import physicsobject
from Environment import platform

# Setup game window
pygame.init()
pygame.display.set_caption("Game Window")

# Set FPS here
fps_limit = 60

# Setup game
worm = physicsobject.Worm(gamemanager.screen_width / 2, 10)
team1_sprites = pygame.sprite.Group()
team1_sprites.add(worm)
gamemanager.teams.append(team1_sprites)

gamemanager.terrain.add(platform.Platform(0, gamemanager.screen_height - 30, gamemanager.screen_width, 30))

game_loop_running = True
while game_loop_running:
    # Event handler
    for event in pygame.event.get():
        # System event for window closing (X button on the window)
        if event.type == pygame.QUIT:
            game_loop_running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                gamemanager.neutral_gameobjects.add(physicsobject.Rocket(0, gamemanager.screen_height - 64))

    # Rendering (Base: White screen)
    gamemanager.screen.fill((255, 255, 255))
    gamemanager.terrain.draw(gamemanager.screen)
    for team in gamemanager.teams:
        team.draw(gamemanager.screen)
    gamemanager.neutral_gameobjects.draw(gamemanager.screen)

    # Players loop
    for team in gamemanager.teams:
        team.update()
        for sprite in gamemanager.terrain.sprites():
            collided = pygame.sprite.spritecollide(sprite, team, False)
            for collidedWorm in collided:
                collidedWorm.handleCollision(sprite)

    # Other entities loop
    gamemanager.neutral_gameobjects.update()
    for sprite in gamemanager.terrain.sprites():
        collided = pygame.sprite.spritecollide(sprite, gamemanager.neutral_gameobjects, False)
        for collidedEntity in collided:
            collidedEntity.handleCollision(sprite)

    # Update game window
    pygame.display.flip()

    # Tick game logic
    gamemanager.clock.tick(fps_limit)

pygame.quit()
sys.exit()