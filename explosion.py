import pygame
from math import floor

class Explosion(pygame.sprite.Sprite):
    FRAMES_PER_DT = 25

    def __init__(self, frames: list[pygame.Surface], pos: tuple[float, float], screen: pygame.Surface, groups: tuple[pygame.sprite.Group, ...]) -> None:
        super().__init__(groups)
        self.screen = screen
        self.screen_rect = screen.get_frect()
        self.frames = frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_frect(center = pos)

    def update(self, dt: float) -> None:
        self.current_frame += self.FRAMES_PER_DT * dt
        if self.current_frame >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[floor(self.current_frame)]