import pygame
from game_object import GameObject


class Computer_checkers(GameObject):

    def __init__(self, x, y, r, color, check_type="ordinary"):
        GameObject.__init__(self, x - r, y - r, r * 2, r * 2)
        self.radius = r
        self.diameter = r * 2
        self.color = color
        self.checkers_type = check_type

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.center, self.radius)
