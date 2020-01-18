import torch
import math

class Constants:

    TEAM_MARL = 1
    TEAM_SARL = -1
    TEAM_NONE = 0

    MASS_OF_AIR = 1.1
    ELASTICITY = 0.75

    BACKGROUND_COLOR = (0, 150, 0)
    LINE_COLOR = (255,255,255)

    SIZE_WIDTH = 600
    SIZE_HEIGHT = 375

    TEAM_MARL_COLOUR = (0,0,255)
    TEAM_SARL_COLOUR = (255,0,0)
    BALL_COLOUR = (255,255,0)

    UPDATE_DOUBLE_DXY = 0.7
    UPDATE_SINGLE_DXY = 1
    MAX_DISTANCE_TO_GOAL_LINE = math.sqrt((int((19*SIZE_WIDTH)/20)-10)**2 + (int(SIZE_HEIGHT/3)-10)**2)
    MAX_DISTANCE_TO_BALL = math.sqrt((790-20)**2 + (390-20)**2)

    BUFFER_SIZE = int(1e5)  # replay buffer size
    BATCH_SIZE = 64  # minibatch size
    GAMMA = 0.99  # discount factor
    TAU = 1e-3  # for soft update of target parameters
    LR = 5e-4  # learning rate
    UPDATE_EVERY = 4  # how often to update the network
    # device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    DEVICE = torch.device("cpu")

    STATE_SIZE = 10
    ACTION_SIZE = 9

    #Reward
    MARL = 1
    SARL = 0
    ON = 1
    ARKA = 0
    ALT = -1
    UST = 1
    ORTA = -5

    START_POSITION = ((int(SIZE_WIDTH/4), int(SIZE_HEIGHT/4), int(SIZE_WIDTH/4), int(3*SIZE_HEIGHT/4), int(3*SIZE_WIDTH/4), int(SIZE_HEIGHT/4), int(3*SIZE_WIDTH/4), int(3*SIZE_HEIGHT/4), int(SIZE_WIDTH/4), int(SIZE_HEIGHT/2)),
                      (100, 100, 200, 200, 150, 200, 180, 320, 300, 110),
                      (500, 100, 300, 300, 250, 100, 600, 170, 300, 210),
                      (320, 50, 100, 300, 350, 300, 280, 170, 360, 70),
                      (600, 100, 500, 200, 90, 70, 50, 310, 400, 190),
                      (200, 100, 90, 100, 220, 60, 180, 330, 200, 140),
                      (100, 300, 200, 70, 320, 130, 500, 190, 120, 50),
                      (440, 270, 200, 300, 110, 230, 420, 80, 330, 330))

