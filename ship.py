import pygame
from os.path import join
from settings import Settings
from laser import Laser

class Ship(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, settings: Settings, group: pygame.sprite.Group, laser_group: pygame.sprite.Group) -> None:
        super().__init__(group)
        self.screen = screen
        self.screen_rect = screen.get_frect()
        self.settings = settings
        self.group = group
        self.laser_group = laser_group

        self.image = pygame.image.load(join('assets','spaceship.png')).convert_alpha()
        self.rect = self.image.get_frect(midleft = (10, self.settings.screen_height / 2))

        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False

        self.cooldown_active = False
        self.last_shot_time = 0
        self.cooldown_time = 200

    def _update_cooldown_state(self) -> None:
        if self.cooldown_active:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time >= self.cooldown_time:
                self.cooldown_active = False

    def update(self, dt: float) -> None:
        if self.moving_up:
            self.rect.top = max(self.rect.top - self.settings.ship_speed * dt, self.screen_rect.top)

        if self.moving_down:
            self.rect.bottom = min(self.rect.bottom + self.settings.ship_speed * dt, self.screen_rect.bottom)

        if self.moving_left:
            self.rect.left = max(self.rect.left - self.settings.ship_speed * dt, self.screen_rect.left)

        if self.moving_right:
            self.rect.right = min(self.rect.right + self.settings.ship_speed * dt, self.screen_rect.right)

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and not self.cooldown_active:
            Laser(self.screen, self.settings.laser_surface, self.settings, self.rect.midright, (self.group, self.laser_group))
            self.cooldown_active = True
            self.last_shot_time = pygame.time.get_ticks()
            self.settings.laser_sound.play()
        self._update_cooldown_state()