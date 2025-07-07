import pygame
from random import randint
from .Const import *
from .EntityFactory import EntityFactory

class Level:
    def __init__(self, screen, players_count):
        self.screen = screen
        self.players_count = players_count
        self.init_objects()

    def init_objects(self):
        pygame.time.set_timer(pygame.USEREVENT+1, SPAWN_INTERVAL)
        pygame.time.set_timer(pygame.USEREVENT+2, LIFE_INTERVAL)
        self.hit_sound = pygame.mixer.Sound(PLAYER_HIT_SOUND)
        self.heart_drop_sound=pygame.mixer.Sound(HEART_DROP_SOUND)
        self.heart_pick_sound=pygame.mixer.Sound(HEART_PICK_SOUND)
        from .Score import Score
        self.score = Score()
        self.players = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.player_shots = pygame.sprite.Group()
        self.enemy_shots = pygame.sprite.Group()
        self.hearts = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        controls = [
            {'up':pygame.K_w,'down':pygame.K_s,'left':pygame.K_a,'right':pygame.K_d,'shoot':pygame.K_SPACE},
            {'up':pygame.K_UP,'down':pygame.K_DOWN,'left':pygame.K_LEFT,'right':pygame.K_RIGHT,'shoot':pygame.K_RETURN}
        ]
        for i in range(self.players_count):
            img = PLAYER1_IMG if i == 0 else PLAYER2_IMG
            p = EntityFactory.create('player', x=100+200*i, y=SCREEN_HEIGHT-50, controls=controls[i], img_path=img)
            self.players.add(p)
            self.all_sprites.add(p)
        self.car = EntityFactory.create('car')
        self.all_sprites.add(self.car)

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            now = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); exit()
                # spawn enemy
                if event.type == pygame.USEREVENT+1:
                    etype = 'enemy_ground' if randint(0, 1) == 0 else 'enemy_flying'
                    x = randint(50, SCREEN_WIDTH - 50)
                    # arrumar o inimigo nascendo fora da tela
                    if etype == 'enemy_ground':
                        y = SCREEN_HEIGHT - 50
                    else:
                        y = 40
                    e = EntityFactory.create('enemy_' + etype.split('_')[-1], x=x, y=y)
                    self.enemy_group.add(e)
                    self.all_sprites.add(e)
                # drop heart
                if event.type == pygame.USEREVENT+2:
                    heart = EntityFactory.create('life_heart', x=self.car.rect.centerx, y=self.car.rect.centery)
                    self.hearts.add(heart)
                    self.all_sprites.add(heart)
                    self.heart_drop_sound.play()
                    self.heart_drop_sound.set_volume(0.1)
            # input & update
            keys = pygame.key.get_pressed()
            for p in self.players:
                p.update(keys, now, self.player_shots)
            for en in self.enemy_group:
                en.update(now, self.enemy_shots)
            self.player_shots.update()
            self.enemy_shots.update()
            self.hearts.update()
            # collisions
            for _ in pygame.sprite.groupcollide(self.enemy_group, self.player_shots, True, True):
                self.score.add(10)
            for p in self.players:
                hits = pygame.sprite.spritecollide(p, self.enemy_shots, True)
                if hits:
                    p.lives -= len(hits)
                    self.hit_sound.play()
                    self.hit_sound.set_volume(0.2)
                    if p.lives <= 0:
                        p.kill()
                heart_hits = pygame.sprite.spritecollide(p, self.hearts, True)
                if heart_hits:
                    p.lives += len(heart_hits)
                    self.heart_pick_sound.play()
                    self.heart_pick_sound.set_volume(MASTER_VOLUME)
            # draw
            self.draw()
            if len(self.players) == 0:
                self.show_gameover()
                running = False
            clock.tick(FPS)
        return self.score.points

    def draw(self):
        bg = pygame.image.load(BACKGROUND_IMG).convert()
        bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(bg, (0, 0))
        # draw behind
        self.car.draw(self.screen)
        # draw others
        self.players.draw(self.screen)
        self.enemy_group.draw(self.screen)
        self.player_shots.draw(self.screen)
        self.enemy_shots.draw(self.screen)
        self.hearts.draw(self.screen)
        # UI
        self.score.draw(self.screen)
        font = pygame.font.Font(None, 36)
        for idx, p in enumerate(self.players):
            txt = font.render(f"P{idx+1} Lives: {p.lives}", True, (255, 255, 255))
            self.screen.blit(txt, (600, 10 + idx*30))
        pygame.display.flip()

    def show_gameover(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 100)
        text = font.render("Game Over", True, (255, 0, 0))
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, rect)
        pygame.display.flip()
        pygame.time.wait(2000)
        