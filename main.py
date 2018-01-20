from environment import Environment
import random
import pygame
from pygame.locals import *

class HumanAgent(object):
    def __init__(self, actions_space):
        self.actions_space = actions_space
        self.player_id = None

    def act(self):
        action = None
        for event in pygame.event.get():
            if not hasattr(event, 'key'): continue
            if event.type != KEYDOWN: continue
            if event.key == K_RIGHT: 
                action = 'right'
            elif event.key == K_LEFT: 
                action = 'left'
            elif event.key == K_UP: 
                action = 'up'
            elif event.key == K_DOWN: 
                action = 'down'
            elif event.key == K_SPACE:
                action = 'space'
            elif event.key == K_ESCAPE:
                sys.exit(0)
        return (self.player_id, action)

class RandomAgent(object):
    def __init__(self, actions_space):
        self.actions_space = actions_space
        self.player_id = None

    def act(self):
        return (self.player_id, random.choice(self.actions_space))

if __name__ == '__main__':
    env = Environment()
    env.reset()
    env.render()

    human_agent = HumanAgent(env.actions_space)
    random_agent = RandomAgent(env.actions_space)
    env.register(human_agent)
    env.register(random_agent)

    done = False
    while not done:
        env.render()
        human_action = human_agent.act()
        random_action = random_agent.act()
        ob, reward, done = env.step([human_action, random_action])
        