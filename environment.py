import pygame
from pygame.sprite import Group
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
        self.players_dict = {}

    def register(agent):
        self.num_players += 1
        agent.player_id = self.num_players

    def reset(self):
        pads = [
            PadSprite((200, 200)),
            PadSprite((800, 200)),
            PadSprite((200, 600)),
            PadSprite((800, 600)),
        ]
        cars = [
            CarSprite('car4.png', rect.center), 
            CarSprite('car2.jpg', rect.center)
        ]
        self.pads_group = Group(*pads)
        self.cars_group = Group(*cars)
        self.bullets_group = Group()

    def render(self):
        self.screen.fill((0, 0, 0))
        self.pads_group.draw(self.screen)
        self.cars_group.draw(self.screen)
        self.bullets_group.draw(self.screen)
        pygame.display.flip()

    def step(actions):
        for player_id, action in actions:
            if player_id == None: continue
            bullet = self.cars_group.sprites[player_id].act(action)
            if bullet != None:
                self.bullets_group.add(bullet)
        for car in self.cars_group.sprites:
            collisions = pygame.sprite.spritecollide(car, self.bullets_group, True)
            car.update(delta_t, len(collisions))
        next_state = None
        reward = None
        done = False
        return (next_state, reward, done)