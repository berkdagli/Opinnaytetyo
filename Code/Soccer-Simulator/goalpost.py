import pygame
from constants import Constants

class Goalpost():
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.thickness = 0
        self.colour = (255, 255, 255)

    def display(self, screen):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)