"""
Class Definition and functions for pacman-style ghosts
Includes: Setters and getters
          Functions to determine movement & direction
          Multiple ghost AIs
written by: Abigail Mortensen
"""
import pygame
import os
from game import *
from options import *
from board import *
from status import *
from math import sqrt

#constants
MAX_NUM_GHOSTS = 4


class ghost(object):

    # FIXME, may not need prevpos attribute
    # could calculate it when time comes w/ get_next_tile
    def __init__(self, name):
        self.name = name
        self.mode = None
        self.target = None
        self.pos = None
        self.direction = None
        self.active = 0
        self.prevpos = None

    # **** GETTER FUNCTIONS ****
    def get_ghost_name(self):
        return self.name

    def get_ghost_mode(self):
        return self.mode

    def get_ghost_target(self):
        return self.target

    def get_ghost_pos(self):
        return self.pos

    def get_ghost_direction(self):
        return self.direction


    # **** SETTER FUNCTIONS ****
    def set_ghost_name(self, name):
        self.name = name

    def set_ghost_mode(self, gmode):
        self.mode = gmode

    # FIXME, handled changing to frightened or eaten mode
    def change_ghost_mode(self, fnOrEat=None):
        if fnOrEat == None:
            if self.mode == ghost_mode.chase:
                self.mode = ghost_mode.scatter
            else:
                self.mode = ghost_mode.chase
        else:
            pass

    # Initialize ghost's coordinate attribute
    def init_ghost_pos(self, pos):
        self.pos = pos

    # **** MOVEMENT FUNCTIONS ****

    # FIXME, add in frightened and eaten?
    # FIXME, program target setting for chase
    # determine & set target based on name and mode
    def set_ghost_target(self, gameobj):
        blinkyindex = 0; inkyindex = 2; clydeindex = 3
        if self.name == "blinky":
            if self.mode == ghost_mode.chase:
                # set blinky's target to pacman's tile
                self.target = gameobj.playerPosition
            elif self.mode == ghost_mode.scatter:
                self.target = gameobj.get_corner(corner.top_right)

        elif self.name == "pinky":
            if self.mode == ghost_mode.chase:
                # set pinky's target to two tiles in front of pacman
                newpos = gameobj.playerPosition
                for step in range(2):
                    newpos = (get_next_tile(gameobj, newpos, gameobj.currentDirection)).position
                self.target = newpos
            elif self.mode == ghost_mode.scatter:
                self.target = gameobj.get_corner(corner.top_left)

        elif self.name == "inky":
            # set inky's target based off of blinky's target :
            # rotate blinky's target roughly 180 degrees in the opposite direction
            if self.mode == ghost_mode.chase:
                # get blinky's info
                bpos = gameobj.ghost_list[blinkyindex].pos
                btarget = gameobj.ghost_list[blinkyindex].target
                # rotate the btarget roughly 180 degrees for dist
                # if blinky is above or (same isle) left of the player
                if bpos < btarget:
                    self.target = btarget + bpos
                # if blinky is below or (same isle) right of the player
                else:
                    self.target = btarget - bpos
            elif self.mode == ghost_mode.scatter:
                self.target = gameobj.get_corner(corner.bottom_right)

        elif self.name == "clyde":
            # set clyde's target based off his distance from pacman
            if self.mode == ghost_mode.chase:
                # if clyde's info hasn't been set yet, start off with being the playerpos
                if self.target == None: self.target = gameobj.playerPosition
                # if the distance between them is 8 or more, set to pacman's location
                cdist = calc_dist(self.pos, self.target)
                if cdist >= 8:
                    self.target = gameobj.playerPosition
                # if the distance is less than 8, set to clyde's corner
                else:
                    self.target = gameobj.get_corner(corner.bottom_left)
            elif self.mode == ghost_mode.scatter:
                self.target = gameobj.get_corner(corner.bottom_left)

    # determine & set the next direction based on shortest distance
    # between ghost and target, set the new pos in this new direction
    def set_ghost_dir_pos(self, gameobj):
        # create a list of possible options
        dir_options = get_all_directions()
        # do not allow ghost to turn around 180 degrees
        if self.direction != None:
            dir_options.remove(get_opposite_dir(self.direction))
        for wallDir in get_wall_directions(gameobj, self, dir_options):
            dir_options.remove(wallDir)

        #before storing a new location, remember to store the soon-to-be previous location
        self.prevpos = self.pos

        #if only one possible travel direction, travel there
        if len(dir_options) == 1:
            next_tile = get_next_tile(gameobj, self.pos, dir_options[0])
            self.direction = dir_options[0]
            self.pos = next_tile.position
            return

        #if dir_options are empty, turn the ghost around
        elif len(dir_options) == 0:
            next_tile = get_next_tile(gameobj, self.pos, get_opposite_dir(self.direction))
            self.direction = get_opposite_dir(self.direction)
            self.pos = next_tile.position
            return

        #find which of *multiple* options provides shortest distance
        smallestdist = 100
        for option in dir_options:
            next_tile = get_next_tile(gameobj, self.pos, option)
            npos = next_tile.position
            posdist = calc_dist(npos, self.target)
            if posdist < smallestdist:
                smallestdist = posdist
                smallestdir = option
                smallestpos = next_tile.position

        self.direction = smallestdir
        self.pos = smallestpos

