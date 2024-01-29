import pygame

class Level:

    _window = None
    _geometry = []

    def __init__(self, window):
        self._window = window

    def addToGeometry(self, obstacleGeometry):
        self._geometry.append(obstacleGeometry)

    def clearGeometry(self):
        self._geometry = []

    def drawLevelRender(self):
        for obstacle in self._geometry:
            pygame.draw.polygon(self._window, pygame.Color("brown"), obstacle)

    def serializeLevel(self, path):
        with open(path, "w") as output:
            for obstacle in self._geometry:
                output.write(str(str(i) + "," for i in obstacle))
