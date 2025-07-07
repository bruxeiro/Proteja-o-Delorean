import pygame
from random import randint
from .Const import *
from .EntityFactory import EntityFactory

class Level:
    def __init__(self, screen, players_count):
        # Inicializa o nível com a tela e a quantidade de jogadorees
        self.screen = screen
        self.players_count = players_count
        self.init_objects()

    def init_objects(self):
        """
        Configura:
        - Timers para spawn de inimigos e queda de corações
        - Sons de impacto, queda e coleta de vidas
        - Grupos de sprites para jogadores, inimigos, tiros e corações
        - Instancia os jogadores e o delorean
        """
        # Eventos customizados para spawn de inimigos e corações
        pygame.time.set_timer(pygame.USEREVENT + 1, SPAWN_INTERVAL)
        pygame.time.set_timer(pygame.USEREVENT + 2, LIFE_INTERVAL)

        # Carrega efeitos sonoros do jogo
        self.hit_sound = pygame.mixer.Sound(PLAYER_HIT_SOUND)
        self.heart_drop_sound = pygame.mixer.Sound(HEART_DROP_SOUND)
        self.heart_pick_sound = pygame.mixer.Sound(HEART_PICK_SOUND)

        # Sistema de pontuação
        from .Score import Score
        self.score = Score()

        # Grupos de sprtes para gerenciamento de colisões e atualizações
        self.players = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.player_shots = pygame.sprite.Group()
        self.enemy_shots = pygame.sprite.Group()
        self.hearts = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        # Controles padrão para até dois jogadores
        controls = [
            {
                'up': pygame.K_w, 'down': pygame.K_s,
                'left': pygame.K_a, 'right': pygame.K_d,
                'shoot': pygame.K_SPACE
            },
            {
                'up': pygame.K_UP, 'down': pygame.K_DOWN,
                'left': pygame.K_LEFT, 'right': pygame.K_RIGHT,
                'shoot': pygame.K_RETURN
            }
        ]

        # Cria cada jogador e adiciona aos grupos
        for i in range(self.players_count):
            img = PLAYER1_IMG if i == 0 else PLAYER2_IMG
            p = EntityFactory.create(
                'player',
                x=100 + 200 * i,
                y=SCREEN_HEIGHT - 50,
                controls=controls[i],
                img_path=img
            )
            self.players.add(p)
            self.all_sprites.add(p)

        # Cria o carro e adiciona ao conjunto de sprites geral
        self.car = EntityFactory.create('car')
        self.all_sprites.add(self.car)

    def run(self):
        """
        Loop principal do nível:
        1. Processa eventos de saida, spawn de inimigos e queda de corações
        2. Atualiza todas as entidades conforme entradas e tempo
        3. Verifica colisões:
           - Tiros de jogador vs inimigos
           - Tiros de inimigo vs jogadores
           - Jogadores + corações para vida extra
        4. Renderiza cena e UI
        5. Detecta fim de jogo quando não há jogadores ativos
        Retorna a pontuação final do jogador.
        """
        clock = pygame.time.Clock()
        running = True

        while running:
            now = pygame.time.get_ticks()

            # Processa eventos do Pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # Spawn de inimigos em interavlo definido
                if event.type == pygame.USEREVENT + 1:
                    etype = 'enemy_ground' if randint(0, 1) == 0 else 'enemy_flying'
                    x = randint(50, SCREEN_WIDTH - 50)
                    y = SCREEN_HEIGHT - 50 if etype == 'enemy_ground' else 40
                    e = EntityFactory.create(
                        'enemy_' + etype.split('_')[-1],
                        x=x, y=y
                    )
                    self.enemy_group.add(e)
                    self.all_sprites.add(e)

                # Queda de corações para coleta
                if event.type == pygame.USEREVENT + 2:
                    heart = EntityFactory.create(
                        'life_heart',
                        x=self.car.rect.centerx,
                        y=self.car.rect.centery
                    )
                    self.hearts.add(heart)
                    self.all_sprites.add(heart)
                    self.heart_drop_sound.play()
                    self.heart_drop_sound.set_volume(0.1)

            # Atualiza posições e inputs do jogador
            keys = pygame.key.get_pressed()
            for p in self.players:
                p.update(keys, now, self.player_shots)
            for en in self.enemy_group:
                en.update(now, self.enemy_shots)
            self.player_shots.update()
            self.enemy_shots.update()
            self.hearts.update()

            # Colisão: jogador acerta inimigos
            for _ in pygame.sprite.groupcollide(
                self.enemy_group, self.player_shots, True, True
            ):
                self.score.add(10)

            # Colisão: inimigos acertam jogadores
            for p in self.players:
                hits = pygame.sprite.spritecollide(p, self.enemy_shots, True)
                if hits:
                    p.lives -= len(hits)
                    self.hit_sound.play()
                    self.hit_sound.set_volume(0.2)
                    if p.lives <= 0:
                        p.kill()

                # Coleta de corações para ganhar vida extra
                heart_hits = pygame.sprite.spritecollide(p, self.hearts, True)
                if heart_hits:
                    p.lives += len(heart_hits)
                    self.heart_pick_sound.play()
                    self.heart_pick_sound.set_volume(MASTER_VOLUME)

            # Renderiza o nível e a interface do usuario
            self.draw()

            # Verifica se o jogo acabou
            if not self.players:
                self.show_gameover()
                running = False

            clock.tick(FPS)

        return self.score.points

    def draw(self):
        """
        Renderiza o background, entidades e HUD do jogo:
        - Desenha carro no plano de fundo
        - Desenha jogadores, inimigos, tiros e corações
        - Exibe pontuação e vidas de cada jogador
        """
        # Desenha background escalado
        bg = pygame.image.load(BACKGROUND_IMG).convert()
        bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(bg, (0, 0))

        # Desenha o carro primeiro
        self.car.draw(self.screen)

        # Desenha sprites de jogadores, inimigos, tiros e corações
        self.players.draw(self.screen)
        self.enemy_group.draw(self.screen)
        self.player_shots.draw(self.screen)
        self.enemy_shots.draw(self.screen)
        self.hearts.draw(self.screen)

        # Exibe pontuação e vidas
        self.score.draw(self.screen)
        font = pygame.font.Font(None, 36)
        for idx, p in enumerate(self.players):
            txt = font.render(f"P{idx+1} Lives: {p.lives}", True, (255, 255, 255))
            self.screen.blit(txt, (600, 10 + idx * 30))

        pygame.display.flip()

    def show_gameover(self):
        """
        Exibe a tela de Game Over por 1 segundo
        """
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 100)
        text = font.render("Game Over", True, (255, 0, 0))
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, rect)
        pygame.display.flip()
        pygame.time.wait(1000)
