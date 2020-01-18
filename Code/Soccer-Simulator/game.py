import pygame
import math
from constants import Constants
from player import Player
from ball import Ball
from soccerfield import SoccerField
from coach import Coach
from enemy_coach import Enemy_coach
import numpy as np
import random



class Game():
    def __init__(self,randomness, test=False):
        self.marlScore = 0
        self.sarlScore = 0
        self.randomness = randomness
        self.n = -1
        self.__create_player_ball()
        self.coach = Coach(self.player1, self.player2, self.enemy1, self.enemy2, self.ball)
        self.enemy_coach = Enemy_coach(self.enemy1, self.enemy2, self.player1, self.player2, self.ball)
        self.soccerfield = SoccerField()
        self.test = test


    def activate_screen(self):
        self.screen = pygame.display.set_mode((Constants.SIZE_WIDTH, Constants.SIZE_HEIGHT))
        pygame.display.set_caption('Soccer Simulator')
        pygame.font.init()
        self.font = pygame.font.Font(None, 24)


    def __check_goal(self, ball):
        global marlScore,sarlScore
        if (ball.y > Constants.SIZE_HEIGHT/3) and (ball.y < 2*Constants.SIZE_HEIGHT/3):
            if ball.x + ball.size < int(Constants.SIZE_WIDTH/20):
                self.sarlScore += 1
                return True, Constants.TEAM_SARL
            elif ball.x - ball.size > int(19*Constants.SIZE_WIDTH/20):
                self.marlScore += 1
                return True, Constants.TEAM_MARL
        return False, Constants.TEAM_NONE


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

    def __create_player_ball(self):

        #Create Player1
        size = 20  # random.randint(10, 20)

        density = 3  # random.randint(1, 10)

        if self.randomness:
            
           	x = random.randint(int(Constants.SIZE_WIDTH/20) + size, int(19*Constants.SIZE_WIDTH/20)-size) 
           	y = random.randint(int(Constants.SIZE_HEIGHT/10) + size, int(9*Constants.SIZE_HEIGHT/10)-size) 
           
        else:
            x = int(Constants.SIZE_WIDTH/ 4)
            y = int(Constants.SIZE_HEIGHT/ 4)

        # x, y, size, up, down, left, right, shoot, mass=1
        self.player1 = Player(x, y, size, Constants.STATE_SIZE, Constants.ACTION_SIZE+1, 0, density * size ** 2)
        self.player1.colour = Constants.TEAM_MARL_COLOUR
        self.player1.speed = 0
        self.player1.angle = 0

        # Create Player2
        size = 20  # random.randint(10, 20)
        density = 3  # random.randint(1, 10)

        if self.randomness:
            x = random.randint(int(Constants.SIZE_WIDTH/20) + size, int(19*Constants.SIZE_WIDTH/20)-size) 
            y = random.randint(int(Constants.SIZE_HEIGHT/10) + size, int(9*Constants.SIZE_HEIGHT/10)-size) 
        else:
            x = int(Constants.SIZE_WIDTH / 4)
            y = int(3*Constants.SIZE_HEIGHT / 4)

        # x, y, size, up, down, left, right, shoot, mass=1
        self.player2 = Player(x, y, size, Constants.STATE_SIZE, Constants.ACTION_SIZE+1, 0, density * size ** 2)
        self.player2.colour = Constants.TEAM_MARL_COLOUR
        self.player2.speed = 0
        self.player2.angle = 0

        # Create Enemy1
        size = 20  # random.randint(10, 20)
        density = 3  # random.randint(1, 10)

        if self.randomness:
            x = random.randint(int(Constants.SIZE_WIDTH/20) + size, int(19*Constants.SIZE_WIDTH/20)-size)
            y = random.randint(int(Constants.SIZE_HEIGHT/10) + size, int(9*Constants.SIZE_HEIGHT/10)-size)
        else:
            x = int(3*Constants.SIZE_WIDTH / 4)
            y = int(Constants.SIZE_HEIGHT / 4)

        # x, y, size, up, down, left, right, shoot, mass=1
        self.enemy1 = Player(x, y, size, Constants.STATE_SIZE, Constants.ACTION_SIZE+1, 0, density * size ** 2)
        self.enemy1.colour = Constants.TEAM_SARL_COLOUR
        self.enemy1.speed = 0
        self.enemy1.angle = 0

        # Create Enemy2
        size = 20  # random.randint(10, 20)
        density = 3  # random.randint(1, 10)

        if self.randomness:
            x = random.randint(int(Constants.SIZE_WIDTH/20) + size, int(19*Constants.SIZE_WIDTH/20)-size) 
            y = random.randint(int(Constants.SIZE_HEIGHT/10) + size, int(9*Constants.SIZE_HEIGHT/10)-size) 
        else:
            x = int(3*Constants.SIZE_WIDTH / 4)
            y = int(3 * Constants.SIZE_HEIGHT / 4)

        # x, y, size, up, down, left, right, shoot, mass=1
        self.enemy2 = Player(x, y, size, Constants.STATE_SIZE, Constants.ACTION_SIZE+1, 0, density * size ** 2)
        self.enemy2.colour = Constants.TEAM_SARL_COLOUR
        self.enemy2.speed = 0
        self.enemy2.angle = 0

        #Create Ball
        size = 10  # random.randint(10, 20)
        density = 7  # random.randint(1, 10)

        if self.randomness:
            x = random.randint(int(Constants.SIZE_WIDTH/20) + size, int(19*Constants.SIZE_WIDTH/20)-size) 
            y = random.randint(int(Constants.SIZE_HEIGHT/10) + size, int(9*Constants.SIZE_HEIGHT/10)-size) 
        else:
            x = Constants.SIZE_WIDTH / 2
            y = Constants.SIZE_HEIGHT / 2

        self.ball = Ball(x, y, size, density * size ** 2)
        self.ball.colour = Constants.BALL_COLOUR
        self.ball.speed = 0
        self.ball.angle = 0

        self.n = self.n + 1

    def __get_state(self):
        return np.array( [round(self.player1.x/Constants.SIZE_WIDTH,3), round(self.player1.y/Constants.SIZE_HEIGHT,3), round(self.player2.x/Constants.SIZE_WIDTH,3), round(self.player2.y/Constants.SIZE_HEIGHT,3),
                          round(self.enemy1.x/Constants.SIZE_WIDTH,3), round(self.enemy1.y/Constants.SIZE_HEIGHT,3), round(self.enemy2.x/Constants.SIZE_WIDTH,3), round(self.enemy2.y/Constants.SIZE_HEIGHT,3),

                          round(self.ball.x/Constants.SIZE_WIDTH,3), round(self.ball.y/Constants.SIZE_HEIGHT,3)])

    def __get_state2(self):
        return np.array( [int(self.player1.x), int(self.player1.y), int(self.player2.x), int(self.player2.y),
               int(self.enemy1.x), int(self.enemy1.y), int(self.enemy2.x), int(self.enemy2.y),
               int(self.ball.x), int(self.ball.y)])

    def reset(self):
        self.__create_player_ball()
        return self.__get_state()

    def act(self,state, eps=0):
        player1_actions = self.player1.act(state, eps)
        player2_actions = self.player2.act(state, eps)
        enemy1_actions = self.enemy1.act(state, eps)
        enemy2_actions = self.enemy2.act(state, eps)
        self.coach.information(self.player1, self.player2, self.enemy1, self.enemy2, self.ball)
        self.enemy_coach.information(self.enemy1, self.enemy2, self.player1, self.player2, self.ball)
        p1_action, p2_action = self.coach.determine_actions(player1_actions, player2_actions, state,self.test)
        enemy1_action, enemy2_action = self.enemy_coach.determine_actions(enemy1_actions, enemy2_actions, state,self.test)
        return [p1_action, p2_action, enemy1_action, enemy2_action]

    def __get_rewards(self):
        rightLine_x, rightLine_y_up, rightLine_y_down = self.soccerfield.goalposts[2].x, self.soccerfield.goalposts[
            2].y, self.soccerfield.goalposts[3].y
        leftLine_x, leftLine_y_up, leftLine_y_down = self.soccerfield.goalposts[0].x, self.soccerfield.goalposts[
            0].y, self.soccerfield.goalposts[1].y
        
        e1_reward = self.normalized_distance_to_line(leftLine_x,leftLine_y_up, leftLine_y_down, self.ball) + 0.2* self.normalized_ball_player_distance(self.enemy1, self.ball)
        e2_reward = self.normalized_distance_to_line(leftLine_x,leftLine_y_up, leftLine_y_down, self.ball) + 0.2* self.normalized_ball_player_distance(self.enemy2, self.ball)
        coach_rewards = self.coach.get_rewards(self.player1, self.player2, self.enemy1, self.enemy2, self.ball, controll=True)
        enemy_coach_rewards = self.enemy_coach.get_rewards(self.enemy1, self.enemy2,self.player1, self.player2, self.ball, controll=True)
        return [coach_rewards[0], coach_rewards[1], enemy_coach_rewards[0], enemy_coach_rewards[1]]

    def step(self,state, actions, actions_trace_MARL, actions_trace_SARL):
        old_rewards = self.__get_rewards()
        self.player1.update(actions[0], self.ball, self.player2)
        self.player2.update(actions[1], self.ball, self.player1)
        self.enemy1.update(actions[2], self.ball, self.enemy2)
        self.enemy2.update(actions[3], self.ball, self.enemy1)
        self.player1.move()
        self.player2.move()
        self.enemy1.move()
        self.enemy2.move()
        self.ball.move()
        self.player1.bounce(self.soccerfield)
        self.player2.bounce(self.soccerfield)
        self.enemy1.bounce(self.soccerfield)
        self.enemy2.bounce(self.soccerfield)
        self.ball.bounce(self.soccerfield)
        self.__collide(self.player1, self.player2)
        self.__collide(self.player1, self.enemy1)
        self.__collide(self.player1, self.enemy2)
        self.__collide(self.player1, self.ball)
        self.__collide(self.player2, self.enemy1)
        self.__collide(self.player2, self.enemy2)
        self.__collide(self.player2, self.ball)
        self.__collide(self.enemy1, self.enemy2)
        self.__collide(self.enemy1, self.ball)
        self.__collide(self.enemy2, self.ball)
        next_state = self.__get_state()

        rewards = self.__get_rewards()
        marl_reward = rewards[0] - old_rewards[0] + rewards[1] - old_rewards[1]
        sarl_reward = rewards[2] - old_rewards[2] + rewards[3] - old_rewards[3]
        done = False
        goal_control, who_score = self.__check_goal(self.ball)
        if goal_control:
            done = True
            if who_score == Constants.TEAM_MARL:
                scorer = 0
                actions_trace_MARL.reverse()
                for i in actions_trace_MARL: # gole reward
                    if i["actions"][0] == 0: #Son şutu player1 atmışsa o atmıştır golü diye farzettim
                        self.player1.step(i["state"], 0, 10000, i["next_state"], False)
                        scorer = 1
                        break
                    if i["actions"][1] == 0: #Son şutu player2 atmışsa o atmıştır golü diye farzettim
                        self.player2.step(i["state"], 0, 10000, i["next_state"], False)
                        scorer = 2
                        break

                for i in actions_trace_MARL: # asiste reward
                    if scorer != 1 and i["actions"][0] == 9: #Son pası player1 atmışsa o yapmıştır asisti
                        self.player1.step(i["state"], 9, 5000, i["next_state"], False)
                        break
                    if scorer != 2 and i["actions"][1] == 9: #Son pası player2 atmışsa o yapmıştır asisti
                        self.player2.step(i["state"], 9, 5000, i["next_state"], False)
                        break

            else:
                scorer = 0
                actions_trace_SARL.reverse()
                for i in actions_trace_SARL:  # gole reward
                    if i["actions"][0] == 0:  # Son şutu enemy1 atmışsa o atmıştır golü diye farzettim
                        self.enemy1.step(i["state"], 0, 10000, i["next_state"], False)
                        scorer = 1
                        break
                    if i["actions"][1] == 0:  # Son şutu enemy2 atmışsa o atmıştır golü diye farzettim
                        self.enemy2.step(i["state"], 0, 10000, i["next_state"], False)
                        scorer = 2
                        break

                for i in actions_trace_SARL:  # asiste reward
                    if scorer != 1 and i["actions"][0] == 9:  # Son pası enemy1 atmışsa o yapmıştır asisti
                        self.enemy1.step(i["state"], 9, 5000, i["next_state"], False)
                        break
                    if scorer != 2 and i["actions"][1] == 9:  # Son pası enemy2 atmışsa o yapmıştır asisti
                        self.enemy2.step(i["state"], 9, 5000, i["next_state"], False)
                        break

        # Experience Replay
        self.player1.step(state, actions[0], marl_reward + rewards[0] - old_rewards[0], next_state, done)
        self.player2.step(state, actions[1], marl_reward + rewards[1] - old_rewards[1], next_state, done)
        self.enemy1.step(state, actions[2], sarl_reward + rewards[2] - old_rewards[2], next_state, done)
        self.enemy2.step(state, actions[3], sarl_reward + rewards[3] - old_rewards[3], next_state, done)

        return next_state, marl_reward, sarl_reward, done, who_score


    def step_test(self,state, actions):
        old_rewards = self.__get_rewards()
        self.player1.update(actions[0], self.ball, self.player2)
        self.player2.update(actions[1], self.ball, self.player1)
        self.enemy1.update(actions[2], self.ball, self.enemy2)
        self.enemy2.update(actions[3], self.ball, self.enemy1)
        self.player1.move()
        self.player2.move()
        self.enemy1.move()
        self.enemy2.move()
        self.ball.move()
        self.player1.bounce(self.soccerfield)
        self.player2.bounce(self.soccerfield)
        self.enemy1.bounce(self.soccerfield)
        self.enemy2.bounce(self.soccerfield)
        self.ball.bounce(self.soccerfield)
        self.__collide(self.player1, self.player2)
        self.__collide(self.player1, self.enemy1)
        self.__collide(self.player1, self.enemy2)
        self.__collide(self.player1, self.ball)
        self.__collide(self.player2, self.enemy1)
        self.__collide(self.player2, self.enemy2)
        self.__collide(self.player2, self.ball)
        self.__collide(self.enemy1, self.enemy2)
        self.__collide(self.enemy1, self.ball)
        self.__collide(self.enemy2, self.ball)
        next_state = self.__get_state()

        rewards = self.__get_rewards()
        marl_reward = rewards[0] - old_rewards[0] + rewards[1] - old_rewards[1]
        sarl_reward = rewards[2] - old_rewards[2] + rewards[3] - old_rewards[3]
        done = False
        goal_control, who_score = self.__check_goal(self.ball)
        if goal_control:
            done = True


        return next_state, marl_reward, sarl_reward, done

    def render(self):
        self.screen.fill(Constants.BACKGROUND_COLOR)
        self.soccerfield.display(self.screen)
        self.player1.display(self.screen)
        self.player2.display(self.screen)
        self.enemy1.display(self.screen)
        self.enemy2.display(self.screen)
        self.ball.display(self.screen)

        scoretext = f'Real MARL {self.marlScore} - {self.sarlScore} MARL United'
        text = self.font.render(scoretext, False, (255, 255, 255))
        self.screen.blit(text, (Constants.SIZE_WIDTH / 6, 5))
        pygame.display.flip()

    def normalized_distance_to_line(self, x, y_up, y_down, ball):
        if ball.y < y_up:
            dist = math.sqrt((ball.x - x)**2 + (ball.y - y_up)**2)
        elif ball.y > y_down:
            dist = math.sqrt((ball.x - x) ** 2 + (ball.y - y_down) ** 2)
        else:
            dist = abs(ball.x - x)

        return (Constants.MAX_DISTANCE_TO_GOAL_LINE - dist) # / Constants.MAX_DISTANCE_TO_GOAL_LINE

    def normalized_ball_player_distance(self, player, ball):
        dist = math.sqrt((player.x - ball.x)**2 + (player.y - ball.y)**2)
        return (Constants.MAX_DISTANCE_TO_BALL - dist) # / Constants.MAX_DISTANCE_TO_BALL

    '''
    def run(self):
        self.marlScore = 0
        self.sarlScore = 0

        self.__create_player_ball()

        clock = pygame.time.Clock()


        running = True
        while running:
            dt = clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pressed_keys = pygame.key.get_pressed()

            self.player1.update(pressed_keys, self.ball)
            self.player2.update(pressed_keys, self.ball)
            self.enemy1.update(pressed_keys, self.ball)
            self.enemy2.update(pressed_keys, self.ball)

            self.screen.fill(Constants.BACKGROUND_COLOR)

            self.player1.move()
            self.player2.move()
            self.enemy1.move()
            self.enemy2.move()
            self.ball.move()

            self.player1.bounce(self.soccerfield)
            self.player2.bounce(self.soccerfield)
            self.enemy1.bounce(self.soccerfield)
            self.enemy2.bounce(self.soccerfield)
            self.ball.bounce(self.soccerfield)

            self.__collide(self.player1, self.player2)
            self.__collide(self.player1, self.enemy1)
            self.__collide(self.player1, self.enemy2)
            self.__collide(self.player1, self.ball)
            self.__collide(self.player2, self.enemy1)
            self.__collide(self.player2, self.enemy2)
            self.__collide(self.player2, self.ball)
            self.__collide(self.enemy1, self.enemy2)
            self.__collide(self.enemy1, self.ball)
            self.__collide(self.enemy2, self.ball)

            self.soccerfield.display(self.screen)
            self.player1.display(self.screen)
            self.player2.display(self.screen)
            self.enemy1.display(self.screen)
            self.enemy2.display(self.screen)
            self.ball.display(self.screen)

            if self.__check_goal(self.ball):
                self.__create_player_ball()

            scoretext = f'MARL {self.marlScore} - {self.sarlScore} SARL'
            text = self.font.render(scoretext, False, (255, 255, 255))
            self.screen.blit(text, (Constants.SIZE_WIDTH / 6, 5))
            pygame.display.flip()
    '''





