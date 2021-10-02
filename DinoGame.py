import pygame
import os
import random
pygame.font.init()

WIDTH, HEIGHT = 700, 400
DINO_WIDTH, DINO_HEIGHT = 63, 63
DINO_DUCKING_WIDTH, DINO_DUCKING_HEIGHT = 63, 59
BIRD_WIDTH, BIRD_HEIGHT = 63, 50

DINO_Y = HEIGHT//2 + 48

ONE_CACTUS_TALL_WIDTH, ONE_CACTUS_TALL_HEIGHT = 25, 50
ONE_CACTUS_SMALL_WIDTH, ONE_CACTUS_SMALL_HEIGHT = 15, 30

TWO_CACTUS_TALL_WIDTH, TWO_CACTUS_TALL_HEIGHT = 51, 50
TWO_CACTUS_SMALL_WIDTH, TWO_CACTUS_SMALL_HEIGHT = 36, 35

FOUR_CACTUS_TALL_WIDTH, FOUR_CACTUS_TALL_HEIGHT = 76, 50
FOUR_CACTUS_SMALL_WIDTH, FOUR_CACTUS_SMALL_HEIGHT = 53, 35

FPS = 60
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
DINODUCKING1_IMAGE = pygame.image.load(os.path.join('Assets', 'DinoDucking1.png'))
DINODUCKING2_IMAGE = pygame.image.load(os.path.join('Assets', 'DinoDucking2.png'))
DINODUCKING1 = pygame.transform.scale(DINODUCKING1_IMAGE, (DINO_DUCKING_WIDTH, DINO_DUCKING_HEIGHT))
DINODUCKING2 = pygame.transform.scale(DINODUCKING2_IMAGE, (DINO_DUCKING_WIDTH, DINO_DUCKING_HEIGHT))

BIRD_IMAGE = pygame.image.load(os.path.join('Assets', 'bird.png'))
BIRD2_IMAGE = pygame.image.load(os.path.join('Assets', 'bird2.png'))
BIRD = pygame.transform.scale(BIRD_IMAGE, (BIRD_WIDTH, BIRD_HEIGHT))
BIRD2 = pygame.transform.scale(BIRD2_IMAGE, (BIRD_WIDTH, BIRD_HEIGHT))

ONE_CACTUS_IMAGE = pygame.image.load(os.path.join('Assets', 'OneCactus.png'))
ONE_CACTUS_TALL = pygame.transform.scale(ONE_CACTUS_IMAGE, (ONE_CACTUS_TALL_WIDTH, ONE_CACTUS_TALL_HEIGHT))
ONE_CACTUS_SMALL = pygame.transform.scale(ONE_CACTUS_IMAGE, (ONE_CACTUS_SMALL_WIDTH, ONE_CACTUS_SMALL_HEIGHT))

TWO_CACTUS_IMAGE = pygame.image.load(os.path.join('Assets', 'TwoCactus.png'))
TWO_CACTUS_TALL = pygame.transform.scale(TWO_CACTUS_IMAGE, (TWO_CACTUS_TALL_WIDTH, TWO_CACTUS_TALL_HEIGHT))
TWO_CACTUS_SMALL = pygame.transform.scale(TWO_CACTUS_IMAGE, (TWO_CACTUS_SMALL_WIDTH, TWO_CACTUS_SMALL_HEIGHT))

FOUR_CACTUS_IMAGE = pygame.image.load(os.path.join('Assets', 'FourCactus.png'))
FOUR_CACTUS_TALL = pygame.transform.scale(FOUR_CACTUS_IMAGE, (FOUR_CACTUS_TALL_WIDTH, FOUR_CACTUS_TALL_HEIGHT))
FOUR_CACTUS_SMALL = pygame.transform.scale(FOUR_CACTUS_IMAGE, (FOUR_CACTUS_SMALL_WIDTH, FOUR_CACTUS_SMALL_HEIGHT))

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
        self.dino_ducking_y = y+4
        self.img = DINO
        self.jump_vel = 10
        self.jumping = False
        self.ducking = False
        self.rounded_score = 1
        self.actual_score = 1
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

        if(not self.ducking):
            if self.y != DINO_Y:
                WIN.blit(DINO, (self.x, self.y))
            elif self.animation_count <= 5:
                WIN.blit(DINO1, (self.x, self.y))
            elif 5 <= self.animation_count <= 10:
                WIN.blit(DINO2, (self.x, self.y))
            else:
                WIN.blit(DINO2, (self.x, self.y))
                self.animation_count = 0

        else:
            if self.y != DINO_Y:
                WIN.blit(DINODUCKING1, (self.x, self.y))
            elif self.animation_count <= 5:
                WIN.blit(DINODUCKING1, (self.x, self.dino_ducking_y))
            elif 5 <= self.animation_count <= 10:
                WIN.blit(DINODUCKING2, (self.x, self.dino_ducking_y))
            else:
                WIN.blit(DINODUCKING2, (self.x, self.dino_ducking_y))
                self.animation_count = 0


