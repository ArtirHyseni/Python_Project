import pygame
import os
from enum import Enum
from options import *
from board import *
from Python_Project.Base.ghost import *

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

    # create ghost list
    self.ghost_list = [
                       ghost(name="blinky"),
                       ghost(name="pinky"),
                       ghost(name="inky"),
                       ghost(name="clyde") ]

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
          # if ghost is present,change its attribute's accordingly
          elif c in ['B', 'P', 'I', 'C']:
            if c == 'B': index = get_index(self.ghost_list, "blinky")
            elif c == 'P': index = get_index(self.ghost_list, "pinky")
            elif c == 'I': index = get_index(self.ghost_list, "inky")
            else: index = get_index(self.ghost_list, "clyde")
            self.ghost_list[index].active = 1
            self.ghost_list[index].init_ghost_pos(i)

          self.tile.append(Board(c,i))
    self.tile[self.playerPosition].player = True

    #The directional variable(s) in which Pac-Man moves each update
    self.currentDirection = Direction.Left
    self.currentAxis = Axis.Horizontal

    #Counter which buffers Pac-Man's steps till reaching another index
    #Each index requires Pac-Man to walk 5 steps to reach the next; 3 is the middle
    self.playerCounter = 3

    self.active = True

    # initialize active ghosts' first mode to chase
    # FIXME, change this back to chase (instead of scatter)
    set_all_modes(get_actives(self.ghost_list), ghost_mode.scatter)

  def start(self):

    while self.active:

      #Game's refresh/update rate in miliseconds
      pygame.time.delay(150)

      for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
          self.active = False

      #Listens to player_controller function; responsible for player movement automation 
      self.player_move()

      #After player has been moved, update coordinates in ghost objects
      self.ghosts_move()

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

  def ghosts_move(self):

    # targets of ghosts *may* be dependent on player
    set_all_targets(get_actives(self.ghost_list), self.playerPosition, self)
    # set values for ghosts' direction and pos based on targets
    # this will be updating only the data held within the ghosts themselves, not the board
    set_all_dirs_pos(get_actives(self.ghost_list), self)

  def draw(self):
    for i, tile in enumerate(self.tile):
      x = i % vec_x
      y = int(i / vec_x)

      if tile.passable and not tile.player:
        pygame.draw.rect(self.frame, black, pygame.Rect((x * tile_size, y * tile_size, tile_size, tile_size)))

        if tile.coin:
          pygame.draw.rect(self.frame, green, pygame.Rect((x * tile_size, y * tile_size, tile_size, tile_size)))

        elif tile.enemy:
          if tile.type == 'B':
            pygame.draw.rect(self.frame, red, pygame.Rect((x * tile_size, y * tile_size, tile_size, tile_size)))
          elif tile.type == 'P':
            pygame.draw.rect(self.frame, pink, pygame.Rect((x * tile_size, y * tile_size, tile_size, tile_size)))
          elif tile.type == 'I':
            pygame.draw.rect(self.frame, aqua, pygame.Rect((x * tile_size, y * tile_size, tile_size, tile_size)))
          else:
            pygame.draw.rect(self.frame, olive, pygame.Rect((x * tile_size, y * tile_size, tile_size, tile_size)))

      elif tile.player:
        pygame.draw.rect(self.frame, yellow, pygame.Rect((x * tile_size, y * tile_size, tile_size, tile_size)))

      else:
        pygame.draw.rect(self.frame, blue, pygame.Rect((x * tile_size, y * tile_size, tile_size, tile_size)))
        
  def console_display(self):

    for tile in self.tile:
      tile.update()

    self.update_ghost_tiles()

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

  def update_ghost_tiles(self): # FIXME, need to think about ways this could break
    # delete the old ghost locations
    for ghost in get_actives(self.ghost_list):
      if self.tile[ghost.prevpos].type == '@': # don't overwrite player
        self.tile[ghost.prevpos].enemy = False
      elif self.tile[ghost.prevpos].type == 'o': # don't make coins disappear? FIXME weird but it works?
        self.tile[ghost.prevpos].enemy = False   # need to store what the tile had been prior to the ghost
      elif self.tile[ghost.prevpos].type in ['B','P','I','C']:
        continue
      else:
        self.tile[ghost.prevpos].type = ' '
        self.tile[ghost.prevpos].enemy = False

    # mark the new locations of ghosts on the board
    for ghost in get_actives(self.ghost_list):
      if ghost.name == 'blinky': char = 'B'
      elif ghost.name == 'pinky': char = 'P'
      elif ghost.name == 'inky': char = 'I'
      else: char = 'C'
      self.tile[ghost.pos].type = char
      self.tile[ghost.pos].enemy = True

  # give index of corner specified in string "position"
  # a bit verbose, but if we keep board text files in same format,
  # this should remain flexible
  def get_corner(self, position):
    if position == corner.top_left:
      for tile in self.tile[::]:
        if tile.type != "#": return tile.position

    elif position == corner.top_right:
      start = self.get_corner(corner.top_left)
      for tile in self.tile[start::]:
        if tile.type == "#": return tile.position - 1

    elif position == corner.bottom_left:
      start = self.get_corner(corner.bottom_right)
      for tile in self.tile[start::-1]:
        if tile.type == "#": return tile.position + 1

    else:
      for tile in self.tile[::-1]:
        if tile.type != "#": return tile.position
