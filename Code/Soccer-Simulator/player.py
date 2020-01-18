import pygame
import math

from constants import Constants
import numpy as np
import random
from brain import QNetwork
from replayBuffer import ReplayBuffer
import torch
import torch.nn.functional as F
import torch.optim as optim

class Player():
    def __init__(self, x, y, size, state_size, action_size, seed, mass=1, artificial=False):
        self.x = x
        self.y = y
        self.size = size
        self.colour = (0, 0, 255)
        self.thickness = 0
        self.speed = 0
        self.angle = 0
        self.mass = mass
        self.drag = (self.mass / (self.mass + Constants.MASS_OF_AIR)) ** self.size
        ####################################
        self.state_size = state_size
        self.action_size = action_size
        if not artificial:
            # Q-Network
            self.qnetwork_local = QNetwork(state_size, action_size).to(Constants.DEVICE)
            self.qnetwork_target = QNetwork(state_size, action_size).to(Constants.DEVICE)
            self.optimizer = optim.Adam(self.qnetwork_local.parameters(), lr=Constants.LR)

            # Replay memory
            self.memory = ReplayBuffer(action_size, Constants.BUFFER_SIZE, Constants.BATCH_SIZE)

            # Initialize time step (for updating every UPDATE_EVERY steps)
            self.t_step = 0
            #######################################

    def display(self, screen):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= self.drag

    def bounce(self,soccerfield):
        if self.x > Constants.SIZE_WIDTH - self.size:
            self.x = 2 * (Constants.SIZE_WIDTH - self.size) - self.x
            self.angle = - self.angle
            self.speed *= Constants.ELASTICITY
        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = - self.angle
            self.speed *= Constants.ELASTICITY

        if self.y > Constants.SIZE_HEIGHT - self.size:
            self.y = 2 * (Constants.SIZE_HEIGHT - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= Constants.ELASTICITY
        elif self.y < self.size:
            self.y = 2 * self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= Constants.ELASTICITY

        if self.x > int((19*Constants.SIZE_WIDTH)/20):
            if int(self.y + self.size) == int(Constants.SIZE_HEIGHT/3):
                self.y = 2 * (Constants.SIZE_HEIGHT/3 - self.size) - self.y - 1
                self.angle = math.pi - self.angle
                self.speed *= Constants.ELASTICITY
            elif int(self.y + self.size) == int(2*Constants.SIZE_HEIGHT/3):
                self.y = 2 * self.size - self.y + 1
                self.angle = math.pi - self.angle
                self.speed *= Constants.ELASTICITY
        elif self.x < int(Constants.SIZE_WIDTH/20):
            if int(self.y + self.size) == int(Constants.SIZE_HEIGHT/3):
                self.y = 2 * (Constants.SIZE_HEIGHT/3 - self.size) - self.y - 1
                self.angle = math.pi - self.angle
                self.speed *= Constants.ELASTICITY
            elif int(self.y + self.size) == int(2*Constants.SIZE_HEIGHT/3):
                self.y = 2 * self.size - self.y + 1
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



    '''
    0 -> shoot
    1 -> up + left
    2 -> up + right
    3 -> down + left
    4 -> down + right
    5 -> up 
    6 -> down
    7 -> left
    8 -> right
    '''
    def update(self, action, ball, teammate):
        '''
        if action == 0 and self.control_ball(ball):
            dx = -(self.x - ball.x) / 6
            dy = -(self.y - ball.y) / 6
            ball.angle = 0.5 * math.pi + math.atan2(dy, dx)
            ball.speed = math.hypot(dx, dy)

        '''
        if action == 0 and self.shoot_control(ball): #sut atma
            dx = -(self.x - 19*Constants.SIZE_WIDTH/20 ) / 6
            dy = -(self.y - Constants.SIZE_HEIGHT/2) / 6
            speed_dx = -(self.x - ball.x) / 6
            speed_dy = -(self.y - ball.y) / 6
            ball.angle = 0.5 * math.pi + math.atan2(dy, dx)
            ball.speed = math.hypot(speed_dx, speed_dy)
        if action == 1:
            dx = -Constants.UPDATE_DOUBLE_DXY
            dy = -Constants.UPDATE_DOUBLE_DXY
            self.angle = 0.5 * math.pi + math.atan2(dy, dx)
            self.speed = math.hypot(dx, dy)
        if action == 2:
            dx = Constants.UPDATE_DOUBLE_DXY
            dy = -Constants.UPDATE_DOUBLE_DXY
            self.angle = 0.5 * math.pi + math.atan2(dy, dx)
            self.speed = math.hypot(dx, dy)
        if action == 3:
            dx = -Constants.UPDATE_DOUBLE_DXY
            dy = Constants.UPDATE_DOUBLE_DXY
            self.angle = 0.5 * math.pi + math.atan2(dy, dx)
            self.speed = math.hypot(dx, dy)
        if action == 4:
            dx = Constants.UPDATE_DOUBLE_DXY
            dy = Constants.UPDATE_DOUBLE_DXY
            self.angle = 0.5 * math.pi + math.atan2(dy, dx)
            self.speed = math.hypot(dx, dy)
        if action == 5:
            dx = 0
            dy = -Constants.UPDATE_SINGLE_DXY
            self.angle = 0.5 * math.pi + math.atan2(dy, dx)
            self.speed = math.hypot(dx, dy)
        if action == 6:
            dx = 0
            dy = Constants.UPDATE_SINGLE_DXY
            self.angle = 0.5 * math.pi + math.atan2(dy, dx)
            self.speed = math.hypot(dx, dy)
        if action == 7:
            dx = -Constants.UPDATE_SINGLE_DXY
            dy = 0
            self.angle = 0.5 * math.pi + math.atan2(dy, dx)
            self.speed = math.hypot(dx, dy)
        if action == 8:
            dx = Constants.UPDATE_SINGLE_DXY
            dy = 0
            self.angle = 0.5 * math.pi + math.atan2(dy, dx)
            self.speed = math.hypot(dx, dy)
        if action == 9 and self.pass_control(ball, teammate): #pas atma
            dx = -(self.x - teammate.x) / 6
            dy = -(self.y - teammate.y) / 6
            speed_dx = -(self.x - ball.x) / 6
            speed_dy = -(self.y - ball.y) / 6
            ball.angle = 0.5 * math.pi + math.atan2(dy, dx)
            ball.speed = math.hypot(speed_dx, speed_dy)




    def control_ball(self, ball):
        dx = self.x - ball.x
        dy = self.y - ball.y
        dist = math.hypot(dx, dy)
        if dist - 3 < self.size + ball.size:
            return True
        return False

    def pass_control(self,ball,teammate):
        if self.control_ball(ball):
            if (self.x < ball.x and ball.x < teammate.x) or (self.x > ball.x and ball.x > teammate.x):
                if (self.y < ball.y and ball.y < teammate.y) or (self.y > ball.y and ball.y > teammate.y):
                    return True
        return False

    def shoot_control(self,ball):
        if self.control_ball(ball):
            if (self.x < ball.x):
                if((self.y < ball.y and ball.y < Constants.SIZE_HEIGHT/2) or (self.y > ball.y and ball.y > Constants.SIZE_HEIGHT/2)):
                    return True
        return False

    def addVectors(self, angle1, length1, angle2, length2):
        x = math.sin(angle1) * length1 + math.sin(angle2) * length2
        y = math.cos(angle1) * length1 + math.cos(angle2) * length2

        angle = 0.5 * math.pi - math.atan2(y, x)
        length = math.hypot(x, y)

        return (angle, length)

    ###################
    def step(self, state, action, reward, next_state, done):
        # Save experience in replay memory
        self.memory.add(state, action, reward, next_state, done)

        # Learn every UPDATE_EVERY time steps.
        self.t_step = (self.t_step + 1) % Constants.UPDATE_EVERY
        if self.t_step == 0:
            # If enough samples are available in memory, get random subset and learn
            if len(self.memory) > Constants.BATCH_SIZE:
                experiences = self.memory.sample()
                self.learn(experiences, Constants.GAMMA)

    def act(self, state, eps):
        # Returns actions for given state as per current policy.

        state = torch.from_numpy(state).float().unsqueeze(0).to(Constants.DEVICE)
        self.qnetwork_local.eval()
        with torch.no_grad():
            action_values = self.qnetwork_local(state)
        self.qnetwork_local.train()

        arr = action_values.cpu().data.numpy()
        #print("Arr",arr)
        #print("Arr sort",np.argmax(action_values.cpu().data.numpy()))
        arr = arr.argsort()[-3:][::-1]
        #print("İbn",arr)

        if random.random() > eps:
            return arr
        else:
            return np.asarray([random.sample(list(arr[0]), len(list(arr[0])))])



    def learn(self, experiences, gamma):

        states, actions, rewards, next_states, dones = experiences

        # Get max predicted Q values (for next states) from target model
        Q_targets_next = self.qnetwork_target(next_states).detach().max(1)[0].unsqueeze(1)
        # Compute Q targets for current states
        Q_targets = rewards + (gamma * Q_targets_next * (1 - dones))

        # Get expected Q values from local model
        Q_expected = self.qnetwork_local(states).gather(1, actions)

        # Compute loss
        loss = F.mse_loss(Q_expected, Q_targets)
        # Minimize the loss
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # ------------------- update target network ------------------- #

        self.soft_update(self.qnetwork_local, self.qnetwork_target, Constants.TAU)

    def soft_update(self, local_model, target_model, tau):
        """Soft update model parameters.
        θ_target = τ*θ_local + (1 - τ)*θ_target
        Params
        ======
            local_model (PyTorch model): weights will be copied from
            target_model (PyTorch model): weights will be copied to
            tau (float): interpolation parameter
        """
        for target_param, local_param in zip(target_model.parameters(), local_model.parameters()):
            target_param.data.copy_(tau * local_param.data + (1.0 - tau) * target_param.data)

    '''
        def update(self, pressed_keys, ball):
            doubleflag = False
            if pressed_keys[self.shoot] and self.control_ball(ball):
                dx = -(self.x - ball.x) / 6
                dy = -(self.y - ball.y) / 6
                ball.angle = 0.5 * math.pi + math.atan2(dy, dx)
                ball.speed = math.hypot(dx, dy)
            if pressed_keys[self.up] and pressed_keys[self.left]:
                dx = -Constants.UPDATE_DOUBLE_DXY
                dy = -Constants.UPDATE_DOUBLE_DXY
                self.angle = 0.5 * math.pi + math.atan2(dy, dx)
                self.speed = math.hypot(dx, dy)
                doubleflag = True

            if pressed_keys[self.up] and pressed_keys[self.right]:
                dx = Constants.UPDATE_DOUBLE_DXY
                dy = -Constants.UPDATE_DOUBLE_DXY
                self.angle = 0.5 * math.pi + math.atan2(dy, dx)
                self.speed = math.hypot(dx, dy)
                doubleflag = True

            if pressed_keys[self.down] and pressed_keys[self.left]:
                dx = -Constants.UPDATE_DOUBLE_DXY
                dy = Constants.UPDATE_DOUBLE_DXY
                self.angle = 0.5 * math.pi + math.atan2(dy, dx)
                self.speed = math.hypot(dx, dy)
                doubleflag = True

            if pressed_keys[self.down] and pressed_keys[self.right]:
                dx = Constants.UPDATE_DOUBLE_DXY
                dy = Constants.UPDATE_DOUBLE_DXY
                self.angle = 0.5 * math.pi + math.atan2(dy, dx)
                self.speed = math.hypot(dx, dy)
                doubleflag = True

            if not doubleflag:
                if pressed_keys[self.up]:
                    dx = 0
                    dy = -Constants.UPDATE_SINGLE_DXY
                    self.angle = 0.5 * math.pi + math.atan2(dy, dx)
                    self.speed = math.hypot(dx, dy)
                if pressed_keys[self.down]:
                    dx = 0
                    dy = Constants.UPDATE_SINGLE_DXY
                    self.angle = 0.5 * math.pi + math.atan2(dy, dx)
                    self.speed = math.hypot(dx, dy)
                if pressed_keys[self.left]:
                    dx = -Constants.UPDATE_SINGLE_DXY
                    dy = 0
                    self.angle = 0.5 * math.pi + math.atan2(dy, dx)
                    self.speed = math.hypot(dx, dy)
                if pressed_keys[self.right]:
                    dx = Constants.UPDATE_SINGLE_DXY
                    dy = 0
                    self.angle = 0.5 * math.pi + math.atan2(dy, dx)
                    self.speed = math.hypot(dx, dy)
        '''