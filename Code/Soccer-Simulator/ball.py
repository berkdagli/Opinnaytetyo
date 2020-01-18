import pygame
from constants import Constants
import math
from soccerfield import SoccerField


class Ball():
    def __init__(self, x, y, size, mass=0.7):
        self.x = x
        self.y = y
        self.size = size
        self.colour = (255, 255, 255)
        self.thickness = 0
        self.speed = 0
        self.angle = 0
        self.mass = mass
        self.drag = (self.mass / (self.mass + Constants.MASS_OF_AIR)) ** self.size

    def display(self, screen):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        # (self.angle, self.speed) = addVectors((self.angle, self.speed), gravity)
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= self.drag

    def bounce(self,soccerfield):
        if (self.x > int(19*Constants.SIZE_WIDTH/20) - self.size) and (self.y < int(Constants.SIZE_HEIGHT/3) or self.y > int(2*Constants.SIZE_HEIGHT/3)):
            self.x = 2 * (int(19*Constants.SIZE_WIDTH/20) - self.size) - self.x
            self.angle = - self.angle
            self.speed *= Constants.ELASTICITY
        elif self.x < self.size + int(Constants.SIZE_WIDTH/20) and (self.y < int(Constants.SIZE_HEIGHT/3) or self.y > int(2*Constants.SIZE_HEIGHT/3)):
            self.x = 2 * (self.size + int(Constants.SIZE_WIDTH/20)) - self.x
            self.angle = - self.angle
            self.speed *= Constants.ELASTICITY

        if self.y > int(9*Constants.SIZE_HEIGHT/10) - self.size:
            self.y = 2 * (int(9*Constants.SIZE_HEIGHT/10) - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= Constants.ELASTICITY
        elif self.y < int(Constants.SIZE_HEIGHT/10) + self.size:
            self.y = 2 * (int(Constants.SIZE_HEIGHT/10) + self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= Constants.ELASTICITY

        for i in range(4):
            dx = self.x - soccerfield.goalposts[i].x
            dy = self.y - soccerfield.goalposts[i].y
            dist = math.hypot(dx, dy)
            if dist < self.size + soccerfield.goalposts[i].size:
                angle = math.atan2(dy, dx) + 0.5 * math.pi
                total_mass = self.mass + 9999
                (self.angle, self.speed) = self.addVectors(self.angle, self.speed * (self.mass - 9999) / total_mass, angle,0)
                self.speed *= Constants.ELASTICITY
                overlap = 0.5 * (self.size + soccerfield.goalposts[i].size - dist + 1)
                self.x += math.sin(angle) * overlap
                self.y -= math.cos(angle) * overlap
                break

    def addVectors(self, angle1, length1, angle2, length2):
        x = math.sin(angle1) * length1 + math.sin(angle2) * length2
        y = math.cos(angle1) * length1 + math.cos(angle2) * length2

        angle = 0.5 * math.pi - math.atan2(y, x)
        length = math.hypot(x, y)

        return (angle, length)






