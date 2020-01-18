from game import Game
from collections import deque
import matplotlib.pyplot as plt
import numpy as np
import torch
import sys


def dqn(n_episodes=20000, max_t=700, eps_start=1.0, eps_end=0.3, eps_decay=0.999, append=False):
    """Deep Q-Learning.

    Params
    ======
        n_episodes (int): maximum number of training episodes
        max_t (int): maximum number of timesteps per episode
        eps_start (float): starting value of epsilon, for epsilon-greedy action selection
        eps_end (float): minimum value of epsilon
        eps_decay (float): multiplicative factor (per episode) for decreasing epsilon
    """
    if append:
        marl_f = open('marl_rewards.txt', 'a')
        sarl_f = open('sarl_rewards.txt', 'a')
    else:
        marl_f = open('marl_rewards.txt', 'w')
        sarl_f = open('sarl_rewards.txt', 'w')
    #game.activate_screen()
    marl_scores = []  # list containing scores from each episode
    marl_scores_window = deque(maxlen=100)  # last 100 scores
    sarl_scores = []  # list containing scores from each episode
    sarl_scores_window = deque(maxlen=100)  # last 100 scores
    eps = eps_start  # initialize epsilon
    for i_episode in range(1, n_episodes + 1):
        state = game.reset()
        marl_score = 0
        sarl_score = 0
        t = 0
        actions_trace_MARL = []
        actions_trace_SARL = []
        while t<max_t:
            actions = game.act(state, eps)
            next_state, marl_reward, sarl_reward, done, who_score = game.step(state, actions, actions_trace_MARL, actions_trace_SARL)
            actions_trace_MARL.append({"state": state, "actions": actions[:2], "next_state": next_state})
            actions_trace_SARL.append({"state": state, "actions": actions[2:], "next_state": next_state})
            #game.render()
            state = next_state
            marl_score += marl_reward
            sarl_score += sarl_reward
            t = t + 1
            if done:
                break

        marl_score = marl_score/t
        sarl_score = sarl_score/t
        marl_scores_window.append(marl_score)  # save most recent score
        sarl_scores_window.append(sarl_score)  # save most recent score
        marl_scores.append(marl_score)  # save most recent score
        sarl_scores.append(sarl_score)  # save most recent score
        eps = max(eps_end, eps_decay * eps)  # decrease epsilon
        marl_f.write(str(marl_score) + "\n")
        sarl_f.write(str(sarl_score) + "\n")
        print('\rEpisode {}\t Score MARL: {:.2f}\t Score SARL: {:.2f}'.format(i_episode, marl_score, sarl_score ), end="")

        if i_episode % 100 == 0:
            print('\rEpisode {}\tAverage Score MARL: {:.2f}\tAverage Score SARL: {:.2f}'.format(i_episode, np.mean(marl_scores_window), np.mean(sarl_scores_window)))

        if i_episode % 10 == 0:
            torch.save(game.player1.qnetwork_local.state_dict(), 'brain_record/player1.pth')
            torch.save(game.player2.qnetwork_local.state_dict(), 'brain_record/player2.pth')
            torch.save(game.enemy1.qnetwork_local.state_dict(), 'brain_record/enemy1.pth')
            torch.save(game.enemy2.qnetwork_local.state_dict(), 'brain_record/enemy2.pth')
            f = open("epsilon.txt", "w")
            f.write(str(eps))
            f.close()

    marl_f.close()
    sarl_f.close()
    return marl_scores, sarl_scores


print('Number of arguments:', len(sys.argv), 'arguments.')



if "-r" in str(sys.argv):
    game = Game(True)  # True: random, False: ortadan başlama
    print("Random Başlama")
else:
    game = Game(False)  # True: random, False: ortadan başlama


if "-a" in str(sys.argv):
    f = open("epsilon.txt", "r")
    epsilon = f.read()
    f.close()
    epsilon = float(epsilon)
    game.player1.qnetwork_local.load_state_dict(torch.load('brain_record/player1.pth'))
    game.player2.qnetwork_local.load_state_dict(torch.load('brain_record/player2.pth'))
    game.enemy1.qnetwork_local.load_state_dict(torch.load('brain_record/enemy1.pth'))
    game.enemy2.qnetwork_local.load_state_dict(torch.load('brain_record/enemy2.pth'))
    print("Üstüne kaydetme epsilon", epsilon)
    dqn(eps_start=epsilon, append=True)
else:
    dqn()




