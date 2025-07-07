from .Entity import Entity
from .Const import ENEMY_SHOT_SPEED, SCREEN_HEIGHT, ENEMY_SHOT_IMG

class EnemyShot(Entity):
    def __init__(self, x, y, direction=1):
        super().__init__(ENEMY_SHOT_IMG, x, y)
        #Direção do movimento do tiro: 1 para baixo, -1 para cima
        self.direction = direction

    def update(self):

        self.rect.y += ENEMY_SHOT_SPEED * self.direction
        #Remove se o tiro sair da tela
        if self.direction > 0 and self.rect.top > SCREEN_HEIGHT:
            self.kill()
        elif self.direction < 0 and self.rect.bottom < 0:
            self.kill()
