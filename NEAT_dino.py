import pygame
import os
import random
import neat
from math import sqrt

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

GEN = 0

SCORE_UPDATE = 5/33

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
NUMBER_ALIVE_FONT = pygame.font.Font(font, 12)
GENERATION_FONT = pygame.font.Font(font,12)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('DINO GAME')

class Dino:

    def __init__(self, y):
        self.x = 15
        self.y = y
        self.dino_ducking_y = y+4
        self.img = DINO
        self.jump_vel = 10
        self.ducking = False
        self.animation = 0
        self.animation_count = 0


    def get_mask(self):
        return pygame.mask.from_surface(self.img)

    def jump(self):

        tick_count = 0.5

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
    def add_obstacle(cls, dinos, rounded_score):
        # if rounded_score >= 500:
        random_obstacle = random.choices(cls.obstacle_list, [0.1,0.1,0.1,0.1,0.1,0.1,0.6])[0]
        if random_obstacle.img == BIRD:
            random_obstacle.y = random.choice([HEIGHT//2-10, HEIGHT//2 + 17, DINO_Y + 10])

        else:    
            random_obstacle = random.choice(cls.obstacle_list[:len(cls.obstacle_list)-1])

        new_obstacle = Obstacle(random_obstacle.x, random_obstacle.y, random_obstacle.width, random_obstacle.height, random_obstacle.img)
        cls.current_obstacles.append(new_obstacle)

    @classmethod
    def spawn(cls, dinos, rounded_score, nets, ge):
        
        cls.counter += 1
 
        bottom_counter = random.randint(20, 60) + cls.counter_tick

        if len(cls.current_obstacles) == 0:
            Obstacle.add_obstacle(dinos, rounded_score)

        if rounded_score % 200 == 0 and rounded_score <= 1200:
            cls.right_spawn_border -= 25/6
            cls.counter_tick += 10/6
            cls.obstacle_vel += 1/6
            
        for current in cls.current_obstacles:

            current.x -= cls.obstacle_vel

            for g in ge:
                if current.x <= 10:
                    g.fitness += 5

            if 50 <= current.x <= cls.right_spawn_border and len(cls.current_obstacles) < 2 and bottom_counter <= cls.counter <= 120:
                Obstacle.add_obstacle(dinos, rounded_score)
                cls.counter = 0
            
            if current.x <= -current.width:

                cls.current_obstacles.remove(current)

            collided = current.collide(dinos, nets, ge)

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
        

    def collide(self, dinos, nets, ge):
        for i, dino in enumerate(dinos):
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
                dinos.pop(i)
                nets.pop(i)
                if self.y == HEIGHT//2-10:
                    ge[i].fitness -= 40
                else:
                    ge[i].fitness -= 10
                ge.pop(i)
        

def draw_window(dinos, rounded_score, backgrounds, grounds, nets, ge):

    WIN.fill(WHITE)

    WIN.blit(BACKGROUND, (backgrounds[0] ,0))
    WIN.blit(BACKGROUND2, (backgrounds[1] ,0))
    WIN.blit(BACKGROUND3, (backgrounds[2] ,0))

    score_text = SCORE_FONT.render(f'{rounded_score}', True, GRAY)
    WIN.blit(score_text, (WIDTH - score_text.get_width() - 20, 20))

    gen_text = GENERATION_FONT.render(f'GEN: {GEN}', True, GRAY)
    WIN.blit(gen_text, (3, 10))

    alive_dinos = NUMBER_ALIVE_FONT.render(f'ALIVE: {len(dinos)}', True, GRAY)
    WIN.blit(alive_dinos, (3, 40))

    WIN.blit(GROUND, (grounds[0] ,DINO_Y + 40))
    WIN.blit(GROUND2, (grounds[1] ,DINO_Y + 40))
    WIN.blit(GROUND3, (grounds[2] ,DINO_Y + 40))

    Obstacle.spawn(dinos, rounded_score, nets, ge)

    if len(Obstacle.current_obstacles) < 1:
        Obstacle.spawn(dinos, rounded_score, nets, ge)

    obs_ind = 0

    if len(dinos) > 0:
        if len(Obstacle.current_obstacles) > 1 and dinos[0].x > Obstacle.current_obstacles[0].x:
            obs_ind = 1
    else:
        return 'Finished'

    for dino in dinos:

        ge[dinos.index(dino)].fitness += SCORE_UPDATE

        dino_x = dino.x
        dino_y = dino.y
        obstacle_x = Obstacle.current_obstacles[obs_ind].x
        obstacle_y = Obstacle.current_obstacles[obs_ind].y  
        obstacle_width = Obstacle.current_obstacles[obs_ind].width
        obstacle_height = Obstacle.current_obstacles[obs_ind].height
        dino_distance_obs = abs(dino.x + DINO_WIDTH - obstacle_x)
 
        output = nets[dinos.index(dino)].activate((dino_x, dino_y, obstacle_x, obstacle_y, obstacle_width, obstacle_height, dino_distance_obs))

        if dino.y < DINO_Y:
            dino.jump()
            dino.draw()
        
        elif output[0] > 0.5 and not dino.ducking:
            dino.ducking = True
            dino.draw()

        elif output[0] <= 0.5 and dino.ducking:
            dino.ducking = False
            dino.draw()
        
        elif output[1] > 0.5 and not dino.ducking:
            dino.jump()
            dino.draw()
        
        else:
            dino.draw()

        pygame.display.update()

    pygame.display.update()


def main(genomes, config):

    global GEN
    nets = []
    ge = []
    dinos = []

    for ge_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        dinos.append(Dino(DINO_Y))
        genome.fitness = 0
        ge.append(genome)

    WIN.fill(WHITE)

    actual_score = 1

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

        actual_score += SCORE_UPDATE
        rounded_score = round(actual_score)

        finished = draw_window(dinos, rounded_score, backgrounds, grounds, nets, ge)

        if finished == 'Finished':
            GEN += 1
            run = False
            break

def run(config_path):
    
    config = neat.config.Config(neat.DefaultGenome, 
                                neat.DefaultReproduction, 
                                neat.DefaultSpeciesSet, 
                                neat.DefaultStagnation, 
                                config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())

    best_dino = p.run(main, 30)

if __name__ == "__main__":
    main_dir = os.path.dirname(__file__)        # Gets directory where this file is ran
    print(main_dir)
    config_path = os.path.join(main_dir, 'config-network.txt')      # Load in config-network.txt path
    run(config_path)