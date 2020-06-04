class Board:
  
  def __init__(self, type, position):

    self.type = type
    self.position = position

    self.passable = False
    self.coin = False
    self.warp = False
    self.player = False
    self.enemy = False

    if self.type == ' ':
      self.passable = True

    elif self.type == 'o':
      self.passable = True
      self.coin = True

    elif self.type == '~':
      self.passable = True
      self.warp = True
    
    elif self.type == '@':
      self.passable = True
      self.player = True
    
    elif self.type == 'G':
      self.passable = True
      self.enemy = True

  def update(self):

    if self.enemy == True:
      self.type = 'G'

    elif self.player == True:
     self.type = '@'

    elif self.warp == True:
      self.type = '~'
    
    elif self.coin == True:
      self.type = 'o'

    elif self.passable == True:
      self.type = ' '
