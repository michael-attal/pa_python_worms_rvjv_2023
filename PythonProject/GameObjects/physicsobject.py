import math

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
        elif self.rect.y > h - self.rect.height:
            self.rect.y = h - self.rect.height
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
        self.bounciness = gamemanager.worm_bounciness
        super().__init__(x, y)

    def update(self):

# Uncomment if at some point I figure out why the equation is completely f*cked up...

#        if self.chargeTime != -1:
#            pos0 = self.position + self.shootDirection * self.rect.width
#            f0 = self.shootDirection * min((((pygame.time.get_ticks() - self.chargeTime) / 1000) / gamemanager.maximum_charge_time) * gamemanager.maximum_charge, gamemanager.maximum_charge)
#            print(f0)
#
#            posList = []
#            for t in range(0, 1000):
#                t /= 100
#                posList.append(pygame.Vector2(
#                    pos0.x + f0.x / 0.99 * (1 - math.exp(-0.99 * t)),
#                    pos0.y + ((f0.y / 0.99) - (GRAVITY.y / 0.9801)) * (1 - math.exp(-0.99 * t)) + (GRAVITY.y * t) / 0.99
#                ))
#
#            pygame.draw.lines(gamemanager.screen, pygame.Color("red"), False, posList)

        if self.controlled:
            # Draw "controlled" arrow
            pygame.draw.polygon(gamemanager.screen, pygame.Color("black"),[
                pygame.Vector2(self.position.x, self.rect.y),
                pygame.Vector2(self.position.x + self.rect.width / 4, self.rect.y - 10),
                pygame.Vector2(self.position.x - self.rect.width / 4, self.rect.y - 10)
            ])

            keys = pygame.key.get_pressed()
            # Ground controls
            if self.grounded:
                # Move left and right
                if keys[pygame.K_LEFT] or keys[pygame.K_q]:
                    self.velocity.x = -100
                elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    self.velocity.x = 100
                else:
                    self.velocity.x = 0
                # Jump
                if keys[pygame.K_SPACE]:
                    self.velocity.y -= 250
            #Air controls
            else:
                if keys[pygame.K_SPACE]:
                    pygame.draw.circle(gamemanager.screen, pygame.Color("gray"), [self.rect.x + self.rect.width / 2, self.rect.y - 10], self.rect.width / 2, draw_top_left=True, draw_top_right=True)

                    self.velocity -= ((math.pi * (self.rect.width ** 2) / 2) * gamemanager.air_volumetric_pressure * GRAVITY) * pygame.time.Clock.get_time(gamemanager.clock) / 1000

        self.grounded = False

        super().update()

    def handleCollision(self, platform):
        super().handleCollision(platform)
        self.grounded = True

    def handleEvent(self, event):

        # Rocket event (Right or left click)
        if self.controlled and event.type == pygame.MOUSEBUTTONDOWN:
            self.chargeTime = pygame.time.get_ticks()
            self.shootDirection = (pygame.mouse.get_pos() - self.position).normalize()
            self.controlled = False
        if event.type == pygame.MOUSEBUTTONUP and self.chargeTime != -1:
            rocket_pos = self.position + self.shootDirection * self.rect.width
            force = min((((pygame.time.get_ticks() - self.chargeTime) / 1000) / gamemanager.maximum_charge_time) * gamemanager.maximum_charge, gamemanager.maximum_charge)
            gamemanager.neutral_gameobjects.add(Rocket(rocket_pos.x, rocket_pos.y, self.shootDirection * force))
            self.chargeTime = -1

        # Grenade event (press G)
        if self.controlled and event.type == pygame.KEYDOWN and event.key == pygame.K_g:
            self.chargeTime = pygame.time.get_ticks()
            self.shootDirection = (pygame.mouse.get_pos() - self.position).normalize()
            self.controlled = False
        if event.type == pygame.KEYUP and event.key == pygame.K_g and self.chargeTime != -1:
            grenade_pos = self.position + self.shootDirection * self.rect.width
            force = (((pygame.time.get_ticks() - self.chargeTime) / 1000) / gamemanager.maximum_charge_time) * gamemanager.maximum_charge
            gamemanager.neutral_gameobjects.add(Grenade(grenade_pos.x, grenade_pos.y, self.shootDirection * force))
            self.chargeTime = -1

class Rocket(PhysicsObject):

    def __init__(self, x, y, velocity):
        self.image = pygame.Surface((8, 8))
        self.image.fill(pygame.Color("red"))
        self.rect = self.image.get_rect(topleft=(x, y))
        super().__init__(x, y)
        self.velocity = velocity
        self.explode_time = -1


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

