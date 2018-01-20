# INTIALISATION
import pygame, math, sys
from pygame.locals import *
screen = pygame.display.set_mode((1024, 768))
clock = pygame.time.Clock()
class CarSprite(pygame.sprite.Sprite):
    MAX_FORWARD_SPEED = 10
    MAX_REVERSE_SPEED = -10
    ACCELERATION = 2
    TURN_SPEED = 5

    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load(image)
        self.src_image = pygame.transform.scale(self.src_image,(50,100))
        self.position = position
        self.speed = self.direction = 0
        self.k_left = self.k_right = self.k_down = self.k_up = 0
        self.int_bullets = 100;
        self.rect = self.src_image.get_rect()
        self.life = 100
    def update(self, deltat, int_hit):
        # SIMULATION
        self.speed += (self.k_up + self.k_down)
        if self.speed > self.MAX_FORWARD_SPEED:
            self.speed = self.MAX_FORWARD_SPEED
        if self.speed < self.MAX_REVERSE_SPEED:
            self.speed = self.MAX_REVERSE_SPEED
        self.direction += (self.k_right + self.k_left)
        x, y = self.position
        rad = self.direction * math.pi / 180
        x += self.speed*math.sin(rad)
        y += self.speed*math.cos(rad)
        self.position = (x, y)
        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

        if int_hit != 0:
            for i in range(int_hit):
                self.life -=1
                print('Hit! -1 life, current life is ',self.life)

    def shoot(self):
        print(self.int_bullets)
        if self.int_bullets == 0:
            print('No more bullets')
        else:
            self.int_bullets -= 1
            x_car, y_car = self.position
            rad_car = self.direction * math.pi / 180
            x_bullet = x_car - 80*math.sin(rad_car)
            y_bullet = y_car - 80*math.cos(rad_car)
            return BulletSprite((x_bullet, y_bullet),self.direction)

class BulletSprite(pygame.sprite.Sprite):
    SPEED = -20
    def __init__(self,position,direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('bullet.png')
        self.image = pygame.transform.scale(self.image, (10,10))
        self.image = pygame.transform.rotate(self.image, direction)
        self.direction = direction
        self.position = position
        self.rect = self.image.get_rect()
    def update(self, deltat, hit_list=0):
        x, y = self.position
        rad = self.direction * math.pi / 180
        x += self.SPEED * math.sin(rad)
        y += self.SPEED * math.cos(rad)
        self.position = (x,y)
        self.rect = self.image.get_rect()
        self.rect.center = self.position



class PadSprite(pygame.sprite.Sprite):
    normal = pygame.image.load('pad_normal.png')
    normal = pygame.transform.scale(normal,(100,150))
    hit = pygame.image.load('pad_hit.png')
    hit = pygame.transform.scale(hit,(100,150))
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(self.normal.get_rect())
        self.rect.center = position
    def update(self, hit_list):
        if self in hit_list: self.image = self.hit
        else: self.image = self.normal


pads = [
    PadSprite((200, 200)),
    PadSprite((800, 200)),
    PadSprite((200, 600)),
    PadSprite((800, 600)),
]
pad_group = pygame.sprite.RenderPlain(*pads)

bullet_group = pygame.sprite.RenderPlain()

# CREATE A CAR AND RUN
rect = screen.get_rect()
car = CarSprite('car4.png', rect.center)
car2 = CarSprite('car2.jpg', rect.center)

cars = [car, car2]
car_group = pygame.sprite.RenderPlain(*cars)
while 1:
    # USER INPUT
    deltat = clock.tick(30)
    for event in pygame.event.get():
        if not hasattr(event, 'key'): continue
        down = event.type == KEYDOWN
        if event.key == K_RIGHT: 
            car.k_right = down * -5
        elif event.key == K_LEFT: 
            car.k_left = down * 5
        elif event.key == K_UP: 
            car.k_up = down * -4
        elif event.key == K_DOWN: 
            car.k_down = down * 4
        elif event.key == K_SPACE:
            bullet = car.shoot()
            if bullet != None:
                bullet_group.add(bullet)
        elif event.key == K_ESCAPE: 
            sys.exit(0)
    # RENDERING
    screen.fill((0,0,0))
    collisions = pygame.sprite.spritecollide(car, bullet_group, True)
    car.update(deltat, len(collisions))
    # for bullet_sprite in collisions:
    #     bullet_sprite.kill()

    collisions = pygame.sprite.spritecollide(car2, bullet_group, True)
    car2.update(deltat, len(collisions))
    # for bullet_sprite in collisions:
    #     bullet_sprite.kill()

    car_group.draw(screen)

    collisions = pygame.sprite.spritecollide(car, pad_group, False)
    pad_group.update(collisions)
    pad_group.draw(screen)

    bullet_group.update(deltat)
    bullet_group.draw(screen)
    pygame.display.flip()

