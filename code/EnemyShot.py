from .Entity import Entity
from .Const import ENEMY_SHOT_SPEED, SCREEN_HEIGHT, ENEMY_SHOT_IMG

class EnemyShot(Entity):
    def __init__(self, x, y, direction=1):
        super().__init__(ENEMY_SHOT_IMG, x, y)
        # direction: 1 for down, -1 for up
        self.direction = direction

    def update(self):
        # move shot vertically
        self.rect.y += ENEMY_SHOT_SPEED * self.direction
        # remove if off-screen
        if self.direction > 0 and self.rect.top > SCREEN_HEIGHT:
            self.kill()
        elif self.direction < 0 and self.rect.bottom < 0:
            self.kill()
