import pygame
from os.path import join

class Settings:
    DEFAULT_METEOR_SPEED = 200

    def __init__(self) -> None:
        self.screen_width: int = 1280
        self.screen_height: int = 720

        self.ship_speed: float = 300
        self.meteor_speed: float = self.DEFAULT_METEOR_SPEED
        self.laser_speed: float = 2000

        self.sound_volumes = 0.1

    def create_surfaces(self) -> None:
        self.meteor_surface = pygame.image.load(join('assets','meteor.png')).convert_alpha()
        self.laser_surface = pygame.image.load(join('assets','laser.png')).convert_alpha()
        self.explosion_frames = [pygame.image.load(join('assets', 'explosion', f'{i}.png')).convert_alpha() for i in range(21)]

    def import_sounds(self) -> None:
        self.laser_sound = pygame.mixer.Sound(join('audio', 'laser.wav'))
        self.laser_sound.set_volume(self.sound_volumes)
        self.explosion_sound = pygame.mixer.Sound(join('audio', 'explosion.wav'))
        self.explosion_sound.set_volume(self.sound_volumes)
        self.game_music = pygame.mixer.Sound(join('audio', 'game_music.wav'))
        self.game_music.set_volume(self.sound_volumes)