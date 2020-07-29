from game import *
from introScreen import *
from gameOver import *

if __name__ == '__main__':
  iterator = 0
  intro = introScreen()
  while iterator <= 3:
    #intro = introScreen()
    intro.start()
    iterator = iterator + 1
