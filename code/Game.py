import pygame
from .Const import *
from .Menu import Menu
from .Level import Level
from .DBProxy import DBProxy

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Proteja o Delorean')
        self.db = DBProxy()

    def show_name_input(self):
        name = ""
        font = pygame.font.Font(None, 48)
        input_rect = pygame.Rect(200, SCREEN_HEIGHT//2, 400, 50)
        active = True
        clock = pygame.time.Clock()
        while active:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        active = False
                        break
                    elif e.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < 12:
                            name += e.unicode
            self.screen.fill((0,0,0))
            prompt = font.render("Enter your name:", True, (255,255,255))
            self.screen.blit(prompt, (200, SCREEN_HEIGHT//2 - 60))
            pygame.draw.rect(self.screen, (255,255,255), input_rect, 2)
            name_surf = font.render(name, True, (255,255,255))
            self.screen.blit(name_surf, (input_rect.x+5, input_rect.y+5))
            pygame.display.flip()
            clock.tick(FPS)
        return name.strip() or "Player"

    def run(self):
        while True:
            players = Menu(self.screen).run()
            score = Level(self.screen, players).run()
            pygame.time.wait(500)
            self.screen.fill((0,0,0))
            go_font = pygame.font.Font(None, 100)
            go_text = go_font.render("Game Over", True, (255,0,0))
            go_rect = go_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
            self.screen.blit(go_text, go_rect)
            pygame.display.flip()
            pygame.time.wait(1000)
            name = self.show_name_input()
            self.db.save(name, score)
            Menu(self.screen).show_scores(self.db)