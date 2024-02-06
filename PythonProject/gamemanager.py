import pygame


screen_size = screen_width, screen_height = 600, 400
screen = pygame.display.set_mode(screen_size)
teams = []
neutral_gameobjects = pygame.sprite.Group()
terrain = pygame.sprite.Group()
clock = pygame.time.Clock()
rocket_explosion_radius = 100