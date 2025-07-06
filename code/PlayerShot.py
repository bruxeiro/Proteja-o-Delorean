from .Entity import Entity
from .Const import *

class PlayerShot(Entity):
    def __init__(self, x, y, velocity):
        super().__init__(PLAYER_SHOT_IMG, x, y)
        self.vel = velocity

    def update(self):
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y
        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or
            self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.kill()