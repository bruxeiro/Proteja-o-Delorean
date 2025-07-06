import pygame
from .Entity import Entity
from .Const import PLAYER_SPEED, SHOT_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_LIVES
from pygame.math import Vector2

class Player(Entity):
    def __init__(self, x, y, controls, img_path):
        super().__init__(img_path, x, y)
        self.controls = controls
        self.lives = PLAYER_LIVES
        self.last_shot = 0

    def update(self, keys, now, shots_group):
        # horizontal movement
        if keys[self.controls['left']]:
            self.rect.x -= PLAYER_SPEED
            if self.rect.left < 0:
                self.rect.left = 0
        if keys[self.controls['right']]:
            self.rect.x += PLAYER_SPEED
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
        # vertical movement
        if keys[self.controls['up']]:
            self.rect.y -= PLAYER_SPEED
            if self.rect.top < 0:
                self.rect.top = 0
        if keys[self.controls['down']]:
            self.rect.y += PLAYER_SPEED
            if self.rect.bottom > SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT
        # shooting
        if keys[self.controls['shoot']] and now - self.last_shot > 300:
            mx, my = pygame.mouse.get_pos()
            direction = Vector2(mx - self.rect.centerx, my - self.rect.centery)
            if direction.length() > 0:
                direction = direction.normalize() * SHOT_SPEED
            from .PlayerShot import PlayerShot
            shots_group.add(PlayerShot(self.rect.centerx, self.rect.centery, direction))
            self.last_shot = now