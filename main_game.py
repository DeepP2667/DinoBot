import pygame
import os
import random
pygame.font.init()

WIDTH, HEIGHT = 700, 400
DINO_WIDTH, DINO_HEIGHT = 63, 63
DINO_Y = HEIGHT//2 + 48

ONE_CACTUS_TALL_WIDTH, ONE_CACTUS_TALL_HEIGHT = 25, 50
ONE_CACTUS_SMALL_WIDTH, ONE_CACTUS_SMALL_HEIGHT = 15, 30

TWO_CACTUS_TALL_WIDTH, TWO_CACTUS_TALL_HEIGHT = 51, 50
TWO_CACTUS_SMALL_WIDTH, TWO_CACTUS_SMALL_HEIGHT = 70, 35

FPS = 60
OBSTACLE_VEL = 5
BACKGROUND_VEL = 1

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (83, 83, 83)

DINO_IMAGE = pygame.image.load(os.path.join('Assets', 'Dino.png'))
DINO1_IMAGE = pygame.image.load(os.path.join('Assets', 'dino1.png'))
DINO2_IMAGE = pygame.image.load(os.path.join('Assets', 'dino2.png'))
DINO = pygame.transform.scale(DINO_IMAGE, (DINO_WIDTH, DINO_HEIGHT))
DINO1 = pygame.transform.scale(DINO1_IMAGE, (DINO_WIDTH, DINO_HEIGHT))
DINO2 = pygame.transform.scale(DINO2_IMAGE, (DINO_WIDTH, DINO_HEIGHT))

ONE_CACTUS_IMAGE = pygame.image.load(os.path.join('Assets', 'OneCactus.png'))
ONE_CACTUS_TALL = pygame.transform.scale(ONE_CACTUS_IMAGE, (ONE_CACTUS_TALL_WIDTH, ONE_CACTUS_TALL_HEIGHT))
ONE_CACTUS_SMALL = pygame.transform.scale(ONE_CACTUS_IMAGE, (ONE_CACTUS_SMALL_WIDTH, ONE_CACTUS_SMALL_HEIGHT))

TWO_CACTUS_IMAGE = pygame.image.load(os.path.join('Assets', 'TwoCactus.png'))
TWO_CACTUS_TALL = pygame.transform.scale(TWO_CACTUS_IMAGE, (TWO_CACTUS_TALL_WIDTH, TWO_CACTUS_TALL_HEIGHT))
TWO_CACTUS_SMALL = pygame.transform.scale(ONE_CACTUS_IMAGE, (TWO_CACTUS_SMALL_WIDTH, TWO_CACTUS_SMALL_HEIGHT))

BACKGROUND = pygame.image.load(os.path.join('Assets', 'Background.png'))
BACKGROUND2 = pygame.image.load(os.path.join('Assets', 'Background2.png'))
BACKGROUND3 = pygame.image.load(os.path.join('Assets', 'Background3.png'))

GROUND = pygame.image.load(os.path.join('Assets', 'Ground.png'))
GROUND2 = pygame.image.load(os.path.join('Assets', 'Ground2.png'))
GROUND3 = pygame.image.load(os.path.join('Assets', 'Ground3.png'))

