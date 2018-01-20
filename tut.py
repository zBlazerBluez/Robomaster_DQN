import pygame
import time
from pygame.locals import *

screen = pygame.display.set_mode((1024, 768))
#screen = pygame.display.set_mode((1024, 768), FULLSCREEN)

car = pygame.image.load('car3.png')
clock = pygame.time.Clock()
FRAMES_PER_SECOND = 30
deltat = clock.tick(FRAMES_PER_SECOND)

screen.fill((0,0,0))
screen.blit(car, (100,100))
pygame.display.flip()
for i in range(700):
    # screen.fill((0, 0, 0))
    # screen.blit(car, (i,0))
    # pygame.display.flip()
    #time.sleep(0.01)
    screen.fill((0,0,0))
    screen.blit(car, (100.23,100.23))
    pygame.display.flip()
