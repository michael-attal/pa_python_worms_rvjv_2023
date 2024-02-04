import pygame

GRAVITY = pygame.Vector2(0, 9.8)


class PhysicsObject(pygame.sprite.Sprite):

    velocity = pygame.Vector2(0, 0)

    def __init__(self, clock, x, y):
        super().__init__()
        self.clock = clock
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x += self.velocity.x * (pygame.time.Clock.get_time(self.clock) / 1000.0)
        self.rect.y += self.velocity.y * (pygame.time.Clock.get_time(self.clock) / 1000.0)

        self.velocity += GRAVITY

    def handleCollision(self, platform):
        self.velocity.y = 0


class Worm(PhysicsObject):

    def __init__(self, clock, x, y):
        self.image = pygame.Surface((32, 32))
        self.rect = self.image.get_rect(topleft=(x, y))
        super().__init__(clock, x, y)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.velocity.x = -100
        elif keys[pygame.K_RIGHT]:
            self.velocity.x = 100
        else:
            self.velocity.x = 0

        if keys[pygame.K_SPACE]:
            self.velocity.y = -100

        super().update()