BORDER = pygame.Rect(0, HEIGHT//2 + 100, WIDTH, 1)

font = r'C:\Users\deepp\Desktop\VSCodeFiles\Python\Games\DinoAi\Assets\PressStart2P-Regular.ttf'
SCORE_FONT = pygame.font.Font(font, 12)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('DINO GAME')

class Dino:

    def __init__(self, y):
        self.x = 15
        self.y = y
        self.img = DINO
        self.jump_vel = 10
        self.jumping = False
        self.rounded_score = 0
        self.actual_score = 0
        self.animation = 0
        self.animation_count = 0


    def get_mask(self):
        return pygame.mask.from_surface(self.img)

    def jump(self):

        tick_count = 0.5
        tick_count -= 1/1000

        if self.y >= DINO_Y - 100:
            if self.y <= DINO_Y - 90:
                tick_count = 0.2
            d = tick_count * self.jump_vel + 1.5 * tick_count ** 2
            self.y -= d

        if self.y >= DINO_Y:
            self.jump_vel *= -1
            self.y = DINO_Y
            return True

        if self.y <= DINO_Y - 100:
            self.jump_vel *= -1
            d = tick_count * self.jump_vel + 1.5 * tick_count ** 2
            self.y -= d

    def draw(self):

        self.animation_count += 1

        if self.y != DINO_Y:
            WIN.blit(DINO, (self.x, self.y))
        elif self.animation_count <= 5:
            WIN.blit(DINO1, (self.x, self.y))
        elif 5 <= self.animation_count <= 10:
            WIN.blit(DINO2, (self.x, self.y))
        else:
            WIN.blit(DINO2, (self.x, self.y))
            self.animation_count = 0


class Obstacle:

    obstacle_list = []
    current_obstacles = []
    counter = 0

    def __init__(self, x, y, width, height, img):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = img
    
    @classmethod
    def add_obstacle(cls):
        random_obstacle = random.choice(cls.obstacle_list)
        new_obstacle = Obstacle(random_obstacle.x, random_obstacle.y, random_obstacle.width, random_obstacle.height, random_obstacle.img)
        cls.current_obstacles.append(new_obstacle)

    @classmethod
    def spawn(cls, dino):

        cls.counter += 1

        if len(cls.current_obstacles) == 0:
            Obstacle.add_obstacle()

        for current in cls.current_obstacles:

            current.x -= OBSTACLE_VEL

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

        obstacle_offset = (self.x - dino.x, round(self.y - dino.y))

        point = dino_mask.overlap(obstacle_mask, obstacle_offset)

        if point:
            return True

        return False
        

def draw_window(dino, backgrounds, grounds):

    WIN.fill(WHITE)

    WIN.blit(BACKGROUND, (backgrounds[0] ,0))
    WIN.blit(BACKGROUND2, (backgrounds[1] ,0))
    WIN.blit(BACKGROUND3, (backgrounds[2] ,0))

    score_text = SCORE_FONT.render(f'{dino.rounded_score}', True, GRAY)
    WIN.blit(score_text, (WIDTH - score_text.get_width() - 20, 20))

    WIN.blit(GROUND, (grounds[0] ,DINO_Y + 40))
    WIN.blit(GROUND2, (grounds[1] ,DINO_Y + 40))
    WIN.blit(GROUND3, (grounds[2] ,DINO_Y + 40))

    if dino.jumping:
        reached_ground = dino.jump()
        if reached_ground:
            dino.jumping = False

    dino.draw()

    collided = Obstacle.spawn(dino)

    if collided:
        return True

    pygame.display.update()


def main():

    WIN.fill(WHITE)

    dino = Dino(DINO_Y)
    one_cactus_tall = Obstacle(750, HEIGHT//2 + 57, ONE_CACTUS_TALL_WIDTH, ONE_CACTUS_TALL_HEIGHT, ONE_CACTUS_TALL)
    one_cactus_small = Obstacle(750, HEIGHT//2 + 75, ONE_CACTUS_SMALL_WIDTH, ONE_CACTUS_SMALL_HEIGHT, ONE_CACTUS_SMALL)
    two_cactus_tall = Obstacle(750, HEIGHT//2 + 56, TWO_CACTUS_TALL_WIDTH, TWO_CACTUS_TALL_HEIGHT, TWO_CACTUS_TALL)

    Obstacle.obstacle_list = []
    Obstacle.current_obstacles = []
    Obstacle.counter = 0

    Obstacle.obstacle_list.extend([one_cactus_small, one_cactus_tall, two_cactus_tall])

    bg1x = 0
    bg2x = BACKGROUND.get_width()
    bg3x = BACKGROUND2.get_width() * 2

    grd1x = 0
    grd2x = GROUND.get_width()
    grd3x = GROUND2.get_width() * 2

    clock = pygame.time.Clock()
    run = True
    
    while run:

        clock.tick(FPS)

        bg1x -= BACKGROUND_VEL
        bg2x -= BACKGROUND_VEL
        bg3x -= BACKGROUND_VEL

        grd1x -= OBSTACLE_VEL
        grd2x -= OBSTACLE_VEL
        grd3x -= OBSTACLE_VEL


        if bg1x < BACKGROUND.get_width() * -1:
            bg1x = BACKGROUND.get_width()
        if bg2x < BACKGROUND.get_width() * -1:
            bg2x = BACKGROUND.get_width()
        if bg3x < BACKGROUND.get_width() * -1:
            bg3x = BACKGROUND.get_width()

        if grd1x < GROUND.get_width() * -1:
            grd1x = GROUND.get_width()
        if grd2x < GROUND.get_width() * -1:
            grd2x = GROUND.get_width()
        if grd3x < GROUND.get_width() * -1:
            grd3x = GROUND.get_width()

        backgrounds = [bg1x, bg2x, bg3x]
        grounds = [grd1x, grd2x, grd3x]
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and dino.y == DINO_Y:
                    dino.jumping = True

        dino.actual_score += 5/33
        dino.rounded_score = round(dino.actual_score)
        collided = draw_window(dino, backgrounds, grounds)
        
        if collided:
            break
    
    main()


if __name__ == "__main__":
    main()