class Obstacle:

    obstacle_list = []
    current_obstacles = []
    counter = 0
    right_spawn_border = WIDTH // 2 + 50
    counter_tick = 0
    obstacle_vel = 5

    def __init__(self, x, y, width, height, img):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = img
        self.animation_count = 0
    
    @classmethod
    def add_obstacle(cls, dino):
        if dino.rounded_score >= 500:
            random_obstacle = random.choice(cls.obstacle_list)
            if random_obstacle.img == BIRD:
                random_obstacle.y = random.choice([HEIGHT//2-10, HEIGHT//2 + 17, DINO_Y + 10])

        else:    
            random_obstacle = random.choice(cls.obstacle_list[:len(cls.obstacle_list)-1])

        new_obstacle = Obstacle(random_obstacle.x, random_obstacle.y, random_obstacle.width, random_obstacle.height, random_obstacle.img)
        cls.current_obstacles.append(new_obstacle)

    @classmethod
    def spawn(cls, dino):

        cls.counter += 1
 
        bottom_counter = random.randint(20, 60) + cls.counter_tick

        if len(cls.current_obstacles) == 0:
            Obstacle.add_obstacle(dino)

        if dino.rounded_score % 200 == 0 and dino.rounded_score <= 1200:
            cls.right_spawn_border -= 25/6
            cls.counter_tick += 10/6
            cls.obstacle_vel += 1/6

        for current in cls.current_obstacles:

            current.x -= cls.obstacle_vel

            if 50 <= current.x <= cls.right_spawn_border and len(cls.current_obstacles) < 2 and bottom_counter <= cls.counter <= 120:
                Obstacle.add_obstacle(dino)
                cls.counter = 0
            
            if current.x <= -current.width:
                cls.current_obstacles.remove(current)

            collided = current.collide(dino)

            if collided:
                return True

            current.draw()  


    def draw(self):

        if self.img != BIRD:
            WIN.blit(self.img, (self.x, self.y))

        elif 0 <= self.animation_count <= 15:
            WIN.blit(BIRD, (self.x, self.y))
            self.animation_count += 1

        elif 15 <= self.animation_count <= 30:
            WIN.blit(BIRD2, (self.x, self.y))
            self.animation_count += 1

        else:
            WIN.blit(BIRD, (self.x, self.y))
            self.animation_count = 0
        

    def collide(self, dino):
        dino_mask = dino.get_mask()
        obstacle_mask = pygame.mask.from_surface(self.img)
        
        if not dino.ducking:
            obstacle_offset = (round(self.x - dino.x), round(self.y - dino.y))

        elif dino.ducking and dino.y == DINO_Y:
            obstacle_offset = (round(self.x - dino.x), round(self.y - dino.dino_ducking_y))

        else:
            obstacle_offset = (round(self.x - dino.x), round(self.y - dino.y))

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
    one_cactus_small = Obstacle(750, HEIGHT//2 + 75, ONE_CACTUS_SMALL_WIDTH, ONE_CACTUS_SMALL_HEIGHT, ONE_CACTUS_SMALL)
    one_cactus_tall = Obstacle(750, HEIGHT//2 + 57, ONE_CACTUS_TALL_WIDTH, ONE_CACTUS_TALL_HEIGHT, ONE_CACTUS_TALL)
    two_cactus_small = Obstacle(750, HEIGHT//2 + 70, TWO_CACTUS_SMALL_WIDTH, TWO_CACTUS_SMALL_HEIGHT, TWO_CACTUS_SMALL)
    two_cactus_tall = Obstacle(750, HEIGHT//2 + 56, TWO_CACTUS_TALL_WIDTH, TWO_CACTUS_TALL_HEIGHT, TWO_CACTUS_TALL)
    four_cactus_small = Obstacle(750, HEIGHT//2 + 70, FOUR_CACTUS_SMALL_WIDTH, FOUR_CACTUS_SMALL_HEIGHT, FOUR_CACTUS_SMALL)
    four_cactus_tall = Obstacle(750, HEIGHT//2 + 56, FOUR_CACTUS_TALL_WIDTH, FOUR_CACTUS_TALL_HEIGHT, FOUR_CACTUS_TALL)
    bird = Obstacle(750, HEIGHT//2, BIRD_WIDTH, BIRD_HEIGHT, BIRD)

    Obstacle.obstacle_list = []
    Obstacle.current_obstacles = []
    Obstacle.counter = 0
    Obstacle.obstacle_vel = 5

    Obstacle.obstacle_list.extend([one_cactus_small, one_cactus_tall, two_cactus_small, two_cactus_tall, 
                                   four_cactus_small, four_cactus_tall, bird])

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

        grd1x -= Obstacle.obstacle_vel
        grd2x -= Obstacle.obstacle_vel
        grd3x -= Obstacle.obstacle_vel


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

                if event.key == pygame.K_DOWN:
                    dino.ducking = True

            else:
                dino.ducking = False

        dino.actual_score += 5/33
        dino.rounded_score = round(dino.actual_score)
        collided = draw_window(dino, backgrounds, grounds)
        
        if collided:
            break
    
    main()


if __name__ == "__main__":
    main()