# **** MISCELLANEOUS FUNCTIONS ****
# ideally these "set all" and "get all" functions should be given
# a list of which ghosts are active in the ghost_list parameter
# so that inactive ghosts aren't wrongfully affected
def set_all_modes(ghost_list, gmode):
    for g in ghost_list:
        g.set_ghost_mode(gmode)

def change_all_modes(ghost_list):
    for g in ghost_list:
        g.change_ghost_mode()

def set_all_targets(ghost_list, gameobj):
    for g in ghost_list:
        g.set_ghost_target(gameobj)

def set_all_dirs_pos(ghost_list, gameobj):
    for g in ghost_list:
        g.set_ghost_dir_pos(gameobj)

def init_all_pos(ghost_list, pos_list):
    for index in range(0,4):
        ghost_list[index].init_ghost_pos(pos_list[index])

def get_actives(ghost_list):
    return [g for g in ghost_list if g.active == 1]

def get_index(ghost_list, name):
    return [i for i in range(0, MAX_NUM_GHOSTS) if ghost_list[i].name == name][0]

def get_all_pos(ghost_list):
    return [g.pos for g in ghost_list]

def get_ghosts_start_pos(level): #FIXME
    return [0,0,0,0]

def get_all_directions():
    return [dir for dir in Direction]

def get_opposite_dir(dir):
    if dir == Direction.Down:
        return Direction.Up
    elif dir == Direction.Up:
        return Direction.Down
    elif dir == Direction.Left:
        return Direction.Right
    else:
        return Direction.Left

# returns a list of all directions where movement in said direction
# is a wall, or not a passable object
def get_wall_directions(gameobj, ghostobj, dir_options):
    wall_dirs = []
    for dir in dir_options:
        possible_tile = get_next_tile(gameobj, ghostobj.pos, dir)
        if possible_tile.passable == False:
            wall_dirs.append(dir)

    return wall_dirs

# return the tile you would be on if traveling in direction parameter
# this funct based on James's code
def get_next_tile(gameobj, spos, dir):
    if dir == Direction.Left:
        if (spos - 1) <= 0: return 0
        return gameobj.tile[spos - 1]
    elif dir == Direction.Right:
        if (spos + 1) >= len(gameobj.tile): return gameobj.tile[len(gameobj.tile)-1]
        return gameobj.tile[spos + 1]
    elif dir == Direction.Up:
        if (spos - vec_x) <= 0: return 0
        return gameobj.tile[spos - vec_x]
    elif dir == Direction.Down:
        if (spos + vec_x) >= len(gameobj.tile): return gameobj.tile[len(gameobj.tile)-1]
        return gameobj.tile[spos + vec_x]


def calc_dist(pos, target):
    # turn pos into an ordered pair - based on James's code
    ghostcoords = [ pos % vec_x, int(pos / vec_x)]
    # turn target into an ordered pair - based on James's code
    targetcoords = [ target % vec_x, int(target / vec_x)]
    # return distance between these two pairs
    return sqrt(
          ((targetcoords[0] - ghostcoords[0])**2)
        + ((targetcoords[1] - ghostcoords[1])**2)  )