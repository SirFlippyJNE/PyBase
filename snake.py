#imports
import pygame as pg
from random import randrange
#snek variables
pg.font.init()
WINDOW = 1000
TILE_SIZE = 50
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE)
get_random_post = lambda: [randrange(*RANGE), randrange(*RANGE)]
snek = pg.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
snek.center = get_random_post()
length = 1
segments = [snek.copy()]
snek_dir = (0, 0)
time, time_step = 0, 110
food = snek.copy()
food.center = get_random_post()
screen = pg.display.set_mode([WINDOW] * 2)
clock = pg.time.Clock()
dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
#score variables
current_score = 0
high_score = 0
#snek
while True:
    if current_score > high_score:
        high_score = current_score
    font = pg.font.Font(None, 36)
    score_surface = font.render(f"Score: {current_score}  High Score: {high_score}", True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w and dirs[pg.K_w]:
                snek_dir = (0, -TILE_SIZE)
                dirs = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1}
            elif event.key == pg.K_s and dirs[pg.K_s]:
                snek_dir = (0, TILE_SIZE)
                dirs = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
            elif event.key == pg.K_a and dirs[pg.K_a]:
                snek_dir = (-TILE_SIZE, 0)
                dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0}
            elif event.key == pg.K_d and dirs[pg.K_d]:
                snek_dir = (TILE_SIZE, 0)
                dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1}
    screen.fill('black')
    #check borders and selfeating
    self_eating = pg.Rect.collidelist(snek, segments[:-1]) != -1
    if snek.left < 0 or snek.right > WINDOW or snek.top < 0 or snek.bottom > WINDOW or self_eating:
        snek.center, food.center = get_random_post(), get_random_post()
        length, snek_dir = 1, (0, 0)
        segments = [snek.copy()]
    if snek.center == food.center:
        food.center = get_random_post()
        length += 1
        current_score += 1
    #draw food
    pg.draw.rect(screen, 'red', food)
    #draw snek
    [pg.draw.rect(screen, 'green', segment) for segment in segments]
    #move snek
    time_now = pg.time.get_ticks()
    if time_now - time > time_step:
        time = time_now
        snek.move_ip(snek_dir)
        segments.append(snek.copy())
        segments = segments[-length:]
    pg.display.flip()
    clock.tick(60)