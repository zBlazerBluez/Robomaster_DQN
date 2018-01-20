from tut3 import *
import pygame
from pygame.sprite import Group, RenderPlain
from pygame.locals import *

class Environment(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((1024, 768))
        self.clock = pygame.time.Clock()
        self.delta_t = self.clock.tick(30)

        self.actions_space = ['up', 'down', 'left', 'right']

        self.pads_group = None
        self.cars_group = None
        self.bullets_group = None

        self.num_players = 0
        self.players_dict = {
            1: CarSprite('car4.png', self.screen.get_rect().center),
            2: CarSprite('car2.jpg', self.screen.get_rect().center)
        }

    def register(self, agent):
        self.num_players += 1
        agent.player_id = self.num_players

    def reset(self):
        pads = [
            PadSprite((0,384),(5,768)),
            PadSprite((1024,384),(5,768)),
            PadSprite((512,0),(1024,5)),
            PadSprite((512,768),(1024,5)),
            PadSprite((200, 200),(100,150)),
            PadSprite((800, 200),(100,150)),
            PadSprite((200, 600),(100,150)),
            PadSprite((800, 600),(100,150))
        ]
        cars = list(self.players_dict.values())
        self.pads_group = RenderPlain(*pads)
        self.cars_group = RenderPlain(*cars)
        self.bullets_group = RenderPlain()

    def render(self):
        self.screen.fill((0, 0, 0))
        self.pads_group.draw(self.screen)
        self.cars_group.draw(self.screen)
        self.bullets_group.draw(self.screen)
        pygame.display.flip()

    def step(self, actions):
        for player_id, action in actions:
            if player_id == None: continue
            bullet = self.players_dict[player_id].act(action)
            if bullet != None:
                self.bullets_group.add(bullet)
        for car in self.cars_group.sprites():
            collisions = pygame.sprite.spritecollide(car, self.bullets_group, True)
            car.update(self.delta_t, len(collisions))
        next_state = None
        reward = None
        done = False
        return (next_state, reward, done)