import pygame
import os
import images
import time
from options import *
from board import *
from ghost import *
from status import *
from gameOver import *
from random import randint

pygame.init()
pygame.display.set_caption("Pac-Man")

class Game:

	def __init__(self):

		#The frame/window size of the game
		self.frame = pygame.display.set_mode((frame_width, frame_height))

		#Background color of the game
		self.frame.fill(black)

		#List to create 2D vector for levels
		self.tile = []

		#Game's refresh/update rate in miliseconds
		pygame.time.delay(25)

		
		#change colors each level
		self.levelColors = [olive, darkgreen, medGray, black]
		
		# create ghost list
		self.ghost_list = [
											 ghost(name="blinky"),
											 ghost(name="pinky"),
											 ghost(name="inky"),
											 ghost(name="clyde") ]
		self.ghost_counter = 0

		#The directional variable(s) in which Pac-Man moves each update
		self.currentDirection = None
		self.currentAxis = None

		#Counter which buffers Pac-Man's steps till reaching another index; 1 to 5 with 3 being the crossroad
		self.playerCounter = None

		#Game variable declarations
		self.coinCounter = 0
		self.playerScore = 0
		self.currentLevel = randint(1, 3)
		self.playerLives = 3
		self.playerAlive = True
		pygame.font.init()
		self.scoreFont = pygame.font.SysFont('Times New Roman', 25)

	def start(self):

		#Menu/UI goes here (should loop and encapsulate game)





		while True:

			#Probably add the level tune here if I can find it.
			for event in pygame.event.get(): 
				if event.type == pygame.QUIT:
					break

			#Builds/Rebuilds level when conditions are met. 
			if self.coinCounter == 0 or self.playerAlive == False:
				self.build_level()
				self.draw()
				pygame.display.update()
				time.sleep(5)

			#After player has been moved, update coordinates in ghost objects
			self.ghosts_move()

			#Listens to player_controller function; responsible for player movement automation 
			self.player_move()

			#Handles game objectives, defeat scenario, and scoring
			self.game_events()

			#Updates display to console
			self.console_display()

			self.draw()
			pygame.display.update()

			if self.playerLives == 0: 
				#Game over screen
				#Update score to scores.txt
				
				gameov = gameOver()
				gameov.begin()

				#Update game variables for newgame
				self.coinCounter = 0
				self.playerScore = 0
				self.currentLevel = randint(1, 3)
				self.playerLives = 3
				self.playerAlive = True
				
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

		#Saves directional state for next update
		self.currentDirection = nextDirection
		self.currentAxis = nextAxis

	def ghosts_move(self):
		if self.ghost_counter%5 == 0:
			# targets of ghosts *may* be dependent on player
			set_all_targets(get_actives(self.ghost_list), self)
			# set values for ghosts' direction and pos based on targets
			# this will be updating only the data held within the ghosts themselves, not the board
			set_all_dirs_pos(get_actives(self.ghost_list), self)
		self.ghost_counter += 1

	#Draw Function
	def draw(self):

		#Draws board elements; this will always be drawn first, so it is considered the back layer
		for i, tile in enumerate(self.tile):
			x = i % vec_x
			y = int(i / vec_x)
			
			lives = "Player Lives: " + str(self.playerLives)
			scores = "Score: " + str(self.playerScore)
			scoreText = self.scoreFont.render(scores, False, (0,0,0))
			LivesText = self.scoreFont.render(lives, False, (0,0,0))

			if tile.passable and not tile.enemy:
				pygame.draw.rect(self.frame, self.levelColors[self.currentLevel-1], pygame.Rect((x * tile_size, y * tile_size, tile_size, tile_size)))

			elif tile.enemy:
				if tile.type == 'B':
					i = 0; img = "images.blinky"
				elif tile.type == 'P':
					i = 1; img = "images.pinky"
				elif tile.type == 'I':
					i = 2; img = "images.inky"
				else:
					i = 3; img = "images.clyde"

				if self.ghost_list[i].direction == Direction.Left:
					img = img + "_left"
				elif self.ghost_list[i].direction == Direction.Right:
					img = img + "_right"
				elif self.ghost_list[i].direction == Direction.Up:
					img = img + "_up"
				else:
					img = img + "_down"

				self.frame.blit(eval(img), (x * tile_size, y * tile_size))
			
			else:
				pygame.draw.rect(self.frame, blue, pygame.Rect((x * tile_size, y * tile_size, tile_size, tile_size)))

			if tile.coin:
				self.frame.blit(images.coin,(x * tile_size + tile_size/3, y * tile_size + tile_size/3))

		x = self.playerPosition % vec_x
		y = int(self.playerPosition / vec_x)

		#Draws player elements; this will be the top layer when drawn
		self.frame.blit(scoreText, (15, 1))
		self.frame.blit(LivesText, (350, 1))
		
		if self.currentAxis == Axis.Horizontal:
			actual_x = x * tile_size + ((self.playerCounter-3) * (tile_size / 5))
			actual_y = y * tile_size
		else:
			actual_x = x * tile_size
			actual_y = y * tile_size + ((self.playerCounter-3) * (tile_size / 5))

		if self.playerCounter % 2 != 0:
			if self.currentDirection == Direction.Left:
				self.frame.blit(images.pacLeftOpen,(actual_x, actual_y))
			elif self.currentDirection == Direction.Right:
				self.frame.blit(images.pacRightOpen,(actual_x, actual_y))
			elif self.currentDirection == Direction.Up:
				self.frame.blit(images.pacUpOpen,(actual_x, actual_y))
			else:
				self.frame.blit(images.pacDownOpen,(actual_x, actual_y))

		else:
			if self.currentDirection == Direction.Left:
				self.frame.blit(images.pacLeftClosed,(actual_x, actual_y))
			elif self.currentDirection == Direction.Right:
				self.frame.blit(images.pacRightClosed,(actual_x, actual_y))
			elif self.currentDirection == Direction.Up:
				self.frame.blit(images.pacUpClosed,(actual_x, actual_y))
			else:
				self.frame.blit(images.pacDownClosed,(actual_x, actual_y))

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

