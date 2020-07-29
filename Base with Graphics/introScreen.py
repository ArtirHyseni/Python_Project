import pygame
import os
import images
import sys
from options import *
from board import *
from ghost import *
from status import *
from game import *
from options import frame_height

pygame.init()
pygame.display.set_caption("Pac-Man")

class introScreen:
    def __init__(self):
        self.frame = pygame.display.set_mode((frame_width, frame_height))

        # Background color of the game
        self.frame.fill(black)

        self.running = True
        self.state = 'start'
        self.active = True

    def start(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            else:
                pass

    def draw_text(self, words, frame, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        frame.blit(text, pos)

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game = Game()
                game.start()
                pygame.quit()
                sys.exit()


    def start_update(self):
        pass

    def start_draw(self):
        self.frame.fill(black)
        self.draw_text('PUSH SPACE BAR', self.frame, [
            frame_width // 2, frame_height // 2 - 50], START_TEXT_SIZE, (170, 132, 58), START_FONT, centered=True)
        self.draw_text('1 PLAYER ONLY', self.frame, [
            frame_width // 2, frame_height // 2 + 50], START_TEXT_SIZE, (44, 167, 198), START_FONT, centered=True)
        self.draw_text('HIGH SCORE', self.frame, [4, 0],
                       START_TEXT_SIZE, (255, 255, 255), START_FONT)

        pygame.display.update()



