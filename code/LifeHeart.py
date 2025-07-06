from .Entity import Entity
from .Const import LIFE_HEART_IMG

class LifeHeart(Entity):
    def __init__(self, x, y):
        super().__init__(LIFE_HEART_IMG, x, y)
    def update(self, *args):
        pass 