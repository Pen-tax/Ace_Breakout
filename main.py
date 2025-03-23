## Breakout in Pygame
## importing nessisary libraries
from operator import itemgetter
import pygame, sys, math, random, json
from pygame.locals import QUIT
from pygame import freetype
from matplotlib.patches import Rectangle
## Simple colour values
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
orange = (200, 100, 0)
yellow = (200, 200, 0)
green = (0, 200, 0)
purple = (200, 0, 200)
## Images and art
Title_art = pygame.image.load("images/acebreakout_art.png")
Main_title = pygame.image.load("images/acebreakout_main.png")
controls = pygame.image.load("images/acebreakoutcontrols.png")
high_src = pygame.image.load("images/acebreakout_High.png")
## sfx
pygame.mixer.init()
Paddle1_hit = pygame.mixer.Sound("Sounds/blip.wav")
Paddle1_bounce = pygame.mixer.Sound("Sounds/bounce.wav")
Paddle2_bounce = pygame.mixer.Sound("Sounds/blunk.wav")
Destroyed = pygame.mixer.Sound("Sounds/bwah.wav")
proceed = pygame.mixer.Sound("Sounds/game_enter.wav")
music = pygame.mixer.Sound("Sounds/Menu_M.wav")
## sfx methods allows output
def Menu_Music():
  pygame.mixer.Sound.play(music)
  pygame.mixer.music.stop()  
def Hit1():
  pygame.mixer.Sound.play(Paddle1_hit)
  pygame.mixer.music.stop()
def bounce1():
  pygame.mixer.Sound.play(Paddle1_bounce)
  pygame.mixer.music.stop()
def bounce2():
  pygame.mixer.Sound.play(Paddle2_bounce)
  pygame.mixer.music.stop()
def brick_b():
  pygame.mixer.Sound.play(Destroyed)
  pygame.mixer.music.stop()
def enter():
  pygame.mixer.Sound.play(proceed)
  pygame.mixer.music.stop()
  
## State machine
game_state = "Title_Art"
## Game window settings
pygame.init()
display = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Ace Breakout')
## game window values + boarder values
Top = 480
Bottom = 0
Left = 0
Right = 640
middle_1 = 270
middle_2 = 370

## fonts
font = pygame.font.Font('Gamer.ttf', 30)

## method to add text in game
def text(text, font, text_colour, x, y):
  img = font.render(text, True, text_colour)
  display.blit(img, (x, y))


##game Variables
p1_score = 0
p2_score = 0
p1_Lives = 4
p2_Lives = 4
Level = 1
## allows ball to stop and reset
global ballserve
ballserve = False

## game framerate
frames = pygame.time.Clock()
vec = pygame.math.Vector2
fps = 60


## player boundries
def Player_1_Bound():
  display.fill(black)
  pygame.draw.line(display, white, (0, Top - 410), (Right, Top - 410), 10)
  pygame.draw.line(display, white, (0, Top - 50), (Right, Top - 50), 10)
  pygame.draw.line(display, white, (Right - 2, 0), (Right - 2, Top), 10)
  pygame.draw.line(display, white, (Left + 2, 0), (Left + 2, Top), 10)

  text("Score: " + str(p1_score), font, white, 20, 15)
  text("Level: " + str(Level), font, white, 200, 15)
  text("Ace_Breakout", font, white, 20, 450)
  text("Lives: " + str(p1_Lives), font, white, 500, 15)
## Two player boundries
def Player_2_Bound():
  display.fill(black)
  pygame.draw.line(display, white, (0, Top - 480), (Right, Top - 480), 10)
  #pygame.draw.line(display, white, (0, Top - 50), (Right, Top - 50), 10)
  pygame.draw.line(display, white, (Right - 2, 0), (Right - 2, Top), 10)
  pygame.draw.line(display, white, (Right - 270, 0), (Right - 270, Top), 10)
  pygame.draw.line(display, white, (Left + 2, 0), (Left + 2, Top), 10)
  pygame.draw.line(display, white, (Left + 270, 0), (Left + 270, Top), 10)

  text("Score", font, red, 290, 30)
  text(str(p1_score) + " : ", font, white, 295, 60)
  text(str(p2_score), font, white, 330, 60)
  text("Ace_Breakout", font, white, 20, 450)
  text("Lives", font, red, 290, 100)
  text(str(p1_Lives) + " : ", font, white, 295, 130)
  text(str(p2_Lives), font, white, 325, 130)
  
  
