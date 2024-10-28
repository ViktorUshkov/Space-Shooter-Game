import pygame
from os.path import join
from settings import Settings

class Laser(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, surface: pygame.Surface, settings: Settings, pos: tuple[float, float], groups: tuple[pygame.sprite.Group, ...]) -> None:
        super().__init__(groups)
        self.screen = screen
        self.screen_rect = screen.get_frect()
        self.settings = settings

        self.image = surface
        self.rect = self.image.get_frect(midleft = pos)
        self.direction = pygame.math.Vector2(1, 0)

    def update(self, dt: float) -> None:
        self.rect.center += self.direction * self.settings.laser_speed * dt
        if self.rect.left > self.screen_rect.right:
            self.kill()
