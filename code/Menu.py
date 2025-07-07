# File: Menu.py
import pygame
from .Const import *
from .DBProxy import DBProxy

class Menu:
    def __init__(self, screen):
        """
        Inicializa o menu principal:
        - Armazena a superfície de exibição
        - Define opções de menu
        - Carrega som de início de partida
        """
        self.screen = screen
        self.options = ['1 Player', '2 Players', 'High Scores', 'Exit']  
        self.selected = 0                                           
        self.start_sound = pygame.mixer.Sound(GAME_START_SOUND)     

    def run(self):
        """
        Exibe o menu e trata interações:
        1. Toca música de fundo em loop
        2. Navega entre opções com setas
        3. Seleciona opção com Enter:
           - '1 Player' ou '2 Players': retorna número de jogadores
           - 'High Scores': exibe placar e retorna ao menu
           - 'Exit': encerra o jogo
        """
        db = DBProxy()                    
        clock = pygame.time.Clock()

        # Loop principal do menu
        while True:
            # Processa eventos de teclado e janela
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); db.close(); exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    if e.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    if e.key == pygame.K_RETURN:
                        # Toca som de confirmação
                        self.start_sound.set_volume(MASTER_VOLUME)
                        self.start_sound.play()
                        opt = self.options[self.selected]
                        if opt == 'Exit':
                            pygame.quit(); db.close(); exit()
                        if opt == 'High Scores':
                            self.show_scores(db)
                            continue
                        # Retorna 1 para '1 Player' ou 2 para '2 Players'
                        return 1 if opt == '1 Player' else 2

            # Renderiza bakcground - arrumando o bug do tamanho
            bg_img = pygame.image.load(BACKGROUND_IMG_MENU).convert()
            bg = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(bg, (0, 0))

            # Desenha titulo centralizado
            title_font = pygame.font.Font(None, 96)
            title = title_font.render('Protect The Delorean', True, (255, 255, 0))
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
            self.screen.blit(title, title_rect)

            # Desenha opções de menu
            option_font = pygame.font.Font(None, 64)
            for idx, option in enumerate(self.options):
                color = (255, 100, 100) if idx == self.selected else (200, 200, 200)
                surf = option_font.render(option, True, color)
                rect = surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + idx * 80))
                self.screen.blit(surf, rect)

            pygame.display.flip()
            clock.tick(FPS)

    def show_scores(self, db):
        """
        Exibe a tela de High Scores:
        - Recupera top 10 do banco
        - Lista nomes e pontuações
        - Aguarda ESC para voltar ao menu ou QUIT para sair
        """
        scores = db.retrieve_top10()
        clock = pygame.time.Clock()
        font_title = pygame.font.Font(None, 72)
        font_score = pygame.font.Font(None, 48)

        while True:
            # Processa evntos de retorno
            for ev in pygame.event.get():
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    return  # Volta ao menu
                if ev.type == pygame.QUIT:
                    pygame.quit(); db.close(); exit()

            # Fundo escuro
            self.screen.fill((0, 0, 50))

            # Título 'High Scores'
            title_surf = font_title.render('High Scores', True, (255, 255, 0))
            title_rect = title_surf.get_rect(center=(SCREEN_WIDTH//2, 80))
            self.screen.blit(title_surf, title_rect)

            # Lista as pontuações
            for idx, (name, score, _) in enumerate(scores):
                text = f"{idx+1}. {name} - {score}"
                surf = font_score.render(text, True, (255, 255, 255))
                rect = surf.get_rect(center=(SCREEN_WIDTH//2, 140 + idx * 45))
                self.screen.blit(surf, rect)

            # Prompt de retorno
            prompt = font_score.render('Press ESC to return', True, (200, 200, 200))
            prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 15))
            self.screen.blit(prompt, prompt_rect)

            pygame.display.flip()
            clock.tick(FPS)
