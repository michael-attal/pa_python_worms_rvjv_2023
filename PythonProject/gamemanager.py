import math
import random

import pygame

# General game options
screen_size = screen_width, screen_height = 600, 400
screen = pygame.display.set_mode(screen_size)
teams = []
neutral_gameobjects = pygame.sprite.Group()
terrain = pygame.sprite.Group()
clock = pygame.time.Clock()
wind = pygame.Vector2(0, 0)
worm_bounciness = 1
grenade_bounciness = 1
maximum_charge_time = 1
maximum_charge = 500
rocket_explosion_radius = 100
explosions_duration = .5
grenade_explosion_radius = 50
grenade_nb_of_seconds_before_explosion = 2

def initGame():
    for team in teams:
        teamColor = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        for worm in team:
            worm.image.fill(teamColor)

    teams[0].sprites()[0].controlled = True

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

    # Determine wind direction
    angleRad = random.random() * 2 * math.pi
    wind = pygame.Vector2(math.cos(angleRad), math.sin(angleRad))
    wind *= random.random() * 5.0


def finishGame():
    print("Game over!")
    pygame.event.post(pygame.event.Event(pygame.QUIT))