import pygame
import random
import time

#loading pygame
pygame.init()

#initializing game screen
window_x = 750
window_y = 750

#initializing colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
yellow = pygame.Color(255, 255, 0)
lightblue = pygame.Color(46,224,230)
lightred = pygame.Color(255, 95, 95)

#setting up the display and name
pygame.display.set_caption('Snake')
game_window = pygame.display.set_mode((window_x, window_y))

#initializing important variables
score = 0
level = 1
next_level_goal = 1
fps = pygame.time.Clock()

#initializing snake-related variables
snake_speed = 9
snake_position = [100, 50] #fixed starting position
snake_body = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]
              ] #creating snake body

#initializing fruit-related variables
fruit_position = [random.randrange(1, (window_x//10)) * 10,
                  random.randrange(1, (window_y//10)) * 10] #random position
fruit_spawn = False #setting false for fruit generration AFTER loading the game
fruit_color = None
fruit_points = 0
fruit_time = 0
fruits_collected = 0

#setting the default direction to right
direction = 'RIGHT'
change_to = direction

#.......initializing game functions:

#1 - setting score text
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score: ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface, score_rect)

#2 - setting level info
def show_level(choice, color, font, size):
    global snake_speed, level
    level_font = pygame.font.SysFont('times new roman', size)
    level_surface = level_font.render('Level: ' + str(level), True, color)
    level_rect = level_surface.get_rect()
    level_rect.bottomleft = (0, 40)
    game_window.blit(level_surface, level_rect)

#3 - setting the conditions of the next level
def next_level():
    global snake_speed, level
    snake_speed += 2
    level += 1

#4 - getting the fruit type
def get_fruit():
    global fruit_color, fruit_points, fruit_time
    x = random.randint(1,10)
    if x == 10:
        fruit_points = 5
        fruit_color = yellow
        fruit_time = 4
    elif 7 <= x <= 9:
        fruit_points = 3
        fruit_color = red
        fruit_time = 7
    else:
        fruit_points = 1
        fruit_color = white
        fruit_time = 10

#5 - game over activation
def game_over():
    #score text
    my_font_s = pygame.font.SysFont('times new roman', 50)
    game_over_surface_s = my_font_s.render('Your Score is: ' + str(score), True, red)
    game_over_rect_s = game_over_surface_s.get_rect()
    game_over_rect_s.midtop = (window_x/2, window_y/4)
    game_window.blit(game_over_surface_s, game_over_rect_s)
    #level text
    my_font_l = pygame.font.SysFont('times new roman', 30)
    game_over_surface_l = my_font_l.render('Your Level is: ' + str(level), True, lightred)
    game_over_rect_l = game_over_surface_l.get_rect()
    game_over_rect_l.midtop = (window_x/2, window_y/4 + 50)
    game_window.blit(game_over_surface_l, game_over_rect_l)
    #refreshing the display to print out the text
    pygame.display.flip()
    time.sleep(4) #waiting 4 seconds before quitting
    pygame.quit()
    quit()

FRUIT_TIMER_EXPIRED = pygame.USEREVENT + 1
done = False

while not done:
    #handling key events
    for event in pygame.event.get():
        #quitting the game
        if event.type == pygame.QUIT:
            done = True
        #pressing the keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
        if event.type == FRUIT_TIMER_EXPIRED:
            fruit_spawn = False

    #changing direction
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    #moving the snake
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    #when do we get to the next level?
    if fruits_collected == next_level_goal:
        next_level()
        fruits_collected = 0
        next_level_goal += 1

    #eating the fruit
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += fruit_points
        fruits_collected += 1
        fruit_spawn = False
    else:
        snake_body.pop()

    #spawning the fruit if its not there
    if not fruit_spawn:
        get_fruit()
        fruit_position = [random.randrange(1, (window_x//10)) * 10,
                          random.randrange(1, (window_y//10)) * 10]
        pygame.time.set_timer(FRUIT_TIMER_EXPIRED, 10000)
    fruit_spawn = True

    game_window.fill(black)

    #drawing fruit and snake
    for pos in snake_body: #drawing rectangles according to the list
        pygame.draw.rect(game_window, lightblue, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, fruit_color, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

    #touching the walls
    if snake_position[0] < 0 or snake_position[0] > window_x-10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_y-10:
        game_over()

    #touching the snake's body
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    #showing the score and level
    show_score(1, white, 'times new roman', 20)
    show_level(1, white, 'times new roman', 20)

    pygame.display.flip()
    fps.tick(snake_speed)
