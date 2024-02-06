import pygame

class Platform(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, bounciness=0.1):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.bounciness = bounciness