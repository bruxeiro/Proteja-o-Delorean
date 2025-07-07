import pygame
from .Entity import Entity
from .Const import *

class Enemy(Entity):
    def __init__(self, enemy_type, x, y):
        img = ENEMY_GROUND_IMG if enemy_type == 'enemy_ground' else ENEMY_FLY_IMG
        super().__init__(img, x, y)
        self.type = enemy_type
        self.speed = ENEMY_SPEED
        self.dir = 1  # horizontal oscillation direction
        self.last_shot = 0
        self.death_sound = pygame.mixer.Sound(ENEMY_HIT_SOUND)

    def update(self, now, shots_group):
        # movement: both ground and flying enemies oscillate horizontally
        self.rect.x += self.speed * self.dir
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.dir *= -1

        # shooting logic: ground shoots up, flying shoots down
        if now - self.last_shot > 1500:
            from .EnemyShot import EnemyShot
            if self.type == 'enemy_ground':
                shots_group.add(EnemyShot(self.rect.centerx, self.rect.top, direction=-1))
            else:
                shots_group.add(EnemyShot(self.rect.centerx, self.rect.bottom, direction=1))
            self.last_shot = now
        
    def kill(self):
        self.death_sound.play()
        self.death_sound.set_volume(MASTER_VOLUME)
        super().kill()