## main paddle
class paddle1:

  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.rect = pygame.Rect(x, y, 100, 20)
    ## controls
    ## single player paddle
  def P1_Move(self):
    key = pygame.key.get_pressed()
    if key[pygame.K_a] and self.rect.left >= 5:
      self.rect.move_ip(-5, 0)
    if key[pygame.K_d] and self.rect.right < 635:
      self.rect.move_ip(5, 0)
      ## allows to move paddle upwards a bit to hit ball
    if key[pygame.K_w] and self.rect.y == 400:
      self.rect.move_ip(0, -5)
## player 1 for two player movement
  def Player1_Move(self):
    key = pygame.key.get_pressed()
    if key[pygame.K_a] and self.rect.left >= 5:
      self.rect.move_ip(-5, 0)
    if key[pygame.K_d] and self.rect.right < 270:
      self.rect.move_ip(5, 0)
      ## allows to move paddle upwards a bit
    if key[pygame.K_w] and self.rect.y == 400:
      self.rect.move_ip(0, -5)

## player 2 for two player movement
  def Player2_Move(self):
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and self.rect.left >= 375:
      self.rect.move_ip(-5, 0)
    if key[pygame.K_RIGHT] and self.rect.right < 635:
      self.rect.move_ip(5, 0)
      ## allows to move paddle upwards a bit to hit ball
    if key[pygame.K_UP] and self.rect.y == 400:
      self.rect.move_ip(0, -5)
## Resets position of paddle after losing life
  def reset(self, x, y):
    self.x = x
    self.y = y
    self.rect = pygame.Rect(x, y, 100, 20)
      
## paddle display

  def main(self):
    pygame.draw.rect(display, white, self.rect)


## ball class
class ball:

  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.rect = pygame.Rect(x, y, 10, 10)
    self.velocity = [random.randint(2,3), random.randint(-3,3)]
## Ball collision values
  def main(self):
    global ballserve
    global p1_Lives
    pygame.draw.rect(display, (255,255,255), self.rect)
    self.rect.x += self.velocity[0]
    self.rect.y += self.velocity[1]
   # if ball.rect.x>=800:
        #ball.velocity[0] = -ball.velocity[0]
    #if ball.rect.x<=0:
        #ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x>= Right - 10:
      ball.velocity[0] = -ball.velocity[0]
      Hit1()
    if ball.rect.x<= Left:
      ball.velocity[0] = -ball.velocity[0]
      Hit1()
    #if ball.rect.top> 410:
        #ball.velocity[1] = -ball.velocity[1]
    if ball.rect.bottom< 70:
        ball.velocity[1] = -ball.velocity[1]
        Hit1()
    ## bounces balls off paddles
    if self.rect.colliderect(player):
      self.velocity[0] = -self.velocity[0]
      self.velocity[1] = random.randint(-3,-1)
      bounce1()
    ## Player fail state
    if self.rect.top> 410:
      ballserve = False
      p1_Lives = p1_Lives - 1
    ## resets ball when player loses life  
  def reset(self, x, y):
    self.x = x
    self.y = y
    self.rect = pygame.Rect(x, y, 10, 10)
    self.velocity = [random.randint(3, 3), random.randint(-3, 3)]
## two player mode ball class
class ball2:

  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.rect = pygame.Rect(x, y, 10, 10)
    self.velocity = [random.randint(2, 3), random.randint(-3, 3)]
