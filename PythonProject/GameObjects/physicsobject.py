import pygame
import gamemanager

GRAVITY = pygame.Vector2(0, 9.8)

class PhysicsObject(pygame.sprite.Sprite):
    def _getPosition(self):
        return pygame.Vector2(self.rect.center[0], self.rect.center[1])

    position = property(_getPosition)

    def __init__(self, x, y, frictionmod=0.01):
        super().__init__()
        self.velocity = pygame.Vector2(0, 0)
        self.rect.x = x
        self.rect.y = y
        self.frictionmod = frictionmod

    def update(self):
        self.rect.x += self.velocity.x * (pygame.time.Clock.get_time(gamemanager.clock) / 1000.0)
        self.rect.y += self.velocity.y * (pygame.time.Clock.get_time(gamemanager.clock) / 1000.0)

        # Don't go out of the screen
        w, h = pygame.display.get_surface().get_size()
        if self.rect.x < 0:
            self.rect.x = 0
            self.velocity.x = 0
        elif self.rect.x > w - self.rect.width:
            self.rect.x = w - self.rect.width
            self.velocity.x = 0

        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > h - self.rect.width:
            self.rect.y = h - self.rect.width
            self.velocity.y = 0

        self.velocity += GRAVITY
        self.velocity *= 1 - self.frictionmod

    def handleCollision(self, platform):
        if (self.velocity.y > 0):
            self.rect.bottom = platform.rect.top

        self.velocity.y = -self.velocity.y * platform.bounciness
        self.velocity.x = self.velocity.x * (1 - platform.friction)

    # Calculates the effective radius of the rectangle compared to another point in space; In other words, the distance beetween the closest point of the rectangle and its center
    def calculateEffectiveRadius(self, point):
        center = pygame.Vector2(self.rect.center[0], self.rect.center[1])
        v1 = (center - point).normalize()

        # Please don't ask, I don't know why I need to do this either
        v1.x = abs(v1.x)
        v1.y = abs(v1.y)

        return 1 / 2 * abs(pygame.Vector2(self.rect.width, 0).dot(v1) + pygame.Vector2(0, self.rect.height).dot(v1))


class Worm(PhysicsObject):

    def __init__(self, x, y):
        self.image = pygame.Surface((32, 32))
        self.image.fill(pygame.Color("brown"))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.grounded = False
        self.controlled = False
        self.chargeTime = -1
        super().__init__(x, y)

    def update(self):
        if self.controlled:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.velocity.x = -100
            elif keys[pygame.K_RIGHT]:
                self.velocity.x = 100
            else:
                self.velocity.x = 0

            if keys[pygame.K_SPACE] and self.grounded:
                self.velocity.y -= 250

        self.grounded = False

        super().update()

    def handleCollision(self, platform):
        super().handleCollision(platform)
        self.grounded = True

    def handleEvent(self, event):
        if self.controlled and event.type == pygame.MOUSEBUTTONDOWN:
            self.chargeTime = pygame.time.get_ticks()
            self.shootDirection = (pygame.mouse.get_pos() - self.position).normalize()
            self.controlled = False
        if event.type == pygame.MOUSEBUTTONUP and self.chargeTime != -1:
            rocket_pos = self.position + self.shootDirection * self.rect.width
            force = (((pygame.time.get_ticks() - self.chargeTime) / 1000) / gamemanager.maximum_charge_time) * gamemanager.maximum_charge
            gamemanager.neutral_gameobjects.add(Rocket(rocket_pos.x, rocket_pos.y, self.shootDirection * force))
            self.chargeTime = -1

class Rocket(PhysicsObject):

    explode_time = -1

    def __init__(self, x, y, velocity):
        self.image = pygame.Surface((8, 8))
        self.image.fill(pygame.Color("red"))
        self.rect = self.image.get_rect(topleft=(x, y))
        super().__init__(x, y)
        self.velocity = velocity


    def update(self):
        super().update()
        self.velocity += gamemanager.wind

        if self.explode_time != -1:
            self.velocity = pygame.Vector2(0, 0)
            time_since_explosion = pygame.time.get_ticks() - self.explode_time
            if time_since_explosion / 1000.0 > gamemanager.explosions_duration:
                self.kill()
                gamemanager.nextTurn()
                return
            pygame.draw.circle(gamemanager.screen, pygame.Color("orange"), self.position, (1 - ((time_since_explosion / 1000.0) / gamemanager.explosions_duration)) * gamemanager.rocket_explosion_radius)

    def handleCollision(self, platform):
        super().handleCollision(platform)

        # On initial collision
        if self.explode_time == -1:
            self.image = pygame.Surface((0, 0))
            self.explode_time = pygame.time.get_ticks()

            for team in gamemanager.teams:
                for worm in team:
                    center_pos = pygame.Vector2(self.rect.center[0], self.rect.center[1])
                    eff_radius = worm.calculateEffectiveRadius(center_pos)
                    worm_center_pos = pygame.Vector2(worm.rect.center[0], worm.rect.center[1])
                    if gamemanager.rocket_explosion_radius + eff_radius > center_pos.distance_to(worm_center_pos):
                        worm.kill()