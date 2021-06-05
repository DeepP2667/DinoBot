import pygame
import os
import time
import random

WIDTH, HEIGHT = 700, 400
DINO_WIDTH, DINO_HEIGHT = 63, 63

ONE_CACTUS_TALL_WIDTH, ONE_CACTUS_TALL_HEIGHT = 25, 50
ONE_CACTUS_SMALL_WIDTH, ONE_CACTUS_SMALL_HEIGHT = 15, 30

TWO_CACTUS_TALL_WIDTH, TWO_CACTUS_TALL_HEIGHT = 51, 50
TWO_CACTUS_SMALL_WIDTH, TWO_CACTUS_SMALL_HEIGHT = 70, 35



FPS = 30
VEL = 5
BACKGROUND_VEL = 1.5

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

BACKGROUND = pygame.image.load(os.path.join('Assests', 'Background.png'))
BACKGROUND2 = pygame.image.load(os.path.join('Assests', 'Background2.png'))
BACKGROUND3 = pygame.image.load(os.path.join('Assests', 'Background3.png'))


BORDER = pygame.Rect(0, HEIGHT//2 + 100, WIDTH, 1)


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('DINO GAME')


class Dino:

    def __init__(self, y):
        self.x = 15
        self.y = y
        self.img = DINO


    def draw(self):
        WIN.blit(DINO, (self.x, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

    def jump(self):
        self.jump_vel = 10
        self.tick_count = 0




class Obstacle:

    obstacle_list = []
    current_obstacles = []
    counter = 0

    def __init__(self, x, y, width, height, img):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 0
        self.img = img
    
    @classmethod
    def add_obstacle(cls):
        random_obstacle = random.choice(cls.obstacle_list)
        new_rect = Obstacle(random_obstacle.x, random_obstacle.y, random_obstacle.width, 
                            random_obstacle.height, random_obstacle.img)
        
        cls.current_obstacles.append(new_rect)

    @classmethod
    def spawn(cls, dino):
        cls.counter += 1

        for current in cls.current_obstacles:
            current.x -= VEL

            if 50 <= current.x <= WIDTH // 2 + 50 and len(cls.current_obstacles) < 2 and random.randint(20, 60) <= cls.counter <= 120:
                Obstacle.add_obstacle()
                cls.counter = 0
            
            if current.x <= -30:
                cls.current_obstacles.remove(current)

            collided = current.collide(dino)

            if collided:
                return True

            current.draw()  


    def draw(self):
        WIN.blit(self.img, (self.x, self.y))

    def collide(self, dino):
        dino_mask = dino.get_mask()
        obstacle_mask = pygame.mask.from_surface(self.img)

        obstacle_offset = (self.x - dino.x, self.y - dino.y)

        point = dino_mask.overlap(obstacle_mask, obstacle_offset)

        if point:
            return True

        return False
        

def draw_window(dino, backgrounds):

    WIN.blit(BACKGROUND, (backgrounds[0] ,0))
    WIN.blit(BACKGROUND, (backgrounds[1] ,0))
    WIN.blit(BACKGROUND, (backgrounds[2] ,0))


    dino.draw()

    collided = Obstacle.spawn(dino)
    if collided:
        return True

    pygame.display.update()



def main():

    WIN.fill(WHITE)

    dino = Dino(HEIGHT//2 + 48)
    one_cactus_tall = Obstacle(750, HEIGHT//2 + 57, ONE_CACTUS_TALL_WIDTH, ONE_CACTUS_TALL_HEIGHT, ONE_CACTUS_TALL)
    one_cactus_small = Obstacle(750, HEIGHT//2 + 75, ONE_CACTUS_SMALL_WIDTH, ONE_CACTUS_SMALL_HEIGHT, ONE_CACTUS_SMALL)
    two_cactus_tall = Obstacle(750, HEIGHT//2 + 56, TWO_CACTUS_TALL_WIDTH, TWO_CACTUS_TALL_HEIGHT, TWO_CACTUS_TALL)

    Obstacle.obstacle_list = []
    Obstacle.current_obstacles = []

    Obstacle.obstacle_list.extend([one_cactus_small, one_cactus_tall, two_cactus_tall])
    Obstacle.current_obstacles.append(random.choice(Obstacle.obstacle_list))

    bg1x = 0
    bg2x = BACKGROUND.get_width()
    bg3x = BACKGROUND2.get_width() * 2

    clock = pygame.time.Clock()
    run = True
    
    while run:

        bg1x -= BACKGROUND_VEL
        bg2x -= BACKGROUND_VEL
        bg3x -= BACKGROUND_VEL

        if bg1x < BACKGROUND.get_width() * -1:
            bg1x = BACKGROUND.get_width()
        if bg2x < BACKGROUND.get_width() * -1:
            bg2x = BACKGROUND.get_width()
        if bg3x < BACKGROUND.get_width() * -1:
            bg3x = BACKGROUND.get_width()

        backgrounds = [bg1x, bg2x, bg3x] 

        clock.tick(FPS)


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()


        collided = draw_window(dino, backgrounds)
        
        if collided:
            break
    
    main()





if __name__ == "__main__":
    main()