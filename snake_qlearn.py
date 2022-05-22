# Juego de snake extraído de: https://www.edureka.co/blog/snake-game-with-pygame/

import pygame
import random
import AI

pygame.init()

YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (20, 13, 213)
RED = (255, 0, 0)


BLOCK_SIZE = 10 
DIS_WIDTH = 600
DIS_HEIGHT = 400

QVALUES_N = 50
FRAMESPEED = 3000

def DrawFood(foodx, foody):
    pygame.draw.rect(dis, RED, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])   

def DrawScore(score):
    font = pygame.font.SysFont("arial", 35)
    value = font.render(f"Score: {score}", True, BLACK)
    dis.blit(value, [0, 365])

def DrawSnake(snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, BLACK, [x[0], x[1], BLOCK_SIZE, BLOCK_SIZE])

def GameLoop():
    global dis
    
    dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
    pygame.display.set_caption('Snake')
    clock = pygame.time.Clock()

    x1 = DIS_WIDTH / 2
    y1 = DIS_HEIGHT / 2
    x1_change = 0
    y1_change = 0
    snake_list = [(x1,y1)]
    length_of_snake = 1

    foodx = round(random.randrange(0, DIS_WIDTH - BLOCK_SIZE) / 10.0) * 10.0
    foody = round(random.randrange(0, DIS_HEIGHT - BLOCK_SIZE) / 10.0) * 10.0

    dead = False
    reason = None
    while not dead:
        action = learner.act(snake_list, (foodx,foody))
        if action == "left":
            x1_change = -BLOCK_SIZE
            y1_change = 0
        elif action == "right":
            x1_change = BLOCK_SIZE
            y1_change = 0
        elif action == "up":
            y1_change = -BLOCK_SIZE
            x1_change = 0
        elif action == "down":
            y1_change = BLOCK_SIZE
            x1_change = 0

        x1 += x1_change
        y1 += y1_change
        snake_head = (x1,y1)
        snake_list.append(snake_head)

        if x1 >= DIS_WIDTH or x1 < 0 or y1 >= DIS_HEIGHT or y1 < 0:
            reason = 'Bordes'
            dead = True

        if snake_head in snake_list[:-1]:
            reason = 'Cola'
            dead = True

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, DIS_WIDTH - BLOCK_SIZE) / 10.0) * 10.0
            foody = round(random.randrange(0, DIS_HEIGHT - BLOCK_SIZE) / 10.0) * 10.0
            length_of_snake += 1

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        dis.fill(BLUE)
        DrawFood(foodx, foody)
        DrawSnake(snake_list)
        DrawScore(length_of_snake - 1)
        pygame.display.update()

        learner.UpdateQValues(reason)
        
        clock.tick(FRAMESPEED)

    return length_of_snake - 1, reason



game_count = 1

learner = AI.AI(DIS_WIDTH, DIS_HEIGHT, BLOCK_SIZE)

epsi_range = (0.5, 0)
max_e_iter = 100

while True:
    learner.Reset()
    if game_count > max_e_iter:
        learner.epsilon = 0
    else:
        new_e = (epsi_range[0]-epsi_range[1])*(max_e_iter - game_count)/max_e_iter + epsi_range[1]
        print(new_e)
        learner.epsilon = new_e
    score, reason = GameLoop()
    print(f"No. iter: {game_count}; Puntaje: {score}; Error: {reason}") 
    game_count += 1
    if game_count % QVALUES_N == 0:
        print("Guardar tabla Q")
        learner.SaveQvalues()
