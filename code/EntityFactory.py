from .Player import Player
from .Enemy import Enemy
from .PlayerShot import PlayerShot
from .EnemyShot import EnemyShot
from .Car import Car
from .LifeHeart import LifeHeart

class EntityFactory:
    @staticmethod
    def create(entity_type, **kw):
        if entity_type == 'player':
            # Usa a imagem do sprite baseado no input
            return Player(kw['x'], kw['y'], kw['controls'], kw['img_path'])
        if entity_type in ('enemy_ground', 'enemy_flying'):
            return Enemy(entity_type, kw['x'], kw['y'])
        if entity_type == 'player_shot':
            return PlayerShot(kw['x'], kw['y'], kw['velocity'])
        if entity_type == 'enemy_shot':
            return EnemyShot(kw['x'], kw['y'])
        if entity_type == 'car':
            return Car()
        if entity_type == 'life_heart':
            return LifeHeart(kw['x'], kw['y'])
        return None