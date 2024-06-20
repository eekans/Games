#note: don't forget to add paths for the images!!!!!!!!

#imports
import pygame, sys
from pygame.locals import *
import random, time

#initializing pygame
pygame.init()

#setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()

#initializing game screen
window_x = 400
window_y = 600

#initializing colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#setting up the display and name
pygame.display.set_caption('Racer')
game_window = pygame.display.set_mode((window_x, window_y))
game_window.fill(WHITE)

#initializing important variables
SPEED = 5
SCORE = 0
POINTS = 0
COINS_COLLECTED = 0
COINS_GOAL = 3

#setting up Fonts
font = pygame.font.SysFont("Eras Demi ITC", 50)
font_small = pygame.font.SysFont("Times new roman", 20)
game_over = font.render("GAME OVER...", True, BLACK)

#loading background
background = pygame.image.load() #PATH NEEDED

#creating ENEMY class
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__()
        self.image = pygame.image.load() #PATH NEEDED!!!!
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, window_x - 40), 0)

      def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, window_x  - 40), 0)

#creating PLAYER class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load() #PATH NEEDED!!!!
        self.rect = self.image.get_rect()
        self.rect.center = (160, 540)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < window_x:
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)

#creating COIN class and its subclasses to create diff coins
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = None
        self.rect = None
        self.points = None

    def spawn(self):
        pass

class BasicCoin(Coin):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load() #PATH NEEDED!!!!
        self.rect = self.image.get_rect()
        self.points = 1

    def spawn(self):
        self.rect.centerx = random.randint(40, window_x - 40)
        self.rect.centery = 540

class SuperCoin(Coin):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load() #PATH NEEDED!!!!
        self.rect = self.image.get_rect()
        self.points = 3

    def spawn(self):
        self.rect.centerx = random.randint(40, window_x - 40)
        self.rect.centery = 540

class BestCoin(Coin):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load() #PATH NEEDED!!!!
        self.rect = self.image.get_rect()
        self.points = 5

    def spawn(self):
        self.rect.centerx = random.randint(40, window_x - 40)
        self.rect.centery = 540

#setting up Sprites
P1 = Player()
E1 = Enemy()

#creating Sprites Groups
coins = pygame.sprite.Group()
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

#spawning a coin every 3 seconds
SPAWN_COIN = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_COIN, 3000)
#increasing enemy's speed everytime COINS_COLLECTED = n
INC_SPEED_ENEMY = pygame.USEREVENT + 1
#playing the background music
pygame.mixer.music.load() #PATH NEEDED!!!!
pygame.mixer.music.play(-1)

#game Loop
while True:
    #handling key events
    for event in pygame.event.get():
        if event.type == INC_SPEED_ENEMY and COINS_COLLECTED == COINS_GOAL:
              SPEED += 1
              COINS_GOAL = COINS_GOAL + 3 #increasing enemy's speed everytime we collect n coins
        if event.type == SPAWN_COIN:
            if len(coins) < 1: #spawning coins only when there are no coins on the road
                coin_type = random.choice([BasicCoin, SuperCoin, BestCoin])
                new_coin = coin_type()
                new_coin.spawn()
                coins.add(new_coin)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    #setting up the background and scores text
    game_window.blit(background, (0,0))
    scores = font_small.render("score: " + str(SCORE), True, BLACK)
    coins_scores = font_small.render("coins: " + str(COINS_COLLECTED), True, BLACK)
    points_scores = font_small.render("points: " + str(POINTS), True, BLACK)
    game_window.blit(scores, (5, 0))
    game_window.blit(points_scores, (5, 15))
    game_window.blit(coins_scores, (330, 0))

    #moving and re-drawing all Sprites
    for entity in all_sprites:
        game_window.blit(entity.image, entity.rect)
        entity.move()

    #handling enemy and player collision (game over situation)
    if pygame.sprite.spritecollideany(P1, enemies):
          pygame.mixer.music.stop()
          pygame.mixer.Sound().play() #PATH NEEDED!!!!
          time.sleep(0.5)

          game_window.fill(RED)
          game_window.blit(game_over, (30,250))

          pygame.display.update()
          for entity in all_sprites:
                entity.kill()
          time.sleep(3)
          pygame.quit()
          sys.exit()

    #picking up the coins"
    for coin in coins:
        if pygame.sprite.spritecollideany(P1, coins):
            pygame.mixer.Sound().play() #PATH NEEDED!!!!
            COINS_COLLECTED += 1
            POINTS += coin.points
            coin.kill() #deleting the coin to avoid "infinite coin" bug

    coins.draw(game_window)
    pygame.display.update()
    FramePerSec.tick(FPS)
