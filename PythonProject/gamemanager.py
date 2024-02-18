import math
import random
import pygame

from GameObjects import physicsobject

# General game options

# Technical assists
screen_size = screen_width, screen_height = 600, 400
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
air_volumetric_pressure = 1.293

# Game state trackers
teams = []
neutral_gameobjects = pygame.sprite.Group()
terrain = pygame.sprite.Group()
wind = pygame.Vector2(0, 0)

# Worms
worm_size = 32
worm_base_hp = 1000
worm_bounciness = 1
grenade_bounciness = 1
maximum_charge_time = 1
maximum_charge = 500

# Explosives / Projectiles
explosions_duration = .5
rocket_max_damage = 600
rocket_max_force = 500
rocket_explosion_radius = 50
rocket_friction_mod = 0.1
grenade_max_damage = 1100
grenade_max_force = 100
grenade_explosion_radius = 100
grenade_friction_mod = 0.1
grenade_nb_of_seconds_before_explosion = 2

# UI
wind_arrow_max_length = 100

def resetWind():
    global wind
    angleRad = random.random() * 2 * math.pi
    wind = pygame.Vector2(math.cos(angleRad), math.sin(angleRad))
    wind *= random.random() * 3.0


# Game-managing methods
def initGame(num_teams, num_worms):
    for i in range(num_teams):
        teamColor = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        team = pygame.sprite.Group()
        for j in range(num_worms):
            worm = physicsobject.Worm(random.randint(0, screen_width - worm_size), random.randint(0, screen_height // 2), teamColor)
            team.add(worm)
        teams.append(team)

    teams[0].sprites()[0].controlled = True
    resetWind()

def nextTurn():
    # Check game ending conditions
    for team in teams:
        if len(team.sprites()) == 0:
            teams.remove(team)

    if len(teams) <= 1:
        finishGame()
        return

    currentWorm = teams[0].sprites()[0]
    currentWorm.controlled = False
    # Tiny trick to put current worm back to the end of the group
    teams[0].remove(currentWorm)
    teams[0].add(currentWorm)

    # Same trick with teams
    currentTeam = teams.pop(0)
    teams.append(currentTeam)

    # Give turn to next worm
    teams[0].sprites()[0].controlled = True

    resetWind()


def finishGame():
    print("Game over!")
    pygame.event.post(pygame.event.Event(pygame.QUIT))