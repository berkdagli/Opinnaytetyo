import torch
from game import Game


game = Game(True,test=True) # True: random, False: ortadan başlama


game.player1.qnetwork_local.load_state_dict(torch.load('brain_record/player1.pth'))
game.player2.qnetwork_local.load_state_dict(torch.load('brain_record/player2.pth'))
game.enemy1.qnetwork_local.load_state_dict(torch.load('brain_record/enemy1.pth'))
game.enemy2.qnetwork_local.load_state_dict(torch.load('brain_record/enemy2.pth'))

game.activate_screen()

for i in range(10):
    state = game.reset()
    for j in range(2000):
        actions = game.act(state)
        game.render()
        state, marl_reward, sarl_reward, done = game.step_test(state, actions)

        if done:
            break

print("Finished")