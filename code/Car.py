from .Entity import Entity
from .Const import *

class Car(Entity):
    def __init__(self):
        super().__init__(CAR_IMG, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)