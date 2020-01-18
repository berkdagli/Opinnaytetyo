from player import Player
from enemy import Enemy
from ball import Ball
from constants import Constants
from soccerfield import SoccerField
import numpy as np
import math

class Enemy_coach():
    def __init__(self, player1, player2, enemy1, enemy2, ball):
        self.player1111 = player1
        self.player2222 = player2
        self.enemy1111 = enemy1
        self.enemy2222 = enemy2
        self.ball3333 = ball
        self.soccerfield = SoccerField()

    def create_animation_players(self):
        size = 20
        density = 3
        player1_animation = Player(self.player1111.x, self.player1111.y, size, Constants.STATE_SIZE, Constants.ACTION_SIZE+1, 0, density * size ** 2, artificial=True)
        player2_animation = Player(self.player2222.x, self.player2222.y, size, Constants.STATE_SIZE, Constants.ACTION_SIZE+1, 0, density * size ** 2, artificial=True)
        enemy1_animation = Player(self.enemy1111.x, self.enemy1111.y, size, Constants.STATE_SIZE, Constants.ACTION_SIZE+1, 0, density * size ** 2, artificial=True)
        enemy2_animation = Player(self.enemy2222.x, self.enemy2222.y, size, Constants.STATE_SIZE, Constants.ACTION_SIZE+1, 0, density * size ** 2, artificial=True)

        ball_size = 10
        ball_density = 7
        ball_animation = Ball(self.ball3333.x, self.ball3333.y, ball_size, ball_density * ball_size ** 2)

        return player1_animation, player2_animation, enemy1_animation, enemy2_animation, ball_animation

    def init_position_angle_speed(self, player1,player2,enemy1,enemy2,ball):
        player1.x = self.player1111.x
        player1.y = self.player1111.y
        player1.angle = self.player1111.angle
        player1.speed = self.player1111.speed

        player2.x = self.player2222.x
        player2.y = self.player2222.y
        player2.angle = self.player2222.angle
        player2.speed = self.player2222.speed

        enemy1.x = self.enemy1111.x
        enemy1.y = self.enemy1111.y
        enemy1.angle = self.enemy1111.angle
        enemy1.speed = self.enemy1111.speed

        enemy2.x = self.enemy2222.x
        enemy2.y = self.enemy2222.y
        enemy2.angle = self.enemy2222.angle
        enemy2.speed = self.enemy2222.speed

        ball.x = self.ball3333.x
        ball.y = self.ball3333.y
        ball.angle = self.ball3333.angle
        ball.speed = self.ball3333.speed


    def __addVectors(self, angle1, length1, angle2, length2):
        x = math.sin(angle1) * length1 + math.sin(angle2) * length2
        y = math.cos(angle1) * length1 + math.cos(angle2) * length2

        angle = 0.5 * math.pi - math.atan2(y, x)
        length = math.hypot(x, y)

        return (angle, length)

    def __collide(self, p1, p2):

        dx = p1.x - p2.x
        dy = p1.y - p2.y

        dist = math.hypot(dx, dy)
        if dist < p1.size + p2.size:
            angle = math.atan2(dy, dx) + 0.5 * math.pi
            total_mass = p1.mass + p2.mass

            (p1.angle, p1.speed) = self.__addVectors(p1.angle, p1.speed * (p1.mass - p2.mass) / total_mass, angle, 2 * p2.speed * p2.mass / total_mass)
            (p2.angle, p2.speed) = self.__addVectors(p2.angle, p2.speed * (p2.mass - p1.mass) / total_mass, angle + math.pi, 2 * p1.speed * p1.mass / total_mass)
            p1.speed *= Constants.ELASTICITY
            p2.speed *= Constants.ELASTICITY

            overlap = 0.5 * (p1.size + p2.size - dist + 1)
            p1.x += math.sin(angle) * overlap
            p1.y -= math.cos(angle) * overlap
            p2.x -= math.sin(angle) * overlap
            p2.y += math.cos(angle) * overlap

    def normalized_distance_to_line(self, control,  x, y_up, y_down, ball): #Control true ise doğru orantı false ise ters orantı
        if ball.y <= y_up:
            dist = math.sqrt((ball.x - x)**2 + (ball.y - y_up)**2)
        elif ball.y >= y_down:
            dist = math.sqrt((ball.x - x) ** 2 + (ball.y - y_down) ** 2)
        else:
            dist = abs(ball.x - x)
        if control:
            return  dist / Constants.MAX_DISTANCE_TO_GOAL_LINE
        else:
            return (Constants.MAX_DISTANCE_TO_GOAL_LINE - dist) / Constants.MAX_DISTANCE_TO_GOAL_LINE

    def normalized_ball_player_distance(self, control, player, ball,): #Control True ise doğru orantı false ise ters orantı
        dist = math.sqrt((player.x - ball.x)**2 + (player.y - ball.y)**2)
        if control:
            return   dist / Constants.MAX_DISTANCE_TO_BALL
        else:
            return (Constants.MAX_DISTANCE_TO_BALL - dist) / Constants.MAX_DISTANCE_TO_BALL

    def control_ball(self,player, ball):
        dx = player.x - ball.x
        dy = player.y - ball.y
        dist = math.hypot(dx, dy)
        if dist - 3 < player.size + ball.size:
            return True
        return False

    def get_rewards(self,player1,player2,enemy1,enemy2,ball, controll=False):

        rightLine_x, rightLine_y_up, rightLine_y_down = self.soccerfield.goalposts[2].x, self.soccerfield.goalposts[2].y, self.soccerfield.goalposts[3].y
        leftLine_x, leftLine_y_up, leftLine_y_down = self.soccerfield.goalposts[0].x, self.soccerfield.goalposts[0].y, self.soccerfield.goalposts[1].y

        p1_reward = self.normalized_distance_to_line(False, leftLine_x, leftLine_y_up, leftLine_y_down, ball) + 0.2 * self.normalized_ball_player_distance(False,player1, ball)
        p2_reward = self.normalized_distance_to_line(False, leftLine_x, leftLine_y_up, leftLine_y_down, ball) + 0.2 * self.normalized_ball_player_distance(False,player2, ball)
        return [p1_reward, p2_reward, 0, 0]


    def closest_first_second_player_team(self,player1,player2,enemy1,enemy2,ball):

        p1_dist = self.normalized_ball_player_distance(True, player1, ball)
        p2_dist = self.normalized_ball_player_distance(True, player2, ball)
        e1_dist = self.normalized_ball_player_distance(True, enemy1, ball)
        e2_dist = self.normalized_ball_player_distance(True, enemy2, ball)

        closest_first_player_team = -1
        closest_second_player_team = -1
        min_dist = 1000
        closest_MARL_player = None
        closest_SARL_player = None
        closest_MARL_player_distance = 10000000
        closest_SARL_player_distance = 10000000
        attack_MARL = False
        attack_SARL = False
        if p1_dist < min_dist:
            closest_MARL_player = player1
            min_dist = p1_dist
            closest_MARL_player_distance = p1_dist

        if p2_dist < min_dist:
            closest_MARL_player = player2
            min_dist = p2_dist
            closest_MARL_player_distance = p2_dist
        min_dist = 1000
        if e1_dist < min_dist:
            closest_SARL_player = enemy1
            min_dist = e1_dist
            closest_SARL_player_distance = e1_dist

        if e2_dist < min_dist:
            closest_SARL_player = enemy2
            min_dist = e2_dist
            closest_SARL_player_distance = e2_dist

        if closest_MARL_player_distance <= closest_SARL_player_distance:
            closest_first_player_team = Constants.MARL
            if closest_MARL_player is player1:
                if p2_dist <= closest_SARL_player_distance:
                    closest_second_player_team = Constants.MARL
                else:
                    closest_second_player_team = Constants.SARL
            else:
                if p1_dist <= closest_SARL_player_distance:
                    closest_second_player_team = Constants.MARL
                else:
                    closest_second_player_team = Constants.SARL
        else:
            closest_first_player_team = Constants.SARL
            if closest_SARL_player is enemy1:
                if e2_dist <= closest_MARL_player_distance:
                    closest_second_player_team = Constants.SARL
                else:
                    closest_second_player_team = Constants.MARL
            else:
                if e1_dist <= closest_MARL_player_distance:
                    closest_second_player_team = Constants.SARL
                else:
                    closest_second_player_team = Constants.MARL

        return closest_first_player_team, closest_second_player_team, closest_MARL_player, closest_SARL_player


    def step(self,player1, player2, enemy1, enemy2, ball, actions):

        old_rewards = self.get_rewards(player1,player2,enemy1,enemy2,ball)

        for _ in range(3):

            player1.update(actions[0], ball, player2)
            player2.update(actions[1], ball, player1)
            enemy1.update(actions[2], ball, enemy2)
            enemy2.update(actions[3], ball, enemy1)


            player1.move()
            player2.move()
            enemy1.move()
            enemy2.move()
            ball.move()

            player1.bounce(self.soccerfield)
            player2.bounce(self.soccerfield)
            enemy1.bounce(self.soccerfield)
            enemy2.bounce(self.soccerfield)
            ball.bounce(self.soccerfield)

            self.__collide(player1, player2)
            self.__collide(player1, enemy1)
            self.__collide(player1, enemy2)
            self.__collide(player1, ball)
            self.__collide(player2, enemy1)
            self.__collide(player2, enemy2)
            self.__collide(player2, ball)
            self.__collide(enemy1, enemy2)
            self.__collide(enemy1, ball)
            self.__collide(enemy2, ball)

        rewards = self.get_rewards(player1,player2,enemy1,enemy2,ball)

        result = [ rewards[0] - old_rewards[0], rewards[1] - old_rewards[1], rewards[2] - old_rewards[2], rewards[3] - old_rewards[3] ]

        return result


    def information(self,player1, player2, enemy1,enemy2,ball ):
        self.player1111 = player1
        self.player2222 = player2
        self.enemy1111 = enemy1
        self.enemy2222 = enemy2
        self.ball3333 = ball
    def determine_actions(self, player1_actions, player2_actions, state, test=False):


        '''
        player1_position_x, player1_position_y = state[0], state[1]
        player2_position_x, player2_position_y = state[2], state[3]
        enemy1_position_x, enemy1_position_y = state[4], state[5]
        enemy2_position_x, enemy2_position_y = state[6], state[7]
        ball_position_x, ball_position_y = state[8], state[9]
        '''

        if not test:
            player1_actions = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
            player2_actions = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])  # player2_actions[0]
        else:
            player1_actions = player1_actions[0][-5:] #[:3]
            player2_actions = player2_actions[0][-5:] #[:3]

        enemy1_actions = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        enemy2_actions = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

        player1_animation, player2_animation, enemy1_animation, enemy2_animation, ball_animation = self.create_animation_players()

        max_enemy1 = -100000
        act_enemy1 = -1
        for en1 in enemy1_actions:
            actions = [-1,-1, en1, -1]
            self.init_position_angle_speed(player1_animation, player2_animation, enemy1_animation, enemy2_animation, ball_animation)
            rewards = self.step(player1_animation, player2_animation, enemy1_animation, enemy2_animation, ball_animation, actions)
            if rewards[2] >= max_enemy1:
                max_enemy1 = rewards[2]
                act_enemy1 = en1

        max_enemy2 = -100000
        act_enemy2 = -1
        for en2 in enemy2_actions:
            actions = [-1, -1, -1, en2]
            self.init_position_angle_speed(player1_animation, player2_animation, enemy1_animation, enemy2_animation, ball_animation)
            rewards = self.step(player1_animation, player2_animation, enemy1_animation, enemy2_animation, ball_animation, actions)
            if rewards[3] >= max_enemy2:
                max_enemy2 = rewards[3]
                act_enemy2 = en2

        max_marl = -100000
        act_player1 = -1
        act_player2 = -1
        for pl1 in player1_actions:
            for pl2 in player2_actions:
                actions = [pl1, pl2, act_enemy1, act_enemy2]
                self.init_position_angle_speed(player1_animation, player2_animation, enemy1_animation, enemy2_animation, ball_animation)
                rewards = self.step(player1_animation, player2_animation, enemy1_animation, enemy2_animation, ball_animation, actions)
                if (rewards[0] + rewards[1]) >= max_marl:
                    max_marl = rewards[0] + rewards[1]
                    act_player1 = pl1
                    act_player2 = pl2


        return act_player1, act_player2