#Console draw display
	def console_display(self):

		for tile in self.tile:
			tile.update()

		#if self.ghost_counter%5 == 0:
		self.update_ghost_tiles()
		# if enough time has passed, switch modes and refresh ghost_counter
		if self.ghost_counter % 500 == 0:
			change_all_modes(get_actives(self.ghost_list))
			self.ghost_counter = 0

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

	def game_events(self):
		#Checks if player collides with an enemy in the same index
		if self.tile[self.playerPosition].enemy == True:
			self.playerAlive = False
			self.playerLives -= 1
			time.sleep(5)
			return

		#Checks if Pac-Man obtains a coins; scores him points and increments the counter
		if self.tile[self.playerPosition].coin == True:
			self.tile[self.playerPosition].coin = False
			self.coinCounter -= 1
			self.playerScore += coin_value

			#Maybe make an animation here?

#Reads in text documents from Levels directory and creates tile objects out of class Board
#Creates a 2D vector when constructed
#Refreshes level instead if Pac-Man is defeated
	def build_level(self):

		if self.playerAlive == True:
			self.tile = []
			self.currentLevel = randint(1, 3)

		else:
			for tile in self.tile:
				tile.enemy = False
				tile.player = False
			
		temp = "Levels/level" + str(self.currentLevel) + ".txt"
		with open(temp, "r") as f:
				f_text = f.read().replace('\n','')
				f_text.replace('\n','')
				for i, c in enumerate(f_text):

					#Create a variable that references the player location
					if c == '@': self.playerPosition = i

					#Increment coins to counter if new level is built
					elif c == 'o' and self.playerAlive == True: self.coinCounter += 1

					# if ghost is present,change its attribute's accordingly
					elif c in ['B', 'P', 'I', 'C']:
						if c == 'B': index = get_index(self.ghost_list, "blinky")
						elif c == 'P': index = get_index(self.ghost_list, "pinky")
						elif c == 'I': index = get_index(self.ghost_list, "inky")
						else: index = get_index(self.ghost_list, "clyde")
						self.ghost_list[index].active = 1
						self.ghost_list[index].init_ghost_pos(i)

					if self.playerAlive == True: self.tile.append(Board(c,i))
		self.tile[self.playerPosition].player = True

		# initialize active ghosts' first mode to chase
		# FIXME, change this back to chase (instead of scatter)
		set_all_modes(get_actives(self.ghost_list), ghost_mode.chase)

		#Default status for Pac-Man
		self.currentDirection = Direction.Left
		self.currentAxis = Axis.Horizontal
		self.playerCounter = 3
		self.playerAlive = True

	'''
	def update_score(self):
		TODO: append player's final score to scores.txt and his initials
	'''
