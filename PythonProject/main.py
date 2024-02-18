import sys
import pygame
import gamemanager
from Environment import platform

def drawUI():
    if pygame.font:
        # Instructions
        font = pygame.font.Font(None, 16)
        text = font.render("ZQSD - Click for rockets - G for grenades - Space to jump", True, (0, 0, 0))
        textpos = text.get_rect(centerx=gamemanager.screen_width * 2/5, y=0, width=gamemanager.screen_width * 4/5, height=50)
        gamemanager.screen.blit(text, textpos)

        # Wind arrow
        arrow_center_pos = pygame.Vector2(gamemanager.screen_width - gamemanager.wind_arrow_max_length / 2, gamemanager.wind_arrow_max_length / 2)
        arrow_length = (gamemanager.wind.magnitude() / 3) * gamemanager.wind_arrow_max_length
        normalized_wind = gamemanager.wind.normalize()
        pygame.draw.line(gamemanager.screen, pygame.Color("purple"), arrow_center_pos + normalized_wind * arrow_length / 2, arrow_center_pos - normalized_wind * arrow_length / 2)

        wind_normal = pygame.Vector2(-gamemanager.wind.y, gamemanager.wind.x).normalize() * 3
        pygame.draw.polygon(gamemanager.screen, pygame.Color("purple"), [
            arrow_center_pos + wind_normal,
            arrow_center_pos + normalized_wind * arrow_length / 2,
            arrow_center_pos - wind_normal
    ])


# Ask for parameters
num_teams = int(input("How many teams?"))
num_worms = int(input("How many worms per team?"))

# Setup game window
pygame.init()
pygame.display.set_caption("Game Window")

# Set FPS here
fps_limit = 60

# Setup game
background = pygame.image.load("./Assets/background.jpg")
backgroundRect = background.get_rect()
backgroundRect.left, backgroundRect.top = 0, 0

gamemanager.terrain.add(platform.Platform(0, gamemanager.screen_height - 30, gamemanager.screen_width, 30))

gamemanager.initGame(num_teams, num_worms)

game_loop_running = True
while game_loop_running:
    # Event handler
    for event in pygame.event.get():
        # System event for window closing (X button on the window)
        if event.type == pygame.QUIT:
            game_loop_running = False

        for team in gamemanager.teams:
            for worm in team:
                worm.handleEvent(event)

    # Rendering (Base: White screen)
    gamemanager.screen.fill((255, 255, 255))
    gamemanager.screen.blit(background, backgroundRect)
    gamemanager.terrain.draw(gamemanager.screen)
    for team in gamemanager.teams:
        team.draw(gamemanager.screen)
    gamemanager.neutral_gameobjects.draw(gamemanager.screen)
    drawUI()

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