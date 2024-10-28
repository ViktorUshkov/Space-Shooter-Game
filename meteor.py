import pygame
from os.path import join
from settings import Settings
from random import randint, uniform
from interface import Stats

class Meteor(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, surface: pygame.Surface, settings: Settings, stats: Stats, groups: tuple[pygame.sprite.Group, ...]) -> None:
        super().__init__(groups)
        self.screen = screen
        self.screen_rect = screen.get_frect()
        self.settings = settings
        self.stats = stats

        self.image = self.original_image = surface
        self.rect = self.image.get_frect(center =
                                         (randint(self.settings.screen_width + 50, self.settings.screen_width + 100),
                                          randint(0, self.settings.screen_height)))
        self.born_time = pygame.time.get_ticks()
        self.lifetime = 10000
        self.rotation_angle = 0
        self.rotation_speed = randint(10, 100)

        self.direction = pygame.math.Vector2(-1, uniform(-1.0, 1.0)).normalize()

    def update(self, dt: float) -> None:
        if self.rect.right <= self.screen_rect.left:
            self.kill()
            self.stats.score += self.stats.dodge_meteor_award

        if self.rect.top <= self.screen_rect.top or self.rect.bottom >= self.screen_rect.bottom:
            self.direction.y *= -1

        self.rect.center += self.direction * self.settings.meteor_speed * dt

        self.rect.top = max(self.rect.top, self.screen_rect.top)
        self.rect.bottom = min(self.rect.bottom, self.screen_rect.bottom)

        self.rotation_angle += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_image, self.rotation_angle, 1)
        self.rect = self.image.get_frect(center = self.rect.center)
