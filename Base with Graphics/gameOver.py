import pygame
import os
import images
import sys
from options import *
from board import *
from ghost import *
from status import *
from game import *
from Base.options import frame_height

pygame.init()
pygame.display.set_caption("Pac-Man")

class gameOver:
    def __init__(self):
        self.frame = pygame.display.set_mode((frame_width, frame_height))

        # Background color of the game
        self.frame.fill(black)

        self.running = True
        self.state = 'game over'
        self.active = True

    def begin(self):
        while self.running:
            if self.state == 'game over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
            else:
                pass
        pygame.quit()
        sys.exit()

    def draw_text(self, words, frame, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        frame.blit(text, pos)

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def game_over_update(self):
        pass

    def game_over_draw(self):
        self.frame.fill(black)
        quit_text = "Press the escape button to QUIT"
        again_text = "Press SPACE bar to PLAY AGAIN"
        self.draw_text("GAME OVER", self.frame, [frame_width // 2, 100], 52, (170, 132, 58), START_FONT, centered=True)
        self.draw_text(again_text, self.frame, [
            frame_width // 2, frame_height // 2], 36, (190, 190, 190), START_FONT, centered=True)
        self.draw_text(quit_text, self.frame, [
            frame_width // 2, frame_height // 1.5], 36, (190, 190, 190), START_FONT, centered=True)
        pygame.display.update()