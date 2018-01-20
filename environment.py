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
            1: CarSprite('car4.png', [300, 375]),
            2: CarSprite('car5.jpeg', [700, 375])
        }

    def register(self, agent):
        self.num_players += 1
        agent.player_id = self.num_players

    def reset(self):
        pads = [
            # PadSprite((0,384),(5,768)),
            # PadSprite((1024,384),(5,768)),
            # PadSprite((512,0),(1024,5)),
            # PadSprite((512,768),(1024,5)),
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

        # Temporarily workaround.
        car_collision = pygame.sprite.collide_rect(self.players_dict[1], self.players_dict[2])
        for car in self.cars_group.sprites():
            bullet_collisions = pygame.sprite.spritecollide(car, self.bullets_group, True)
            pad_collisions = pygame.sprite.spritecollide(car, self.pads_group, False)
            self.pads_group.update(pad_collisions)
            car.update(self.delta_t, len(bullet_collisions), len(pad_collisions) != 0 or car_collision)

        pygame.sprite.groupcollide(self.bullets_group, self.pads_group, True, False)
        self.bullets_group.update(self.delta_t)

        next_state = None
        reward = None
        done = False
        return (next_state, reward, done)