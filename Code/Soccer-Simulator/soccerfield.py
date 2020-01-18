import pygame
from constants import Constants
from goalpost import Goalpost

class SoccerField:
    def __init__(self):
        self.linecolor = Constants.LINE_COLOR
        self.thickness = 1
        self.goalposts = self.create_goalposts()

    def display(self, screen):
        pygame.draw.circle(screen, self.linecolor, (int(Constants.SIZE_WIDTH/2), int(Constants.SIZE_HEIGHT/2)), int((8*Constants.SIZE_HEIGHT/10)/5), self.thickness)
        pygame.draw.line(screen, self.linecolor, (int(Constants.SIZE_WIDTH/2), int(Constants.SIZE_HEIGHT/10)), (int(Constants.SIZE_WIDTH/2), int(9*Constants.SIZE_HEIGHT/10)), 1)
        for i in range(4):
            self.goalposts[i].display(screen)
        pygame.draw.line(screen, self.linecolor, (self.goalposts[0].x, int(Constants.SIZE_HEIGHT/10)), (self.goalposts[2].x, int(Constants.SIZE_HEIGHT/10)), 1)
        pygame.draw.line(screen, self.linecolor, (self.goalposts[0].x, int(9*Constants.SIZE_HEIGHT/10)), (self.goalposts[2].x, int(9*Constants.SIZE_HEIGHT/10)), 1)
        pygame.draw.line(screen, self.linecolor, (self.goalposts[0].x, int(Constants.SIZE_HEIGHT/10)), (self.goalposts[1].x, int(9*Constants.SIZE_HEIGHT/10)), 1)
        pygame.draw.line(screen, self.linecolor, (self.goalposts[2].x, int(Constants.SIZE_HEIGHT/10)), (self.goalposts[3].x, int(9*Constants.SIZE_HEIGHT/10)), 1)
        pygame.draw.line(screen, self.linecolor, (self.goalposts[0].x, self.goalposts[0].y), (0, self.goalposts[0].y), 1)
        pygame.draw.line(screen, self.linecolor, (self.goalposts[1].x, self.goalposts[1].y), (0, self.goalposts[1].y), 1)
        pygame.draw.line(screen, self.linecolor, (self.goalposts[2].x, self.goalposts[2].y), (Constants.SIZE_WIDTH, self.goalposts[2].y), 1)
        pygame.draw.line(screen, self.linecolor, (self.goalposts[3].x, self.goalposts[3].y), (Constants.SIZE_WIDTH, self.goalposts[3].y), 1)

    def create_goalposts(self):
        leftUp = Goalpost(int(Constants.SIZE_WIDTH/20), int(Constants.SIZE_HEIGHT/3), 7)
        leftDown = Goalpost(int(Constants.SIZE_WIDTH/20), int((2*Constants.SIZE_HEIGHT)/3), 7)
        rightUp = Goalpost(int((19*Constants.SIZE_WIDTH)/20), int(Constants.SIZE_HEIGHT/3), 7)
        rightDown = Goalpost(int((19*Constants.SIZE_WIDTH)/20), int((2*Constants.SIZE_HEIGHT)/3), 7)
        return [leftUp,leftDown,rightUp,rightDown]