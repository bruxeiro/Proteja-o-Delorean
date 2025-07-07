import pygame
from .Const import *
from .Menu import Menu
from .Level import Level
from .DBProxy import DBProxy

class Game:
    def __init__(self):
        # Inicializa o Pygame e o mixer de áudio
        pygame.init()
        pygame.mixer.init()

        # Configura a janela do jogo
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Proteja o Delorean')

        # Conexão com o banco de dados para salvar pontuações
        self.db = DBProxy()

    def show_name_input(self):
        """
        Exibe uma caixa de entrada para o jogador digitar seu nome.
        Retorna o nome digitado ou 'Player' se nenhum caractere for inserido.
        """
        name = ""
        font = pygame.font.Font(None, 48)
        input_rect = pygame.Rect(200, SCREEN_HEIGHT // 2, 400, 50)
        active = True
        clock = pygame.time.Clock()

        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Confirmação: finaliza a entrada
                        active = False
                        break
                    elif event.key == pygame.K_BACKSPACE:
                        # Remove último caractere
                        name = name[:-1]
                    else:
                        # Adiciona caractere se não ultrapassar 12 caracteres
                        if len(name) < 12:
                            name += event.unicode

            # Renderiza o prompt e o texto digitado
            self.screen.fill((0, 0, 0))
            prompt = font.render("Enter your name:", True, (255, 255, 255))
            self.screen.blit(prompt, (200, SCREEN_HEIGHT // 2 - 60))
            pygame.draw.rect(self.screen, (255, 255, 255), input_rect, 2)
            name_surf = font.render(name, True, (255, 255, 255))
            self.screen.blit(name_surf, (input_rect.x + 5, input_rect.y + 5))

            pygame.display.flip()
            clock.tick(FPS)

        # Se o jogador não digitou nada, usa 'Player'
        return name.strip() or "Player"

    def run(self):
        """
        Laço principal do jogo:
        - Exibe o menu inicial
        - Executa o nível selecionado e captura a pontuação
        - Exibe tela de Game Over
        - Solicita nome e salva a pontuação
        - Exibe tabela de highscores
        """
        while True:
            # Música de menu em loop
            pygame.mixer.music.load(MENU_MUSIC)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(MASTER_VOLUME)

            # Exibe menu e obtém número de jogadores
            players = Menu(self.screen).run()

            # Inicia música de jogo
            pygame.mixer.music.load(GAME_MUSIC)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.05)

            # Executa o nível e obtém pontuação final
            score = Level(self.screen, players).run()

            # Pequena pausa antes de exibir Game Over
            pygame.time.wait(500)
            self.screen.fill((0, 0, 0))

            # Renderiza texto de Game Over
            go_font = pygame.font.Font(None, 100)
            go_text = go_font.render("Game Over", True, (255, 0, 0))
            go_rect = go_text.get_rect(center=(SCREEN_WIDTH // 2,
                                               SCREEN_HEIGHT // 2 - 100))
            self.screen.blit(go_text, go_rect)
            pygame.display.flip()

            # Aguarda antes de solicitar nome
            pygame.time.wait(1000)

            # Captura nome do jogador e salva no banco
            name = self.show_name_input()
            self.db.save(name, score)

            # Exibe tabela de pontuações
            Menu(self.screen).show_scores(self.db)