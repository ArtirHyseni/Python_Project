import pygame
import os
from enum import Enum
from options import *
from board import *

pygame.init()
pygame.display.set_caption("Pac-Man")

class Direction(Enum):
  Left  = 0
  Up    = 1
  Right = 2
  Down  = 3

class Axis(Enum):
  Horizontal = 0
  Vertical = 1

class Game:

  def __init__(self):

    #The frame/window size of the game
    self.frame = pygame.display.set_mode((frame_width, frame_height))

    #Background color of the game
    self.frame.fill(black)

    #self.timer = pygame.time.Clock()
    #self.vec = pygame.math.Vector2[vec_x][vec_y]
    
    #Reads in board.txt and creates tile objects out of class Board
    #which creates a 2D vector when constructed
    self.tile = []
    with open("board.txt", "r") as f:
        f_text = f.read().replace('\n','')
        f_text.replace('\n','')
        for i, c in enumerate(f_text):
          if c == '@':
            self.playerPosition = i
            c = ' '
          self.tile.append(Board(c, i))

    self.tile[self.playerPosition].player = True

    #The directional variable(s) in which Pac-Man moves each update
    self.currentDirection = Direction.Left
    self.currentAxis = Axis.Horizontal

    #Counter which buffers Pac-Man's steps till reaching another index
    #Each index requires Pac-Man to walk 5 steps to reach the next; 3 is the middle
    self.playerCounter = 3

    self.active = True

  def start(self):

    while self.active:

      #Game's refresh/update rate in miliseconds
      pygame.time.delay(150)

      for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
          self.active = False

      #Listens to player_controller function; responsible for player movement automation 
      self.player_move()

      #Updates display to console
      self.console_display()
      
      self.draw()
      pygame.display.update()

    #pygame.Quit()
    #sys.exit()
  
  #Obtains player input from the keyboard arrow keys
  def player_controller(self):
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
      return Direction.Left
    elif keys[pygame.K_RIGHT]:
      return Direction.Right
    elif keys[pygame.K_UP]:
      return Direction.Up
    elif keys[pygame.K_DOWN]:
      return Direction.Down
    else:
      return self.currentDirection

  #Obtains the direction for Pac-Man to move from player input
  def get_tile_direction(self, dir : Direction):
    if dir == Direction.Left:
      return self.tile[self.playerPosition - 1]
    elif dir == Direction.Right:
      return self.tile[self.playerPosition + 1]
    elif dir == Direction.Up:
      return self.tile[self.playerPosition - vec_x]
    elif dir == Direction.Down:
      return self.tile[self.playerPosition + vec_x]

  #Obtains information regarding what axis Pac-Man is moving on
  def get_axis(self, dir : Direction):
    if dir == Direction.Left or dir == Direction.Right:
      return Axis.Horizontal
    else:
      return Axis.Vertical

  def player_move(self):

    #Obtains new directional information from player input
    nextDirection = self.player_controller()
    nextTile = self.get_tile_direction(nextDirection)
    nextAxis = self.get_axis(nextDirection)
    default = True

    #Checks if player attemps to change axis, otherwise defaults to previous state
    if self.currentAxis != nextAxis:
      if nextTile.passable and self.playerCounter == 3:
        default = False

      #Revert to previous state if attempt invalid
      else:
        nextDirection = self.currentDirection
        nextAxis = self.currentAxis
        nextTile = self.get_tile_direction(nextDirection)

    #Default condition; also checks if player changes direction on same axis
    if default:
      if nextDirection == Direction.Down or nextDirection == Direction.Right:
        if (not nextTile.passable and self.playerCounter < 3) \
        or (nextTile.passable and self.playerCounter < 5):
          self.playerCounter += 1

        elif nextTile.passable and self.playerCounter == 5:
          self.tile[self.playerPosition].player = False
          self.playerPosition = nextTile.position
          nextTile.player = True
          self.playerCounter = 1

      elif nextDirection == Direction.Up or nextDirection == Direction.Left:
        if (not nextTile.passable and self.playerCounter > 3) \
        or (nextTile.passable and self.playerCounter > 1):
          self.playerCounter -= 1
        
        elif nextTile.passable and self.playerCounter == 1:
          self.tile[self.playerPosition].player = False
          self.playerPosition = nextTile.position
          nextTile.player = True
          self.playerCounter = 5

    if self.tile[self.playerPosition].coin == True:
      self.tile[self.playerPosition].coin = False

    #Saves directional state for next update
    self.currentDirection = nextDirection
    self.currentAxis = nextAxis

  def draw(self):
    for i, tile in enumerate(self.tile):
      x = i % vec_x
      y = int(i / vec_x)

      if tile.passable and not tile.player:
        pygame.draw.rect(self.frame, black, pygame.Rect((x * tile_size, y * tile_size, tile_size, tile_size)))

        if tile.coin:
          pygame.draw.rect(self.frame, green, pygame.Rect((x * tile_size, y * tile_size, tile_size, tile_size)))
      
      elif tile.player:
        pygame.draw.rect(self.frame, yellow, pygame.Rect((x * tile_size, y * tile_size, tile_size, tile_size)))

      else:
        pygame.draw.rect(self.frame, blue, pygame.Rect((x * tile_size, y * tile_size, tile_size, tile_size)))
        
  def console_display(self):

    for tile in self.tile:
      tile.update()

    output = ""
    for i, tile in enumerate(self.tile):
      if i % vec_x == 0 and i != 0:
        output += "\n"
      output += tile.type
    os.system("clear")
    print(output)
    print("position: (%d, %d)" % (self.playerPosition % vec_x, int(self.playerPosition / vec_x)))
    print("Counter: ", self.playerCounter)
    print(self.currentDirection)
    print(self.currentAxis)
    print()
