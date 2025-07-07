# code/Menu.py
import pygame
from .Const import *
from .DBProxy import DBProxy

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.options = ['1 Player', '2 Players', 'High Scores', 'Exit']
        self.selected = 0
        self.start_sound = pygame.mixer.Sound(GAME_START_SOUND)

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
                        self.start_sound.set_volume(MASTER_VOLUME)
                        self.start_sound.play()
                        opt = self.options[self.selected]
                        if opt == 'Exit':
                            pygame.quit(); db.close(); exit()
                        if opt == 'High Scores':
                            self.show_scores(db)
                            continue
                        return 1 if opt == '1 Player' else 2

            # draw background scaled
            bg_img = pygame.image.load(BACKGROUND_IMG_MENU).convert()
            bg = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(bg, (0, 0))

            # draw title
            title_font = pygame.font.Font(None, 96)
            title_surf = title_font.render('Protect The Delorean', True, (255, 255, 0))
            title_rect = title_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
            self.screen.blit(title_surf, title_rect)

            # draw menu options centered
            option_font = pygame.font.Font(None, 64)
            for idx, option in enumerate(self.options):
                color = (255, 100, 100) if idx == self.selected else (200, 200, 200)
                surf = option_font.render(option, True, color)
                rect = surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + idx * 80))
                self.screen.blit(surf, rect)

            pygame.display.flip()
            clock.tick(FPS)

    def show_scores(self, db):
        scores = db.retrieve_top10()
        clock = pygame.time.Clock()
        font_title = pygame.font.Font(None, 72)
        font_score = pygame.font.Font(None, 48)
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    return
                if ev.type == pygame.QUIT:
                    pygame.quit(); db.close(); exit()

            # draw background
            self.screen.fill((0, 0, 50))

            title_surf = font_title.render('High Scores', True, (255, 255, 0))
            title_rect = title_surf.get_rect(center=(SCREEN_WIDTH//2, 80))
            self.screen.blit(title_surf, title_rect)

            # draw scores
            for idx, (name, score, _) in enumerate(scores):
                text = f"{idx+1}. {name} - {score}"
                surf = font_score.render(text, True, (255, 255, 255))
                rect = surf.get_rect(center=(SCREEN_WIDTH//2, 140 + idx * 45))
                self.screen.blit(surf, rect)

            prompt = font_score.render('Press ESC to return', True, (200, 200, 200))
            prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 15))
            self.screen.blit(prompt, prompt_rect)

            pygame.display.flip()
            clock.tick(FPS)