## first player boundaries collision
  def main1(self):
    global ballserve
    global p1_Lives
    pygame.draw.rect(display, (255,255,255), self.rect)
    self.rect.x += self.velocity[0]
    self.rect.y += self.velocity[1]
   # if ball.rect.x>=800:
        #ball.velocity[0] = -ball.velocity[0]
    #if ball.rect.x<=0:
        #ball.velocity[0] = -ball.velocity[0]
    if ball_p1.rect.right>= middle_1 - 10:
        ball_p1.velocity[0] = random.randint(-3,-1)
        Hit1()
    if ball_p1.rect.left<= Left:
        ball_p1.velocity[0] = -ball_p1.velocity[0]
        Hit1()
    #if ball.rect.top> 410:
        #ball.velocity[1] = -ball.velocity[1]
    if ball_p1.rect.bottom< 10:
        ball_p1.velocity[1] = -ball_p1.velocity[1]
        Hit1()
    ## bounces balls off paddles
    if self.rect.colliderect(player1):
      self.velocity[0] = -self.velocity[0]
      self.velocity[1] = random.randint(-3,-1)
      bounce1()
    
    if self.rect.top> 410:
      ballserve = False
      p1_Lives = p1_Lives - 1
  ## second player boundaries collision
  def main2(self):
    global ballserve
    global p2_Lives
    pygame.draw.rect(display, (255,255,255), self.rect)
    self.rect.x += self.velocity[0]
    self.rect.y += self.velocity[1]
   # if ball.rect.x>=800:
        #ball.velocity[0] = -ball.velocity[0]
    #if ball.rect.x<=0:
        #ball.velocity[0] = -ball.velocity[0]
    if ball_p2.rect.right>= Right - 5:
        ball_p2.velocity[0] = random.randint(-3,-1)
        Hit1()
    if ball_p2.rect.left<= middle_2 + 5:
        ball_p2.velocity[0] = -ball_p2.velocity[0]
        Hit1()
    #if ball.rect.top> 410:
        #ball.velocity[1] = -ball.velocity[1]
    if ball_p2.rect.bottom< 50:
        ball_p2.velocity[1] = -ball_p1.velocity[1]
        Hit1()
    ## bounces balls off paddles
    if self.rect.colliderect(player2):
      self.velocity[0] = -self.velocity[0]
      self.velocity[1] = random.randint(-3,-1)
      bounce2()
      
    ## ends game when hitting the bottom
    if self.rect.top> 410:
      ballserve = False
      p2_Lives = p2_Lives - 1
   ## Resets ball when player loses life   
  def reset(self, x, y):
    self.x = x
    self.y = y
    self.rect = pygame.Rect(x, y, 10, 10)
    self.velocity = [random.randint(3, 3), random.randint(-3, 3)]


  


    
## brick class
class Brick(pygame.sprite.Sprite):
  def __init__(self, color, width, height):
    super().__init__()
    self.image = pygame.Surface([width, height])
    self.image.fill(black)
    self.image.set_colorkey(black)
    pygame.draw.rect(self.image, color, [0, 0, width, height])
    self.rect = self.image.get_rect()



## creates sprites for bricks
all_sprites_list = pygame.sprite.Group()

all_bricks = pygame.sprite.Group()
## Adds in bricks
if Level == 1:
  for i in range(6):
        brick = Brick(red,95,15)
        brick.rect.x = 20 + i* 100
        brick.rect.y = 80
        all_sprites_list.add(brick)
        all_bricks.add(brick)
  for i in range(6):
        brick = Brick(blue,95,15)
        brick.rect.x = 20 + i* 100
        brick.rect.y = 100
        all_sprites_list.add(brick)
        all_bricks.add(brick)
  for i in range(6):
        brick = Brick(green,95,15)
        brick.rect.x = 20 + i* 100
        brick.rect.y = 120
        all_sprites_list.add(brick)
        all_bricks.add(brick)
  for i in range(6):
        brick = Brick(orange,95,15)
        brick.rect.x = 20 + i* 100
        brick.rect.y = 140
        all_sprites_list.add(brick)
        all_bricks.add(brick)
## adding in extra levels (not finished)
if Level == 2:
  for i in range(3):
        brick = Brick(red,95,15)
        brick.rect.x = 20 + i* 100
        brick.rect.y = 80
        all_sprites_list.add(brick)
        all_bricks.add(brick)
  for i in range(6):
        brick = Brick(blue,95,15)
        brick.rect.x = 20 + i* 100
        brick.rect.y = 100
        all_sprites_list.add(brick)
        all_bricks.add(brick)
  for i in range(6):
        brick = Brick(green,95,15)
        brick.rect.x = 20 + i* 100
        brick.rect.y = 120
        all_sprites_list.add(brick)
        all_bricks.add(brick)
  for i in range(3):
        brick = Brick(orange,95,15)
        brick.rect.x = 20 + i* 100
        brick.rect.y = 140
        all_sprites_list.add(brick)
        all_bricks.add(brick)
  