class Grenade(PhysicsObject):
    def __init__(self, x, y, velocity):
        self.image = pygame.Surface((13, 13))
        self.image.fill(pygame.Color("green"))
        self.rect = self.image.get_rect(topleft=(x, y))
        super().__init__(x, y)
        self.velocity = velocity
        self.explode_time = -1
        self.bounciness = gamemanager.grenade_bounciness
        self.thrown_time = pygame.time.get_ticks()

    def update(self):
        backup_velocity_x = self.velocity.x
        backup_velocity_y = self.velocity.y
        super().update()

        if self.explode_time != -1:
            self.velocity = pygame.Vector2(0, 0)
            time_since_explosion = pygame.time.get_ticks() - self.explode_time
            if time_since_explosion / 1000.0 > gamemanager.explosions_duration:
                self.kill()
                gamemanager.nextTurn()
                return
            pygame.draw.circle(gamemanager.screen, pygame.Color("orange"), self.position, (1 - ((time_since_explosion / 1000.0) / gamemanager.explosions_duration)) * gamemanager.grenade_explosion_radius)


        # Check if the grenade hasn't already exploded and the timer has expired
        if self.explode_time == -1 and pygame.time.get_ticks() - self.thrown_time > gamemanager.grenade_nb_of_seconds_before_explosion * 1000:
            self.explode()

        # Bounce off walls. Comment it out if you prefer to only block grenades from hitting the wall.
        w, h = pygame.display.get_surface().get_size()
        if self.rect.left <= 0 or self.rect.right >= w:
            self.velocity.x = -backup_velocity_x * self.bounciness
        if self.rect.top <= 0 or self.rect.bottom >= h:
            self.velocity.y = -backup_velocity_y * self.bounciness

        # Check if the grenade collide with a worm
        for team in gamemanager.teams:
            for worm in team:
                if pygame.sprite.collide_rect(self, worm):
                    self.handleCollision(worm)

    def explode(self):
        self.explode_time = pygame.time.get_ticks();
        self.image = pygame.Surface((0, 0));
        for team in gamemanager.teams:
            for worm in team:
                center_pos = pygame.Vector2(self.rect.center[0], self.rect.center[1])
                eff_radius = worm.calculateEffectiveRadius(center_pos)
                worm_center_pos = pygame.Vector2(worm.rect.center[0], worm.rect.center[1])
                if gamemanager.grenade_explosion_radius + eff_radius > center_pos.distance_to(worm_center_pos):
                    worm.kill()

    def handleCollision(self, collided_with):
        bounciness = getattr(collided_with, 'bounciness', 1)  # if bounciness doesn't exist set 1 by default
        # Adjust the position of the grenade upon collision with any element to prevent it from being blocked.
        while pygame.sprite.collide_rect(self, collided_with):
            self.adjust_position_after_collision(collided_with)

        if isinstance(collided_with, Worm):
                self.velocity.y *= -1 * bounciness * self.bounciness
                self.velocity.x *= -1 * bounciness * self.bounciness
        # Grenade collided with the platform, so I need to adjust its bounciness since 0.1 is not satisfactory to me.
        else:
            self.velocity.y *= -1 * bounciness * self.bounciness * 5
            # We only have a horizontal plateform for now, so the grenade will never bounce horizontally.
            # self.velocity.x *= -1 * bounciness * self.bounciness * 5

    def adjust_position_after_collision(self, collided_with):
        # Calculation of the position difference between the center of the Grenade and the object with which it collides.
        delta_x = self.rect.centerx - collided_with.rect.centerx
        delta_y = self.rect.centery - collided_with.rect.centery

        # Calculation of the combined width and height of the two rectangles to determine collision.
        combined_half_width = (self.rect.width + collided_with.rect.width) / 2
        combined_half_height = (self.rect.height + collided_with.rect.height) / 2

        if abs(delta_x) / combined_half_width < abs(delta_y) / combined_half_height:
            # Adjust vertical collision rect offset
            if delta_y > 0:  # From the top
                self.rect.y = collided_with.rect.y + collided_with.rect.height
            else:
                self.rect.y = collided_with.rect.y - self.rect.height
        else:
            # Adjust horizontal collision rect offset
            if delta_x > 0: # From the left
                self.rect.x = collided_with.rect.x + collided_with.rect.width
            else:
                self.rect.x = collided_with.rect.x - self.rect.width
