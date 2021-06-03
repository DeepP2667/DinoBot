import pygame
import os
import time
import random

WIDTH, HEIGHT = 700, 400
DINO_WIDTH, DINO_HEIGHT = 63, 63

ONE_CACTUS_TALL_WIDTH, ONE_CACTUS_TALL_HEIGHT = 28, 55
ONE_CACTUS_SMALL_WIDTH, ONE_CACTUS_SMALL_HEIGHT = 15, 30

TWO_CACTUS_TALL_WIDTH, TWO_CACTUS_TALL_HEIGHT = 56, 55
TWO_CACTUS_SMALL_WIDTH, TWO_CACTUS_SMALL_HEIGHT = 70, 35


VEL = 7
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


DINO_IMAGE = pygame.image.load(os.path.join('Assests', 'Dino.png'))
DINO = pygame.transform.scale(DINO_IMAGE, (DINO_WIDTH, DINO_HEIGHT))

ONE_CACTUS_IMAGE = pygame.image.load(os.path.join('Assests', 'OneCactus.png'))
ONE_CACTUS_TALL = pygame.transform.scale(ONE_CACTUS_IMAGE, (ONE_CACTUS_TALL_WIDTH, ONE_CACTUS_TALL_HEIGHT))
ONE_CACTUS_SMALL = pygame.transform.scale(ONE_CACTUS_IMAGE, (ONE_CACTUS_SMALL_WIDTH, ONE_CACTUS_SMALL_HEIGHT))

TWO_CACTUS_IMAGE = pygame.image.load(os.path.join('Assests', 'TwoCactus.png'))
TWO_CACTUS_TALL = pygame.transform.scale(TWO_CACTUS_IMAGE, (TWO_CACTUS_TALL_WIDTH, TWO_CACTUS_TALL_HEIGHT))
TWO_CACTUS_SMALL = pygame.transform.scale(ONE_CACTUS_IMAGE, (TWO_CACTUS_SMALL_WIDTH, TWO_CACTUS_SMALL_HEIGHT))

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('DINO GAME')


class Dino:

    def __init__(self, x, y):
        self.x = x
        self.y = y




class Obstacle:

    obstacle_list = []
    current_obstacles = []

    def __init__(self, x, y, width, height, img):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 0
        self.img = img
        self.obsRect = pygame.Rect(self.x, self.y, width, height)
        Obstacle.obstacle_list.append(self)


    @classmethod
    def spawn(cls):

        for current in cls.current_obstacles:
            
            current.obsRect.x -= VEL

            if random.uniform(0, WIDTH//2) <= current.obsRect.x <= WIDTH//2 + 20 and len(cls.current_obstacles) < 3:
                new_obs = random.choice(cls.obstacle_list)
                new_obs_Rect = pygame.Rect(new_obs.x, new_obs.y, new_obs.width, new_obs.height)
                cls.current_obstacles.append(new_obs_Rect)
            
            if current.obsRect.x <= 0:
                cls.current_obstacles.remove(current)

            current.draw()
            
    def draw(self):
        WIN.blit(self.img, (self.obsRect.x, self.obsRect.y))


def draw_window(dino):

    WIN.fill(WHITE)
    
    WIN.blit(DINO, (dino.x, dino.y))

    Obstacle.spawn()
    pygame.display.update()



def main():

    WIN.fill(WHITE)

    dino = Dino(15, HEIGHT//2 + 50)
    one_cactus_tall = Obstacle(750, HEIGHT//2 + 55, ONE_CACTUS_TALL_WIDTH, ONE_CACTUS_TALL_HEIGHT, ONE_CACTUS_TALL)
    one_cactus_small = Obstacle(750, HEIGHT//2 + 75, ONE_CACTUS_SMALL_WIDTH, ONE_CACTUS_SMALL_HEIGHT, ONE_CACTUS_SMALL)
    two_cactus_tall = Obstacle(750, HEIGHT//2 + 52, TWO_CACTUS_TALL_WIDTH, TWO_CACTUS_TALL_HEIGHT, TWO_CACTUS_TALL)

    Obstacle.current_obstacles.append(one_cactus_tall)

    clock = pygame.time.Clock()
    run = True
    
    while run:

        clock.tick(FPS)


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()



        draw_window(dino)

main()