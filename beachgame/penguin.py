# import the random library, to set the initial position of the rock.
import random

# Set the size of the window
WIDTH = 600
HEIGHT = 500

# Calculate the centre of the screen, to avoid doing so several
# times later on
centre_x = WIDTH/2
centre_y = HEIGHT/2

# The score
score = 0


# are the friends together
together = False

# Create the actors
penguin = Actor('penguin2')    # The penguin actor
cow = Actor('cow')    # The cow actor
ball = Actor('ball') # The ball actor

ball_vx = 0
ball_vy = 0


def startPositions():
  #print('start posns now')
  global cow
  global penguin
  global ball
  global ball_vx
  global ball_vy
  global score
  global topScore
  global together
  
  penguin.image = 'penguin2'
  cow.image = 'cow'
  penguin.pos = 35, 350  # The initial position of the penguin
  cow.pos = 550, 370  # The initial position of the cow
  ball.pos = 0, HEIGHT*2  # off screen
  ball_vx = 0
  ball_vy = 0
  score = 0
  topScore = 0
  together = False
  

# Starting settings for the game
gameOver = False # The game has not finished yet
startPositions() # Set the initial positions of the spacecraft and rock


def newBallPos():
  return  random.randint(0,WIDTH), -50  # off screen

def newBallVel():
  return  (random.randint(-2,2),  (random.randint(2,4) ) ) # off screen

def on_key_down(key):
  if key == keys.SPACE:
    set_penguin_jump()
    

def set_penguin_jump():
    sounds.karate.play()
    animate(penguin, tween='decelerate', duration=1,pos=(penguin.x, penguin.y - 100))
    clock.schedule_unique(set_penguin_normal, 1.0)


def set_penguin_normal():
    animate(penguin, tween='bounce_end', duration=1.0,pos=(penguin.x, penguin.y + 100))
 
    


# ---------------------------------------
# The draw function
def draw():
  screen.clear()
  screen.blit('beach2', (0,0))
  
  penguin.draw()
  cow.draw()  
  ball.draw()

   # Draw the score information at the bottom of the screen.
  screen.draw.text("Cones delivered: "+str(score), center=(centre_x-100, HEIGHT-10.))
 
  # Check to see if the game is over
  if gameOver:
    # If the game is over, then print a series of red rectangles
    # with a text message.
    for i in range(20,-5,-5):
      screen.draw.filled_rect(Rect((centre_x-(100+i), centre_y-(30+i)), (200+(i*2), 80+(i*2))), (200-(i*8), 0, 0))
    screen.draw.text("GAME OVER!", center=(centre_x, centre_y))
    screen.draw.text("(n to restart)", center=(centre_x, centre_y+20))

def resetPositions():
  global together
  penguin.image = 'penguin2'
  cow.image = 'cow'
  penguin.pos = 35, 350  # The initial position of the penguin
  together = False
  (ball.x, ball.y) = newBallPos()
  (ball_vx, ball_vy) = newBallVel()


def updatePenguin():
  global penguin
  # If the cursor keys are pressed, then move the
  # penguin left and right within the screen.
  if keyboard.left and penguin.left > 2:
    penguin.x -= 2
  if keyboard.right and penguin.right < WIDTH+2:
    penguin.x += 2

def updateBall():
  ##print("ball top: " + str(ball.top))
  ##print("ball bot: " + str(ball.bottom))
  global ball
  global ball_vx
  global ball_vy
  
  if ball.top > HEIGHT or ball.right < 0 or ball.left > WIDTH:
   # print("off screen")
    (ball.x, ball.y) = newBallPos()
    (ball_vx, ball_vy) = newBallVel()

  ball.y = ball.y + ball_vy
  ball.x = ball.x + ball_vx
  ball.draw()


# ---------------------------------------
# The update function
def update():
  global gameOver
  global score
  global topScore
  global together
  global moo_effect
  global pow_effect

##  print("Together is: " + str(together))
  if not gameOver:
    updateBall()
    updatePenguin()
  else:
    # If the game is over, test to see if the n key has been pressed.
    # If it has been pressed, reset the positions of the spracecraft and
    # rock and restart the game.
    if keyboard.n:
      startPositions()
      gameOver = False

  cow_collision = cow.colliderect(ball)
  penguin_collision = penguin.colliderect(ball)
  friend_collision = penguin.colliderect(cow)

  if penguin_collision:
    penguin.image = 'pow'
    sounds.pow.play()      # sound of penguin exploding 
    ball.pos = 0, HEIGHT*2  # off screen
    gameOver = True

  if friend_collision:
    if not together:
      cow.image = 'cowlove'
      sounds.moo.play()   #  cow moos when it gets an ice cream
      score += 1
      together = True
      clock.schedule(resetPositions, 0.5)
      
    


  
    
    
    

  

  
  
