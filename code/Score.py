import pygame
from .Const import *

class Score:
    def __init__(self):
        self.points = 0
        self.start_time = pygame.time.get_ticks()

    def add(self, pts):
        self.points += pts

    def draw(self, surface):
        font = pygame.font.Font(None, 36)
        # points
        text = font.render(f"Score: {self.points}", True, (255,255,255))
        surface.blit(text, (10,10))
        # time
        elapsed = (pygame.time.get_ticks() - self.start_time)//1000
        ttext = font.render(f"Time: {elapsed}s", True, (255,255,255))
        surface.blit(ttext, (10,50))