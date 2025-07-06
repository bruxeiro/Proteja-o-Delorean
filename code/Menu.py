import pygame
from .Const import BACKGROUND_IMG_MENU, FPS
from .DBProxy import DBProxy

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.options = ['1 Player', '2 Players', 'High Scores', 'Exit']
        self.selected = 0

    def run(self):
        db = DBProxy()
        clock = pygame.time.Clock()
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); db.close(); exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    if e.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    if e.key == pygame.K_RETURN:
                        opt = self.options[self.selected]
                        if opt == 'Exit':
                            pygame.quit(); db.close(); exit()
                        if opt == 'High Scores':
                            self.show_scores(db)
                            continue
                        return 1 if opt == '1 Player' else 2

            # draw background
            bg = pygame.image.load(BACKGROUND_IMG_MENU).convert()
            self.screen.blit(bg, (0, 0))
            # draw menu options
            font = pygame.font.Font(None, 74)
            for i, o in enumerate(self.options):
                color = (255, 0, 0) if i == self.selected else (255, 255, 255)
                txt = font.render(o, True, color)
                self.screen.blit(txt, (200, 150 + i * 80))

            pygame.display.flip()
            clock.tick(FPS)

    def show_scores(self, db):
        scores = db.retrieve_top10()
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 48)
        self.screen.blit(font.render("High Scores", True, (255, 255, 0)), (250, 50))
        small = pygame.font.Font(None, 36)
        for idx, (n, s, d) in enumerate(scores):
            self.screen.blit(small.render(f"{idx+1}. {n} - {s}", True, (255, 255, 255)), (200, 150 + idx * 40))
        pygame.display.flip()
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    return