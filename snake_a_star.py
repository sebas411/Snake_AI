# Juego de snake extraído de: https://www.edureka.co/blog/snake-game-with-pygame/

import pygame
import random

pygame.init()

YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (20, 13, 213)
RED = (255, 0, 0)


BLOCK_SIZE = 10 
DIS_WIDTH = 600
DIS_HEIGHT = 400

FRAMESPEED = 30

def DrawFood(foodx, foody):
    pygame.draw.rect(dis, RED, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])   

def DrawScore(score):
    font = pygame.font.SysFont("arial", 35)
    value = font.render(f"Score: {score}", True, BLACK)
    dis.blit(value, [0, 365])

def DrawSnake(snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, BLACK, [x[0], x[1], BLOCK_SIZE, BLOCK_SIZE])

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def a_star(food, snake):
    head_node = Node(position=snake[-1])
    head_node.g = head_node.h = head_node.f = 0
    food_node = Node(None, food)
    food_node.g = food_node.h = food_node.f = 0

    open_list = []
    closed_list = []
    open_list.append(head_node)

    while len(open_list) > 0:

        current_node = open_list[0]
        current_index = 0
        for index, node in enumerate(open_list):
            if node.f < current_node.f:
                current_node = node
                current_index = index
        
        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node == food_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_position = (current_node.position[0] + new_position[0]*BLOCK_SIZE, current_node.position[1] + new_position[1]*BLOCK_SIZE)
            if node_position[0] >= DIS_WIDTH or node_position[0] < 0 or node_position[1] >= DIS_HEIGHT or node_position[1] < 0:
                continue

            if node_position in snake:
                continue

            new_node = Node(current_node, node_position)

            children.append(new_node)

        for child in children:

            for closed_child in closed_list:
                if child == closed_child:
                    continue

            child.g = current_node.g + 1
            child.h = (((child.position[0] - food_node.position[0])/BLOCK_SIZE) ** 2) + (((child.position[1] - food_node.position[1])/BLOCK_SIZE) ** 2)
            child.f = child.g + child.h

            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            open_list.append(child)
    return -1

    

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

    path = a_star((foodx, foody), snake_list)

    while not dead:
        if not path:
            path = a_star((foodx, foody), snake_list)
        print(path[-1], (foodx, foody))
        nextpos = path.pop(0)
        action = "down"
        if nextpos[0] > x1: action = "right"
        elif nextpos[0] < x1: action = "left"
        elif nextpos[1] < y1: action = "up"

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

        
        clock.tick(FRAMESPEED)

    return length_of_snake - 1, reason



game_count = 1



while True:
    score, reason = GameLoop()
    print(f"No. iter: {game_count}; Puntaje: {score}; Error: {reason}") 
    game_count += 1
    