## brick class 2

    
## Turning classes into variables
player = paddle1(300, 400)
ball = ball(310, 390)
##2 player mode
player1 = paddle1(100, 400)
player2 = paddle1(420,400)

ball_p1 = ball2(110,390)
ball_p2 = ball2(430,390)

## title art code (first thing you see)
while game_state == "Title_Art":
  display.blit(Title_art, (0, 0))
  pygame.mixer.music.load("Sounds/Menu_M.wav")
  pygame.mixer.music.play(-1)
  keys = pygame.key.get_pressed()
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
## enters main screen
  if keys[pygame.K_RETURN]:
    enter()
    game_state = "Title"
    ## exit game
  if keys[pygame.K_ESCAPE]:
    sys.exit()
    pygame.QUIT
  pygame.display.update()

## main title screen
while game_state == "Title":
  pygame.mixer.music.stop()
  keys = pygame.key.get_pressed()
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
  display.blit(Main_title, (0, 0))
## changes the game state to the specified option
  if keys[pygame.K_1]:
    game_state = "Single_Player"
    enter()
  if keys[pygame.K_2]:
    game_state = "Two_Player"
    enter()
  if keys[pygame.K_3]:
    game_state = "Controls"
    enter()
  if keys[pygame.K_4]:
    game_state = "High_Score"
    enter()
  if keys[pygame.K_ESCAPE]:
    sys.exit()
    pygame.QUIT

  pygame.display.update()

## Single player mode
while game_state == "Single_Player":
  frames.tick(fps)
  keys = pygame.key.get_pressed()
  Player_1_Bound()
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
  if keys[pygame.K_ESCAPE]:
    sys.exit()
    pygame.QUIT
## spawns in ball and player when pressing space
  if keys[pygame.K_SPACE]:
    ballserve = True
  ##paddle
  player.main()
  ## stops and starts new game session
  if ballserve == True:
    player.P1_Move()
    ## ball
    ball.main()
  if keys[pygame.K_SPACE] and ballserve == False:
    ballserve = False
    ball.reset(310, 390)
    player.reset(300,400)

## ball
# ball.main()
  
## text for when player starts
  if ballserve == False:
    text("Press Space to start", font, red, 220, 330)
## game over conditions
  if p1_Lives < 0:
    game_state = "High_Score"
  if p1_score == 24:
    game_state = "High_Score"
## adds bricks
  brick_collision_list = pygame.sprite.spritecollide(ball,all_bricks,False)
  for brick in brick_collision_list:
    ball.velocity[1] = -ball.velocity[1]
    brick.kill()
    brick_b()
    p1_score = p1_score + 1
    if len(all_bricks)==0:
      Level = Level + 1
      ballserve = False
      all_sprites_list.draw(display)
  
  all_sprites_list.draw(display)


  pygame.display.update()

  

## Two player 1v1 mode
while game_state == "Two_Player":
  frames.tick(fps)
  keys = pygame.key.get_pressed()
  Player_2_Bound()
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
  if keys[pygame.K_ESCAPE]:
    sys.exit()
    pygame.QUIT

  ##paddles spawn in when players press space
  if keys[pygame.K_SPACE]:
    ballserve = True
  ##paddle
  player1.main()
  player2.main()
  ## stops and starts new game session
  if ballserve == True:
    player1.Player1_Move()
    player2.Player2_Move()
    ## ball spawing 
    ball_p1.main1()
    ball_p2.main2()
    ## Resets when someone loses a life
  if keys[pygame.K_SPACE] and ballserve == False:
    ballserve = False
    ball_p1.reset(110, 390)
    ball_p2.reset(430,400)
    player1.reset(100,400)
    player2.reset(420,400)

## ball
# ball.main()
  
## text for when player starts
  if ballserve == False:
    text("Press Space to start", font, red, 220, 330)

  if Level == 2:
    ballserve = False
## adds in bricks and collsision for player 1
  brick_collision_list = pygame.sprite.spritecollide(ball_p1,all_bricks,False)
  for brick in brick_collision_list:
    ball_p1.velocity[1] = -ball_p1.velocity[1]
    brick.kill()
    brick_b()
    p1_score = p1_score + 1
    if len(all_bricks)==0:
      Level = Level + 1
## collision for player two allows for them to score
  brick_collision_list = pygame.sprite.spritecollide(ball_p2,all_bricks,False)
  for brick in brick_collision_list:
    ball_p2.velocity[1] = -ball_p2.velocity[1]
    brick.kill()
    brick_b()
    p2_score = p2_score + 1
    if len(all_bricks)==0:
      Level = Level + 1
  
  all_sprites_list.draw(display)
## When player 1 loses all lives player 2 wins
  if p1_Lives == 0:
    text("Player 2 Wins!", font, red, 220, 330)
    pygame.time.delay(10000)
    game_state = "High_Score2"
## When player 2 loses all lives player 1 wins
  if p2_Lives == 0:
    text("Player 1 Wins!", font, red, 220, 330)
    game_state = "High_Score2"
## player 1 gets all bricks
  if p1_score == 12:
    text("Player 1 Wins!", font, red, 220, 330)
    game_state = "High_Score2"
## player 2 gets all bricks
  if p2_score == 12:
    text("Player 2 Wins!", font, red, 220, 330)
    game_state = "High_Score2"

  pygame.display.update()

## Controls screen
while game_state == "Controls":
  keys = pygame.key.get_pressed()
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
  display.blit(controls, (0, 0))
  ## Supposed to change the game state again (currently not working)
  if keys[pygame.K_RETURN]:
    game_state = "Title"
  if keys[pygame.K_ESCAPE]:
    sys.exit()
    pygame.QUIT

    

  pygame.display.update()

## High score screens
FONT = freetype.Font(None, 24)
  
while game_state == "High_Score":
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
      ## High score background
  display.blit(high_src, (0, 0))
## opens text file and reads values
  try:
    with open('highscore.txt', 'r') as f:
        highscores = json.load(f)
  except FileNotFoundError:
    # If the file doesn't exist, use your default values
    highscores = [
        ('Isa', 20),
        ('Dalip', 14),
        ('Andrew', 5),
        ]

## orders high scores in order of score
  highscores = sorted(highscores, key = itemgetter(1), reverse = True)[:10]

  with open('highscore.txt', 'w') as f:
    json.dump(highscores, f)

  highscores = []
  ## Allows to display high scores
  def load():
    try:
        with open('highscore.txt', 'r') as file:
            highscores = json.load(file)  # Read the json file.
            playerName = "Your Score:"#input("what is your name? ")
            playerScore = p1_score
            highscores.append((playerName, playerScore))
    except FileNotFoundError:
      highscores = [
        ('Isa', 20),
        ('Dalip', 14),
        ('Andrew', 5),
        ]
    return sorted(highscores, key = itemgetter(1), reverse = True)[:8]
  
  highscore = load()
  ## Shows high score in list
  for y, (hi_name, hi_score) in enumerate(highscore):
    FONT.render_to(display, (240, y*50+100), f'{hi_name} {hi_score}', white)
  #text("Your Score: " + str(p1_score), font, red, 400, 200)
  
  pygame.display.update()

## High score system for two player mode
while game_state == "High_Score2":
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
      ## High score background
  display.blit(high_src, (0, 0))
  text("Player 1 Score: " + str(p1_score), font, white, 200, 100)
  text("Player 2 Score: " + str(p2_score), font, white, 200, 200)
  ## Different win condtions -- Shows who wins depending on score
  if p1_score > p2_score:
    text("Player 1 Wins!", font, red, 220, 250)
  if p1_score < p2_score:
    text("Player 2 Wins!", font, red, 220, 250)
  if p1_score == p2_score and p1_score > 0:
    text("Draw!", font, red, 230, 250)
  
  pygame.display.update()
